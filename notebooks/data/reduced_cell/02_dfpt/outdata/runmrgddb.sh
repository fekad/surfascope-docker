#!/bin/bash
cd /Users/fekad/Work/surfascope/python-tools/notebooks/reduced_cell/02_dftp/outdata
# OpenMp Environment
export OMP_NUM_THREADS=1
mrgddb --nostrict < /Users/fekad/Work/surfascope/python-tools/notebooks/reduced_cell/02_dftp/outdata/mrgddb.stdin > /Users/fekad/Work/surfascope/python-tools/notebooks/reduced_cell/02_dftp/outdata/mrgddb.stdout 2> /Users/fekad/Work/surfascope/python-tools/notebooks/reduced_cell/02_dftp/outdata/mrgddb.stderr
