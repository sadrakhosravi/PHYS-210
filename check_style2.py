import pycodestyle as pycodestyle_module
from nbformat import reader
import sys
import io
import os

# in a notebook cell, set cells_to_check and nb_name
# or leave cells_to_check empty, and use cells_to_exclude
# stop_at: if not empty will be a list of cells to terminate at.

# then do: run -i check_style2.py

cells_found = []
tfile = '._test_pycodestyle.py'

ignore_codes = ['W292', 'W391', 'F401', 'F821', 'E266', 'E402', 'W605']  # E266 catches ###
# E402 gets import after %magic on first line
# W 605 finds \m inside a latex string...
ignore_base = ['E121', 'E123', 'E126', 'E133', 'E226', 'E241', 'E242', 'E704', 'W503', 'W504', 'W505']

# read in the notebook.
nbf = open(nb_name,"r")
nb = reader.read(nbf)
nbf.close()

errors = False

test_only = False
try:
    if len(cells_to_check) > 0:
        test_only = True
except:
    cells_to_check = []

def do_cell(cell):
    g = open(tfile,"w")
    g.write(cell.source)
    g.close()
    try:
        print("checking cell:", cell.metadata.nbgrader.grade_id)
    except:
        print("checking unnamed cell")
    old_stdout = sys.stdout
    sys.stdout = io.StringIO()
    # use pycodestyle as the magic does:
    pycodestyle = pycodestyle_module.StyleGuide(format='%(row)d:%(col)d: %(code)s %(text)s', 
           ignore=ignore_codes + ignore_base, max_line_length=79)
    pcs_result = pycodestyle.check_files(paths=[tfile])
    out_result = sys.stdout.getvalue().splitlines()
    sys.stdout = old_stdout
    os.remove(tfile)
    if len(out_result) > 0:
        #errors = True
        print("Style errors or warnings found:")
        for l in out_result:
            print(l)
        return True
    return False

if test_only:
    for cell in nb.cells:
        found = False
        if cell.cell_type != 'code':
            continue
        try:
            # print(cell.metadata.nbgrader.grade_id)
            if cell.metadata.nbgrader.grade_id in stop_at:
                break
            if cell.metadata.nbgrader.grade_id in cells_to_check:
                errors = do_cell(cell) or errors
        except:
            continue
else:
    for cell in nb.cells:
        found = False
        if cell.cell_type != 'code':
            continue
        try:
            # print(cell.metadata.nbgrader.grade_id)
            if cell.metadata.nbgrader.grade_id in stop_at:
                break
            if cell.metadata.nbgrader.grade_id in cells_to_exclude:
                continue
        except:
            pass
        errors = do_cell(cell) or errors

if errors:
    raise AssertionError
