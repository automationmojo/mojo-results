
from typing import Optional

import json
import logging
import requests
import os
import threading
import time
import traceback

from socketserver import _AfInetAddress, ThreadingMixIn
from http.server import HTTPServer, SimpleHTTPRequestHandler

from mojo.results.model.forwardinginfo import ForwardingInfo
from mojo.results.model.progressinfo import ProgressInfo

from mojo.results.recorders.resultrecorder import ResultRecorder


class ProgressCallbackHandler(SimpleHTTPRequestHandler):
    """
        The :class:`ResultConcentratorService` 
    """

    def do_POST(self):

        errmsg = None

        if 'content-length' in self.headers:

            content_length = self.headers["content-length"]
            length = int(content_length) if content_length else 0

            if length:
                try:
                    content = self.rfile.read(length)
                    
                    data = json.loads(content)

                    progress = ProgressInfo.from_dict(data)
                    server: ProgressConcentratorServer = self.server
                    
                    server.update_task_progress(progress)

                except Exception as perr:
                    errmsg_msg_lines = [
                        "Error processing progress postback.",
                        "EXCEPTION:",
                        traceback.format_exc()
                    ]
                    errmsg = os.linesep.join(errmsg_msg_lines)

        if not errmsg:
            self.send_response(200, message=None)
            self.send_header("Content-Type", "text/html")
        else:
            self.send_response(500, message=errmsg)
            self.send_header("Content-Type", "text/html")
        
        self.end_headers()

        return


class ProgressConcentratorServer(ThreadingMixIn, HTTPServer):
    """
        The :class:`ResultConcentratorServer` runs a web server for the purpose of receiving and concentrating result
        callbacks from remote tasks or processes.
    """

    def __init__(self, recorder: ResultRecorder, server_address: _AfInetAddress, forwarding_info: Optional[ForwardingInfo] = None,
                bind_and_activate: bool = True) -> None:

        self._recorder = recorder
        self._forwarding_info = forwarding_info

        super().__init__(server_address, ProgressCallbackHandler, bind_and_activate)

        self._forward_thread = None
        self._forwarding_running = False

        self._server_thread = None
        self._server_running = False

        self._logger = logging.getLogger()

        return

    def start(self):
        """
            Starts the server request accept thread.  This method does not return until after the
            service has started.
        """
        
        if self._forwarding_info is not None:
            fwd_gate = threading.Event()
            fwd_gate.clear()
            
            self._forward_thread = threading.Thread(target=self._forwarding_thread_entry, name='prog-forwarder', args=(fwd_gate,), daemon=True)
            self._forward_thread.start()

            fwd_gate.wait()

        svr_gate = threading.Event()
        svr_gate.clear()

        self._server_running = True
        
        self._server_thread = threading.Thread(target=self._service_thread_entry, name='prog-concentrator', args=(svr_gate,), daemon=True)
        self._server_thread.start()

        svr_gate.wait()

        return
    
    def _forwarding_thread_entry(self, start_gate: threading.Event):
        
        self._forwarding_running

        headers = {
            "Content-Type": "application/json"
        }

        forwarding_interval = self._forwarding_info.forwarding_interval
        forwarding_url = self._forwarding_info.forwarding_url
        forwarding_headers = self._forwarding_info.forwarding_headers

        if forwarding_headers is not None:
            headers.update(forwarding_headers)

        start_gate.set()

        while self._forwarding_running:

            try:
                summary = self._recorder.summary

                requests.post(forwarding_url, json=summary, headers=headers)

                time.sleep(forwarding_interval)

            except Exception:
                errmsg = traceback.format_exc()
                self._logger.error(errmsg)

        return

    def _service_thread_entry(self, start_gate: threading.Event):
        
        self._server_running = True

        start_gate.set()

        self.serve_forever()

        return

    def update_task_progress(self, progress: ProgressInfo):
        self._recorder.post_task_progress(progress)
        return


