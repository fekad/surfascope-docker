from math import ceil
import numpy as np


def chunkstring(string, length):
    string = string.rstrip('\n')
    return (string[0+i:length+i] for i in range(0, len(string), length))


def build_symmetric_matrix(values, dims):
    # assert len(values) == dims * (dims + 1) // 2
    hessian = np.zeros((dims, dims))

    lt_inds = np.tril_indices(dims)
    hessian[lt_inds] = values

    # Creating a symmetric matric
    irows, icols = np.tril_indices(dims, k=1)
    hessian[irows, icols] = hessian[icols, irows]

    # hessian += np.tril(hessian, k=-1).T

    # assert (hessian.transpose() == hessian).all()
    return hessian


class FchkData(dict):
    """Dictionary like object 
    """
    @classmethod
    def from_file(cls, file):
        """
        The first two lines in the file contain strings describing the job:
        - Initial 72 characters of the title section	    	Complete route and title appear later.
        - Type, Method, Basis	    	Format: A10,A30,A30

        All other data contained in the file is located in a labeled line/section set up in one of the following forms:
        - Scalar values appear on the same line as their data label. This line consists of a string describing the data item, a flag indicating the data type, and finally the value:
          - Integer scalars: Name,I,IValue (format A40,3X,A1,5X,I12).
          - Real scalars: Name,R,Value (format A40,3X,A1,5X,E22.15).
          - Character string scalars: Name,C,Value (format A40,3X,A1,5X,A12).
          - Logical scalars: Name,L,Value (format A40,3X,A1,5X,L1).
        - Vector and array data sections begin with a line naming the data and giving the type and number of values, followed by the data on one or more succeeding lines (as needed):
          - Integer arrays: Name,I,Num (format A40,3X,A1,3X,’N=’,I12). The N= indicates that this is an array, and the string is followed by the number of values. The array elements then follow starting on the next line in format 6I12.
          - Real arrays: Name,R,Num (format A40,3X,A1,3X,’N=’,I12), where the N= string again indicates an array and is followed by the number of elements. The elements themselves follow on succeeding lines in format 5E16.8. Note that the Real format has been chosen to ensure that at least one space is present between elements, to facilitate reading the data in C.
          - Character string arrays (first type): Name,C,Num (format A40,3X,A1,3X,’N=’,I12), where the N= string indicates an array and is followed by the number of elements. The elements themselves follow on succeeding lines in format 5A12.
          - Character string arrays (second type): Name,H,Num (format A40,3X,A1,3X,’N=’,I12), where the N= string indicates an array and is followed by the number of elements. The elements themselves follow on succeeding lines in format 9A8.
          - Logical arrays: Name,L,Num (format A40,3X,A1,3X,’N=’,I12), where the N= string indicates an array and is followed by the number of elements. The elements themselves follow on succeeding lines in format 72L1.

        All quantities are in atomic units and in the standard orientation, if that was determined by the Gaussian run. Standard orientation is seldom an interesting visual perspective, but it is the natural orientation for the vector fields. The field names are fairly verbose to make them informative and should not be an impediment as only the interface program needs to use them. An example program, demofc, is distributed with Gaussian and demonstrates how to extract a named field.

        Type is one of the following keywords:
        - SP	  	Single point
        - FOPT	  	Full optimization to a minimum
        - POPT	  	Partial optimization to a minimum
        - FTS	  	Full optimization to a transition state
        - PTS	  	Partial optimization to a transition state
        - FSADDLE	  	Full optimization to a saddle point of order 2 or higher
        - PSADDLE	  	Partial optimization to a saddle point of order 2 or higher
        - FORCE	  	Energy+gradient calculation
        - FREQ	  	Vibrational frequency (2nd derivative) calculation
        - SCAN	  	Potential surface scan
        - GUESS=ONLY	  	Generate molecular orbitals only, also used with localized orbital generation
        - LST	  	Linear synchronous transit
        - STABILITY	  	Test of SCF/KS stability
        - REARCHIVE/MS-RESTART	  	Generate archive information from checkpoint file
        - MIXED	  	Mixed method model chemistry (CBS-x, G1, G2, etc.), with method and basis set implied by model

        The following items are among those currently defined:
        - Route
        - Full Title
        - Number of atoms
        - Charge
        - Multiplicity
        - Number of electrons
        - Number of alpha electrons
        - Number of beta electrons
        - Number of basis functions
        - Number of contracted shells
        - Highest angular momentum
        - Largest degree of contraction
        - Number of primitive shells
        - Virial Ratio
        - Atomic numbers
        - Nuclear charges
        - Current Cartesian coordinates
        - Alpha Orbital Energies
        - Beta Orbital Energies
        - Alpha MO coefficients
        - Beta MO coefficients
        - Shell types
        - Number of primitives per shell
        - Shell to atom map
        - Primitive exponents
        - Contraction coefficients
        - P(S=P) Contraction coefficients
        - Coordinates of each shell
        - Total SCF Density
        - Spin SCF Density
        - Total MP2 Density
        - Spin MP2 Density
        - Total CI Density
        - Spin CI Density
        - Total CC Density
        - Spin CC Density
        - Cartesian Forces
        - Cartesian Force Constants
        - Dipole Moment
        - Dipole Derivatives
        - Polarizability
        - Dipole 2nd Derivatives
        - Polarizability Derivatives
        - HyperPolarizability

        """

        data = {}
        with open(file) as f:

            # Initial 72 characters of the title section (format: A72)
            data['title'] = next(f).strip()

            # Type, Method, Basis (format: A10,A60,A20) (format: A10,A30,A30 ???)
            line = next(f)
            data['type'] = line[0:10].strip()
            data['method'] = line[10:70].strip()
            data['basis'] = line[70:].strip()

            for line in f:

                pname, ptype = line[:40].strip(), line[43]

                if line[47:49] != 'N=':
                    # Scalar values
                    if ptype == 'I':
                        pdata = int(line[49:])
                    elif ptype == 'R':
                        pdata = float(line[49:])
                    elif ptype == "C":
                        pdata = line[49:].strip()
                    elif ptype == "L":
                        # NOTE: not tested yet (test case is missing)
                        pdata = bool(line[49])
                    else:
                        raise ValueError

                else:
                    # Vector and array data sections
                    ndata = int(line[49:])

                    if ptype == 'I':
                        nrows = ceil(ndata / 6)
                        pdata = []
                        for _ in range(nrows):
                            pdata.extend(map(int, chunkstring(next(f), 12)))
                    elif ptype == 'R':
                        nrows = ceil(ndata / 5)
                        pdata = []
                        for _ in range(nrows):
                            pdata.extend(map(float, chunkstring(next(f), 16)))
                    elif ptype == "C":
                        nrows = ceil(ndata / 5)
                        pdata = []
                        for _ in range(nrows):
                            pdata.extend(chunkstring(next(f), 12))
                    elif ptype == "H":
                        # NOTE: not tested yet (test case is missing)
                        nrows = ceil(ndata / 9)
                        pdata = []
                        for _ in range(nrows):
                            pdata.extend(chunkstring(next(f), 8))
                    elif ptype == "L":
                        # NOTE: not tested yet (test case is missing)
                        nrows = ceil(ndata / 72)
                        pdata = []
                        for _ in range(nrows):
                            pdata.extend(map(bool, chunkstring(next(f), 1)))
                    else:
                        raise ValueError

                data[pname] = pdata

        return cls(data)

    @property
    def ifc(self):

        values = self.get('Internal Force Constants', None)

        if not values:
            return None

        n = self['Number of atoms']
        return build_symmetric_matrix(values, n)

    @property
    def hessian(self):

        values = self.get('Cartesian Force Constants', None)

        if not values:
            return None

        n = self['Number of atoms']
        return build_symmetric_matrix(values, 3*n)

    @property
    def hessian_tensor(self):
        n = self['Number of atoms']
        return self.hessian.reshape((n, 3, n, 3))

    @property
    def vibrational_frequencies(self):

        nmodes = self['Number of Normal Modes']
        freqs = self['Vib-E2'][:nmodes]
        return freqs


