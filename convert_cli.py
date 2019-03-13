# -*- coding: utf-8 -*-
"""
convert_cli.py

This cli utility convets a jupyter notebook .ipynb-file into a .tex file. 

Arugments are:

--infile
--outdir
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


def main():
    
    notebook_select_help_msg = "Select a Jupyter notebook file (.ipynb-file) to process"
    outdir_select_help_msg = "Select an output directory. . for current directory"
    template_select_help_msg = "Select a template (.tplx-file) to apply"

    parser = ArgumentParser()
    parser.add_argument(
        "--infile", help=notebook_select_help_msg)
    parser.add_argument(
        "--outdir", help=outdir_select_help_msg)
    parser.add_argument(
        "--template", help=template_select_help_msg)

    args = parser.parse_args()
    
    # construct output .tex-file file path
    outfile_Path = Path(args.outdir, Path(args.infile).stem)

    # construct template file path
    template_file_Path = Path(args.template)

    # convert input notebook to a notebook node object
    nbnode = file_to_nbnode(args.infile)
    
    # create lab_title.tplx file where the lab title from the input notebook file name is derived
    lab_title_str = extract_lab_title(args.infile)
    create_lab_title_template(lab_title_str, "lab_title.tplx")

    # export notebook node object to .tex file
    export_nbnode(nbnode, outfile_Path, pdf=False, template_file=template_file_Path)

    print(f"\n input notebook: {args.infile}")
    print(f" output .tex-file: {outfile_Path}.tex")
    print(f" template file: {args.template} \n")


if __name__ == "__main__":
    main()
