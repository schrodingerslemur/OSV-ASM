import sys

from src.assemble import parse_op, handle_address_and_label
from src.errors import MissingOperationError, InvalidOperationError

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

def test_get_opcode_and_type_invalid():
    from src.assemble import get_opcode_and_type
    invalid_op = "invalid_op"
    try:
        get_opcode_and_type(invalid_op)
    except InvalidOperationError as e:
        assert isinstance(e, InvalidOperationError)

def test_get_opcode_and_type_valid():
    from src.assemble import get_opcode_and_type
    op = "add"
    opcode, opcode_type = get_opcode_and_type(op)
    assert opcode == '0110011'
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