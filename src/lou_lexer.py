from enum import IntEnum, auto
from dataclasses import dataclass
from pathlib import Path

from lou_error import Loc, report_error
from lou_utils import read_file

class TokenType(IntEnum):
    INT = auto()
    WORD = auto()

@dataclass
class Token:
    type: TokenType
    text: str
    loc: Loc

    def __repr__(self) -> str:
        return f"{self.type.name}: `{self.text}`"
    
class Lexer:
    def __init__(self, filepath: Path):
        if not filepath.exists():
            report_error(f"`{filepath}` does not exist")

        if str(filepath.name).split(".")[1] != "lou":
            report_error("expected filepath with .lou extension")

        self.loc = Loc(filepath, 1, 1)
        self.start = 0
        self.current = 0
        self.pos_helper = 1

        self.source = read_file(filepath)
        self.tokens = []

    def is_at_end(self) -> bool:
        return self.current >= len(self.source)
    
    def advance(self) -> str:
        self.current += 1
        self.pos_helper += 1
        return self.source[self.current - 1]

    def peek(self, ahead: int = 0) -> str:
        if self.current + ahead >= len(self.source): return "\0"
        return self.source[self.current + ahead]

    def match(self, char: str) -> bool:
        if self.peek() == char:
            self.advance()
            return True
        else:
            return False

    def add_token(self, token_type: TokenType):
        self.tokens.append(Token(token_type, self.source[self.start:self.current], self.loc.copy()))

    def skip_comment(self):
        if self.match("/"):
            while not self.is_at_end() and self.peek() != "\n":
                self.advance()
        else:
            self.add_token(TokenType.WORD)

    def make_word(self):
        while not self.is_at_end() and not self.peek() in (" ", "\r", "\t", "\n"):
            self.advance()

        self.add_token(TokenType.WORD)

    def make_number(self):
        while self.peek().isdigit():
            self.advance()

        if self.peek() == "." and self.peek(1).isdigit():
            report_error("floats aren't supported")

        self.add_token(TokenType.INT)

    def make_token(self):
        char = self.advance()

        match char:
            case " " | "\r" | "\t": pass
            case "\n": self.loc.line += 1; self.pos_helper = 1
            case "/": self.skip_comment()
            case _ if char.isdigit(): self.make_number()
            case _: self.make_word()

    def lex(self) -> list[Token]:
        while not self.is_at_end():
            self.start = self.current
            self.loc.pos = self.pos_helper
            self.make_token()

        return self.tokens