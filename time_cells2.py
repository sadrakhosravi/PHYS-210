# See https://nbviewer.jupyter.org/gist/minrk/5491090/analysis.ipynb
from nbformat import reader
import time as _time
# this is time_cells2.py
# Updated Oct 2020 CM

# Interface: 
# set nb_name, cells_to_time and cells_to_exclude.
# if cells_to_time is not empty, we time only the cells listed.
# if cells_to time is empty or doesn't exist, we test all cells except those in cells_to_exclude
# stop_at has a list of cells that will be stopping points.

# then do: run -i time_cells2.py


cells_found = []
# current notebook file:

tdiff = 0
nbf = open(nb_name, "r")
nb = reader.read(nbf)
nbf.close()

ip = get_ipython()

time_only = False
try:
    if len(cells_to_time) > 0:
        time_only = True
except:
    pass

try:
    if len(stop_at) > 0:
        pass
except:
    stop_at = []
# print("time_only is",time_only)
if time_only == True:
    # time only premade cells, with listed cell id's
    for cell in nb.cells:
        if cell.cell_type != 'code':
            continue
        try:
            if cell.metadata.nbgrader.grade_id in stop_at:
                # print("Stopping at cell", cell.metadata.nbgrader.grade_id)
                break
            if cell.metadata.nbgrader.grade_id in cells_to_time:
                cells_found.append(cell.metadata.nbgrader.grade_id)
                start = _time.process_time()
                ip.run_cell(cell.source)
                end = _time.process_time()
                tdiff += end-start
                print("Time for cell:", cell.metadata.nbgrader.grade_id,"time: %.2f"%(end-start))
        except:
            pass
else:
    for cell in nb.cells:
        # here, we want to time code cells that students might have created, that don't have ids
        if cell.cell_type != 'code':
            continue
        try:
            if cell.metadata.nbgrader.grade_id in stop_at:
                # print("Stopping at cell", cell.metadata.nbgrader.grade_id)
                break
            if cell.metadata.nbgrader.grade_id in cells_to_exclude:
                continue
            cells_found.append(cell.metadata.nbgrader.grade_id)
        except:
            pass
        start = _time.process_time()
        ip.run_cell(cell.source)
        end = _time.process_time()
        tdiff += end-start
        try:
            print("Time for cell:",cell.metadata.nbgrader.grade_id,"time: %.2f"%(end-start))
        except:
            print("Time for unnamed cell: %.2f"%(end-start))
# print("Found cells:", cells_found)
# print("Cells desired:",cells_to_time)
print("Total time: %.2f"%(tdiff))
