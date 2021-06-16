import os
import tempfile
import numpy as np

from pathlib import Path
from pymatgen import Structure

from abipy.abio.factories import scf_input
from abipy.flowtk.tasks import TaskManager, AbinitTask

from pseudo_dojo import OfficialDojoTable


Bohr_to_Angstrom = 0.5291772086


def build_fake_input(structure:Structure):
    """Creates an Abinitinput object by using only essential parameters.
    
    Args:
      structure: pymatgen's Structure object.
    """
    pseudo_table = OfficialDojoTable.from_dojodir("ONCVPSP-PBE-PDv0.4", accuracy='standard')

    # build an input as basic as possible
    inp = scf_input(structure, pseudo_table, smearing=None, spin_mode="unpolarized")

    inp["ngkpt"] = [1, 1, 1]
    inp["nshiftk"] = 1
    inp["shiftk"] = [[0, 0, 0]]
    inp["nstep"] = 0
    inp["ecut"] = 1  # should be something reasonable, otherwise abinit raises an error
    inp["nband"] = 1
    inp["charge"] = structure.num_valence_electrons(pseudo_table) - 1 # needed to allow just one band
    
    return inp


def generarte_ddb_header(structure:Structure, manager:TaskManager=None):
    """Runs a dummy calculation to generate a proper header of the DDB file.
    
    Args:
      structure: pymatgen's Structure object.
      manager: flowtk manager
    """
    
    import tempfile
    
    inp = build_fake_input(structure)

    header = []
    with tempfile.TemporaryDirectory() as tmpdir:
        
        task = AbinitTask.temp_shell_task(inp, workdir=tmpdir, manager=manager)
        task.start_and_wait(autoparal=False)
        tmp_ddb_path = os.path.join(tmpdir, "outdata", "out_DDB")
        
        with open(tmp_ddb_path, 'r') as file:
            for line in file:
                if line == ' **** Database of total energy derivatives ****\n':
                    break
                header.append(line)

        return header

def ddb_writer(file:Path, structure:Structure, d2cart:np.ndarray, manager:TaskManager=None):
    """Creates a DDB file based on an structure and matrix which containes 
    all the second derivatives.
    
    Args:
      file: path to the output file
      structure: pymatgen's Structure object
      d2cart: the tensor of the second rericatives in real space (shape: (n_atoms, 3, n_atoms, 3))
      manager: flowtk manager
    """
    
    n_atoms = len(structure)
    rprim = structure.lattice.matrix / Bohr_to_Angstrom

    d2matr = np.zeros_like(d2cart)
    for i in range(n_atoms):
        for j in range(n_atoms):
            d2matr[i,:,j,:] =  np.dot(d2cart[i, :, j, :], rprim**2)

    with file.open('w') as f:
    
        f.writelines(generarte_ddb_header(structure, manager=manager))

        f.write(' **** Database of total energy derivatives ****\n')
        f.write(' Number of data blocks= {:4d}\n'.format(1))
        f.write('\n')
        f.write(' 2nd derivatives (non-stat.)  - # elements :{:8d}\n'.format(3*n_atoms*3*n_atoms))
        f.write(' qpt{:16.8E}{:16.8E}{:16.8E}{:6.1f}\n'.format(0., 0., 0., 1.))

        for ipert1 in range(n_atoms):
            for idir1 in range(3):
                for ipert2 in range(n_atoms):
                    for idir2 in range(3):
                        f.write('{:3d}{:3d}{:3d}{:3d}{:22.14E}{:22.14E}\n'.format(
                            idir1 + 1, ipert1 + 1, 
                            idir2 + 1, ipert2 + 1, 
                            np.real(d2matr[ipert1, idir1, ipert2, idir2]), 
                            np.imag(d2matr[ipert1, idir1, ipert2, idir2]))
                        )
        f.write('\n')
