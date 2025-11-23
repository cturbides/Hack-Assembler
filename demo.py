#!/usr/bin/env python3
"""
Demo script showing how to use the Hack Assembler programmatically.

This script demonstrates the basic usage of the assembler API.
"""

from assembler import assemble
import os


def demo():
    """Demonstrate basic assembler usage."""
    print("Hack Assembler Demo")
    print("=" * 50)
    
    # Example 1: Assemble a simple program
    print("\nExample 1: Assembling Add.asm")
    print("-" * 50)
    
    input_file = "examples/Add.asm"
    if os.path.exists(input_file):
        binary_code = assemble(input_file)
        print(f"Input file: {input_file}")
        print(f"Number of instructions: {len(binary_code)}")
        print("\nFirst 3 binary instructions:")
        for i, instruction in enumerate(binary_code[:3]):
            print(f"  Line {i}: {instruction}")
    else:
        print(f"Error: {input_file} not found")
    
    # Example 2: Show supported features
    print("\n\nExample 2: Assembler Features")
    print("-" * 50)
    print("✓ A-instructions: @value or @symbol")
    print("✓ C-instructions: dest=comp;jump")
    print("✓ Labels: (LABEL_NAME)")
    print("✓ Comments: // comment")
    print("✓ Predefined symbols: R0-R15, SP, LCL, ARG, THIS, THAT, SCREEN, KBD")
    print("✓ User-defined variables (allocated from RAM[16])")
    
    # Example 3: Show available example files
    print("\n\nExample 3: Available Examples")
    print("-" * 50)
    examples_dir = "examples"
    if os.path.exists(examples_dir):
        asm_files = [f for f in os.listdir(examples_dir) if f.endswith('.asm')]
        for asm_file in sorted(asm_files):
            filepath = os.path.join(examples_dir, asm_file)
            with open(filepath, 'r') as f:
                lines = [l for l in f.readlines() if l.strip() and not l.strip().startswith('//')]
                print(f"  {asm_file}: {len(lines)} code lines")
    
    print("\n" + "=" * 50)
    print("Demo complete!")


if __name__ == '__main__':
    demo()
