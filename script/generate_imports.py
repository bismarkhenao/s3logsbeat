import sys
from os import listdir, getcwd
from os.path import abspath, isdir, join, dirname, basename
from argparse import ArgumentParser

comment = """Package include imports all input packages so that they register
their factories with the global registry. This package can be imported in the
main package to automatically register all of the standard supported inputs
modules."""

import_line_format = "\t_ \"{beat_path}/{module}/{name}\""
import_template = """/*
{comment}
*/
package {package}

import (
\t// This list is automatically generated by `make imports`
{imports}
)
"""


def get_importable_lines(go_beat_path, import_line):
    path = abspath("input")

    imported_input_lines = []

    # Skip the file folder, its not an input but I will do the move with another PR
    inputs = [p for p in listdir(path) if isdir(join(path, p)) and p.find("file") is -1]
    for input in sorted(inputs):
        input_import = import_line.format(beat_path=go_beat_path, module="input", name=input)
        imported_input_lines.append(input_import)

    return imported_input_lines


def generate_and_write_to_file(outfile, go_beat_path):
    imported_beat_lines = get_importable_lines(go_beat_path, import_line_format)
    imported_lines = "\n".join(imported_beat_lines)
    package = basename(dirname(outfile))
    list_go = import_template.format(package=package,
                                     comment=comment,
                                     imports=imported_lines)
    with open(outfile, "w") as output:
        output.write(list_go)


if __name__ == "__main__":
    parser = ArgumentParser(description="Generate imports for Beats packages")
    parser.add_argument("--out", default="include/list.go")
    parser.add_argument("beats_path")
    args = parser.parse_args()

    generate_and_write_to_file(args.out, args.beats_path)
