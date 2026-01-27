import pyrtl


def countAllToggles(simTrace, block=None):
    if block is None:
        block = pyrtl.working_block()
    allToggles = {}

    for wire in block.wirevector_set:
        if isinstance(wire, pyrtl.Const):
            continue
        if not wire.name:
            continue

        try:
            values = simTrace.trace[wire.name]
        except pyrtl.PyrtlError:
            continue

        width = len(wire)
        togglesPerBit = [0] * width

        for i in range(len(values) - 1):
            prevVal = values[i]
            newVal = values[i + 1]

            delta = prevVal ^ newVal
            if delta != 0:
                for bit in range(width):
                    if (delta >> bit) & 1:
                        togglesPerBit[bit] += 1

        allToggles[wire.name] = togglesPerBit

    return allToggles


def estPowerAllWires(allToggles, capacitanceF, voltage, clockFreqHz, simCycles):
    halfVoltageSquared = 0.5 * (voltage ** 2)
    energyPerWireJ = {}

    for name, togglesPerBit in allToggles.items():
        energyBits = [
            toggles * capacitanceF * halfVoltageSquared
            for toggles in togglesPerBit
        ]
        energyPerWireJ[name] = sum(energyBits)

    totalEnergyJ = sum(energyPerWireJ.values())
    simTimeS = simCycles / float(clockFreqHz) if clockFreqHz > 0 else 0.0
    avgPowerW = totalEnergyJ / simTimeS if simTimeS > 0 else 0.0

    return {
        "energyPerWireJ": energyPerWireJ,
        "totalEnergyJ": totalEnergyJ,
        "avgPowerW": avgPowerW,
    }


def estimatePower(inputGenerator, capacitanceF=1e-15, voltage=1.0, clockFreqHz=50e6, block=None):

    if block is None:
        block = pyrtl.working_block()

    simTrace = pyrtl.SimulationTrace()
    sim = pyrtl.Simulation(tracer=simTrace)

    simCycles = 0
    for inputs in inputGenerator():
        sim.step(inputs)
        simCycles += 1

    allToggles = countAllToggles(simTrace, block)

    powerReport = estPowerAllWires(
        allToggles=allToggles,
        capacitanceF=capacitanceF,
        voltage=voltage,
        clockFreqHz=clockFreqHz,
        simCycles=simCycles
    )

    powerReport["toggles"] = allToggles
    powerReport["simCycles"] = simCycles

    return powerReport