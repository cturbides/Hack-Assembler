"""
Hack Assembler Package

A Python implementation of the Hack Assembler from the NAND to Tetris course.
"""

__version__ = '1.0.0'
__author__ = 'NAND to Tetris Implementation'

from .parser import Parser
from .code import Code
from .symbol_table import SymbolTable
from .assembler import assemble

__all__ = ['Parser', 'Code', 'SymbolTable', 'assemble']
