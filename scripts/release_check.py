"""Run offline source replay, tests and generated export integrity checks."""
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]

def main():
    commands = [
        ['-m', 'csg', 'validate'],
        ['-m', 'unittest', 'discover', '-s', 'tests', '-v'],
        ['-m', 'csg', 'verify-export', 'exports'],
    ]
    for command in commands:
        result = subprocess.run([sys.executable, *command], cwd=ROOT)
        if result.returncode:
            return result.returncode
    print('Release checks passed. Epigraphic review and exhaustive coverage remain separate gates.')
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
