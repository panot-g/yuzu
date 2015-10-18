#!/usr/bin/env python
# -*- coding: utf-8 -*-

from threading import Thread
from Queue import Queue
import SimpleHTTPServer
import SocketServer
import logging
import urlparse
import time
import os
import json


PORT = 8080


# basic logging configuration
log_fmt = '[%(levelname)s] (%(threadName)-10s) %(message)s'
logging.basicConfig(level=logging.DEBUG, format=log_fmt)


MESSAGES = [
  {'from': 'kure', 'message': 'pong~ 日本語!'},
  {'from': 'elli', 'message': 'yo!'},
]


class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    pass


class ChatHTTPRequestHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):

  def do_GET(self):
   # Parse query data & params to find out what was passed
   parsedParams = urlparse.urlparse(self.path)
   queryParsed = urlparse.parse_qs(parsedParams.query)

   # request is either for a file to be served up or our test
   if parsedParams.path == '/chat':
      self.processMyRequest(queryParsed)
   else:
      # Default to serve up a local file
      SimpleHTTPServer.SimpleHTTPRequestHandler.do_GET(self)


  def processMyRequest(self, query):
    self.send_response(200)
    self.send_header('Content-Type', 'application/json')
    self.send_header('Access-Control-Allow-Origin', '*')
    self.end_headers()

    msg = json.dumps(MESSAGES)

    self.wfile.write(msg);

    # Artificial latency added and removed here. (For testing..)
    # time.sleep(10)

    self.wfile.close();


def spawn_server_thread(server_queue):
    Handler = ChatHTTPRequestHandler

    try:
      server = ThreadedTCPServer(("", PORT), Handler)
    except Exception as e:
      print e
      return

    logging.debug("serving at port %d", PORT)
    server_queue.put(server)

    server.serve_forever()


def start_server():
    server_queue = Queue()

    # Start a thread with the server -- that thread will then start one
    # more thread for each request
    server_thread = Thread(
        target=spawn_server_thread,
        args=[server_queue])

    # Exit the server thread when the main thread terminates
    server_thread.daemon = True
    server_thread.start()

    logging.debug("Server loop running in thread: %s", server_thread.name)

    return server_queue.get(), server_thread


if __name__ == '__main__':
  server_queue, server_thread = start_server()

  while server_thread.is_alive():
    time.sleep(1)
