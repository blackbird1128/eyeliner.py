import argparse
import sys
from typing import Tuple
import importlib
from plugin_manager import *

def hex_to_rgb(code : str, regex: str) -> Tuple[int, int, int]:
    """ Converts a hex code to rgb """
    code = code[1:]
    r = int(code[0:2], 16)
    g = int(code[2:4], 16)
    b = int(code[4:6], 16)
    return r, g, b

def css_rgb(code : str, regex: str ) -> Tuple[int, int, int]:
    """ Converts a css rgb code to rgb """
    code = code[4:-1]
    r, g, b = code.split(",")
    return int(r), int(g), int(b)

if __name__ == "__main__":

    built_in_regexes = [ (r"(#[\da-fA-F]{6})", hex_to_rgb),
                        (r"/rgb\((\d{3})\s*,\s*(\d{0,3})\s*,\s*(\d{3})\s*\)/gm",
                         css_rgb) ]
 
    parser = argparse.ArgumentParser(description="Colors hex codes in a text file")
    parser.add_argument("--file", "-f", nargs="+", help="File to color")
    parser.add_argument("--plugin", "-p", nargs="+", help="Plugins to use")
    parser.add_argument("--rgb", "-r",  help="RGB css color regex", action="store_true")
    parser.add_argument("--hex", "-x", help="Hex color regex", action="store_true",default=True)
    args = parser.parse_args()
    content = None   

    if args.plugin:
        for plugin in args.plugin:
            if not plugin.endswith(".py"):
                raise ValueError("Plugin must be a python file")
            importlib.import_module(plugin[:-3]) # Remove .py

    if args.file:
        with open(args.file[0], "r") as f:
            content = f.read().strip()
    else:
        content = sys.stdin.read().strip()

    if args.hex:
        register_for(r"(#[\da-fA-F]{6})")(hex_to_rgb)

    if args.rgb:
        register_for(r"/rgb\((\d{3})\s*,\s*(\d{0,3})\s*,\s*(\d{3})\s*\)/gm")(css_rgb)

    for regex in regex_converter.regexes_dict:
        for x in regex_converter.get_compiled_regex(regex).findall(content):
            r, g, b = regex_converter.get_to_rgb_func(regex)(x,regex)
            current_code = f"\033[38;2;{r};{g};{b}m"
            content = content.replace(x, current_code + x + "\033[0m")
    print(content)
