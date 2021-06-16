import warnings
import numpy as np

from itertools import product

from abipy import abilab
from abipy import flowtk
from abipy.flowtk import Flow
from abipy.abilab import AbinitInput

from pymatgen import Structure, Lattice
from pseudo_dojo import OfficialDojoTable


warnings.filterwarnings("ignore")  # Ignore warnings

pseudos_table = OfficialDojoTable.from_dojodir(
    "ONCVPSP-PBE-PDv0.4", accuracy="standard"
)


def fcc_prim(element: str, a: float):

    # a_prim = a * np.sqrt(2) / 2
    # lattice=Lattice.rhombohedral(a_prim, 60)
    structure = Structure(
        lattice=Lattice([[a / 2, a / 2, 0], [0, a / 2, a / 2], [a / 2, 0, a / 2]]),
        species=[element],
        coords=[[0, 0, 0]],
    )
    return structure


def fcc_conv(element: str, a: float):
    # lattice=Lattice.cubic(a)
    structure = Structure(
        lattice=Lattice([[a, 0, 0], [0, a, 0], [0, 0, a]]),
        species=4 * [element],
        coords=[[0, 0, 0], [0.5, 0.5, 0], [0.5, 0, 0.5], [0, 0.5, 0.5]],
    )
    return structure


def fcc_100(element: str, a: float, n: int, vacuum: float, centered=True):

    h = (n - 1) * a / 2 + vacuum

    coords = np.zeros((n, 3))
    coords[1::2, 0] = a / 2
    coords[:, 2] = [i * a / 2 for i in range(n)]
    # coords[:, 2] = np.arange(n) * a / 2

    if centered:
        coords[:, 2] += vacuum / 2

    structure = Structure(
        lattice=Lattice([[a / 2, -a / 2, 0], [a / 2, a / 2, 0], [0, 0, h]]),
        species=n * [element],
        coords=coords,
        coords_are_cartesian=True,
    )
    return structure


