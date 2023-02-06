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

def get_remote_ip(host):
    #print(f'Getting IP for {host}')
    try:
        remote_ip = socket.gethostbyname( host )
    except socket.gaierror:
        print ('Hostname could not be resolved. Exiting')
        sys.exit()

    #print (f'Ip address of {host} is {remote_ip}')
    return remote_ip

def help():
    print("httpclient.py [GET/POST] [URL]\n")

class HTTPResponse(object):
    def __init__(self, code=200, body=""):
        self.code = code
        self.body = body
    

class HTTPClient(object):
    #def get_host_port(self,url):

    def connect(self, host, port):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        print("host is: "+str(host))
        remote_ip = get_remote_ip(host)
        self.socket.connect((remote_ip, port))
        #print("here")
        return self.socket

    def get_code(self, data):
        return None

    def get_headers(self,data):
        return None

    def get_body(self, data):
        return None
    
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
        #code = 500
        body = ""
        # self.get_headers(url)
        #return HTTPResponse(code, body)
        
        # self.sendall(request)
        #self.recvall()
        print("1")
        u = urlparse(url)
        host = u.hostname
        #print(host)
        query = u.query
        path = u.path

        if host == "127.0.0.1":
            port = u.port
        else:
            port = 80
        
        print("port is: "+str(port))
        # # request = 'GET ' + '/'+ url + '/ ' + 'HTTP/1.1'
        # request = "GET /about/about_careers.htm HTTP/1.1\n"
        # request=request+"User-Agent: Mozilla/4.0 (compatible; MSIE5.01; Windows NT)\n"
        # request=request+"Host: www.tutorialspoint.com\n"
        # request=request+"Accept-Language: en-us\n"
        # request=request+"Accept-Encoding: gzip, deflate\n"
        # request=request+"Connection: Kill\n"
        request = f'GET {path} HTTP/1.1\r\nHost: {host}\r\n\r\n'

        print("request is: ")
        print(request)
        print('-'*50)
        self.connect(host,port)
        #print(self.socket)
        self.sendall(request)
        self.socket.shutdown(socket.SHUT_WR)
        #print(request)
        print("2")
        response = str(self.recvall(self.socket))
        print(response)
        print("3")
        parts = response.split(" ")
        print(parts)
        code = int(parts[1])
        print("body is :")
        

        headers_and_body = response.split("\r\n\r\n")
        body = headers_and_body[1]
        print(body)

        return HTTPResponse(code, body) # do this baby
        

    def POST(self, url, args=None):
        code = 500
        body = ""
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
