from src.code import Code
from src.parser import Parser
from src.utils import (
    SYMBOL_TABLE,
    save_output_file,
    populate_symbol_table,
    find_and_clean_asm_file,
    debug_print_symbol_table,
    debug_print_cleaned_lines,
    debug_print_binary_commands
)



if __name__ == "__main__":
    cleaned_lines = find_and_clean_asm_file()
    populate_symbol_table(cleaned_lines, SYMBOL_TABLE)
    
    parser = Parser(cleaned_lines)

    processed_commands = []

    while parser.has_more_commands():
        parser.advance()
        command_type, command_value = parser.process_command()

        binary_command = None

        if command_type == "A":
            binary_command = Code.transform_a_command((command_type, command_value))
        elif command_type == "C":
            binary_command = Code.transform_c_command((command_type, command_value))
        else:
            continue

        if binary_command is not None:
            processed_commands.append(binary_command)

    # Save the processed commands to a .hack file
    save_output_file(processed_commands)

    # Debugging output
    #debug_print_cleaned_lines(cleaned_lines)
    #debug_print_symbol_table(SYMBOL_TABLE)
    #debug_print_binary_commands(processed_commands)
    
