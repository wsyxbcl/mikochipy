#!/usr/bin/python3

#TODO integreted with ezvasp
# Currently used to correct GGA+U

import argparse
import os
from pathlib import Path

def add_hubbard_U(dir_INCAR, aimed_atom, u_value):
    with open(dir_INCAR.joinpath("POSCAR")) as fp:
        file_POSCAR = list(fp)
        atom_types = file_POSCAR[0].split()
        atom_nums = file_POSCAR[5].split()
        value_LDAUL = ['-1'] * len(atom_types)
        value_LDAUU = ['0.00'] * len(atom_types)
    if aimed_atom in atom_types:
        #TODO support multiple atoms
        with open(dir_INCAR.joinpath("INCAR"), 'r+') as fp:
            value_LDAUL[atom_types.index(aimed_atom)] = '2'
            value_LDAUU[atom_types.index(aimed_atom)] = str(u_value)
            fp.read()
            fp.write("# GGA+U\nLDAU = .TRUE.\nLDAUTYPE = 2\n")
            fp.write("LDAUL = {}\nLDAUU = {}\n".format(' '.join(value_LDAUL),
                                                       ' '.join(value_LDAUU)))
            fp.write("LDAUPRINT = 2\nLMAXMIX = 4\n")
        print("Add GGA+U to {}".format(dir_INCAR))

if __name__ == '__main__':
    
    #TODO correct variable names & types
    #############################
    # System = "CE_NaXMnAlO opt GGA+U_4eV"
    # ISTART = 1
    # ICHARG = 1
    # ENCUT = 500
    # ISMEAR = 0
    # SIGMA = 0.05

    # LORBIT = 11

    # # spin
    # ISPIN = 2

    # # electronic step
    # EDIFF = 1E-05
    # NELM = 300
    # NELMIN = 5

    # # ionic step
    # ISIF = 3
    # EDIFFG = -0.02 # force
    # NSW = 500
    # IBRION = 1

    # # GGA+U
    # LDAU = .TRUE.
    # LDAUTYPE = 2
    # LDAUL = 2 -1 -1 -1
    # LDAUU = 4.00 0.00 0.00 0.00
    # LDAUJ = 0.00 0.00 0.00 0.00
    # LDAUPRINT = 2
    # LMAXMIX = 4

    # NPAR = 4
    #############################
    parser = argparse.ArgumentParser(description="Automatic INCAR generation")
    parser.add_argument(dest='data_dir', type=Path, 
                        help="Directory to be iterated")
    #TODO add paresr for other parameters
    args = parser.parse_args()

    dir_task = args.data_dir
    for dir_INCAR in [dir_task.joinpath(task) for task in os.listdir(dir_task)
                      if os.path.isdir(os.path.join(dir_task, task))]:
        add_hubbard_U(dir_INCAR=dir_INCAR, aimed_atom='Mn', u_value='4.00')