#!/usr/bin/env python

from process_cutfile import process_cutfile
import os

####################################
basedir = '/nfs/slac/g/exo_data6/groups/Energy/data/WIPP/selection/2017_Phase1_v2/AfterCalibration/fv_162_10_182'

def run_one(runno, outdir='./tmp_out'):
    """ process one DATA file """
    fp = Filepath(basedir)
    filepath = fp.get_filepath(runno)
    outfilepath = outdir + '/run_%d.root' % runno
    if not fp.exists:
        print fp.filepath, 'file does not exists, skip'
    else:
        if not os.path.exists(outdir):
            os.system('mkdir -p ' + outdir)
        process_cutfile(filepath, outfilepath)
    return

def run_data_txt_input(runlist):
    f = open(runlist, 'r')
    runs = []
    for line in f:
        line = line.strip()
        if line.startswith('#'):
            continue
        runs.append(int(line))
    print runs
    run_data(runs)
    
def run_data(runs):
    """ process a list of runs """
    if type(runs)==str:
        run_data_txt_input(runs)
        
    filepath = os.path.realpath(__file__)
    filedir = os.path.dirname(filepath)
    outdir = filedir + '/output'
    for runno in runs:
        run_one(runno, outdir)
    return

def run_mc():
    """ run MC """
    mcfilepath = '/nfs/slac/g/exo_data6/groups/Fitting/data/MC/selection/2017_Phase1_v2/group2/fv_162_10_182/SourceS5_Th228.cut.root'

    filepath = os.path.realpath(__file__)
    filedir = os.path.dirname(filepath)
    outdir = filedir + '/output_mc'
    outfilepath = outdir + '/Th228_S5.root'
    if not os.path.exists(outdir):
        os.system('mkdir -p ' + outdir)
    process_cutfile(mcfilepath, outfilepath)
    return

if __name__=='__main__':
    #run_data('./list')
    #run_data([2966])
    run_mc()
