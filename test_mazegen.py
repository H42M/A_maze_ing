from mazegen import MazeGenerator


generator = MazeGenerator(
    width=20,
    height=15,
    entry=(0, 0),
    exit=(19, 14),
    seed=42,
    perfect=True,
)

generator.generate()

print(generator.to_output_text())
