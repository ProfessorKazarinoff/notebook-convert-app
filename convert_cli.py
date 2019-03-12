# -*- coding: utf-8 -*-
"""
convert_cli.py

This cli utility convets a jupyter notebook .ipynb-file into a .tex file. 

Arugments are:

--notebook
--template

@author: peter.kazarinoff
"""

from pathlib import Path
from argparse import ArgumentParser
#from gooey import Gooey, GooeyParser

from convert_funcs import (
    file_to_nbnode,
    export_nbnode,
    extract_lab_title,
    create_lab_title_template,
)


@Gooey(dump_build_config=True, program_name="Jupter Notebook Conversion Tool")
def main():
    desc = "A Python GUI App to convert Jupyter Notebooks to other formats"
    notebook_select_help_msg = "Select a Jupyter notebook file (.ipynb-file) to process"
    template_select_help_msg = "Select a template (.tplx-file) to apply"

    parser = ArgumentParser()
    parser.add_argument(
        "--infile", help=notebook_select_help_msg)
    parser.add_argument(
        "--outdir", help="Directory to save output")
    parser.add_argument(
        "--template", help=template_select_help_msg)

    args = parser.parse_args()
    nbnode = file_to_nbnode(args.Notebook_to_Convert)
    # construct output .tex file file path
    outfile_Path = Path(args.Output_Directory, Path(args.Notebook_to_Convert).stem)

    # construct template file path
    template_file_Path = Path(args.Template_File)

    # create lab_title.tplx file where the lab title from the input notebook file name is derived
    lab_title_str = extract_lab_title(args.Notebook_to_Convert)
    create_lab_title_template(lab_title_str, "lab_title.tplx")

    # export notebook node object to .tex file
    export_nbnode(nbnode, outfile_Path, pdf=False, template_file=template_file_Path)

    print(f"input file \n {args.Notebook_to_Convert}")
    print()
    print(f"output directory \n {args.Output_Directory}")
    print()
    print(f"template file \n {args.Template_File}")


if __name__ == "__main__":
    main()
