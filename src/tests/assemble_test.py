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
    assert get_register('r0') == 0
    assert get_register('r15') == 15
    assert get_register('r31') == 31
    try:
        get_register('r32')
    except InvalidRegisterError as e:
        assert isinstance(e, InvalidRegisterError)

def test_check_imm():
    from src.assemble import check_imm
    assert check_imm('100') == '100'
    assert check_imm('-50') == '-50'
    try:
        check_imm('abc')
    except InvalidArgumentError as e:
        assert isinstance(e, InvalidArgumentError)