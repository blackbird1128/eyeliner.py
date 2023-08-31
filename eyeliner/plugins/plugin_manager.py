import re

class RegexConverter:
    """
    Class to store regexes and their respective functions to convert to rgb
    """
    def __init__(self) -> None:
        self.regexes_dict = {}
    
    def add_regex_manually(self, regex, func_to_rgb):
        self.regexes_dict[regex] = (func_to_rgb, re.compile(regex))

    def get_compiled_regex(self, regex):
        return self.regexes_dict[regex][1]

    def get_to_rgb_func(self, regex):
        return self.regexes_dict[regex][0]

global regex_converter
regex_converter = RegexConverter()

def register_for(regex :str):
    """
    Decorator to register a function to convert a regex match to rgb
    The function must have the following signature:
    def func_to_rgb(code : str, regex: str) -> Tuple[int, int, int]:
    """
    def decorator_regex_register(func):
        if regex in regex_converter.regexes_dict:
            raise ValueError(f"Regex {regex} already exists")
        else:
            regex_converter.add_regex_manually(regex, func)
        return func
    return decorator_regex_register
