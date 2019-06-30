#import hou
import csv
import os
import sys
import math
from os import path
from random import randint

# insert library
sys.path.insert(0, "/Users/dani/matplotlib")
sys.path.insert(0, "/Users/dani/numpy")

class Cell:
    def __init__(self, name, i):
        self.name = name
        self.data = {}
        self.id = i

    def addProtein(self, protein, value):
        self.data[protein] = value

    def __iter__(self):
        return iter(self.data.items())

    def __str__(self):
        return "Cell(name: {} id: {} proteins: {})".format(self.name, self.id, len(self.data))

class Universe:
    def __init__(self, reader):
        reader.load()
        cells = []

        for (cell_id, cell_name)in reader.cells:
            cell = Cell(cell_name, cell_id)
            cells.append(cell)

        for cell in cells:  
            for (protein, protein_id) in reader.proteins.items():
                # print(cell.name, protein, protein_id, cell.id)
                # print(reader.rows[protein_id][cell.id])
                value = reader.rows[protein_id][cell.id]
                cell.addProtein(protein, value)
        self.cells = cells


    def __iter__(self):
        return iter(self.cells)
    def __str__(self):
        return "Universe(size: {})".format(len(self.cells))


class Reader:
    def __init__(self, filename):
        self.filename = filename
        self.cells = []
        self.rows = []
        self.proteins = {} 
    
    def load(self):
        with open(self.filename) as fp:
            reader = csv.reader(fp)
            header = next(reader)
            self.cells = [ (index-1, name) for index, name in enumerate(header) if name != ""]
            index = 0
            for row in reader:
                self.rows.append([ float(i) for i in row[1:]])
                self.proteins[row[0]] = index
                index += 1
               
    

def mul(v, f): return [ v[0] * f, v[1] * f, v[2] * f]
def add(v, i): return [ v[0] + i, v[1] + i, v[2] + i]

class Render:
    def __init__(self, context, config):
        self.config = config
        self.context = context
        
        # configure cells
        self.context.addAttrib(hou.attribType.Point, "source", "")
        self.context.addAttrib(hou.attribType.Point, "pscale", (1.0))
        self.context.addAttrib(hou.attribType.Point, "protein", "")
        self.context.addAttrib(hou.attribType.Point, "Cd", (1.0, 1.0, 1.0))
    
    def render(self, cell):
        config = self.config[cell.name]

        direction = config['vec']
        config = config['color']
        delta = 1
        offset = 0

        for (protein, value) in cell:
            pos = hou.Vector3(*add(direction, delta*offset))
            
            point = self.context.createPoint()

            point.setPosition(pos)
            point.setAttribValue("source", cell.name)
            point.setAttribValue("pscale", value)
            point.setAttribValue("protein", protein)
            point.setAttribValue("Cd", *mul(color, value))

            offset += 1
            
            # point = geo.createPoint()
            # point.setPosition(vec)
            # point.setAttribValue("source", cell_name)
            # point.setAttribValue("protein", cell_protein)
            # color
            # point.setAttribValue("Cd", hou.Vector3(*cell_color))


def main(data_file, context, config):
    print("Reading % s" % data_file)
    reader = Reader(data_file)

    print("Processing data...")
    universe = Universe(reader)
    print("Using Universe: ", universe)

    print("Creating Renderer...")
    render = Render(context, config)

    for cell in universe:
        print("Rendering: ", cell)
        render.render(cell)
        break
        




