# -*- coding: utf-8 -*-
"""
convert_GUI.py

This script produces a GUI window that converts Jupyter notebooks into different formats
Created on Wed Dec  5 10:26:57 2018

@author: peter.kazarinoff
"""

from pathlib import Path

from gooey import Gooey, GooeyParser

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

    my_parser = GooeyParser(description=desc)
    my_parser.add_argument(
        "Notebook_to_Convert", help=notebook_select_help_msg, widget="FileChooser"
    )
    my_parser.add_argument(
        "Output_Directory", help="Directory to save output", widget="DirChooser"
    )
    my_parser.add_argument(
        "Template_File", help=template_select_help_msg, widget="FileChooser"
    )

    args = my_parser.parse_args()
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
