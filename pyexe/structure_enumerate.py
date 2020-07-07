import ase.io
from ase.db import connect
from icet.tools import enumerate_structures

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