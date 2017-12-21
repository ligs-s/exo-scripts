from Filepath import Filepath
import ROOT
import os
import numpy as np

# need for EXOEventSummary
ROOT.gSystem.Load("libEXOROOT")
ROOT.gSystem.Load("libEXOUtilities")

def process_cutfile(cutfilename, outfilepath=None):
    """ take cutfilename as input, plot distributions as wanted"""
    cutfile = ROOT.TFile(cutfilename, "read")
    prefilename = cutfile.Get("fFullInputName").GetTitle()
    list_ss = cutfile.Get("EventList_ss")
    list_ms = cutfile.Get("EventList_ms")
    prefile = ROOT.TFile(prefilename, "read")
    tree = prefile.Get("dataTree")
    if tree==None:
        tree = prefile.Get("mcTree")
    print "Total entries ", tree.GetEntries()

    nEntries = list_ms.GetN()
    print nEntries
    if nEntries==0:
        print ' !!! Warning, no entries in this file ...'
        return

    # loop entries or tree->Draw(), do your stuff

    ## Draw()
    #tree.SetEntryList(list_ms)
    #tree.Draw("multiplicity>>h_mult(10, 0, 10)")
    #h_mult = ROOT.gDirectory.Get('h_mult')

    h_rms = ROOT.TH1F('h_rms', '', 500, 0, 100)
    h_mult = ROOT.TH1F('h_mult', '', 10, 0, 10)

    # OR loop
    for i in range(nEntries):
        entry =  list_ms.GetEntry(i)
        tree.GetEntry(entry)
        es = tree.EventSummary
        run = es.runNum
        evt = es.eventNum
        energy = es.energy
        mult = es.multiplicity
        if tree.GetName()=="mcTree":
            energy = es.energy_mc
        if energy<1000 or energy>3000:
            continue
        #print mult, len(es.cluster_x)
        rms_x = np.std(es.cluster_x)
        rms_y = np.std(es.cluster_y)
        rms_z = np.std(es.cluster_z)
        rms = np.sqrt(rms_x*rms_x + rms_y*rms_y + rms_z*rms_z)
        h_mult.Fill(mult)
        h_rms.Fill(rms)

        #num_ind_wires = es.num_ind_wires
        #num_coll_wires = es.num_coll_wires

    # save outputs if needed
    if not outfilepath==None:
        outfile = ROOT.TFile(outfilepath, 'recreate')
        h_mult.Write()
        h_rms.Write()
        outfile.Close()

    return


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
    process_cutfile(mcfilepath, outfilepath)
    return

if __name__=='__main__':
    #run_data('./list')
    #run_data([2966])
    run_mc()
