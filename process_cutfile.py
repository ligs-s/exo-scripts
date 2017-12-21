"""
    process_cutfile() defines your operations on the preprocessed tree
"""

import ROOT
import os, sys
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
    #print "Total entries ", tree.GetEntries()

    nEntries = list_ms.GetN()
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
        basedir = os.path.dirname(outfilepath)
        if not os.path.exists(basedir):
            print basedir, 'does not exist, make a new one.'
            os.system('mkdir -p ' + basedir)

        outfile = ROOT.TFile(outfilepath, 'recreate')
        h_mult.Write()
        h_rms.Write()
        outfile.Close()

    return

if __name__=='__main__':
    process_cutfile(cutfilename=sys.argv[1], 
                    outfilepath=sys.argv[2])
