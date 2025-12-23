# Hack Assembler

A Python implementation of the Hack Assembler from the [NAND to Tetris](https://www.nand2tetris.org/) course (also known as "The Elements of Computing Systems"). This assembler translates programs written in Hack assembly language into binary machine code that can run on the Hack computer platform.

## Features

- **Two-pass assembly**: First pass builds the symbol table, second pass generates machine code
- **Complete instruction support**: A-instructions, C-instructions, and labels
- **Symbol table management**: Handles predefined symbols (R0-R15, SP, LCL, ARG, THIS, THAT, SCREEN, KBD) and user-defined labels and variables
- **Comment handling**: Properly processes and ignores comments
- **Comprehensive test suite**: Includes unit tests for all components

## Installation

No external dependencies required! Just Python 3.6 or higher.

```bash
git clone https://github.com/cturbides/Hack-Assembler.git
cd Hack-Assembler
```

## Usage

### Basic Usage

```bash
python assembler.py <input.asm>
```

This will create a `.hack` file with the same name as the input file.

### Example

```bash
python assembler.py examples/Add.asm
```

This will generate `examples/Add.hack` containing the binary machine code.

## Architecture

The assembler consists of four main modules:

### 1. Parser (`parser.py`)
Handles the parsing of assembly language files:
- Reads and cleans assembly code (removes comments and whitespace)
- Identifies instruction types (A-instructions, C-instructions, labels)
- Extracts instruction components (symbol, dest, comp, jump)

### 2. Code (`code.py`)
Translates Hack assembly mnemonics into binary codes:
- Converts computation mnemonics to 7-bit binary codes
- Converts destination mnemonics to 3-bit binary codes
- Converts jump mnemonics to 3-bit binary codes

### 3. Symbol Table (`symbol_table.py`)
Manages the symbol table:
- Initializes with predefined Hack symbols
- Tracks label addresses
- Allocates RAM addresses for variables (starting at address 16)

### 4. Assembler (`assembler.py`)
Main driver that orchestrates the assembly process:
- **First pass**: Scans code to build symbol table with label definitions
- **Second pass**: Generates binary machine code

## Hack Assembly Language Syntax

### A-Instructions
Load a value into the A register:
```
@value   // Load constant value
@symbol  // Load address of symbol
```

### C-Instructions
Perform computations and jumps:
```
dest=comp;jump
```
- `dest`: Where to store the result (A, D, M, or combinations)
- `comp`: The computation to perform (e.g., D+1, A-D, M)
- `jump`: Jump condition (JGT, JEQ, JGE, JLT, JNE, JLE, JMP)

### Labels
Define symbolic labels for jump destinations:
```
(LABEL_NAME)
```

### Comments
```
// This is a comment
@2    // Inline comment
```

## Examples

The `examples/` directory contains sample programs:

### Add.asm
A simple program that computes 2 + 3 and stores the result in RAM[0]:
```asm
@2
D=A
@3
D=D+A
@0
M=D
```

### Max.asm
Computes the maximum of two numbers stored in RAM[0] and RAM[1], storing the result in RAM[2].

### Rect.asm
Draws a rectangle at the top-left corner of the screen.

## Running Tests

Run the comprehensive test suite:

```bash
python tests/test_assembler.py
```

Or with verbose output:
```bash
python tests/test_assembler.py -v
```

The test suite covers:
- Parser functionality (A-instructions, C-instructions, labels, comments)
- Code translation (dest, comp, jump mnemonics)
- Symbol table operations
- Complete assembly process
- Label and variable handling

## Project Structure

```
Hack-Assembler/
├── assembler.py       # Main assembler driver
├── parser.py          # Assembly language parser
├── code.py            # Binary code translator
├── symbol_table.py    # Symbol table manager
├── examples/          # Sample assembly programs
│   ├── Add.asm
│   ├── Max.asm
│   └── Rect.asm
├── tests/             # Test suite
│   └── test_assembler.py
└── README.md          # This file
```

## Binary Code Format

### A-Instruction (16 bits)
```
0vvvvvvvvvvvvvvvv
```
- Leading 0 identifies it as an A-instruction
- Following 15 bits represent the value/address

### C-Instruction (16 bits)
```
111accccccdddjjj
```
- Leading 111 identifies it as a C-instruction
- `a`: 1 bit (use A or M register)
- `cccccc`: 6 bits (computation)
- `ddd`: 3 bits (destination)
- `jjj`: 3 bits (jump)

## Predefined Symbols

| Symbol | Value | Description |
|--------|-------|-------------|
| R0-R15 | 0-15  | Virtual registers |
| SP     | 0     | Stack pointer |
| LCL    | 1     | Local segment base |
| ARG    | 2     | Argument segment base |
| THIS   | 3     | This segment base |
| THAT   | 4     | That segment base |
| SCREEN | 16384 | Screen memory map base |
| KBD    | 24576 | Keyboard memory map |

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Based on the [NAND to Tetris](https://www.nand2tetris.org/) course by Noam Nisan and Shimon Schocken
- Part of the book "The Elements of Computing Systems: Building a Modern Computer from First Principles"

## Resources

- [NAND to Tetris Official Website](https://www.nand2tetris.org/)
- [Course on Coursera](https://www.coursera.org/learn/build-a-computer)
- [Hack Computer Specification](https://www.nand2tetris.org/_files/ugd/44046b_7ef1c00a714c46768f08c459a6cab45a.pdf)