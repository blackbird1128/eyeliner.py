import argparse
import sys
import importlib
import plugins.plugin_manager as plugin_manager
import colors.colors_converter as colors_converter

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Colors hex codes in a text file")
    parser.add_argument("--file", "-f", nargs="+", help="File to color")
    parser.add_argument("--plugin", "-p", nargs="+", help="Plugins to use")
    parser.add_argument("--css", "-c",  help="RGB css color regex",
                        action="store_true")
    parser.add_argument("--hex", "-x", help="Hex color regex",
                        action="store_true",default=True)
    args = parser.parse_args()
    content = None

    if args.plugin:
        for plugin in args.plugin:
            if not plugin.endswith(".py"):
                raise ValueError("Plugin must be a python file")
            plugin = plugin[:-3]
            plugin = plugin.replace("/", ".")
            importlib.import_module(plugin) # Remove .py
    if args.file:
        with open(args.file[0], "r") as f:
            content = f.read().strip()
    else:
        content = sys.stdin.read().strip()

    if args.hex:
        plugin_manager.register_for(r"(#[\da-fA-F]{6})")(colors_converter.hex_to_rgb)

    if args.css:
        plugin_manager.register_for(r"/rgb\((\d{3})\s*,\s*(\d{0,3})\s*,\s*(\d{3})\s*\)/gm")(colors_converter.css_rgb)

    for regex in plugin_manager.regex_converter.regexes_dict:
        for x in plugin_manager.regex_converter.get_compiled_regex(regex)\
                               .findall(content):
            r, g, b = plugin_manager.regex_converter.get_to_rgb_func(regex)(x,regex)
            current_code = f"\033[38;2;{r};{g};{b}m"
            content = content.replace(x, current_code + x + "\033[0m")
    print(content)
