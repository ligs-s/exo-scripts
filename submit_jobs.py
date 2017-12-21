#!/usr/bin/env python

from ROOT import gROOT
import os, sys
from subprocess import Popen, PIPE, STDOUT, check_output
import time

MAX_JOBS=100

def get_list(listname):
    f = open(listname, 'r')
    filelist = []
    for line in f:
        if line.startswith('#') or line=='\n':
            continue
        line = line.strip()
        filelist.append(line)
    return filelist

def make_job(jobdir, jobname, cmd, jobtime=60, on_the_fly=True, delay_submit=False):
    sub_cmd = None
    if on_the_fly:
        sub_cmd = 'bsub -W %d -R rhel60 %s' % (jobtime, cmd)
    else:
        if not os.path.exists(jobdir):
            os.system('mkdir -p %s' % jobdir)
        jobfile = jobdir+'/'+jobname
        f = open(jobfile, 'w')
        f.write(cmd)
        f.close()
        os.system("chmod 755 %s" % jobfile)
        sub_cmd = 'bsub -W %d -R rhel60 -o %s/%s.out -e %s/%s.err %s' % (jobtime, jobdir, jobname, jobdir, jobname, jobfile)
    print sub_cmd
    if delay_submit:
        while(get_current_job_num()>=MAX_JOBS):
            print 'Number of jobs exceeded limit, wait 60s ...'
            time.sleep(60)
    os.system(sub_cmd)
    return

def get_current_job_num():
    cmd = 'bjobs -u ligs | wc -l'
    p = Popen(cmd, shell=True, stdout=PIPE, stderr=PIPE)
    #out = p.stdout.read()
    out, err = p.communicate()
    #out = check_output(cmd, shell=True)
    n_jobs = int(out.strip()) - 1
    #print n_jobs, "jobs in the queue now."
    return n_jobs

######################################################

### jobs specific ###
def run_noise_jobs(jobtime=60, on_the_fly=True, delay_submit=False):
    """ wrapper to run noise jobs """
    pos = 'S5' 
    filelist = get_list('./%s.txt' % pos)
    jobdir = './job'
    job_idx = 0
    for line in filelist:   
        runno  = int(line)
        # phase 1
        basedir = "/nfs/slac/g/exo_data6/groups/Energy/data/WIPP/selection/2017_Phase1_v2/AfterCalibration/fv_162_10_182"
        # phase 2
        #basedir = "/nfs/slac/g/exo_data6/groups/Energy/data/WIPP/selection/2017_Phase2_v3/AfterCalibration/fv_162_10_182/"
        cutfilename = basedir + "/run_%d_tree.root" % runno
        if not os.path.exists(cutfilename):
            print cutfilename, 'does not exists, skip ...'
            continue 
        cmd = "python /nfs/slac/g/exo_data4/users/ligs/EXO/rec/get_event_rms_noise.py %d %s" % (runno, pos)
        make_job(jobdir, "job%d.sh" % job_idx, cmd, jobtime, on_the_fly, delay_submit)
        job_idx += 1

def run_mc_job(jobtime=60, on_the_fly=True, delay_submit=False):
    cmd = "python /nfs/slac/g/exo_data4/users/ligs/EXO/rec/get_event_rms_noise.py"
    make_job("", "" , cmd, jobtime, on_the_fly, delay_submit)
    
        
if __name__=='__main__':
    """ """
    #get_current_job_num()
    run_noise_jobs(120, on_the_fly=True, delay_submit=True)
    #run_mc_job()
