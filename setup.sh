#!/bin/bash

# ROOT env setup
export ROOTSYS=/nfs/slac/g/exo/mgmarino/rhel6/root/5.34.21
export LD_LIBRARY_PATH=${ROOTSYS}/lib:${LD_LIBRARY_PATH}
export PATH=${ROOTSYS}/bin:${PATH}
export PYTHONPATH=${ROOTSYS}/lib:${PYTHONPATH}

# EXO lib env setup
export EXOOUT=/nfs/slac/g/exo_data4/users/ligs/EXO/trunk/offline/exoout # modify this for offline version
source ${EXOOUT}/setup.sh

# EXO Fitting env setup
export EXO_FITTING_PATH=/nfs/slac/g/exo_data4/users/ligs/EXO/trunk/EXO_Fitting/EXO_Fitting # modify this path for EXOFitting version
export EXOFITINC=${EXO_FITTING_PATH}/EXOFitting/
export EXOFITLIB=${EXO_FITTING_PATH}/lib/
export LD_LIBRARY_PATH=${EXOFITLIB}:${LD_LIBRARY_PATH}
