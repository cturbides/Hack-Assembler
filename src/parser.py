from src.utils import SYMBOL_TABLE

class Parser:
    def __init__(self: "Parser", lines: list[str]):
        self.lines = lines
        self.current_command = None
        self.current_index = -1

    def has_more_commands(self):
        return self.current_index + 1 < len(self.lines)

    def advance(self):
        if self.has_more_commands():
            self.current_index += 1
            self.current_command = self.lines[self.current_index]
    
    def is_label(self):
        return self.current_command.startswith("(") and self.current_command.endswith(")")

    def is_a_command(self):
        return self.current_command.startswith("@")
    
    def is_c_command(self):
        return not self.is_a_command() and not self.is_label()
    
    def process_command(self) -> tuple[str, str]:
        if self.is_label():
            return "L", self.current_command[1:-1]
        elif self.is_a_command():
            return self.process_a_command()
        elif self.is_c_command():
            return self.process_c_command()
        else:
            raise ValueError(f"Invalid command: {self.current_command}")

    def process_a_command(self) -> tuple[str, str]:
        symbol = self.current_command[1:]

        if symbol.isdigit():
            return "A", symbol
        elif symbol in SYMBOL_TABLE:
            return "A", str(SYMBOL_TABLE[symbol])
        else:
            raise ValueError(f"Undefined symbol: {symbol}") 

    def process_c_command(self) -> tuple[str, str]:
        dest, comp, jump = None, None, None

        # C command format: dest=comp;jump
        # dest and jump are optional
        if "=" in self.current_command: # dest=comp;jump
            dest, rest = self.current_command.split("=", 1) # rest = comp;jump.  dest = dest
        else:
            rest = self.current_command # comp;jump
        
        if ";" in rest: # comp;jump
            comp, jump = rest.split(";", 1) # comp = comp, jump = jump
        else:
            comp = rest # comp only
        
        return "C", (dest, comp, jump)
