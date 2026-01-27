import pyrtl
from EightBitAdder import build_adder
from PowerEstimator import estimatePower

# Build the circuit
pyrtl.reset_working_block()
build_adder()

# Define input generator
def inputGenerator():
    testData = [
        (0b00000000, 0b00000000),
        (0b10010101, 0b10010111),
        (0b10101010, 0b11110101),
        (0b10100010, 0b10000100),
    ]
    for a_val, b_val in testData:
        yield {'A': a_val, 'B': b_val}

# Run power estimation
report = estimatePower(
    inputGenerator,
    capacitanceF=1e-15,
    voltage=1.0,
    clockFreqHz=50e6
)

print("Per-wire toggles (per bit)")
for name, togglesPerBit in report["toggles"].items():
    print(f"  {name}: {togglesPerBit}, total = {sum(togglesPerBit)}")

print(f"\n Simulation cycles: {report['simCycles']}")

print("\n Per-wire energy (J)")
for name, energy in report["energyPerWireJ"].items():
    print(f"  {name}: {energy:.3e} J")

print(f"\n Total energy: {report['totalEnergyJ']:.3e} J")
print(f"Average power: {report['avgPowerW']:.3e} W")