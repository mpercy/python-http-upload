#!/usr/bin/python

import BaseHTTPServer
import os
import re

class UploadRequestHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    def do_POST(self):
        print "GOT A POST"
        r, info = self.deal_post_data()
        print r, info, "by: ", self.client_address
        print self.headers.getplist()
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        return
        for line in self.rfile:
            # do something with the line
            print line

    def deal_post_data(self):
        boundary = self.headers.plisttext.split("=")[1]
        #print "BOUNDARY:", boundary
        # TODO: Why do I have to do this?
        boundary = '--' + boundary
        remainbytes = int(self.headers['content-length'])
        #print "ABOUT TO READ"
        data = self.rfile.read(remainbytes)
        #print "============================"
        #print data
        #print "============================"
        #data = re.sub(boundary + '--', '', data, flags=re.DOTALL)
        #print data
        #print "SPLITTING"
        parts = data.split(boundary)
        #print "POST SPLIT"
        fn = None
        for p in parts:
            #print "Looking at part"
            #print "---------------------"
            #print p
            #print "---------------------"
            fn = re.search(r'Content-Disposition.*name="file"; filename="(.*)"', p)
            if fn:
                break
        if not fn:
            return (False, "Can't find out file name...")

        outfile = os.path.join(".", fn.group(1))
        try:
            out = open(outfile, 'wb')
        except IOError:
            return (False, "Can't create file to write, do you have permission to write?")

        data = re.sub('^.*?\r\n\r\n', '', p, flags=re.DOTALL)
        data = re.sub('\r\n$', '', data)

        #print "THIS IS THE DATA...."
        #print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
        #print data
        #print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
        out.write(data)
        out.close()
        return (True, "File '%s' upload success!" % outfile)

def test(HandlerClass = UploadRequestHandler,
         ServerClass = BaseHTTPServer.HTTPServer):
    BaseHTTPServer.test(HandlerClass, ServerClass)

if __name__ == '__main__':
    test()
