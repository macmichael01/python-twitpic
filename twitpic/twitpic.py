#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
# python-twitpic - Dead-simple Twitpic image uploader.

# Copyright (c) 2009, Chris McMichael
# http://chrismcmichael.com/
# http://code.google.com/p/python-twitpic/

# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#     * Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#     * Redistributions in binary form must reproduce the above copyright
#       notice, this list of conditions and the following disclaimer in the
#       documentation and/or other materials provided with the distribution.
#     * Neither the name of the author nor the names of its contributors may
#       be used to endorse or promote products derived from this software
#       without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE AUTHOR AND CONTRIBUTORS``AS IS'' AND ANY
# EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE AUTHOR OR CONTRIBUTORS BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

"""

from xml.dom import minidom as xml
import httplib, mimetypes
from urllib import urlopen

try:
    import cStringIO as StringIO
except ImportError:
    import StringIO

class TwitPicAPI(object):
    
    SERVER = 'twitpic.com'
    PORT = 80
    UPLOAD_URL = '/api/upload/'
    UPLOAD_POST_URL = '/api/uploadAndPost/'
    
    def __init__(self, username, password, image=None, filename=None,   
                server=SERVER, port=PORT, upload_url=UPLOAD_URL,
                upload_post_url=UPLOAD_POST_URL):
        self.server = server
        self.port = port
        self.username = username
        self.password = password
        self.filename = filename
        self.filedata = None
        self.image = image
        self.upload_url = upload_url
        self.upload_post_url = upload_post_url
        self.connection = httplib.HTTPConnection("%s:%d" % (self.server,
                                                                self.port))
    
    def upload(self, image=None, message=None, post_to_twitter=False):
        if image:
            self.image = image
        self.get_filedata()
        fields = [('username', self.username), ('password',self.password)]
        if message is not None:
            fields.append(('message', message))
        content_type, body = self.encode_multipart_formdata(fields)
        url = self.upload_url
        if post_to_twitter:
            url = self.upload_post_url
        headers = {'User-Agent': 'Python-TwitPic', 'Content-Type': content_type}
        self.connection.request('POST', url, body, headers)
        response = self.connection.getresponse()
        if response.status != 200:
            raise Exception('Error uploading image: TwitPic returned HTTP \
                             %s (%s)' % (response.status, response.reason))
        return self.parse_xml(response.read())
    
    def encode_multipart_formdata(self, fields=None):
        boundary = '-------tHISiStheMulTIFoRMbOUNDaRY'
        crlf = '\r\n'
        l = []
        if fields:
            for (key, value) in fields:
                l.append('--' + boundary)
                l.append('Content-Disposition: form-data; name="%s"' % str(key))
                l.append('')
                l.append(str(value))
        for (filename, value) in [(self.image, self.filedata)]:
            l.append('--' + boundary)
            l.append('Content-Disposition: form-data; name="media"; \
                      filename="%s"' % (str(filename),))
            l.append('Content-Type: %s' % self.get_content_type())
            l.append('')
            l.append(value.getvalue())
        l.append('--' + boundary + '--')
        l.append('')
        body = crlf.join(l)
        content_type = 'multipart/form-data; boundary=%s' % boundary
        return content_type, body
    
    def get_content_type(self):
        return mimetypes.guess_type(self.image)[0] or 'application/octet-stream'
    
    def get_filedata(self):
        if self.filename is None:
            try:
                import Image
            except ImportError:
                self.filedata = StringIO.StringIO(urlopen(self.image).read())
            else:
                #img = Image.open(self.image)
                self.filedata = StringIO.StringIO(urlopen(self.image).read())
                img = Image.open(self.filedata)
                #img.save(self.filedata, img.format)
        else:
            try:
                self.filedata = StringIO.StringIO(self.image)
            except Exception, e:
                print e
            self.image = self.filename
    
    def parse_xml(self, xml_response):
        dom = xml.parseString(xml_response)
        node = dom.getElementsByTagName('rsp')
        if node[0].getAttribute('stat') == 'ok' \
        or node[0].getAttribute('status') == 'ok':
            # return URL
            url = dom.getElementsByTagName('mediaurl')
            return url[0].childNodes[0].data
        elif node[0].getAttribute('stat') == 'fail':
            childNode = node[0].childNodes[1]
            if childNode.getAttribute('code') == '1001':
                # Invalid twitter username or password
                return 1001
            elif childNode.getAttribute('code') == '1002':
                # Image not found
                return 1002
            elif childNode.getAttribute('code') == '1003':
                # Invalid image type
                return 1003
            else:
                # Image larger than 4MB
                return 1004
        # Unidentified Error
        return 0

if __name__ == '__main__':
    from optparse import OptionParser
    optPsr = OptionParser("usage: %prog -u USER_NAME [options] IMG_PATH")
    optPsr.add_option('-u', '--user', type='string', help='Twitpic user name')
    optPsr.add_option('-p', '--passwd', type='string', help='Twitpic password')
    optPsr.add_option('-b', '--both', action='store_true', default=False,
            help = 'post to twitter together')
    optPsr.add_option('-m', '--msg', type='string', help='message')
    (opts, args) = optPsr.parse_args()

    if not opts.user:
        optPsr.error("no USER_NAME")    
    elif not args:
        optPsr.error('no IMG_PATH to upload')
    elif len(args) > 1:
        optPsr.error('multiple img upload not allowed')

    if not opts.passwd:
        import getpass
        passwd = getpass.getpass()
    else:
        passwd = opts.passwd

    twitpic = TwitPicAPI(opts.user, passwd)
    posted_url = twitpic.upload(args[0],
            message=opts.msg, post_to_twitter=opts.both)

    print posted_url

# vim: set et sw=4:
