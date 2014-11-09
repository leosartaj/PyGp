#!/usr/bin/env python2

##
# PyGp
# https://github.com/leosartaj/PyGp.git
#
# Copyright (c) 2014 Sartaj Singh
# Licensed under the MIT license.
##

# system imports
import sys

# twisted imports
from twisted.internet import gtk2reactor
gtk2reactor.install() # install reactor for gui
from twisted.internet import reactor
from twisted.python import log
from twisted.internet import defer

# protocol
from protocol.ChatClientFactory import ChatClientFactory
from protocol.ChatClientProtocol import ChatClientProtocol

# Other imports
from defer import * # import all the callbacks and errbacks
from options import parse_args

def start_factory(options):
    """
    Starts the factory
    """
    deferred = defer.Deferred()
    factory = ChatClientFactory(options.name, deferred) # setting up the factory
    factory.protocol = ChatClientProtocol
    reactor.connectTCP(HOST, options.port, factory)
    return deferred

if __name__ == '__main__':
    options, HOST = parse_args() # parse the arguments

    # setup the factory
    deferred = start_factory(options)
    deferred.addBoth(stop_log) 
    deferred.addBoth(stop_reactor) 

    log.startLogging(sys.stdout)  # Start Logging
    #clientGUIClass('gui/clientGUI.glade', factory) # start the GUI interface

    reactor.run()