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
    address = 0
    labels = {}

    for idx in range(len(lines)):
        line = lines[idx].strip()

        # Comments or empty lines
        if line == '' or line.startswith('#'):
            continue 

        # Operation-handling
        match = re.search(r'\s*(\w+)\s+(.*)', line)
        op = match.group(1)
        non_op = match.group(2)

        # Label-handling
        if op.endswith(':'):
            labels[op[:-1]] = address
        else:
            address += 4

        # Instruction-handling
        if op in pseudo:
            for pseudo_inst in pseudo[op]:
                # assembled_lines.append(pseudo_inst.replace('label', non_op))


    return '\n'.join(assembled_lines)

if __name__ == "__main__":
    assemble(sys.argv[1])