#!/usr/bin/env python2

##
# PyChat
# https://github.com/leosartaj/PyChat.git
# Copyright (c) 2014 Sartaj Singh
# Licensed under the MIT license.
##

"""
Contains Helper functions
"""

import os
import gtk

def find_file(dire, fName):
    """
    Finds file in the given directory
    returns the complete path
    """
    path = os.path.join(os.path.dirname(dire), fName)
    return path

def center(widget, parent):
    """
    Centers the window to the
    location of open instance of
    parent window
    """
    widget.set_transient_for(parent) # set parent
    widget.set_position(gtk.WIN_POS_CENTER_ON_PARENT)