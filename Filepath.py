"""
input: runno, production directory

production directory:
data:
/nfs/slac/g/exo_data6/groups/Energy/data/WIPP/preprocessed/2017_Phase1_v2/AfterCalibration/run_[RunNumber]_tree.root
/nfs/slac/g/exo_data6/groups/Energy/data/WIPP/selection/2017_Phase1_v2/AfterCalibration/fv_162_10_182/run_[RunNumber]_tree.root

mc: 
/nfs/slac/g/exo_data6/groups/Fitting/data/MC/preprocessed/2017_Phase1_v2/group2/
/nfs/slac/g/exo_data6/groups/Fitting/data/MC/selection/2017_Phase1_v2/group2/fv_162_10_182/
"""

import os

class Filepath:
    """ handling the filepath """
    def __init__(self, file_dir=None):
        self.file_dir = file_dir
        self.runno = None
        self.filepath = None
        self.exists = None

    def set_file_dir(self, file_dir):
        self.file_dir = file_dir
        return

    def set_runno(self, runno):
        self.runno = runno 
        return

    def get_filepath(self, runno):
        self.set_runno(runno)
        self.filepath = self.file_dir + '/run_%d_tree.root' % self.runno
        self.exists = True
        if not os.path.exists(self.filepath):
            self.exists = False
        return self.filepath

if __name__=="__main__":
    base_dir = '/nfs/slac/g/exo_data6/groups/Energy/data/WIPP/selection/2017_Phase1_v2/AfterCalibration/fv_162_10_182'
    fp = Filepath(base_dir)
    filepath = fp.get_filepath(2315)
    if not fp.exists:
        print ' !!! Warning:', filepath, 'does not exist'
    print filepath
