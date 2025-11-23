import os
import sys

from src.constants import DEFAULT_OUTPUT_FILE

START_VARIABLE_ADDRESS = 16

SYMBOL_TABLE = {
    "R0": 0,
    "R1": 1,
    "R2": 2,
    "R3": 3,
    "R4": 4,
    "R5": 5,
    "R6": 6,
    "R7": 7,
    "R8": 8,
    "R9": 9,
    "R10": 10,
    "R11": 11,
    "R12": 12,
    "R13": 13,
    "R14": 14,
    "R15": 15,
    "SCREEN": 16384,
    "KBD": 24576,
    "SP": 0,
    "LCL": 1,
    "ARG": 2,
    "THIS": 3,
    "THAT": 4,
}

def find_and_clean_asm_file() -> list[str]:
    # Get file path from args
    
    if len(sys.argv) < 2:
        raise ValueError("Please provide the relative file path to the .asm file as an argument.")
    
    file_path = sys.argv[1]

    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"File '{file_path}' not found.")
    if not file_path.endswith(".asm"):
        raise ValueError(f"File '{file_path}' is not an .asm file.")
        

    cleaned_lines = []

    with open(file_path, "r") as f:
        lines = f.readlines()
    
        for line in lines:
            line = line.strip()
            line = line.replace(" ", "")
            line = line.replace("\t", "")
            line = line.replace("\r", "")
            line = line.replace("\n", "")

            if line.startswith("//") or not line:
                continue
            
            if line.startswith("(") and line.endswith(")"):
                cleaned_lines.append(line)
                continue
            
            if "//" in line:
                line = line.split("//")[0].strip()
            
            cleaned_lines.append(line)
    
    return cleaned_lines

def populate_symbol_table(cleaned_lines: list[str], symbol_table: dict[str, int]) -> None:
    # First pass: populate symbol table with labels
    instruction_address = 0

    for line in cleaned_lines:
        if line.startswith("(") and line.endswith(")"):
            label = line[1:-1]
            if label not in symbol_table:
                symbol_table[label] = instruction_address
        else:
            instruction_address += 1
    
    # Second pass: populate symbol table with variables
    variable_address = START_VARIABLE_ADDRESS
    for line in cleaned_lines:
        if line.startswith("@"):
            symbol = line[1:]
            if not symbol.isdigit() and symbol not in symbol_table:
                symbol_table[symbol] = variable_address
                variable_address += 1

def save_output_file(processed_commands: list[str]) -> None:
    if len(sys.argv) >= 3:
        output_file = sys.argv[2]
    else:
        output_file = DEFAULT_OUTPUT_FILE
    
    with open(output_file, "w") as f:
        for command in processed_commands:
            f.write(command + "\n")
        
        # Remove the last newline character
        f.seek(0, os.SEEK_END)
        f.seek(f.tell() - 1, os.SEEK_SET)
        f.truncate()


def debug_print_symbol_table(symbol_table: dict[str, int]) -> None:
    print("Symbol Table:")
    for symbol, address in symbol_table.items():
        print(f"{symbol}: {address}")

def debug_print_cleaned_lines(cleaned_lines: list[str]) -> None:
    print("Cleaned lines:")
    instruction_number = 0

    for line in cleaned_lines:
        if line.startswith("(") and line.endswith(")"):
            print(f"{line} (label)")
        else:
            print(f"{line} (instruction {instruction_number})")
            instruction_number += 1

def debug_print_binary_commands(binary_commands: list[str]) -> None:
    print("Binary commands:")
    for command in binary_commands:
        print(command)