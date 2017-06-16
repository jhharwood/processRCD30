# ****************************************************************************
#
# NAME: J. Heath Harwood
# DATE: 21  April 2017
#
#
# DESCRIPTION:  This script
#
#
# DEPENDENCIES: Python Standard Library, lxml
#
# SOURCE(S):
#
##############################################################################

###>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>.IMPORT STATEMENTs.>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>###

import os, glob, sys, re
from lxml import etree
from xml.parsers.expat import ExpatError
import argparse
import easygui
from dialog import Dialog
from PySide import QtGui, QtCore
###>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>.MAIN.>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>###

def main():

    # Exception Handling
    try:
        app = QtGui.QApplication(sys.argv)
        dialog = Dialog()
        dialog.show()
        sys.exit(app.exec_())

    except NameError:
        print("Name Error:", sys.exc_info()[1])
    except SystemExit:
        print("Closing Window...")
    except Exception:
        print(sys.exc_info()[1])

if __name__ == "__main__":
    main()

