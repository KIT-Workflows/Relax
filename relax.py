import os
import yaml

from ase.build import bulk
from ase.io import write


def create_relax_pwi(element, lattice_param, cubic, crystal, kpts):
    """
    Creates a Quantum ESPRESSO input file ('relax.pwi') for a crystal structure relaxation.

    This function generates an input file for performing variable-cell relaxation (vc-relax)
    calculations using Quantum ESPRESSO. It sets up the crystal structure, defines the
    k-points grid, and includes necessary calculation parameters and pseudopotentials.

    Parameters:
    element (str): The chemical symbol of the element to create the bulk structure.
    lattice_param (float): The lattice parameter for the bulk structure.
    cubic (bool): Flag to determine if the structure should be cubic.
    crystal (str): The crystal type (True or False).
    kpts (tuple of int): A tuple representing the k-points grid (e.g., (3, 3, 3)).

    Writes to 'relax.pwi'.
    """

    os.environ['ESPRESSO_PSEUDO'] = os.getcwd()

    pseudopotentials = {element: f"{element}.pbe-n-kjpaw_psl.1.0.0.UPF"}
    input_data_relax = {
        'calculation': 'vc-relax',
        'cell_dofree': 'ibrav',
    }

    structure = bulk(element, a=lattice_param, cubic=cubic)

    write(
        'relax.pwi',
        structure,
        Crystal=crystal,
        kpts=kpts,
        input_data=input_data_relax,
        pseudopotentials=pseudopotentials,
        tstress=True,
        tprnfor=True
    )


if __name__ == '__main__':
    with open("structure.yml", "r") as file:
        params = yaml.safe_load(file)

    create_relax_pwi(
        element=params['element'],
        lattice_param=float(params['lattice_param']),
        cubic=params['cubic'],
        crystal=params['crystal'],
        kpts=tuple(map(int, params['kpts'].split(','))),
    )
