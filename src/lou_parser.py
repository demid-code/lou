from enum import IntEnum, auto
from dataclasses import dataclass

from lou_error import report_error
from lou_lexer import TokenType, Token

class OpType(IntEnum):
    # push
    PUSH_INT = auto()

    # intrinsics
    PLUS = auto()
    MINUS = auto()
    MULTIPLY = auto()
    DIVIDE = auto()
    DUMP = auto()

    # specific
    EOF = auto()

assert len(OpType) == 7, "Exhaustive handling of OpType in WORD_TO_OPTYPE definition"
WORD_TO_OPTYPE = {
    # intrinsics
    "+":    OpType.PLUS,
    "-":    OpType.MINUS,
    "*":    OpType.MULTIPLY,
    "/":    OpType.DIVIDE,
    "dump": OpType.DUMP,
}

@dataclass
class Op:
    type: OpType
    operand: object
    token: Token

    def __repr__(self) -> str:
        return f"{self.type.name}{f", {self.operand}" if self.operand != None else ""}"
    
class Parser:
    def __init__(self, tokens: list[Token]):
        self.tokens = tokens
        self.current = 0

        self.ops = []

    def is_at_end(self) -> bool:
        return self.current >= len(self.tokens)
    
    def advance(self) -> tuple[Token, int]:
        idx = self.current
        self.current += 1
        return (self.tokens[idx], idx)

    def add_op(self, op_type: OpType, token: Token, operand: object = None):
        self.ops.append(Op(op_type, operand, token))

    def make_op(self):
        token, token_idx = self.advance()

        match token.type:
            case TokenType.INT:
                self.add_op(OpType.PUSH_INT, token, int(token.text))

            case TokenType.WORD:
                if token.text in WORD_TO_OPTYPE:
                    self.add_op(WORD_TO_OPTYPE.get(token.text), token)
                else:
                    report_error(f"`{token.text}` is not a built-in intrinsic")

            case _:
                assert False, f"Unsupported TokenType.{token.type.name} in Parser.make_op()"

    def parse(self) -> list[Op]:
        while not self.is_at_end():
            self.make_op()

        self.add_op(OpType.EOF, self.tokens[-1])
        
        return self.ops