import pathlib


root = pathlib.Path(__file__).parent.resolve()

if __name__ == "__main__":
    readme = root / "README.md"
    readme.open("w").write("Hello Happy World")
