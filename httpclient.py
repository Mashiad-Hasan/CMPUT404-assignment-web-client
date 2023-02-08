#!/usr/bin/env python3
# coding: utf-8
# Copyright 2016 Abram Hindle, https://github.com/tywtyw2002, and https://github.com/treedust
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Do not use urllib's HTTP GET and POST mechanisms.
# Write your own HTTP GET and POST
# The point is to understand what you have to send and get experience with it

import sys
import socket
import re
# you may use urllib to encode data appropriately
import urllib.parse
from urllib.parse import urlparse


def help():
    print("httpclient.py [GET/POST] [URL]\n")

class HTTPResponse(object):
    def __init__(self, code=200, body=""):
        self.code = code
        self.body = body
    
def get_remote_ip(host):
    #print(f'Getting IP for {host}')
    try:
        remote_ip = socket.gethostbyname( host )
    except socket.gaierror:
        print ('Hostname could not be resolved. Exiting')
        sys.exit()

    return remote_ip


class HTTPClient(object):

    def connect(self, host, port):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        remote_ip = get_remote_ip(host)
        self.socket.connect((remote_ip, port))
        return self.socket

    def get_code(self, response):
        parts = response.split(" ")
        code = int(parts[1])

        return code

    def get_response(self):
        response = self.recvall(self.socket)

        return response

    def get_body(self, response):
        headers_and_body = response.split("\r\n\r\n")
        body = headers_and_body[1]

        return body
    
    def sendall(self, data):
        self.socket.sendall(data.encode('utf-8'))
        
    def close(self):
        self.socket.close()

    # read everything from the socket
    def recvall(self, sock):
        buffer = bytearray()
        done = False
        while not done:
            part = sock.recv(1024)
            if (part):
                buffer.extend(part)
            else:
                done = not part
        return buffer.decode('utf-8')

    def GET(self, url, args=None):
        u = urlparse(url)
       
        host = u.hostname
        query = u.query
        path = u.path

        if path == '':
            path = path + '/'
        port = u.port

        if host == "127.0.0.1":
            port = u.port
        else:
            port = 80
        
        request = f'GET {path} HTTP/1.1\r\nHost: {host}\r\nConnection: close\r\n\r\n'
        
        self.connect(host,port)
        
        self.sendall(request)
        #self.socket.shutdown(socket.SHUT_WR)
        
        response = self.get_response()
        code = self.get_code(response)
        body = self.get_body(response)
        
        self.close()
        return HTTPResponse(code, body) 
        

    def POST(self, url, args=None):
        u = urlparse(url)
        
        host = u.hostname
        query = u.query
        path = u.path

        if path == '':
            path = path + '/'
        port = u.port

        if host == "127.0.0.1":
            port = u.port
        else:
            port = 80

        content_length = int(sys.getsizeof(args)) + 10
        request = f'POST {path} HTTP/1.1\r\nHost: {host}\r\nConnection: close\r\nContent-Length: {content_length}\r\nContent-Type: application/x-www-form-urlencoded\r\n\r\n'
        
        if args.__class__.__name__ == 'dict':
            req_body = ''
            for key,value in args.items():
                req_body=req_body+str(key)+'='+str(value)+'&'
            req_body = req_body[:-1]
        else:
            req_body = str(args)

        request = request + req_body 
        
        self.connect(host,port)
      
        self.sendall(request) # send body of post to the server
        self.socket.shutdown(socket.SHUT_WR)
        
        response = self.get_response()
        code = self.get_code(response)
        body = self.get_body(response)
        
        self.close()
        return HTTPResponse(code, body)

    def command(self, url, command="GET", args=None):
        if (command == "POST"):
            return self.POST( url, args )
        else:
            return self.GET( url, args )
    
if __name__ == "__main__":
    client = HTTPClient()
    command = "GET"
    if (len(sys.argv) <= 1):
        help()
        sys.exit(1)
    elif (len(sys.argv) == 3):
        print(client.command( sys.argv[2], sys.argv[1] ))
    else:
        print(client.command( sys.argv[1] ))
