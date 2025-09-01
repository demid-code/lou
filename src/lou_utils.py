import subprocess
from lou_error import report_error

def read_file(filepath: str) -> str:
    try:
        with open(filepath, "r") as f:
            return f.read()
    except Exception as e:
        report_error(str(e))

def write_file(filepath: str, content: set):
    try:
        with open(filepath, "w") as f:
            return f.write(content)
    except Exception as e:
        report_error(str(e))

def cmd_call(cmd: list[str], print_info: bool = True):
    assert type(cmd) == list
    str_cmd = [str(x) for x in cmd]

    if print_info:
        print(f"CMD: {" ".join(str_cmd)}")

    subprocess.call(str_cmd)