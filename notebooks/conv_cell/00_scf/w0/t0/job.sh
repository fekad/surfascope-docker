#!/bin/bash
cd /home/jovyan/notebooks/conv_cell/00_scf/w0/t0
# OpenMp Environment
export OMP_NUM_THREADS=1
mpirun  -n 4 abinit --timelimit 1-0:0:0 < /home/jovyan/notebooks/conv_cell/00_scf/w0/t0/run.files > /home/jovyan/notebooks/conv_cell/00_scf/w0/t0/run.log 2> /home/jovyan/notebooks/conv_cell/00_scf/w0/t0/run.err
