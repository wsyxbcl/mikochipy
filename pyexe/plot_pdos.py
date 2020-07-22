#!/usr/bin/python3

# Extract and Plot density of states (DOS) from VASP output file (vasprun.xml)
# Reference
# https://github.com/why-shin/VASP-DOS_extractor/blob/master/DOS_extractor.py
# https://github.com/materialsproject/pymatgen/blob/v2019.12.22/pymatgen/electronic_structure/plotter.py#L2070-L2529

import argparse
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from pymatgen.io.vasp.outputs import Vasprun
from pymatgen.core.periodic_table import Element
from pymatgen.electronic_structure.core import Spin, Orbital, OrbitalType


def extract_dos_orbital(dos_complete, element, orbital):
    """
    input:
        dos_complete - <pymatgen.electronic_structure.dos.CompleteDos>
        element - str, element which the orbital belongs, e.g. 'O', 'Li'
        orbital - str, aimed orbital, e.g. 's', 'p', 'd'
    output:
        dos_orbital - list, length of 2 (spin up/down) or 1, desired orbital pDOS
        (Notice that spin down dos will be assigned with negative values)
    """
    dos_orbital = []
    for spin in (Spin.up, Spin.down):
        dos_densities = dos_complete.get_element_spd_dos(element)[OrbitalType[orbital]].densities
        if spin in dos_densities:
            dos_orbital.append(dos_densities[spin] * int(spin))
    return dos_orbital

def extract_dos_element(dos_complete, element):
    """
    input:
        dos_complete - <pymatgen.electronic_structure.dos.CompleteDos>
        element - str, element which the orbital belongs, e.g. 'O', 'Li'
    output:
        dos_element - list, length of 2 (spin up and down) or 1, desired element pDOS
        (Notice that spin down dos will be assigned with negative values)
    """
    dos_element = []
    for spin in (Spin.up, Spin.down):
        dos_densities = dos_complete.get_element_dos()[Element[element]].densities
        if spin in dos_densities:
            dos_element.append(dos_densities[spin] * int(spin))
    return dos_element

def plot_dos(dos, energy, label, color, lw=1, color_fill=None):
    """
    Plot DOS on given axes.
    input:
        dos - list of np.array, DOS to be plotted
        energy - np.array, E - Ef
        ax - matplotlib.axes
        label - string
        color - matplotlib recognizable color
        color_fill - fill between if set
    """
    for d in dos:
        plt.plot(energy, d, color=color, label=label, lw=lw)
        if color_fill is not None:
            plt.fill_between(energy, 0, d, edgecolor=color, facecolor=color_fill)

def main(path, dos_element_plot, dos_orbital_plot, dos_total_plot, xmin, xmax, ymin, ymax, outfile, text):
    plt.close()
    # Colormaps
    colors = plt.get_cmap("tab10").colors
    # colors = ['blue', 'orange', 'green', 'red']

    # Pymatgen API
    # dos_complete.get_element_dos()[Element['Fe']].densities[Spin.up]
    # dos_complete.get_element_spd_dos('Fe')[OrbitalType['d']].densities[Spin.up]
    # dos_complete.densities[Spin.up]
    # dos_complete.energies

    # Get DOS informations
    print(path)
    vasprun = Vasprun(str(path))
    dos_complete = vasprun.complete_dos
    dos_ef = dos_complete.efermi # Fermi Level

    fig = plt.figure(tight_layout=True)

    # plot PDOS by element
    if dos_element_plot is not None:
        for i, element in enumerate(dos_element_plot):
            dos = extract_dos_element(dos_complete=dos_complete, element=element)
            plot_dos(dos=dos, 
                     energy=(dos_complete.energies-dos_ef), 
                     label=element,
                     color=colors[i])
    # plot PDOS by orbitals
    if dos_orbital_plot is not None:
        dos_orbital_plot = [o.split('-') for o in dos_orbital_plot]
        for i, orbital in enumerate(dos_orbital_plot):
            dos = extract_dos_orbital(dos_complete=dos_complete,
                                      element=orbital[0],
                                      orbital=orbital[1])
            plot_dos(dos=dos,
                     energy=(dos_complete.energies-dos_ef),
                     label=orbital[0]+'-'+orbital[1],
                     color=colors[i])
    # plot TDOS
    if dos_total_plot == 'on':
        plot_dos(dos=[dos_complete.densities[Spin.up], - dos_complete.densities[Spin.down]], 
                energy=(dos_complete.energies-dos_ef),
                # ax=ax,
                label='Total',
                color='black')

    # Configure axes
    plt.axvline(x=0, color='black', linestyle='--') # Fermi level
    if xmax is not None:
        plt.xlim(right=xmax)
    if xmin is not None:
        plt.xlim(left=xmin)
    if ymax is not None:
        plt.ylim(top=ymax)
    if ymin is not None:
        plt.ylim(bottom=ymin)
    plt.ylabel('DOS')
    plt.xlabel('$E-E_F$ / eV')
    handles, labels = plt.gca().get_legend_handles_labels()
    by_label = dict(zip(labels, handles))
    plt.legend(by_label.values(), by_label.keys(), loc='upper right')
    if text is not None:
        plt.text(0.9, 0.05, text, transform=plt.gca().transAxes)
    if outfile is not None:
        plt.savefig(outfile, dpi=300)
    else:
        print("Autosaving to "+str(path.parent.joinpath('dos.png')))
        plt.savefig(path.parent.joinpath('dos.png'), dpi=300)
    plt.show()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="plot DOS from vasprun.xml")
    parser.add_argument(dest='data_path', type=Path, 
                        help="Path of vasprun.xml")
    parser.add_argument('-e', '--elements', dest='dos_element_plot',
                        metavar='element', action='append',
                        help="elements for pDOS plot, e.g. Li O")
    parser.add_argument('-o', '--orbitals', dest='dos_orbital_plot',
                        metavar='orbital', action='append',
                        help="orbitals for pDOS plot, e.g. Li-s O-p")
    parser.add_argument('-t', '--total', dest='dos_total_plot', action='store',
                        choices={'on', 'off'}, default='on',
                        help='total DOS')
    parser.add_argument('--xmin', dest='xmin', type=float, help="lower boundary of x")
    parser.add_argument('--xmax', dest='xmax', type=float, help="higher boundary of x")
    parser.add_argument('--ymin', dest='ymin', type=float, help="lower boundary of y")
    parser.add_argument('--ymax', dest='ymax', type=float, help="higher boundary of y")
    parser.add_argument('--output', dest='outfile', type=Path, help='output file')
    parser.add_argument('--text', dest='text', type=str, help='plt.text')                          
    args = parser.parse_args()
    main(args.data_path, args.dos_element_plot, args.dos_orbital_plot, 
         args.dos_total_plot, args.xmin, args.xmax, args.ymin, args.ymax, args.outfile, args.text)
