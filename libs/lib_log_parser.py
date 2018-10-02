''' Log Parsing '''

import os
from time import sleep
from pygtail import Pygtail
from threading import Thread

class LogParser():

    log_filename = ''
    sample_interval = 5
    log_thread = None
    end_monitoring = False
    callback_handler = None

    def __init__(self, callback_handler):
        self.callback_handler = callback_handler

    def get_lines(self):
        while not self.end_monitoring:
            lines=[]
            for line in Pygtail(self.log_filename):
                if os.path.exists("{}.offset".format(self.log_filename)):
                    lines.append(line)

            self.callback_handler(lines)
            sleep(self.sample_interval)

        print("Thread ended.")

    def start_monitoring(self):
        ''' Initialize monitoring '''
        print("Starting Montor", flush=True)
        self.end_monitoring = False
        self.log_thread = Thread(target=self.get_lines, args=())
        self.log_thread.start()
        print("Thread Started.", flush=True)