def fcc_100_conv(element: str, a: float, n: int, vacuum: float, centered=True):

    h = (n - 1) * a / 2 + vacuum

    coords = np.zeros((2 * n, 3))

    coords[0::4, :] = [[0, 0, i * a] for i in range((n + 1) // 2)]
    coords[1::4, :] = [[a / 2, a / 2, i * a] for i in range((n + 1) // 2)]
    coords[2::4, :] = [[a / 2, 0, a / 2 + i * a] for i in range(n // 2)]
    coords[3::4, :] = [[0, a / 2, a / 2 + i * a] for i in range(n // 2)]

    if centered:
        coords[:, 2] += vacuum / 2

    structure = Structure(
        lattice=Lattice([[a, 0, 0], [0, a, 0], [0, 0, h]]),
        species=2 * n * [element],
        coords=coords,
        coords_are_cartesian=True,
    )
    return structure


def fcc_110(element: str, a: float, n: int, vacuum: float):

    h = (n - 1) * a / 4 + vacuum / np.sqrt(2)

    coords = np.zeros((n, 3))

    for ind in range(0, n, 2):
        i = ind / 2
        coords[ind, :] = (i * a / 2, i * a / 2, 0)

    for ind in range(1, n, 2):
        i = (ind - 1) / 2
        coords[ind, :] = [a / 2 + i * a / 2, i * a / 2, a / 2]

    structure = Structure(
        lattice=Lattice([[0, 0, a], [a / 2, -a / 2, 0], [h, h, 0]]),
        species=n * [element],
        coords=coords,
        coords_are_cartesian=True,
    )
    return structure


def fcc_111(element: str, a: float, n: int, vacuum: float):

    # np.array([[.5, 0, -.5], [0, .5, -.5], [1, 1, 1]])

    h = (n - 1) * a / 3 + vacuum / np.sqrt(3)

    coords = np.zeros((n, 3))
    for ind in range(0, n, 3):
        i = ind / 3
        coords[ind, :] = (i * a, i * a, i * a)

    for ind in range(1, n, 3):
        i = (ind - 1) / 3
        coords[ind, :] = (a / 2 + i * a, a / 2 + i * a, i * a)

    for ind in range(2, n, 3):
        i = (ind - 2) / 3
        coords[ind, :] = (a + i * a, a + i * a, i * a)

    structure = Structure(
        lattice=Lattice([[a / 2, 0, -a / 2], [0, a / 2, -a / 2], [h, h, h]]),
        species=n * [element],
        coords=coords,
        coords_are_cartesian=True,
    )
    return structure


# class FlowScheduler(Flow):
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self._scheduler = None

#     def run(self, force=False):
#         if force:
#             self.rmtree()
#         if self._scheduler is None:
#             self._scheduler = self.make_scheduler()

#         self._scheduler.start()


# class ConvFlow(FlowScheduler):
#     def __init__(self, structure, workdir="flow_conv"):
#         super().__init__(workdir)


# class ConvCalculation(object):
#     def __init__(self, structure, workdir="01_ecut_conv"):

#         self.scheduler = None
#         self.structure = structure

#         inp = abilab.AbinitInput(structure=structure, pseudos=pseudos_table)

#         ## Definition of the k-point grid

#         # Automatically select ngkpt, shift, kptopt for the sampling of the BZ
#         # from the lattice and the number of divisions
#         # inp.set_autokmesh(nksmall=4)

#         inp["ngkpt"] = [4, 4, 4]
#         inp["kptopt"] = 1
#         inp["nshiftk"] = 4
#         inp["shiftk"] = [0.5, 0.5, 0.5, 0.5, 0.0, 0.0, 0.0, 0.5, 0.0, 0.0, 0.0, 0.5]

#         # inp['ngkpt'] = [8, 8, 8]
#         # inp['kptopt'] = 1
#         # inp['nshiftk'] = 1
#         # inp['shiftk'] = [0.5, 0.5, 0.5]

#         ## Definition of occupation
#         inp["occopt"] = 6
#         inp["tsmear"] = 0.01

#         ## Definition of the SCF procedure
#         inp["nstep"] = 50  # Maximal number of SCF cycles
#         inp["tolvrs"] = 1e-10

#         ## Optimization of the lattice parameters
#         inp["optcell"] = 1
#         inp["ionmov"] = 2
#         inp["ntime"] = 10
#         inp["dilatmx"] = 1.05

#         ## Definition of the planewave basis set
#         # Maximal kinetic energy cut-off, in Hartree (16, 20, 26)
#         inp["ecut"] = ecut

#         self.flow = None

#     def run(self, force=False):

#         if force:
#             self.flow.rmtree()

#         if self.scheduler is None:
#             self.scheduler = self.flow.make_scheduler()

#         self.scheduler.start()

#         ## Optimization of the lattice parameters
#         # inp['optcell'] = 1
#         # inp['ionmov'] = 2
#         # inp['ntime'] = 10
#         # inp['dilatmx'] = 1.05
#         # inp['ecutsm'] = 0.5

#         # inp['rfdir'] = [1, 1, 1]
#         # inp['rfatpol'] = [1, len(structure)]


# class Calculations(object):
#     pass


# class FCC_Calculations(Calculations):
#     def __init__(
#         self,
#         element: str,
#         lattice_constant: float,
#         ecut: float = 20,
#         tsmear: float = 0.01,
#     ):
#         a = lattice_constant
#         self.structure = Structure(
#             lattice=Lattice([[a, 0, 0], [0, a, 0], [0, 0, a]]),
#             species=4 * [element],
#             coords=[[0, 0, 0], [0.5, 0.5, 0], [0.5, 0, 0.5], [0, 0.5, 0.5]],
#         )

#         self.ecut = ecut
#         self.tsmear = tsmear

#     def relaxation_conv(self, workdir="01_relax", force=False, shifted=False):
#         """Generate input for optimization of the lattice parameter
#         at fixed number of k points and broadening.
#         """

#         inp = abilab.AbinitInput(structure=self.structure, pseudos=pseudos_table)

#         # inp['chksymbreak'] = None
#         inp["chkprim"] = 0

#         inp["ecut"] = self.ecut
#         inp["tsmear"] = self.tsmear

#         # Definition of the k-point grid
#         inp["kptopt"] = 1
#         inp["ngkpt"] = [16, 16, 16]
#         inp["nshiftk"] = 1

#         inp["shiftk"] = [0.5, 0.5, 0.5] if shifted else [0.0, 0.0, 0.0]

#         ## Optimization of the lattice parameters
#         inp["optcell"] = 1
#         inp["ionmov"] = 2

#         inp["ntime"] = 10
#         inp["dilatmx"] = 1.05
#         inp["ecutsm"] = 0.5

#         ## Definition of the SCF procedure
#         # Maximal number of SCF cycles
#         inp["nstep"] = 50

#         # Will stop when, twice in a row, the difference
#         # between two consecutive evaluations of total energy
#         # differ by less than toldfe (in Hartree)
#         # This value is way too large for most realistic studies of materials
#         # inp['toldfe'] = 1e-8
#         inp["tolvrs"] = 1e-10

#         # return inp

#         workdir = "01_relax"

#         flow = flowtk.Flow.from_inputs(workdir, inputs=inp)

#         if force:
#             flow.rmtree()

#         try:
#             scheduler = flow.make_scheduler()
#             scheduler.start()
#         except:
#             pass

#         abo = abilab.abiopen("01_relax/w0/t0/run.abo")
#         self.structure = abo.final_structure

#     def qmesh(self, workdir="02_qmesh", force=False, shifted=False):
#         """
#         Build and return a Flow to compute the dynamical matrix on a (2, 2, 2) qmesh
#         as well as DDK and Born effective charges.
#         The final DDB with all perturbations will be merged automatically and placed
#         in the Flow `outdir` directory.
#         """
#         inp = abilab.AbinitInput(structure=self.structure, pseudos=pseudos_table)

#         # inp['chksymbreak'] = None
#         inp["chkprim"] = 0

#         inp["ecut"] = self.ecut
#         inp["tsmear"] = self.tsmear

#         # Definition of the k-point grid
#         inp["kptopt"] = 1
#         inp["ngkpt"] = [16, 16, 16]
#         inp["nshiftk"] = 1

#         inp["shiftk"] = [0.5, 0.5, 0.5] if shifted else [0.0, 0.0, 0.0]

#         #  occopt 6
#         #  nband 18
#         inp["occopt"] = 6
#         inp["nband"] = 3 * 4 + 6

#         ## Definition of the SCF procedure
#         # Maximal number of SCF cycles
#         inp["nstep"] = 50

#         # Will stop when, twice in a row, the difference
#         # between two consecutive evaluations of total energy
#         # differ by less than toldfe (in Hartree)
#         # This value is way too large for most realistic studies of materials
#         # inp['toldfe'] = 1e-8
#         inp["tolvrs"] = 1e-10

#         flow = flowtk.PhononFlow.from_scf_input(
#             workdir, inp, ph_ngqpt=(2, 2, 2), with_becs=False
#         )

#         if force:
#             flow.rmtree()

#         try:
#             scheduler = flow.make_scheduler()
#             scheduler.start()
#         except:
#             pass

#     @staticmethod
#     def launch(inp, workdir, force=False):

#         flow = flowtk.Flow.from_inputs(workdir, inputs=inp)

#         if force:
#             flow.rmtree()

#         scheduler = flow.make_scheduler()

#         scheduler.start()