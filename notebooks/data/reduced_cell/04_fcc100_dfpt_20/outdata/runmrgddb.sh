#!/bin/bash
cd /home/jovyan/abinit/reduced_cell/04_fcc100_dfpt_20/outdata
# OpenMp Environment
export OMP_NUM_THREADS=1
mpirun  -n 1 mrgddb --nostrict < /home/jovyan/abinit/reduced_cell/04_fcc100_dfpt_20/outdata/mrgddb.stdin > /home/jovyan/abinit/reduced_cell/04_fcc100_dfpt_20/outdata/mrgddb.stdout 2> /home/jovyan/abinit/reduced_cell/04_fcc100_dfpt_20/outdata/mrgddb.stderr
