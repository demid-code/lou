from lou_parser import OpType, Op

class Compiler:
    def __init__(self, ops: list[Op]):
        self.ops = ops
        self.current = 0

        self.write_mode = None
        self.writes = {"init": "", "main": ""}

        self.includes = []
        self.add_include("\"lou_lib.h\"")

    def add_include(self, include: str):
        if not include in self.includes:
            self.includes.append(include)

    def is_at_end(self) -> bool:
        return self.current >= len(self.ops)
    
    def advance(self) -> tuple[Op, int]:
        idx = self.current
        self.current += 1
        return (self.ops[idx], idx)

    def write(self, code: str, tabs: int = 0):
        self.writes[self.write_mode] += f"{"    " * tabs}{code}"

    def writeln(self, code: str, tabs: int = 0):
        self.writes[self.write_mode] += f"{"    " * tabs}{code}\n"

    def scan_op(self):
        op, op_idx = self.advance()

        write_jump = True
        self.writeln(f"addr_{op_idx}: %s // {op.type.name}" % "{", 1)

        match op.type:
            case OpType.PUSH_INT:
                self.writeln(f"stack_pushU64(&stack, {op.operand});", 2)

            case OpType.PLUS:
                self.writeln("uint64_t b = stack_popU64(&stack);", 2)
                self.writeln("uint64_t a = stack_popU64(&stack);", 2)
                self.writeln("stack_pushU64(&stack, a + b);", 2)
            
            case OpType.MINUS:
                self.writeln("uint64_t b = stack_popU64(&stack);", 2)
                self.writeln("uint64_t a = stack_popU64(&stack);", 2)
                self.writeln("stack_pushU64(&stack, a - b);", 2)

            case OpType.MULTIPLY:
                self.writeln("uint64_t b = stack_popU64(&stack);", 2)
                self.writeln("uint64_t a = stack_popU64(&stack);", 2)
                self.writeln("stack_pushU64(&stack, a * b);", 2)

            case OpType.DIVIDE:
                self.writeln("uint64_t b = stack_popU64(&stack);", 2)
                self.writeln("uint64_t a = stack_popU64(&stack);", 2)
                self.writeln("stack_pushU64(&stack, (uint64_t)a / b);", 2)

            case OpType.DUMP:
                self.writeln("printf(\"%\" PRIu64 \"\\n\", stack_popU64(&stack));", 2)

            case OpType.EOF:
                write_jump = False
                self.writeln("stack_free(&stack);", 2)
                self.writeln("return 0;", 2)

            case _:
                assert False, f"Unsupported OpType.{op.type.name} in Compiler.scan_op()"

        if write_jump:
            self.writeln(f"goto addr_{op_idx + 1};", 2)
        self.writeln("}", 1)

    def compile(self) -> str:
        self.write_mode = "main"
        while not self.is_at_end():
            self.scan_op()

        self.write_mode = "init"
        self.writeln("Stack stack;", 1)
        self.writeln("stack_init(&stack, 2097152); // 2MB\n", 1)
        
        self.writeln("goto addr_0;\n", 1)
        
        output = ""

        if len(self.includes) > 0:
            for include in self.includes:
                output += f"#include {include}\n"
            output += "\n"

        output += "int main() {\n"
        output += self.writes["init"]
        output += self.writes["main"]
        output += "}"

        return output