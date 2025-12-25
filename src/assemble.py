import re
import sys

from constants import opcode, pseudo, funct_3, funct_7

def assemble(
        content: str
) -> str:
    """
    The function takes plain text RISCV 32I ISA instructions and assembles it into binary machine code.
    
    :param content: .asm file content
    :type content: str
    :return: assembled content in binary
    :rtype: str
    """
    assembled_lines = []
    lines = content.splitlines()

    for idx in range(len(lines)):
        line = lines[idx].strip()

        # Comments or empty lines
        if line == '' or line.startswith('#'):
            continue 

        # Instructions
        # parse instruction
        match = re.search(r'\s*(\w+)\s+(.*)', line)
        op = match.group(1)
        non_op = match.group(2)

        if op.endswith(':'):
            # label
            continue
        # TODO: check if it is valid instruction

        pass

    return '\n'.join(assembled_lines)

if __name__ == "__main__":
    assemble(sys.argv[1])