import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class FinalScoreBuilderTests(unittest.TestCase):
    def test_final_score_summary_is_regenerable(self) -> None:
        result = subprocess.run(
            [sys.executable, "scripts/build_final_scores.py", "--check"],
            cwd=ROOT,
            capture_output=True,
            text=True,
        )
        if result.returncode != 0:
            self.fail(result.stderr.strip() or result.stdout.strip())


if __name__ == "__main__":
    unittest.main()
