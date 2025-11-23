"""
Parser module for Hack Assembly Language.

This module handles the parsing of .asm files, breaking down each instruction
into its underlying components.
"""


class Parser:
    """Encapsulates access to the input code. Reads an assembly language command,
    parses it, and provides convenient access to the command's components."""
    
    A_COMMAND = 0
    C_COMMAND = 1
    L_COMMAND = 2
    
    def __init__(self, input_file):
        """Opens the input file and gets ready to parse it."""
        with open(input_file, 'r') as f:
            self.lines = f.readlines()
        self.current_line = 0
        self.current_command = None
        
    def has_more_commands(self):
        """Are there more commands in the input?"""
        return self.current_line < len(self.lines)
    
    def advance(self):
        """Reads the next command from the input and makes it the current command.
        Should be called only if has_more_commands() is true."""
        while self.has_more_commands():
            line = self.lines[self.current_line].strip()
            self.current_line += 1
            
            # Remove comments
            if '//' in line:
                line = line[:line.index('//')]
            line = line.strip()
            
            # Skip empty lines
            if not line:
                continue
                
            self.current_command = line
            return
            
        self.current_command = None
    
    def command_type(self):
        """Returns the type of the current command:
        A_COMMAND for @Xxx where Xxx is either a symbol or a decimal number
        C_COMMAND for dest=comp;jump
        L_COMMAND for (Xxx) where Xxx is a symbol."""
        if self.current_command is None:
            return None
            
        if self.current_command.startswith('@'):
            return self.A_COMMAND
        elif self.current_command.startswith('(') and self.current_command.endswith(')'):
            return self.L_COMMAND
        else:
            return self.C_COMMAND
    
    def symbol(self):
        """Returns the symbol or decimal Xxx of the current command @Xxx or (Xxx).
        Should be called only when command_type() is A_COMMAND or L_COMMAND."""
        if self.command_type() == self.A_COMMAND:
            return self.current_command[1:]  # Remove @
        elif self.command_type() == self.L_COMMAND:
            return self.current_command[1:-1]  # Remove ( and )
        return None
    
    def dest(self):
        """Returns the dest mnemonic in the current C-command.
        Should be called only when command_type() is C_COMMAND."""
        if self.command_type() != self.C_COMMAND:
            return None
            
        if '=' in self.current_command:
            return self.current_command.split('=')[0]
        return None
    
    def comp(self):
        """Returns the comp mnemonic in the current C-command.
        Should be called only when command_type() is C_COMMAND."""
        if self.command_type() != self.C_COMMAND:
            return None
            
        command = self.current_command
        
        # Remove dest part if exists
        if '=' in command:
            command = command.split('=')[1]
        
        # Remove jump part if exists
        if ';' in command:
            command = command.split(';')[0]
            
        return command
    
    def jump(self):
        """Returns the jump mnemonic in the current C-command.
        Should be called only when command_type() is C_COMMAND."""
        if self.command_type() != self.C_COMMAND:
            return None
            
        if ';' in self.current_command:
            return self.current_command.split(';')[1]
        return None
