import subprocess
from typing import List


def pass_wrapper(*args: str) -> List[str]:
    def execute(args: List[str]) -> subprocess.CompletedProcess:
        return subprocess.run(["pass", *args], stdout=subprocess.PIPE, check=True)

    def extract_output(subprocess_result: subprocess.CompletedProcess):
        return [k.strip() for k in subprocess_result.stdout.split("\n")]

    return extract_output(execute([*args]))
