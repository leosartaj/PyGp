#!/usr/bin/env python2

##
# PyChat
# https://github.com/leosartaj/PyChat.git
#
# Copyright (c) 2014 Sartaj Singh
# Licensed under the MIT license.
##

from twisted.protocols import basic
from twisted.internet import defer, interfaces
from zope.interface import implements 

def filterArgs(func):
    """
    Decorator to call only call function with the first argument passed
    """
    def _wrapper(*args, **kwargs):
        func(args[0])
    return _wrapper

class FileSender(object):
    """
    Sends a file
    """
    implements(interfaces.IPushProducer)

    CHUNK_SIZE = 2 ** 14 - 384

    lastSent = ''
    deferred = None

    def beginFileTransfer(self, fName, consumer, transform=None):
        """
        Starts file transfer of a file
        """
        self.file = open(fName, 'rb')
        self.consumer = consumer
        self.transform = transform
        self._paused = False
        self.consumer.registerProducer(self, streaming=True) # register for streaming
        self.resume = defer.Deferred()
        self.resume.addCallback(self.resumeProducing)
        self.deferred = defer.Deferred()
        return (self.deferred, self.resume)

    @filterArgs
    def resumeProducing(self):
        """
        Sends a chunk to the server
        """
        self._paused = False
        chunk = ''
        if self.file:
            chunk = self.file.read(self.CHUNK_SIZE)
        if not chunk:
            self._cleanup()
            self._complete()
            return
        if self.transform: # if transform function is defined
            chunk = self.transform(chunk)
        self.consumer.write(chunk)
        self.lastSent = chunk[-1:]
        if not self._paused:
            self.resume.addCallback(self.resumeProducing)

    def _cleanup(self):
        """
        Cleans up everything
        """
        if self.file:
            self.file.close()
            self.file = None
        self.consumer.unregisterProducer()

    def _complete(self):
        """
        Completes the file transfer process
        """
        if self.deferred:
            deferred, self.deferred = self.deferred, None
            deferred.callback(self.lastSent)

    def pauseProducing(self):
        self._paused = True

    def stopProducing(self):
        self._cleanup()
        if self.deferred:
            self.deferred.errback(Exception("File transfer stopped"))
            self.deferred = None
