"""PyRTL Power Estimator - estimates power from toggle activity."""

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
    """
    Estimate power consumption for a pyRTL circuit.

    Args:
        inputGenerator: Function returning a generator that yields input dicts per cycle.
                        Dict keys must match your pyrtl.Input wire names.
        capacitanceF: Capacitance per bit in Farads (default: 1)
        voltage: Supply voltage in Volts (default: 1.0V)
        clockFreqHz: Clock frequency in Hz (default: 50MHz)
        block: pyrtl.Block to simulate. If None, uses pyrtl.working_block()

    Returns:
        Dict with energyPerWireJ, totalEnergyJ, avgPowerW, toggles, and simCycles

    Example:
        # Build circuit
        pyrtl.reset_working_block()
        a = pyrtl.Input(8, 'A')
        b = pyrtl.Input(8, 'B')
        out = pyrtl.Output(8, 'SUM')
        out <<= a + b

        # Define inputs matching wire names
        def inputGenerator():
            yield {'A': 10, 'B': 20}
            yield {'A': 50, 'B': 100}

        # Estimate power
        report = estimatePower(inputGenerator)
    """
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


if __name__ == '__main__':
    # Build circuit
    pyrtl.reset_working_block()

    a = pyrtl.Input(8, 'A')
    b = pyrtl.Input(8, 'B')
    sumOut = pyrtl.Output(8, 'SUM')
    carryOut = pyrtl.Output(1, 'CARRY')

    result = a + b
    sumOut <<= result[0:8]
    carryOut <<= result[8]

    # Define input generator
    def inputGenerator():
        inputData = [
            (0b00000000, 0b00000000),
            (0b10010101, 0b10010111),
            (0b10101010, 0b11110101),
            (0b10100010, 0b10000100),
        ]
        for a_val, b_val in inputData:
            yield {'A': a_val, 'B': b_val}

    # Run power estimation
    report = estimatePower(inputGenerator)

    # Print results
    print("Per-wire toggles (per bit)")
    for name, togglesPerBit in report["toggles"].items():
        print(f"  {name:6s}: {togglesPerBit}, total = {sum(togglesPerBit)}")

    print("\nPer-wire energy (J)")
    for name, energy in report["energyPerWireJ"].items():
        print(f"  {name:6s}: {energy:.3e} J")

    print(f"\nTotal energy: {report['totalEnergyJ']:.3e} J")
    print(f"Average power: {report['avgPowerW']:.3e} W")

# user passes generator to give the next step
# same parameters as step_multiple, call step_multiple