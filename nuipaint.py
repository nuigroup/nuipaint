from __future__ import with_statement
from pymt import *
from core.toolbar import *

if __name__ == '__main__':
    w = MTWindow()
    tb = toolbar(win=w)
    w.add_widget(tb)    
    runTouchApp()