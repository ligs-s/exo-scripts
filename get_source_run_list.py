#!/usr/bin/env python

"""
use EXOEnergy to retrieve a list of source runs

-- user proper version of UpdatedLivetimeSourceRunsInfo.txt 
-- apply proper cuts for selection

"""

import ROOT

exoenergydir = './EXOEnergy'
ROOT.gSystem.Load('%s/lib/libEXOEnergy.so' % exoenergydir)

infoRuns = ROOT.EXOSourceRunsPolishedInfo('%s/data/UpdatedLivetimeSourceRunsInfo.txt' % exoenergydir)
infoRuns.CutExact('SourceName','Th-228')
infoRuns.CutExact('SourcePositionS','5')

#for i in range(infoRuns.GetNRuns()):
#    infoRuns.PrintRunList(i,'Th-228_S5_SourceRunsInfo.txt')

runs = infoRuns.GetListOf('RunNumber')
runlist = [] # runlist of selected source runs

for run in runs:
    print run
    runlist.append(int(run))
