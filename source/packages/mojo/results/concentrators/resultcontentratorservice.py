
from typing import Optional

import threading

from datetime import datetime, timedelta
from socketserver import _AfInetAddress, ThreadingMixIn
from http.server import HTTPServer, SimpleHTTPRequestHandler


from mojo.results.model.progressinfo import ProgressInfo

from mojo.results.recorders.resultrecorder import ResultRecorder

class ResultCallbackHandler(SimpleHTTPRequestHandler):
    """
        The :class:`ResultConcentratorService` 
    """

    def do_POST(self):
        server: ResultConcentratorServer = self.server
        return


class ResultConcentratorServer(ThreadingMixIn, HTTPServer):
    """
        The :class:`ResultConcentratorServer` runs a web server for the purpose of receiving and concentrating result
        callbacks from remote tasks or processes.
    """

    def __init__(self, recorder: ResultRecorder, server_address: _AfInetAddress, bind_and_activate: bool = True) -> None:

        self._recorder = recorder

        super().__init__(server_address, ResultCallbackHandler, bind_and_activate)

        return

    def start(self):
        """
            Starts the server request accept thread.  This method does not return until after the
            service has started.
        """
        
        start_gate = threading.Event()
        start_gate.clear()

        self._server_running = True
        
        self._server_thread = threading.Thread(target=self._service_thread_entry, name='tasker', args=(start_gate,), daemon=True)
        self._server_thread.start()

        start_gate.wait()

        return
    
    def _service_thread_entry(self, start_gate: threading.Event):
        
        start_gate.set()

        self.serve_forever()

        return

    def update_task_progress(self, progress: ProgressInfo):
        self._recorder.post_task_progress(progress)
        return