config = {
'Bcells_CIS0012' : { 'color' : [0.0, 0.0, 0.0], 'vec' : [0.0, 0.0, 0.0]},
'CD3-CD4+HLADR+_CIS0012' : { 'color' : [0.0, 0.0, 0.0], 'vec' : [0.0, 0.0, 0.0]},
'CD4Tcells_CIS0012' : { 'color' : [0.0, 0.0, 0.0], 'vec' : [0.0, 0.0, 0.0]},
'CD8Tcells_CIS0012' : { 'color' : [0.0, 0.0, 0.0], 'vec' : [0.0, 0.0, 0.0]},
'DNTcells_CIS0012' : { 'color' : [0.0, 0.0, 0.0], 'vec' : [0.0, 0.0, 0.0]},
'ignore_CIS0012' : { 'color' : [0.0, 0.0, 0.0], 'vec' : [0.0, 0.0, 0.0]},
'Myeloid_CIS0012' : { 'color' : [0.0, 0.0, 0.0], 'vec' : [0.0, 0.0, 0.0]},
'NKcells_CIS0012' : { 'color' : [0.0, 0.0, 0.0], 'vec' : [0.0, 0.0, 0.0]},
'Bcells_CIS0021' : { 'color' : [0.0, 0.0, 0.0], 'vec' : [0.0, 0.0, 0.0]},
'CD3-CD4+HLADR+_CIS0021' : { 'color' : [0.0, 0.0, 0.0], 'vec' : [0.0, 0.0, 0.0]},
'CD4Tcells_CIS0021' : { 'color' : [0.0, 0.0, 0.0], 'vec' : [0.0, 0.0, 0.0]},
'CD8Tcells_CIS0021' : { 'color' : [0.0, 0.0, 0.0], 'vec' : [0.0, 0.0, 0.0]},
'DNTcells_CIS0021' : { 'color' : [0.0, 0.0, 0.0], 'vec' : [0.0, 0.0, 0.0]},
'ignore_CIS0021' : { 'color' : [0.0, 0.0, 0.0], 'vec' : [0.0, 0.0, 0.0]},
'Myeloid_CIS0021' : { 'color' : [0.0, 0.0, 0.0], 'vec' : [0.0, 0.0, 0.0]},
'NKcells_CIS0021' : { 'color' : [0.0, 0.0, 0.0], 'vec' : [0.0, 0.0, 0.0]},
'Bcells_CIS0022' : { 'color' : [0.0, 0.0, 0.0], 'vec' : [0.0, 0.0, 0.0]},
'CD3-CD4+HLADR+_CIS0022' : { 'color' : [0.0, 0.0, 0.0], 'vec' : [0.0, 0.0, 0.0]},
'CD4Tcells_CIS0022' : { 'color' : [0.0, 0.0, 0.0], 'vec' : [0.0, 0.0, 0.0]},
'CD8Tcells_CIS0022' : { 'color' : [0.0, 0.0, 0.0], 'vec' : [0.0, 0.0, 0.0]},
'DNTcells_CIS0022' : { 'color' : [0.0, 0.0, 0.0], 'vec' : [0.0, 0.0, 0.0]},
'ignore_CIS0022' : { 'color' : [0.0, 0.0, 0.0], 'vec' : [0.0, 0.0, 0.0]},
'Myeloid_CIS0022' : { 'color' : [0.0, 0.0, 0.0], 'vec' : [0.0, 0.0, 0.0]},
'NKcells_CIS0022' : { 'color' : [0.0, 0.0, 0.0], 'vec' : [0.0, 0.0, 0.0]},
'Bcells_CIS0024' : { 'color' : [0.0, 0.0, 0.0], 'vec' : [0.0, 0.0, 0.0]},
'CD3-CD4+HLADR+_CIS0024' : { 'color' : [0.0, 0.0, 0.0], 'vec' : [0.0, 0.0, 0.0]},
'CD4Tcells_CIS0024' : { 'color' : [0.0, 0.0, 0.0], 'vec' : [0.0, 0.0, 0.0]},
'CD8Tcells_CIS0024' : { 'color' : [0.0, 0.0, 0.0], 'vec' : [0.0, 0.0, 0.0]},
'DNTcells_CIS0024' : { 'color' : [0.0, 0.0, 0.0], 'vec' : [0.0, 0.0, 0.0]},
'ignore_CIS0024' : { 'color' : [0.0, 0.0, 0.0], 'vec' : [0.0, 0.0, 0.0]},
'Myeloid_CIS0024' : { 'color' : [0.0, 0.0, 0.0], 'vec' : [0.0, 0.0, 0.0]},
'NKcells_CIS0024' : { 'color' : [0.0, 0.0, 0.0], 'vec' : [0.0, 0.0, 0.0]},
'Bcells_CIS0034' : { 'color' : [0.0, 0.0, 0.0], 'vec' : [0.0, 0.0, 0.0]},
'CD3-CD4+HLADR+_CIS0034' : { 'color' : [0.0, 0.0, 0.0], 'vec' : [0.0, 0.0, 0.0]},
'CD4Tcells_CIS0034' : { 'color' : [0.0, 0.0, 0.0], 'vec' : [0.0, 0.0, 0.0]},
'CD8Tcells_CIS0034' : { 'color' : [0.0, 0.0, 0.0], 'vec' : [0.0, 0.0, 0.0]},
'DNTcells_CIS0034' : { 'color' : [0.0, 0.0, 0.0], 'vec' : [0.0, 0.0, 0.0]},
'ignore_CIS0034' : { 'color' : [0.0, 0.0, 0.0], 'vec' : [0.0, 0.0, 0.0]},
'Myeloid_CIS0034' : { 'color' : [0.0, 0.0, 0.0], 'vec' : [0.0, 0.0, 0.0]},
'NKcells_CIS0034' : { 'color' : [0.0, 0.0, 0.0], 'vec' : [0.0, 0.0, 0.0]},
'Bcells_CIS0048' : { 'color' : [0.0, 0.0, 0.0], 'vec' : [0.0, 0.0, 0.0]},
'CD3-CD4+HLADR+_CIS0048' : { 'color' : [0.0, 0.0, 0.0], 'vec' : [0.0, 0.0, 0.0]},
'CD4Tcells_CIS0048' : { 'color' : [0.0, 0.0, 0.0], 'vec' : [0.0, 0.0, 0.0]},
'CD8Tcells_CIS0048' : { 'color' : [0.0, 0.0, 0.0], 'vec' : [0.0, 0.0, 0.0]},
'DNTcells_CIS0048' : { 'color' : [0.0, 0.0, 0.0], 'vec' : [0.0, 0.0, 0.0]},
'ignore_CIS0048' : { 'color' : [0.0, 0.0, 0.0], 'vec' : [0.0, 0.0, 0.0]},
'Myeloid_CIS0048' : { 'color' : [0.0, 0.0, 0.0], 'vec' : [0.0, 0.0, 0.0]},
'NKcells_CIS0048' : { 'color' : [0.0, 0.0, 0.0], 'vec' : [0.0, 0.0, 0.0]},
'Bcells_CIS0050' : { 'color' : [0.0, 0.0, 0.0], 'vec' : [0.0, 0.0, 0.0]},
'CD3-CD4+HLADR+_CIS0050' : { 'color' : [0.0, 0.0, 0.0], 'vec' : [0.0, 0.0, 0.0]},
'CD4Tcells_CIS0050' : { 'color' : [0.0, 0.0, 0.0], 'vec' : [0.0, 0.0, 0.0]},
'CD8Tcells_CIS0050' : { 'color' : [0.0, 0.0, 0.0], 'vec' : [0.0, 0.0, 0.0]},
'DNTcells_CIS0050' : { 'color' : [0.0, 0.0, 0.0], 'vec' : [0.0, 0.0, 0.0]},
'ignore_CIS0050' : { 'color' : [0.0, 0.0, 0.0], 'vec' : [0.0, 0.0, 0.0]},
'Myeloid_CIS0050' : { 'color' : [0.0, 0.0, 0.0], 'vec' : [0.0, 0.0, 0.0]},
'NKcells_CIS0050' : { 'color' : [0.0, 0.0, 0.0], 'vec' : [0.0, 0.0, 0.0]},
'Bcells_CIS0076' : { 'color' : [0.0, 0.0, 0.0], 'vec' : [0.0, 0.0, 0.0]},
'CD3-CD4+HLADR+_CIS0076' : { 'color' : [0.0, 0.0, 0.0], 'vec' : [0.0, 0.0, 0.0]},
'CD4Tcells_CIS0076' : { 'color' : [0.0, 0.0, 0.0], 'vec' : [0.0, 0.0, 0.0]},
'CD8Tcells_CIS0076' : { 'color' : [0.0, 0.0, 0.0], 'vec' : [0.0, 0.0, 0.0]},
'DNTcells_CIS0076' : { 'color' : [0.0, 0.0, 0.0], 'vec' : [0.0, 0.0, 0.0]},
'ignore_CIS0076' : { 'color' : [0.0, 0.0, 0.0], 'vec' : [0.0, 0.0, 0.0]},
'Myeloid_CIS0076' : { 'color' : [0.0, 0.0, 0.0], 'vec' : [0.0, 0.0, 0.0]},
'NKcells_CIS0076' : { 'color' : [0.0, 0.0, 0.0], 'vec' : [0.0, 0.0, 0.0]},
'Bcells_CIS0081' : { 'color' : [0.0, 0.0, 0.0], 'vec' : [0.0, 0.0, 0.0]},
'CD3-CD4+HLADR+_CIS0081' : { 'color' : [0.0, 0.0, 0.0], 'vec' : [0.0, 0.0, 0.0]},
'CD4Tcells_CIS0081' : { 'color' : [0.0, 0.0, 0.0], 'vec' : [0.0, 0.0, 0.0]},
'CD8Tcells_CIS0081' : { 'color' : [0.0, 0.0, 0.0], 'vec' : [0.0, 0.0, 0.0]},
'DNTcells_CIS0081' : { 'color' : [0.0, 0.0, 0.0], 'vec' : [0.0, 0.0, 0.0]},
'ignore_CIS0081' : { 'color' : [0.0, 0.0, 0.0], 'vec' : [0.0, 0.0, 0.0]},
'Myeloid_CIS0081' : { 'color' : [0.0, 0.0, 0.0], 'vec' : [0.0, 0.0, 0.0]},
'NKcells_CIS0081' : { 'color' : [0.0, 0.0, 0.0], 'vec' : [0.0, 0.0, 0.0]},
'Bcells_CIS0089' : { 'color' : [0.0, 0.0, 0.0], 'vec' : [0.0, 0.0, 0.0]},
'CD3-CD4+HLADR+_CIS0089' : { 'color' : [0.0, 0.0, 0.0], 'vec' : [0.0, 0.0, 0.0]},
'CD4Tcells_CIS0089' : { 'color' : [0.0, 0.0, 0.0], 'vec' : [0.0, 0.0, 0.0]},
'CD8Tcells_CIS0089' : { 'color' : [0.0, 0.0, 0.0], 'vec' : [0.0, 0.0, 0.0]},
'DNTcells_CIS0089' : { 'color' : [0.0, 0.0, 0.0], 'vec' : [0.0, 0.0, 0.0]},
'ignore_CIS0089' : { 'color' : [0.0, 0.0, 0.0], 'vec' : [0.0, 0.0, 0.0]},
'Myeloid_CIS0089' : { 'color' : [0.0, 0.0, 0.0], 'vec' : [0.0, 0.0, 0.0]},
'NKcells_CIS0089' : { 'color' : [0.0, 0.0, 0.0], 'vec' : [0.0, 0.0, 0.0]},
'Bcells_CIS0099' : { 'color' : [0.0, 0.0, 0.0], 'vec' : [0.0, 0.0, 0.0]},
'CD3-CD4+HLADR+_CIS0099' : { 'color' : [0.0, 0.0, 0.0], 'vec' : [0.0, 0.0, 0.0]},
'CD4Tcells_CIS0099' : { 'color' : [0.0, 0.0, 0.0], 'vec' : [0.0, 0.0, 0.0]},
'CD8Tcells_CIS0099' : { 'color' : [0.0, 0.0, 0.0], 'vec' : [0.0, 0.0, 0.0]},
'DNTcells_CIS0099' : { 'color' : [0.0, 0.0, 0.0], 'vec' : [0.0, 0.0, 0.0]},
'ignore_CIS0099' : { 'color' : [0.0, 0.0, 0.0], 'vec' : [0.0, 0.0, 0.0]},
'Myeloid_CIS0099' : { 'color' : [0.0, 0.0, 0.0], 'vec' : [0.0, 0.0, 0.0]},
'NKcells_CIS0099' : { 'color' : [0.0, 0.0, 0.0], 'vec' : [0.0, 0.0, 0.0]},
'Bcells_GK0065' : { 'color' : [0.0, 0.0, 0.0], 'vec' : [0.0, 0.0, 0.0]},
'CD3-CD4+HLADR+_GK0065' : { 'color' : [0.0, 0.0, 0.0], 'vec' : [0.0, 0.0, 0.0]},
'CD4Tcells_GK0065' : { 'color' : [0.0, 0.0, 0.0], 'vec' : [0.0, 0.0, 0.0]},
'CD8Tcells_GK0065' : { 'color' : [0.0, 0.0, 0.0], 'vec' : [0.0, 0.0, 0.0]},
'DNTcells_GK0065' : { 'color' : [0.0, 0.0, 0.0], 'vec' : [0.0, 0.0, 0.0]},
'ignore_GK0065' : { 'color' : [0.0, 0.0, 0.0], 'vec' : [0.0, 0.0, 0.0]},
'Myeloid_GK0065' : { 'color' : [0.0, 0.0, 0.0], 'vec' : [0.0, 0.0, 0.0]},
'NKcells_GK0065' : { 'color' : [0.0, 0.0, 0.0], 'vec' : [0.0, 0.0, 0.0]},
'Bcells_GK0066' : { 'color' : [0.0, 0.0, 0.0], 'vec' : [0.0, 0.0, 0.0]},
'CD3-CD4+HLADR+_GK0066' : { 'color' : [0.0, 0.0, 0.0], 'vec' : [0.0, 0.0, 0.0]},
'CD4Tcells_GK0066' : { 'color' : [0.0, 0.0, 0.0], 'vec' : [0.0, 0.0, 0.0]},
'CD8Tcells_GK0066' : { 'color' : [0.0, 0.0, 0.0], 'vec' : [0.0, 0.0, 0.0]},
'DNTcells_GK0066' : { 'color' : [0.0, 0.0, 0.0], 'vec' : [0.0, 0.0, 0.0]},
'ignore_GK0066' : { 'color' : [0.0, 0.0, 0.0], 'vec' : [0.0, 0.0, 0.0]},
'Myeloid_GK0066' : { 'color' : [0.0, 0.0, 0.0], 'vec' : [0.0, 0.0, 0.0]},
'NKcells_GK0066' : { 'color' : [0.0, 0.0, 0.0], 'vec' : [0.0, 0.0, 0.0]},
'Bcells_GK0067' : { 'color' : [0.0, 0.0, 0.0], 'vec' : [0.0, 0.0, 0.0]},
'CD3-CD4+HLADR+_GK0067' : { 'color' : [0.0, 0.0, 0.0], 'vec' : [0.0, 0.0, 0.0]},
'CD4Tcells_GK0067' : { 'color' : [0.0, 0.0, 0.0], 'vec' : [0.0, 0.0, 0.0]},
'CD8Tcells_GK0067' : { 'color' : [0.0, 0.0, 0.0], 'vec' : [0.0, 0.0, 0.0]},
'DNTcells_GK0067' : { 'color' : [0.0, 0.0, 0.0], 'vec' : [0.0, 0.0, 0.0]},
'ignore_GK0067' : { 'color' : [0.0, 0.0, 0.0], 'vec' : [0.0, 0.0, 0.0]},
'Myeloid_GK0067' : { 'color' : [0.0, 0.0, 0.0], 'vec' : [0.0, 0.0, 0.0]},
'NKcells_GK0067' : { 'color' : [0.0, 0.0, 0.0], 'vec' : [0.0, 0.0, 0.0]},
'Bcells_GK0068' : { 'color' : [0.0, 0.0, 0.0], 'vec' : [0.0, 0.0, 0.0]},
'CD3-CD4+HLADR+_GK0068' : { 'color' : [0.0, 0.0, 0.0], 'vec' : [0.0, 0.0, 0.0]},
'CD4Tcells_GK0068' : { 'color' : [0.0, 0.0, 0.0], 'vec' : [0.0, 0.0, 0.0]},
'CD8Tcells_GK0068' : { 'color' : [0.0, 0.0, 0.0], 'vec' : [0.0, 0.0, 0.0]},
'DNTcells_GK0068' : { 'color' : [0.0, 0.0, 0.0], 'vec' : [0.0, 0.0, 0.0]},
'ignore_GK0068' : { 'color' : [0.0, 0.0, 0.0], 'vec' : [0.0, 0.0, 0.0]},
'Myeloid_GK0068' : { 'color' : [0.0, 0.0, 0.0], 'vec' : [0.0, 0.0, 0.0]},
'NKcells_GK0068' : { 'color' : [0.0, 0.0, 0.0], 'vec' : [0.0, 0.0, 0.0]},
'Bcells_GK0070' : { 'color' : [0.0, 0.0, 0.0], 'vec' : [0.0, 0.0, 0.0]},
'CD3-CD4+HLADR+_GK0070' : { 'color' : [0.0, 0.0, 0.0], 'vec' : [0.0, 0.0, 0.0]},
'CD4Tcells_GK0070' : { 'color' : [0.0, 0.0, 0.0], 'vec' : [0.0, 0.0, 0.0]},
'CD8Tcells_GK0070' : { 'color' : [0.0, 0.0, 0.0], 'vec' : [0.0, 0.0, 0.0]},
'DNTcells_GK0070' : { 'color' : [0.0, 0.0, 0.0], 'vec' : [0.0, 0.0, 0.0]},
'ignore_GK0070' : { 'color' : [0.0, 0.0, 0.0], 'vec' : [0.0, 0.0, 0.0]},
'Myeloid_GK0070' : { 'color' : [0.0, 0.0, 0.0], 'vec' : [0.0, 0.0, 0.0]},
'NKcells_GK0070' : { 'color' : [0.0, 0.0, 0.0], 'vec' : [0.0, 0.0, 0.0]},
'Bcells_GK0072' : { 'color' : [0.0, 0.0, 0.0], 'vec' : [0.0, 0.0, 0.0]},
'CD3-CD4+HLADR+_GK0072' : { 'color' : [0.0, 0.0, 0.0], 'vec' : [0.0, 0.0, 0.0]},
'CD4Tcells_GK0072' : { 'color' : [0.0, 0.0, 0.0], 'vec' : [0.0, 0.0, 0.0]},
'CD8Tcells_GK0072' : { 'color' : [0.0, 0.0, 0.0], 'vec' : [0.0, 0.0, 0.0]},
'DNTcells_GK0072' : { 'color' : [0.0, 0.0, 0.0], 'vec' : [0.0, 0.0, 0.0]},
'ignore_GK0072' : { 'color' : [0.0, 0.0, 0.0], 'vec' : [0.0, 0.0, 0.0]},
'Myeloid_GK0072' : { 'color' : [0.0, 0.0, 0.0], 'vec' : [0.0, 0.0, 0.0]},
'NKcells_GK0072' : { 'color' : [0.0, 0.0, 0.0], 'vec' : [0.0, 0.0, 0.0]},
'Bcells_GK0073' : { 'color' : [0.0, 0.0, 0.0], 'vec' : [0.0, 0.0, 0.0]},
'CD3-CD4+HLADR+_GK0073' : { 'color' : [0.0, 0.0, 0.0], 'vec' : [0.0, 0.0, 0.0]},
'CD4Tcells_GK0073' : { 'color' : [0.0, 0.0, 0.0], 'vec' : [0.0, 0.0, 0.0]},
'CD8Tcells_GK0073' : { 'color' : [0.0, 0.0, 0.0], 'vec' : [0.0, 0.0, 0.0]},
'DNTcells_GK0073' : { 'color' : [0.0, 0.0, 0.0], 'vec' : [0.0, 0.0, 0.0]},
'ignore_GK0073' : { 'color' : [0.0, 0.0, 0.0], 'vec' : [0.0, 0.0, 0.0]},
'Myeloid_GK0073' : { 'color' : [0.0, 0.0, 0.0], 'vec' : [0.0, 0.0, 0.0]},
'NKcells_GK0073' : { 'color' : [0.0, 0.0, 0.0], 'vec' : [0.0, 0.0, 0.0]},
'Bcells_GK0079' : { 'color' : [0.0, 0.0, 0.0], 'vec' : [0.0, 0.0, 0.0]},
'CD3-CD4+HLADR+_GK0079' : { 'color' : [0.0, 0.0, 0.0], 'vec' : [0.0, 0.0, 0.0]},
'CD4Tcells_GK0079' : { 'color' : [0.0, 0.0, 0.0], 'vec' : [0.0, 0.0, 0.0]},
'CD8Tcells_GK0079' : { 'color' : [0.0, 0.0, 0.0], 'vec' : [0.0, 0.0, 0.0]},
'DNTcells_GK0079' : { 'color' : [0.0, 0.0, 0.0], 'vec' : [0.0, 0.0, 0.0]},
'ignore_GK0079' : { 'color' : [0.0, 0.0, 0.0], 'vec' : [0.0, 0.0, 0.0]},
'Myeloid_GK0079' : { 'color' : [0.0, 0.0, 0.0], 'vec' : [0.0, 0.0, 0.0]},
'NKcells_GK0079' : { 'color' : [0.0, 0.0, 0.0], 'vec' : [0.0, 0.0, 0.0]},
'Bcells_GK0080' : { 'color' : [0.0, 0.0, 0.0], 'vec' : [0.0, 0.0, 0.0]},
'CD3-CD4+HLADR+_GK0080' : { 'color' : [0.0, 0.0, 0.0], 'vec' : [0.0, 0.0, 0.0]},
'CD4Tcells_GK0080' : { 'color' : [0.0, 0.0, 0.0], 'vec' : [0.0, 0.0, 0.0]},
'CD8Tcells_GK0080' : { 'color' : [0.0, 0.0, 0.0], 'vec' : [0.0, 0.0, 0.0]},
'DNTcells_GK0080' : { 'color' : [0.0, 0.0, 0.0], 'vec' : [0.0, 0.0, 0.0]},
'ignore_GK0080' : { 'color' : [0.0, 0.0, 0.0], 'vec' : [0.0, 0.0, 0.0]},
'Myeloid_GK0080' : { 'color' : [0.0, 0.0, 0.0], 'vec' : [0.0, 0.0, 0.0]},
'NKcells_GK0080' : { 'color' : [0.0, 0.0, 0.0], 'vec' : [0.0, 0.0, 0.0]},
'Bcells_GK0087' : { 'color' : [0.0, 0.0, 0.0], 'vec' : [0.0, 0.0, 0.0]},
'CD3-CD4+HLADR+_GK0087' : { 'color' : [0.0, 0.0, 0.0], 'vec' : [0.0, 0.0, 0.0]},
'CD4Tcells_GK0087' : { 'color' : [0.0, 0.0, 0.0], 'vec' : [0.0, 0.0, 0.0]},
'CD8Tcells_GK0087' : { 'color' : [0.0, 0.0, 0.0], 'vec' : [0.0, 0.0, 0.0]},
'DNTcells_GK0087' : { 'color' : [0.0, 0.0, 0.0], 'vec' : [0.0, 0.0, 0.0]},
'ignore_GK0087' : { 'color' : [0.0, 0.0, 0.0], 'vec' : [0.0, 0.0, 0.0]},
'Myeloid_GK0087' : { 'color' : [0.0, 0.0, 0.0], 'vec' : [0.0, 0.0, 0.0]},
'NKcells_GK0087' : { 'color' : [0.0, 0.0, 0.0], 'vec' : [0.0, 0.0, 0.0]},
'Bcells_GK0XX' : { 'color' : [0.0, 0.0, 0.0], 'vec' : [0.0, 0.0, 0.0]},
'CD3-CD4+HLADR+_GK0XX' : { 'color' : [0.0, 0.0, 0.0], 'vec' : [0.0, 0.0, 0.0]},
'CD4Tcells_GK0XX' : { 'color' : [0.0, 0.0, 0.0], 'vec' : [0.0, 0.0, 0.0]},
'CD8Tcells_GK0XX' : { 'color' : [0.0, 0.0, 0.0], 'vec' : [0.0, 0.0, 0.0]},
'DNTcells_GK0XX' : { 'color' : [0.0, 0.0, 0.0], 'vec' : [0.0, 0.0, 0.0]},
'ignore_GK0XX' : { 'color' : [0.0, 0.0, 0.0], 'vec' : [0.0, 0.0, 0.0]},
'Myeloid_GK0XX' : { 'color' : [0.0, 0.0, 0.0], 'vec' : [0.0, 0.0, 0.0]},
'NKcells_GK0XX' : { 'color' : [0.0, 0.0, 0.0], 'vec' : [0.0, 0.0, 0.0]}
}

node = hou.pwd()
geo = node.geometry()

data_file = node.evalParm('data_file')

#data_file = "data2.csv"
if path.exists(data_file):
    main(data_file, geo, config)
else:
   print("%s doesnt exists!!!" % (data_file))
