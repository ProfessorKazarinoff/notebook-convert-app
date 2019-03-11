# -*- coding: utf-8 -*-
"""
convert_script.py

This script converts a Jupyter notebook into a .tex file

@author: peter.kazarinoff
"""

from pathlib import Path

from convert_funcs import (
    file_to_nbnode,
    export_nbnode,
    extract_lab_title,
    create_lab_title_template,
)


def main():

    nb_filepath = Path('ENGR114-Lab07-Taylor_Series.ipynb')
    nbnode = file_to_nbnode(nb_filepath)
    # construct output .tex file file path
    outfile_Path = Path(Path(nb_filepath).stem)

    # construct template file path
    template_file_Path = Path('templates/ENGR114_lab_assignment.tplx')

    # create lab_title.tplx file where the lab title from the input notebook file name is derived
    lab_title_str = extract_lab_title(nb_filepath)
    create_lab_title_template(lab_title_str, "lab_title.tplx")

    # export notebook node object to .tex file
    export_nbnode(nbnode, outfile_Path, pdf=False, template_file=template_file_Path)

    print(f"input file \n {nb_filepath}")
    print()
    print(f"output directory \n {Path(nb_filepath).stem}")
    print()
    print(f"template file \n {template_file_Path}")


if __name__ == "__main__":
    main()
