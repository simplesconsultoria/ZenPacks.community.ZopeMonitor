#!/usr/bin/env python
# -*- coding:utf-8 -*-
import sys
import re
import urllib2

from optparse import OptionParser

DELIMITERS=""" :""" # presently space and colon

MuninParser = re.compile(r"""(\w+)([%s])([-0-9.]+)""" % DELIMITERS)

class ZenossZopeMonitorPlugin(object):

    def __init__(self, hostname, port, ipAddress, uri, useSsl, authentication):
        self.hostname = hostname
        self.port = str(port) or '8080'
        self.ipAddress = ipAddress
        self.uri = uri
        self.useSsl = useSsl
        self.protocol = useSsl and 'https' or 'http'
        self.authentication = authentication

    def parse_result(self, data=None):
        if not data:
            return None
        result = {}
        for line in data:
            element = line.split('\n')[0].strip()
            match = MuninParser.search(element)
            if match:
                tag, delimiter, value = match.groups()
                result[tag] = float(value)
        return result

    def formatNagios(self, response):
        """OK|foo=0.814667;;;0.000000 bar=30737B;;;0"""
        base = 'OK |'
        for key, value in response.items():
            tmpStr = '%s=%s;;;0 ' % (str(key), str(value))
            base += tmpStr
        return base

    def run(self):
        headers = [('User-agent', 'Zenoss')]
        if self.hostname and self.ipAddress:
            headers.append(('Host', self.hostname))
            address = '%s://%s:%s/@@munin.zope.plugins/%s' % (self.protocol,
                                                              self.ipAddress,
                                                              self.port,
                                                              self.uri)
        else:
            address = '%s://%s:%s/@@munin.zope.plugins/%s' % (self.protocol,
                                                              self.hostname,
                                                              self.port,
                                                              self.uri)
        if self.authentication:
            username, passwd = self.authentication.split(':')
            passman = urllib2.HTTPPasswordMgrWithDefaultRealm()
            passman.add_password(None, address, username, passwd)
            authhandler = urllib2.HTTPBasicAuthHandler(passman)
            opener = urllib2.build_opener(authhandler)
        else:
            opener = urllib2.build_opener()

        opener.addheaders = headers
        f = opener.open(address)
        response = self.parse_result(f)
        response = self.formatNagios(response)
        return response

if __name__ == "__main__":
    parser = OptionParser()
    parser.add_option('-U', '--uri', dest='uri',
                 help='URI for munin data')
    parser.add_option('-H', '--hostname', dest='hostname',
                 help='Hostname of Zope server')
    parser.add_option('-p', '--port', dest='port', default=80, type='int',
                 help='Port of Zope server')
    parser.add_option('-I', '--ipAddress', dest='ipAddress',
                 help='IP Address Zope server')
    parser.add_option('-s', '--useSsl', dest='useSsl', default=False,
                 help='Use SSL?')
    parser.add_option('-t', '--timeout', dest='timeout',
                 help='Timeout')
    parser.add_option('-a', '--authentication', dest='authentication',
                 help='Authentication')
    options, args = parser.parse_args()

    if not options.hostname:
        print "You must specify the hostname parameter."
        sys.exit(1)

    cmd = ZenossZopeMonitorPlugin(options.hostname, options.port,
                                  options.ipAddress,options.uri,
                                  options.useSsl,options.authentication)

    try:
        result = cmd.run()
    except urllib2.HTTPError:
        print 'HTTP Error'
        sys.exit(1)

    if result:
        print result
        sys.exit(0)
    else:
        sys.exit(1)
