import pyrtl


def countAllToggles(simTrace, block=None):
    if block is None:
        block = pyrtl.working_block()
    allToggles = {}

    for wire in block.wirevector_set:

        # Skip hardcoded and unnamed wires
        if isinstance(wire, pyrtl.Const):
            continue
        if not wire.name:
            continue

        try:
            # List of values
            values = simTrace.trace[wire.name]

        # Skip if not recorded
        except pyrtl.PyrtlError:
            continue

        # Input wire length
        width = len(wire)
        togglesPerBit = [0] * width

        # Compare values per cycle
        for i in range(len(values) - 1):
            prevVal = values[i]
            newVal = values[i + 1]

            # XOR change between values
            delta = prevVal ^ newVal

            # Check for toggle change
            if delta != 0:
                for bit in range(width):
                    if (delta >> bit) & 1:
                        # Increment counter
                        togglesPerBit[bit] += 1

        allToggles[wire.name] = togglesPerBit

    return allToggles


def estPowerAllWires(allToggles, capacitanceF, voltage, clockFreqHz, simCycles):
    halfVoltageSquared = 0.5 * (voltage ** 2)
    energyPerWireJ = {}

    # Calculate and sum all energy / bit
    for name, togglesPerBit in allToggles.items():
        energyBits = [toggles * capacitanceF * halfVoltageSquared
            for toggles in togglesPerBit
        ]
        energyPerWireJ[name] = sum(energyBits)

    totalEnergyJ = sum(energyPerWireJ.values())

    # Calculate simulation time in seconds
    if clockFreqHz > 0:
        simTimeS = simCycles / float(clockFreqHz)
    else:
        simTimeS = 0.0

    if simTimeS > 0:
        avgPowerW = totalEnergyJ / simTimeS
    else:
        avgPowerW = 0.0

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