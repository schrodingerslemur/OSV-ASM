# OSTRICH Assembler for RISC-V ISA
Building... 

Refer to [ORV-ISA.md](./docs/ORV-ISA.md) for the full set of instructions which ORV supports and [ORV-ASM.md](./docs/ORV-ASM.md) on how to structure the assembly file.

For reference, I am using the [RISC-V 32I ISA](https://msyksphinz-self.github.io/riscv-isadoc/html/rvi.html) as the basis for the ORV ISA.

p.s. the word `OSTRICH` is purely for performative reasons.

## Usage
1. Clone the repository
2. Install dependencies
```bash
uv install
# or
pip install -r requirements.txt
```
3. Run the assembler
```bash
uv run -m src.main <input_file.asm> [--o <output_file.list>]
```

## Testing
Run
```
uv run -m pytest -vv
```
