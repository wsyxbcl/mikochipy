import random
from pathlib import Path

import ase.io
from ase.db import connect
from icet.tools import enumerate_structures
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

_no_value = object()

# Note For Terminology
# Term 'structures' refers to list of ASE row objects ([ase.db.row.AtomsRow(])
# while 'database' refers to the ASE database (ase.db), which contains all the 
# enumerated structures

def select_structures(database, num_structures, weighted_atom=_no_value):
    """
    Select row from enumerated structure database for calculation.
    A weighted random selection is considered here.
    
    database: ase database
    num_structures: required number of generated structures
    weighted_atom: atom for which the selection is weighted over its concentration
    """
    structures = list(database.select())
    c_atoms = []
    for row in structures:
        try:
            c_atoms.append(row.count_atoms()[weighted_atom] / row.natoms)
        except KeyError:
            c_atoms.append(0)
    if weighted_atom is _no_value:
        selected_structures = np.random.choice(structures, 
                                               size=num_structures,
                                               replace=False)
    else:
        selected_structures = np.random.choice(structures,
                                               size=num_structures,
                                               replace=False,
                                               p=[c / sum(c_atoms) for c in c_atoms])
    return selected_structures
                                                                             
def structures_to_vasp(structures, path_dataset, remove_x=True):
    """
    generate POSCAR and set up directories for VASP calculaiton

    path_dataset: path for vasp calculation (pathlib.Path).
    remove_x: remove X element from structure where X represents vacancy

    file structures:
    - path_dataset
        - entry1 (row1.id)
        - entry2 (row2.id)
        ..
    """
    if remove_x:
        for row in structures:
            # make dataset directory (normally follows $MATERIAL/CE/dataset)
            path_row = path_dataset.joinpath(str(row.id))
            path_row.mkdir(parents=True)
            atoms = row.toatoms()
            del atoms[[atom.index for atom in atoms if atom.symbol == 'X']]
            ase.io.write(path_row.joinpath('POSCAR'),
                         atoms,
                         format='vasp',
                         sort=True)
    else:
        for row in structures:
            path_row = path_dataset.joinpath(str(row.id))
            path_row.mkdir(parents=True)
            ase.io.write(path_row.joinpath('POSCAR'),
                         row.toatoms(),
                         format='vasp',
                         sort=True)
        

def vasp_to_database(database, path_dataset, property):
    """
    extract calculated properties and add back to database

    path_dataset: path for vasp calculation (pathlib.Path)
    """
    #TODO
    pass

def visualize_structures(structures, atom='Li', bins='auto'):
    """
    visualize structures by histogram over the concentration of atom and 
    the number of atoms in structures
    """
    c_atoms = []
    n_atoms = []
    for row in structures:
        try:
            c_atoms.append(row.count_atoms()[atom] / row.natoms)
        except KeyError:
            c_atoms.append(0)
        n_atoms.append(row.natoms)

    plt.figure(1)
    plt.subplot(211)
    plt.hist(c_atoms, bins=bins)
    plt.xlabel(atom+' concentration')
    plt.ylabel('Number of structures')

    plt.subplot(212)
    plt.hist(n_atoms, bins=bins)
    plt.xlabel('Number of atoms')
    plt.ylabel('Number of structures')
    plt.show()
