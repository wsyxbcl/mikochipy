import ase.io
from ase.db import connect
from icet.tools import enumerate_structures
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


# Note For Terminology
# The term 'structures' always refers to a list of ASE atoms([ase.atoms.Atoms])
# while 'database' refers to the ASE database (ase.db), which contains all the 
# enumerated structures

def select_structures(database, remove_x=True):
    """
    select structures from enumerated structure database for calculation

    database: ase database
    remove_x: remove X element from structure where X represents vacancy
    """

def structures_to_vasp(structures, path_calc):
    """
    generate POSCAR and set up directorys for VASP calculaiton
    """

def vasp_to_database(database, path_calc, property):
    """
    extract calculated properties and add back to database
    """

def visualize_database(database, atom='Li', bins='auto'):
    """
    visualize database by histogram over the concentration of atom and 
    the number of atoms in structures
    """
    c_atoms = []
    n_atoms = []
    for row in database.select():
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