#!/usr/bin/python3

# Automation job submission.
# Named after Sen.

# Currently focus on Platform Load Sharing Facility (LSF)
# designed for batch job submission for construct CE dataset

import os
import re
from pathlib import Path
import subprocess 

class Bjob():
    def __init__(self, task_dir, type):
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
            job = pipe.communicate()[0]
            self.jobid = re.findall('\<(.*?)\>', job.decode('utf-8'))[0]



