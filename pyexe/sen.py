#!/usr/bin/python3

# Automation job submission.
# Named after Sen.

# Currently focus on Platform Load Sharing Facility (LSF)
# designed specificly for batch job submission for constructed CE dataset
# Will be reconstructed #TODO

import logging
import os
from pathlib import Path
import re
import subprocess
import time

class Bjob():
    def __init__(self, task_dir, type='vasp'):
        self.task_dir = task_dir
        self.type = type
        self.stat = None
        self.jobid = None

    def get_stat(self):
        if self.jobid is None:
            self.stat = 'TODO'
        else:
            status = subprocess.check_output(['bjobs', self.jobid])
            # TODO
            # Just a temporary implement
            stat = status.decode('utf-8').split()[10]
            self.stat = stat
        return self.stat

    def submit(self):
        os.chdir(self.task_dir)
        if self.type == 'vasp':
            vasp_file = self.task_dir.joinpath('vasp.lsf')
            job = subprocess.check_output('bsub < '+str(vasp_file), shell=True)
            # pipe = subprocess.Popen(['bsub', '-L', '/bin/sh'], 
            #                          stdout=subprocess.PIPE, 
            #                          stderr=subprocess.PIPE, 
            #                          stdin=open(vasp_file, 'r'))
            # job = pipe.communicate()[0]
            self.jobid = re.findall('\<(.*?)\>', job.decode('utf-8'))[0]

def get_bjobs_status():
    # Just a temporary implement
    # TODO form a dictionary or something

    # remove headline and empty string
    status = subprocess.check_output('bjobs').decode('utf-8').split('\n')[1:-1]
    # JOBID, USER, STAT, QUEUE, FROM_HOST, EXEC_HOST, JOB_NAME, SUBMIT_TIME
    bjobs_status = [bjob_stat.split() for bjob_stat in status]
    return bjobs_status

def auto_vasp_ce(dataset_dir, max_job=6, time_sleep=1000):
    logging.basicConfig(
        filename='auto_vasp_ce.log',
        level=logging.DEBUG,
        format='%(levelname)s:%(asctime)s: %(message)s'
    )

    # Specificly for batch job submission for constructed CE dataset
    print("Job begins")
    logging.debug('Job begins')
    print("Dataset: "+str(dataset_dir))
    logging.info("Dataset: "+str(dataset_dir))
    task_dirs = [rootdir.joinpath(rootdir, name) for name in os.listdir(rootdir)
                 if os.path.isdir(os.path.join(rootdir, name))]
    print("Total task: {}".format(len(task_dirs)))
    logging.info("Total task: {}".format(len(task_dirs)))
    # Remove fininshed tasks 
    for task_dir in task_dirs:
        if os.path.exists(task_dir.joinpath('OUTCAR')):
            task_dirs.remove(task_dir)
    print("Task left: {}".format(len(task_dirs)))
    logging.info("Task left: {}".format(len(task_dirs)))
    print("\nGood luck by Sen")
    
    while True:
        num_job = len(get_bjobs_status())
        if num_job < max_job:
            task_dir = random.choice(task_dirs)
            job = Bjob(task_dir=task_dir, type='vasp')
            print("Job created from: {}".format(str(task_dir)))
            logging.info("Job created from: {}".format(str(task_dir)))
            job.submit()
            print("Job submmited as {}, status: {}".format(job.jobid, job.get_stat()))
            logging.info("Job submmited as {}, status: {}".format(job.jobid, job.get_stat()))
            task_dirs.remove(task_dir)
            print("Task removed.")
            continue
        else:
            print("zzzzzzz")
            logging.debug("sleep")
            time.sleep(time_sleep)

if __name__ == '__main__':
    dataset_dir = Path('')
    auto_vasp_ce(dataset_dir=dataset_dir, max_job=6, time_sleep=1000)
