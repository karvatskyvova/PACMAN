from pathlib import Path
import sys

BASE_DIR = Path(__file__).resolve().parent

def asset(*parts) -> str:
    return str(BASE_DIR.joinpath(*parts))

def is_web() -> bool:
    return sys.platform in ("emscripten", "wasi")
