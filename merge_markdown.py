from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent
OUT_MD = ROOT / "merged.md"
OUT_PL_MD = ROOT / "merged.pl.md"
OUT_NAMES = {OUT_MD.name, OUT_PL_MD.name}


def natural_key(path: Path):
    return [int(part) if part.isdigit() else part.lower() for part in re.split(r"(\d+)", path.name)]


def merge(files: list[Path], output: Path) -> None:
    blocks = []
    for path in sorted(files, key=natural_key):
        content = path.read_text(encoding="utf-8").rstrip()
        blocks.append(f"========== {path.name} ===========\n{content}")
    output.write_text("\n\n".join(blocks) + ("\n" if blocks else ""), encoding="utf-8")


def main() -> None:
    pl_files = [p for p in ROOT.glob("*.pl.md") if p.name not in OUT_NAMES]
    md_files = [p for p in ROOT.glob("*.md") if p.name not in OUT_NAMES and not p.name.endswith(".pl.md")]
    merge(md_files, OUT_MD)
    merge(pl_files, OUT_PL_MD)
    print(f"Created: {OUT_MD.name}, {OUT_PL_MD.name}")


if __name__ == "__main__":
    main()

