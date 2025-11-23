"""
Code module for Hack Assembly Language.

This module translates Hack assembly language mnemonics into binary codes.
"""


class Code:
    """Translates Hack assembly language mnemonics into binary codes."""
    
    # Computation mappings (a=0)
    COMP_0 = {
        '0':   '0101010',
        '1':   '0111111',
        '-1':  '0111010',
        'D':   '0001100',
        'A':   '0110000',
        '!D':  '0001101',
        '!A':  '0110001',
        '-D':  '0001111',
        '-A':  '0110011',
        'D+1': '0011111',
        'A+1': '0110111',
        'D-1': '0001110',
        'A-1': '0110010',
        'D+A': '0000010',
        'D-A': '0010011',
        'A-D': '0000111',
        'D&A': '0000000',
        'D|A': '0010101',
    }
    
    # Computation mappings (a=1, using M instead of A)
    COMP_1 = {
        'M':   '1110000',
        '!M':  '1110001',
        '-M':  '1110011',
        'M+1': '1110111',
        'M-1': '1110010',
        'D+M': '1000010',
        'D-M': '1010011',
        'M-D': '1000111',
        'D&M': '1000000',
        'D|M': '1010101',
    }
    
    # Destination mappings
    DEST = {
        None:  '000',
        'M':   '001',
        'D':   '010',
        'MD':  '011',
        'A':   '100',
        'AM':  '101',
        'AD':  '110',
        'AMD': '111',
    }
    
    # Jump mappings
    JUMP = {
        None:  '000',
        'JGT': '001',
        'JEQ': '010',
        'JGE': '011',
        'JLT': '100',
        'JNE': '101',
        'JLE': '110',
        'JMP': '111',
    }
    
    @staticmethod
    def dest(mnemonic):
        """Returns the binary code of the dest mnemonic."""
        return Code.DEST.get(mnemonic, '000')
    
    @staticmethod
    def comp(mnemonic):
        """Returns the binary code of the comp mnemonic."""
        if mnemonic in Code.COMP_0:
            return Code.COMP_0[mnemonic]
        elif mnemonic in Code.COMP_1:
            return Code.COMP_1[mnemonic]
        else:
            raise ValueError(f"Unknown computation mnemonic: {mnemonic}")
    
    @staticmethod
    def jump(mnemonic):
        """Returns the binary code of the jump mnemonic."""
        return Code.JUMP.get(mnemonic, '000')
