#!/usr/bin/env python3
"""
Hack Assembler - Main Module

This is the main driver that puts everything together. It performs a two-pass
assembly process:
1. First pass: Builds the symbol table with all label definitions
2. Second pass: Generates the machine code

Usage: python assembler.py <input.asm>
"""

import sys
import os
from parser import Parser
from code import Code
from symbol_table import SymbolTable


def assemble(input_file, output_file=None):
    """Assembles a Hack assembly file into machine code.
    
    Args:
        input_file: Path to the .asm file
        output_file: Path to the output .hack file (optional)
    
    Returns:
        List of binary instructions
    """
    if output_file is None:
        output_file = input_file.replace('.asm', '.hack')
    
    symbol_table = SymbolTable()
    
    # First pass: Build symbol table with label definitions
    parser = Parser(input_file)
    rom_address = 0
    
    while parser.has_more_commands():
        parser.advance()
        if parser.current_command is None:
            continue
            
        command_type = parser.command_type()
        
        if command_type == Parser.L_COMMAND:
            # Add label to symbol table
            symbol = parser.symbol()
            symbol_table.add_entry(symbol, rom_address)
        else:
            # A-instruction or C-instruction
            rom_address += 1
    
    # Second pass: Generate machine code
    parser = Parser(input_file)
    binary_instructions = []
    ram_address = 16  # Start of RAM for variables
    
    while parser.has_more_commands():
        parser.advance()
        if parser.current_command is None:
            continue
            
        command_type = parser.command_type()
        
        if command_type == Parser.A_COMMAND:
            # A-instruction
            symbol = parser.symbol()
            
            # Check if it's a number or a symbol
            if symbol.isdigit():
                address = int(symbol)
            else:
                # It's a symbol
                if not symbol_table.contains(symbol):
                    # New variable
                    symbol_table.add_entry(symbol, ram_address)
                    ram_address += 1
                address = symbol_table.get_address(symbol)
            
            # Convert to 16-bit binary (A-instruction: 0vvvvvvvvvvvvvvv)
            binary = format(address, '016b')
            binary_instructions.append(binary)
            
        elif command_type == Parser.C_COMMAND:
            # C-instruction: 111accccccdddjjj
            dest = parser.dest()
            comp = parser.comp()
            jump = parser.jump()
            
            dest_code = Code.dest(dest)
            comp_code = Code.comp(comp)
            jump_code = Code.jump(jump)
            
            binary = '111' + comp_code + dest_code + jump_code
            binary_instructions.append(binary)
    
    # Write to output file
    with open(output_file, 'w') as f:
        for instruction in binary_instructions:
            f.write(instruction + '\n')
    
    return binary_instructions


def main():
    """Main function to run the assembler from command line."""
    if len(sys.argv) < 2:
        print("Usage: python assembler.py <input.asm>")
        print("Example: python assembler.py Add.asm")
        sys.exit(1)
    
    input_file = sys.argv[1]
    
    if not os.path.exists(input_file):
        print(f"Error: File '{input_file}' not found.")
        sys.exit(1)
    
    if not input_file.endswith('.asm'):
        print("Error: Input file must have .asm extension.")
        sys.exit(1)
    
    output_file = input_file.replace('.asm', '.hack')
    
    try:
        assemble(input_file, output_file)
        print(f"Assembly successful! Output written to {output_file}")
    except Exception as e:
        print(f"Error during assembly: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
