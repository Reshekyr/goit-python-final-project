def parse_input(input_string: str) -> tuple[str, list[str]]:
    command, *args = input_string.split()
    return command.lower(), args