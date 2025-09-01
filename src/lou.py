#! /usr/local/bin/python3

import sys, shutil, os
from pathlib import Path

from lou_error import report_error
from lou_utils import write_file, cmd_call
from lou_lexer import Lexer
from lou_parser import Parser
from lou_compiler import Compiler

def usage(path: str = None):
    p = path or sys.argv[0]
    print(f"Usage: {p} <subcommand> [flags]")
    print("Subcommands:")
    print("    help                Prints usage and exits")
    print("    lex <filepath>      Generates tokens and prints them out")
    print("    parse <filepath>    Generates op's and prints them out")
    print("    gen <filepath>      Generates build folder")
    print("    com <filepath>      Compiles the source code")
    print()
    print("Flags:")
    print("    -r    Run after successfull compilation")
    print("    -s    Silent mode")
    print()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        usage()
        report_error("no subcommand provided")

    subcommand = sys.argv[1]

    match subcommand:
        case "help":
            usage()

        case "lex" | "parse" | "gen" | "com":
            if len(sys.argv) < 3:
                report_error(f"expected <filepath> for `{subcommand}` subcommand")

            filepath = Path(sys.argv[2])
            lou_path = Path(__file__).parent.parent

            print_info = not ("-s" in sys.argv)

            lexer = Lexer(filepath)
            tokens = lexer.lex()
            if len(tokens) < 1: sys.exit(0)

            if subcommand == "lex":
                for token in tokens:
                    print(token)
                sys.exit(0)

            parser = Parser(tokens)
            ops = parser.parse()
            if len(ops) < 1: sys.exit(0)

            if subcommand == "parse":
                for idx, op in enumerate(ops):
                    print(f"{idx}: {op}")
                sys.exit(0)

            build_path = filepath.parent.joinpath("build")
            build_path.mkdir(exist_ok=True)

            src_lou_lib_h = lou_path.joinpath("src/lou_lib.h")
            src_lou_lib_c = lou_path.joinpath("src/lou_lib.c")

            build_lou_lib_h = build_path.joinpath("lou_lib.h")
            build_lou_lib_c = build_path.joinpath("lou_lib.c")

            main_c_path = build_path.joinpath("main.c")

            compiler = Compiler(ops)
            output = compiler.compile()

            shutil.copyfile(src_lou_lib_h, build_lou_lib_h)
            shutil.copyfile(src_lou_lib_c, build_lou_lib_c)
            write_file(main_c_path, output)

            if subcommand == "gen": sys.exit(0)

            main_path = build_path.joinpath("main.exe") if os.name == "nt" else build_path.joinpath("main")

            cmd_call(["gcc", "-o", main_path, main_c_path, build_lou_lib_c], print_info)

            if "-r" in sys.argv:
                cmd_call([main_path], print_info)

        case _:
            usage()
            report_error(f"invalid subcommand `{subcommand}`")