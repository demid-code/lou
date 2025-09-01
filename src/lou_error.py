import sys
from dataclasses import dataclass

@dataclass
class Loc:
    filepath: str
    line: int
    pos: int

    def copy(self) -> object:
        return Loc(self.filepath, self.line, self.pos)
    
    def __repr__(self) -> str:
        return f"{self.filepath}:{self.line}:{self.pos}"

def report_error(message: str, loc: Loc = None):
    msg = message[0].upper() + message[1:]
    if loc == None:
        print(f"Error: {msg}", file=sys.stderr)
    else:
        print(f"{loc}: Error: {msg}", file=sys.stderr)
    sys.exit(1)