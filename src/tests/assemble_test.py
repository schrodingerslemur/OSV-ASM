import sys

from src.assemble import get_opcode_type, parse_op, handle_address_and_label
from src.errors import InvalidArgumentError, InvalidRegisterError, MissingOperationError, InvalidOperationError

def test_parse_op_valid():
    line = "ADD R1, R2, R3"
    op, non_op = parse_op(line)
    assert op == "add"
    assert non_op == "r1, r2, r3"

    line = "  SUB R4, R5, R6  "
    op, non_op = parse_op(line)
    print(non_op)
    assert op == "sub"
    assert non_op == "r4, r5, r6"

def test_parse_op_missing():
    line = "   "
    try:
        parse_op(line)
    except MissingOperationError as e:
        assert isinstance(e, MissingOperationError)

def test_get_opcode_type_invalid():
    from src.assemble import get_opcode_type
    invalid_op = "invalid_op"
    try:
        get_opcode_type(invalid_op)
    except InvalidOperationError as e:
        assert isinstance(e, InvalidOperationError)

def test_get_opcode_type_valid():
    from src.assemble import get_opcode_type
    op = "add"
    opcode_type = get_opcode_type(op)
    assert opcode_type == 'R'

def test_handle_address_and_label():
    metadata = {
        'labels': {},
        'address': 0,
    }
    op_label = "start:"
    handle_address_and_label(op_label, metadata)
    assert metadata['labels']['start'] == 0
    assert metadata['address'] == 0

    op_instr = "add"
    handle_address_and_label(op_instr, metadata)
    assert metadata['address'] == 4

    op_label2 = "loop:"
    handle_address_and_label(op_label2, metadata)
    assert metadata['labels']['loop'] == 4
    assert metadata['address'] == 4

def test_get_register():
    from src.assemble import get_register
    assert get_register('r0') == '00000'
    assert get_register('r15') == '01111'
    assert get_register('r31') == '11111'
    try:
        get_register('r32')
    except InvalidRegisterError as e:
        assert isinstance(e, InvalidRegisterError)

def test_get_imm():
    from src.assemble import get_imm
    metadata = {
        'labels': {
            'label1': 100,
        }
    }
    assert get_imm('label1', metadata, type='I') == '000001100100'
    assert get_imm('100', metadata, type='I') == '000001100100'
    assert get_imm('-50', metadata, type='I') == '111111001110'

    assert get_imm('200000', metadata, type='U') == '00110000110101000000'

    try:
        get_imm('abc', metadata)
    except InvalidArgumentError as e:
        assert isinstance(e, InvalidArgumentError)

def test_get_args():
    from src.assemble import get_args
    op = "addi"
    args_str = "r1, r2, 100"
    opcode_type = 'I'
    metadata = {}
    args = get_args(op, args_str, opcode_type, metadata)
    assert args == ['0010011', '00001', '00010', '000001100100']

    args_str = " r3 , r4 , -50 "
    args = get_args(op, args_str, opcode_type, metadata)
    assert args == ['0010011', '00011', '00100', '111111001110']

    op = "add"
    args_str = "r5, r6, r7"
    opcode_type = 'R'
    args = get_args(op, args_str, opcode_type, metadata)
    assert args == ['0110011', '00101', '00110', '00111']

    op = "jal"
    args_str = "r1, 200"
    opcode_type = 'J'
    args = get_args(op, args_str, opcode_type, metadata)
    assert args == ['1101111', '00001', '00000000000011001000']
    
def test_get_args_invalid():
    from src.assemble import get_args
    op = "addi"
    args_str = "r1, r2"  # Missing immediate
    opcode_type = 'I'
    metadata = {}
    try:
        get_args(op, args_str, opcode_type, metadata)
    except InvalidArgumentError as e:
        assert isinstance(e, InvalidArgumentError)

def test_add():
    from src.assemble import assemble_line
    metadata = {
        'labels': {},
        'address': 0,
    }
    line = "add r1, r2, r3"
    instruction = assemble_line(line, metadata)
    assert instruction == '0000000' + '00011' + '00010' + '000' + '00001' + '0110011'  # funct7 + rs2 + rs1 + funct3 + rd + opcode

def test_add_invalid():
    from src.assemble import assemble_line
    metadata = {
        'labels': {},
        'address': 0,
    }
    line = "add r1, r2"  # Missing one register
    try:
        assemble_line(line, metadata)
    except InvalidArgumentError as e:
        assert isinstance(e, InvalidArgumentError)

def test_addi():
    from src.assemble import assemble_line
    metadata = {
        'labels': {},
        'address': 0,
    }
    line = "addi r1, r2, 100"
    instruction = assemble_line(line, metadata)
    assert instruction == '000001100100' + '00010' + '000' + '00001' + '0010011'  # imm + rs1 + funct3 + rd + opcode

    line = 'addi r1, r2, 0'
    instruction = assemble_line(line, metadata)
    assert instruction == '000000000000' + '00010' + '000' + '00001' + '0010011'  # imm + rs1 + funct3 + rd + opcode

def test_addi_invalid_imm():
    from src.assemble import assemble_line
    metadata = {
        'labels': {},
        'address': 0,
    }
    line = "addi r1, r2, abc"  # Invalid immediate
    try:
        assemble_line(line, metadata)
    except InvalidArgumentError as e:
        assert isinstance(e, InvalidArgumentError)

def test_get_pseudo_args():
    from src.assemble import get_pseudo_args
    metadata = {}
    op = "mv"
    non_op = "r1, r2"
    args = get_pseudo_args(op, non_op, metadata)
    assert args == ['00001', '00010']

    op = "li"
    non_op = "r3, 1000"
    args = get_pseudo_args(op, non_op, metadata)
    assert args == ['00011', '001111101000']

def test_replace_args_in_pseudo():
    from src.assemble import replace_args_in_pseudo
    pseudo_inst = "addi x0, x0, IMM"
    args = ['00001', '001111101000']  # rd = r1, imm = 1000
    replaced_inst = replace_args_in_pseudo(pseudo_inst, args)
    assert replaced_inst == "addi r1, r1, 1000"

def test_pseudo_mv():
    from src.assemble import assemble_line
    metadata = {
        'labels': {},
        'address': 0,
    }
    line = "mv r1, r2"
    instructions = assemble_line(line, metadata)
    assert len(instructions) == 1
    assert instructions[0] == '0000000' + '00000' + '00010' + '000' + '00001' + '0010011'  # addi r1, r2, 0

# 000000000010 00000 000 00001 0010011
# get_args non_op -> ['r1', 'r2', '100'] etc
# get_instruction(op, opcode_type, args) -> binary instruction

# get_pseudo_args non_op -> ['r1', 'r2'] etc
# replace_args_in_pseudo 'addi x0, x1, 0' -> 'addi r1, r2, 0'