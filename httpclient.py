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
from urllib.parse import urlparse, urlencode

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
        self.socket.connect((host, port))
        return None

    def get_code(self, data):
        return int(self.get_headers(data).split()[1])

    def get_headers(self,data):
        return data.split('\r\n\r\n')[0]

    def get_body(self, data):
        return data.split('\r\n\r\n')[1]
    
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
        #body = ""

        url_parsed=urlparse(url)
        host = url_parsed.hostname
        port = url_parsed.port
        path = url_parsed.path
        scheme = url_parsed.scheme

        if not port:
            if scheme == 'https':
                port = 443
            elif scheme == 'http':
                port = 80

        self.connect(host, port)
        
        if path == '':
            path = '/'
        else:
            path = url_parsed.path
        
        request = f'GET {path} HTTP/1.1\r\nHost: {host}\r\nAccept: */*\r\nConnection: close\r\n\r\n'
        self.sendall(request)

        response = self.sendall(self.socket)
        code = self.get_code(response)
        print(code)
        headers = self.get_headers(response)
        print(headers)
        body = self.get_body(response)
        print(body)
        
        self.close()
        return HTTPResponse(code, body)




    def POST(self, url, args=None):
        #code = 500
        #body = ""
        url_parsed=urlparse(url)
        host = url_parsed.hostname
        port = url_parsed.port
        path = url_parsed.path
        scheme = url_parsed.scheme

        if not port:
            if scheme == 'https':
                port = 443
            elif scheme == 'http':
                port = 80

        self.connect(host, port)

        if path == '':
            path = '/'
        else:
            path = url_parsed.path

        if args == None:
            args_encoded = ''
        else:
            args_encoded = urlencode(args)
        request = "POST {} HTTP/1.1\r\nHost: {}\r\nContent-Type: application/x-www-form-urlencoded\r\nContent-Length: {}\r\nConnection: close\r\n\r\n{}".format(path,host,len(args_encoded),args_encoded)
        
        self.sendall(request)

        response = self.sendall(self.socket)
        code = self.get_code(response)
        print(code)
        headers = self.get_headers(response)
        print(headers)
        body = self.get_body(response)
        print(body)

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
