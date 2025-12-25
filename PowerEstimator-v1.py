import pyrtl

def build():
    pyrtl.reset_working_block()

    a = pyrtl.Input(8, 'A')
    b = pyrtl.Input(8, 'B')

    sumOut = pyrtl.Output(8, 'SUM')
    carryOut = pyrtl.Output(1, 'CARRY')

    # 9-bit result: lower 8 bits = SUM, bit 8 = carry out
    result = a + b
    sumOut <<= result[0:8]
    carryOut <<= result[8]


import pyrtl

def countAllToggles(simTrace):
    workingBlock = pyrtl.working_block()
    allToggles = {}

    for wire in workingBlock.wirevector_set:
        # Skip constants and unnamed wires
        if isinstance(wire, pyrtl.Const):
            continue
        if not wire.name:
            continue

        try:
            values = simTrace.trace[wire.name] # list of ints, one per cycle
        except pyrtl.PyrtlError:
            continue

        width = len(wire)
        togglesPerBit = [0] * width

        for i in range(len(values) - 1):
            prevVal = values[i]
            newVal = values[i + 1]

            # XOR to find bits that changed
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
        # Energy: E = toggles * 0.5 * C * V^2
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


def main():
    build()

    simTrace = pyrtl.SimulationTrace()
    sim = pyrtl.Simulation(tracer=simTrace)

    inputSequences = {
        'A': [0b00000000, 0b10010101, 0b10101010, 0b10100010],
        'B': [0b00000000, 0b10010111, 0b11110101, 0b10000100]
    }

    sim.step_multiple(inputSequences)
    simCycles = len(inputSequences['A'])

    simulation = simTrace.render_trace()

    allToggles = countAllToggles(simTrace)

    print("Per-wire toggles (per bit)")
    for name, togglesPerBit in allToggles.items():
        print(f"  {name:6s}: {togglesPerBit}, total = {sum(togglesPerBit)}")

    capacitanceF = 1e-15 # 1 fF per bit
    voltage = 1.0 # 1 Volt
    clockFreqHz = 50e6 # 50 MHz

    report = estPowerAllWires(
        allToggles=allToggles,
        capacitanceF=capacitanceF,
        voltage=voltage,
        clockFreqHz=clockFreqHz,
        simCycles=simCycles
    )

    print("\nPer-wire energy (J)")
    for name, energy in report["energyPerWireJ"].items():
        print(f"  {name:6s}: {energy:.3e} J")

    print(f"\nTotal energy:  {report['totalEnergyJ']:.3e} J")
    print(f"Average power: {report['avgPowerW']:.3e} W")
    print(simulation)


if __name__ == '__main__':
    main()

# user passes generator to give the next step
# same parameters as step_multiple, call step_multiple