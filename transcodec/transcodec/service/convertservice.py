# coding:utf-8
import os
from daemon import runner

class ConvertService(runner.DaemonRunner):
    """
    Convert Service based on daemon.runner
    overwrite the ``action_functions`` to make start|restart|stop with our need
    """
    start_message = "convert service %(pid)d started"

    def __init__(self, imp):
        import signal
        from daemon import daemon

        import sys
        super(ConvertService, self).__init__(imp)

        
        # this is a hack to runner.DaemonRunner
        # reopen the file obj of output, set mode to no buff
        # and if it's not a tty, set it to append mode
        self.daemon_context.stdout = self.stdhack(self.daemon_context.stdout)
        self.daemon_context.stderr = self.stdhack(self.daemon_context.stderr)        

        # rewrite signal hook to close socketserver 
        sig_map = daemon.make_default_signal_map()
        sig_map[signal.SIGTERM] = self._on_signal_term
        self.daemon_context.signal_map = sig_map

    def stdhack(self, stdfile):
        if stdfile.isatty():
            return stdfile
        fname = stdfile.name
        mode = stdfile.mode
        stdfile.close()
        if mode == 'w+':
            mode = 'a+'
        newstd = open(fname, mode, buffering=0)
        return newstd

    def convert_start(self):
        super(ConvertService, self)._start()

    def convert_stop(self):
        #self.app.stop()
        super(ConvertService, self)._stop()

    def convert_restart(self):
        import time
        self.convert_stop()
        time.sleep(1)
        self.convert_start()

    def convert_status(self):
        import convertreq
        return convertreq.heartbeat()
        

    def _on_signal_term(self, signum, frame):
        import signal
        print("Send SIGTERM")
        #logging.debug("Send SIGTERM")
        self.app.stop()
        pid = self.pidfile.read_pid()
        os.kill(pid, signal.SIGKILL)


    action_funcs = {
            'start': convert_start,
            'stop': convert_stop,
            'restart': convert_restart,
            'status': convert_status,
            }
