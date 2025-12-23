"""
Unit tests for the Hack Assembler.

Run with: python -m pytest test_assembler.py
or: python test_assembler.py
"""

import unittest
import os
import sys
import tempfile
from pathlib import Path

# Add parent directory to path to import modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from parser import Parser
from code import Code
from symbol_table import SymbolTable
from assembler import assemble


class TestParser(unittest.TestCase):
    """Test cases for the Parser class."""
    
    def test_a_command(self):
        """Test parsing of A-commands."""
        # Create a temporary test file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.asm', delete=False) as f:
            test_file = f.name
            f.write('@100\n')
            f.write('@sum\n')
        
        parser = Parser(test_file)
        
        # First command: @100
        parser.advance()
        self.assertEqual(parser.command_type(), Parser.A_COMMAND)
        self.assertEqual(parser.symbol(), '100')
        
        # Second command: @sum
        parser.advance()
        self.assertEqual(parser.command_type(), Parser.A_COMMAND)
        self.assertEqual(parser.symbol(), 'sum')
        
        os.remove(test_file)
    
    def test_c_command(self):
        """Test parsing of C-commands."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.asm', delete=False) as f:
            test_file = f.name
            f.write('D=A\n')
            f.write('D;JGT\n')
            f.write('MD=D+1\n')
            f.write('0;JMP\n')
        
        parser = Parser(test_file)
        
        # D=A
        parser.advance()
        self.assertEqual(parser.command_type(), Parser.C_COMMAND)
        self.assertEqual(parser.dest(), 'D')
        self.assertEqual(parser.comp(), 'A')
        self.assertIsNone(parser.jump())
        
        # D;JGT
        parser.advance()
        self.assertEqual(parser.command_type(), Parser.C_COMMAND)
        self.assertIsNone(parser.dest())
        self.assertEqual(parser.comp(), 'D')
        self.assertEqual(parser.jump(), 'JGT')
        
        # MD=D+1
        parser.advance()
        self.assertEqual(parser.command_type(), Parser.C_COMMAND)
        self.assertEqual(parser.dest(), 'MD')
        self.assertEqual(parser.comp(), 'D+1')
        self.assertIsNone(parser.jump())
        
        # 0;JMP
        parser.advance()
        self.assertEqual(parser.command_type(), Parser.C_COMMAND)
        self.assertIsNone(parser.dest())
        self.assertEqual(parser.comp(), '0')
        self.assertEqual(parser.jump(), 'JMP')
        
        os.remove(test_file)
    
    def test_l_command(self):
        """Test parsing of L-commands (labels)."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.asm', delete=False) as f:
            test_file = f.name
            f.write('(LOOP)\n')
            f.write('(END)\n')
        
        parser = Parser(test_file)
        
        # (LOOP)
        parser.advance()
        self.assertEqual(parser.command_type(), Parser.L_COMMAND)
        self.assertEqual(parser.symbol(), 'LOOP')
        
        # (END)
        parser.advance()
        self.assertEqual(parser.command_type(), Parser.L_COMMAND)
        self.assertEqual(parser.symbol(), 'END')
        
        os.remove(test_file)
    
    def test_comments_and_whitespace(self):
        """Test that comments and whitespace are properly handled."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.asm', delete=False) as f:
            test_file = f.name
            f.write('// This is a comment\n')
            f.write('   \n')
            f.write('@100  // inline comment\n')
            f.write('  D=A  \n')
        
        parser = Parser(test_file)
        
        # First real command after skipping comments
        parser.advance()
        self.assertEqual(parser.command_type(), Parser.A_COMMAND)
        self.assertEqual(parser.symbol(), '100')
        
        # Second command
        parser.advance()
        self.assertEqual(parser.command_type(), Parser.C_COMMAND)
        self.assertEqual(parser.dest(), 'D')
        self.assertEqual(parser.comp(), 'A')
        
        os.remove(test_file)


class TestCode(unittest.TestCase):
    """Test cases for the Code class."""
    
    def test_dest_codes(self):
        """Test destination code translation."""
        self.assertEqual(Code.dest(None), '000')
        self.assertEqual(Code.dest('M'), '001')
        self.assertEqual(Code.dest('D'), '010')
        self.assertEqual(Code.dest('MD'), '011')
        self.assertEqual(Code.dest('A'), '100')
        self.assertEqual(Code.dest('AM'), '101')
        self.assertEqual(Code.dest('AD'), '110')
        self.assertEqual(Code.dest('AMD'), '111')
    
    def test_comp_codes(self):
        """Test computation code translation."""
        # Test a few key computations
        self.assertEqual(Code.comp('0'), '0101010')
        self.assertEqual(Code.comp('1'), '0111111')
        self.assertEqual(Code.comp('-1'), '0111010')
        self.assertEqual(Code.comp('D'), '0001100')
        self.assertEqual(Code.comp('A'), '0110000')
        self.assertEqual(Code.comp('M'), '1110000')
        self.assertEqual(Code.comp('D+A'), '0000010')
        self.assertEqual(Code.comp('D+M'), '1000010')
    
    def test_jump_codes(self):
        """Test jump code translation."""
        self.assertEqual(Code.jump(None), '000')
        self.assertEqual(Code.jump('JGT'), '001')
        self.assertEqual(Code.jump('JEQ'), '010')
        self.assertEqual(Code.jump('JGE'), '011')
        self.assertEqual(Code.jump('JLT'), '100')
        self.assertEqual(Code.jump('JNE'), '101')
        self.assertEqual(Code.jump('JLE'), '110')
        self.assertEqual(Code.jump('JMP'), '111')


class TestSymbolTable(unittest.TestCase):
    """Test cases for the SymbolTable class."""
    
    def test_predefined_symbols(self):
        """Test that predefined symbols are present."""
        table = SymbolTable()
        
        # Test registers
        self.assertTrue(table.contains('R0'))
        self.assertEqual(table.get_address('R0'), 0)
        self.assertTrue(table.contains('R15'))
        self.assertEqual(table.get_address('R15'), 15)
        
        # Test special symbols
        self.assertTrue(table.contains('SP'))
        self.assertEqual(table.get_address('SP'), 0)
        self.assertTrue(table.contains('SCREEN'))
        self.assertEqual(table.get_address('SCREEN'), 16384)
        self.assertTrue(table.contains('KBD'))
        self.assertEqual(table.get_address('KBD'), 24576)
    
    def test_add_entry(self):
        """Test adding new entries to symbol table."""
        table = SymbolTable()
        
        table.add_entry('LOOP', 10)
        self.assertTrue(table.contains('LOOP'))
        self.assertEqual(table.get_address('LOOP'), 10)
        
        table.add_entry('sum', 16)
        self.assertTrue(table.contains('sum'))
        self.assertEqual(table.get_address('sum'), 16)


class TestAssembler(unittest.TestCase):
    """Test cases for the complete assembler."""
    
    def test_add_program(self):
        """Test assembling the Add.asm program."""
        expected_output = [
            '0000000000000010',  # @2
            '1110110000010000',  # D=A
            '0000000000000011',  # @3
            '1110000010010000',  # D=D+A
            '0000000000000000',  # @0
            '1110001100001000',  # M=D
        ]
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.asm', delete=False) as f:
            test_file = f.name
            f.write('@2\n')
            f.write('D=A\n')
            f.write('@3\n')
            f.write('D=D+A\n')
            f.write('@0\n')
            f.write('M=D\n')
        
        result = assemble(test_file)
        self.assertEqual(result, expected_output)
        
        # Clean up
        os.remove(test_file)
        os.remove(test_file.replace('.asm', '.hack'))
    
    def test_labels(self):
        """Test assembling a program with labels."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.asm', delete=False) as f:
            test_file = f.name
            f.write('@R0\n')
            f.write('D=M\n')
            f.write('@STOP\n')
            f.write('D;JEQ\n')
            f.write('(STOP)\n')
            f.write('@STOP\n')
            f.write('0;JMP\n')
        
        result = assemble(test_file)
        
        # The label STOP should point to instruction 4 (index 4)
        # So @STOP should become @4
        self.assertEqual(result[2], '0000000000000100')  # @4
        self.assertEqual(result[4], '0000000000000100')  # @4 (after label)
        
        # Clean up
        os.remove(test_file)
        os.remove(test_file.replace('.asm', '.hack'))
    
    def test_variables(self):
        """Test assembling a program with variables."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.asm', delete=False) as f:
            test_file = f.name
            f.write('@sum\n')
            f.write('M=0\n')
            f.write('@counter\n')
            f.write('M=1\n')
        
        result = assemble(test_file)
        
        # First variable (sum) should be at address 16
        self.assertEqual(result[0], '0000000000010000')  # @16
        # Second variable (counter) should be at address 17
        self.assertEqual(result[2], '0000000000010001')  # @17
        
        # Clean up
        os.remove(test_file)
        os.remove(test_file.replace('.asm', '.hack'))


if __name__ == '__main__':
    unittest.main()
