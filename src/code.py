from src.constants import DEST_TABLE, COMP_TABLE, JUMP_TABLE

class Code:
    @staticmethod
    def transform_a_command(command: tuple) -> str:
        _, value = command
        return f"{int(value):016b}"
    
    @staticmethod
    def transform_c_command(command: tuple) -> str:
        _, value = command
        dest, comp, jump = value
        
        dest_code = DEST_TABLE.get(dest, "000")
        comp_code = COMP_TABLE.get(comp)
        jump_code = JUMP_TABLE.get(jump, "000")

        if comp_code is None:
            raise ValueError(f"Invalid comp mnemonic: {comp}")
        
        return f"111{comp_code}{dest_code}{jump_code}"
