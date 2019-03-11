# -*- coding: utf-8 -*-
"""
converters.py

This module contains functions to convert Jupyter notebooks into different formats
Created on Wed Dec  5 09:10:57 2018

@author: peter.kazarinoff
"""
# standard lib
import os
from pathlib import Path

# nb specific
import nbformat
from nbconvert import LatexExporter
from nbconvert.writers import FilesWriter
from nbformat import NotebookNode

# project specific
from filter_links import convert_links


class MyLatexExporter(LatexExporter):
    def default_filters(self):
        yield from super().default_filters()
        yield ("resolve_references", convert_links)


def nbnode_to_tex(nb_node, filename="texout"):
    """
    function to export a .tex  file given a notebookNode object as input
    :param nb_node: notebookNode object
    :param filename: str, the name of the output .tex file. Don't need .tex extension
    :return: nothing returned, but function will output a new .pdf file
    """
    e = MyLatexExporter
    body, resources = e.from_notebook_node(nb=nb_node)
    writer = FilesWriter()
    writer.write(body, resources, notebook_name=filename)


def file_to_nbnode(notebook_filename):
    """
    a function that creates a single notebook node object from a notebook file path
    :param notebook_filename: of a notebook ends in .ipynb
    :return: a single notebookNode object
    """
    # with open(notebook_filename, 'r', encoding='utf-8') as f:
    #   nb_node = nbformat.read(f, as_version=4)
    with open(notebook_filename, "r", encoding="utf-8") as f:
        nb_node = nbformat.read(f, as_version=4)
    return nb_node


def extract_lab_title(notebook_path):
    """
    Function extracts the name of a lab from a full file path
    ENGR114 is removed from the filename
    All dashes and underscores are converted to spaces

    :param notebook_filename: a full path to a notebook
    :return: str: a string which is the name of the lab, with spaces between the words
    """
    fname = Path(notebook_path).stem
    labname = fname.strip("ENGR114")
    labname_underscore_to_spaces = labname.replace("_", " ")
    labname_dashes_to_spaces = labname_underscore_to_spaces.replace("-", " ")
    labname_no_leading_spaces = labname_dashes_to_spaces.rstrip().lstrip()
    return labname_no_leading_spaces


def create_lab_title_template(labname_str, template_name="lab_title.tplx"):
    """
    Function creater_header_template takes in a lab name with spaces and creates a template file with the lab name in the file
    :param labname:
    :return: None, the function creates a file when it runs
    """
    template_path = os.path.join(os.getcwd(), "templates", template_name)
    header = "%% lab_title.tplx %% \n \n"
    s = "\\newcommand{{{}}}{{{}}} \n".format("\\labtitle", labname_str)
    with open(template_path, "w") as f:
        f.writelines(header)
        f.writelines(s)


def export_nbnode(
    combined_nb: NotebookNode, output_file: Path, pdf=False, template_file=None
):
    resources = {}
    resources["unique_key"] = "combined"
    resources["output_files_dir"] = "combined_files"

    # log.info('Converting to %s', 'pdf' if pdf else 'latex')
    exporter = MyLatexPDFExporter() if pdf else MyLatexExporter()
    if template_file is not None:
        exporter.template_file = str(template_file)
    writer = FilesWriter(build_directory=str(output_file.parent))
    output, resources = exporter.from_notebook_node(combined_nb, resources)
    writer.write(output, resources, notebook_name=output_file.stem)


def convert_notebook(
    notebookfile="sample.ipynb",
    outputfile="texout",
    templatefile="article.tplx",
    debug_flag=False,
):
    # convert notebook file to notebook node object
    nbnode = file_to_nbnode(notebookfile)

    # construct output .tex file file path
    outfile_Path = Path(os.path.join(os.getcwd(), "tex", outputfile))

    # construct template file path
    template_file_Path = Path(os.path.join(os.getcwd(), "templates", templatefile))

    # export notebook node object to .tex file
    export_nbnode(nbnode, outfile_Path, pdf=False, template_file=template_file_Path)

    # print success
    if debug_flag == True:
        print("Notebook conversion successful")
        print(f'Notebook file: {"sample.ipynb"}')
        print(f"Converted to file: {outfile_Path}")


def main(debug_flag=False):
    # convert notebook file to notebook node object
    nbnode = file_to_nbnode("sample.ipynb")

    # construct output .tex file file path
    outfile_Path = Path(os.path.join(os.getcwd(), "tex", "texout"))

    # construct template file path
    template_file_Path = Path(
        os.path.join(os.getcwd(), "templates", "article.tplx")
    )  # more template changes needed, but it is a start

    # export notebook node object to .tex file
    export_nbnode(nbnode, outfile_Path, pdf=False, template_file=template_file_Path)

    # print success
    if debug_flag == True:
        print("Notebook conversion successful")
        print(f'Notebook file: {"sample.ipynb"}')
        print(f"Converted to file: {outfile_Path}")


if __name__ == "__main__":
    convert_notebook(
        notebookfile="sample2.ipynb",
        outputfile="sample2",
        templatefile="ENGR114_lab_assignment.tplx",
        debug_flag=False,
    )
#    main(debug_flag=True)
