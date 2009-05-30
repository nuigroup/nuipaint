from __future__ import with_statement
from pymt import *
from core.toolbar import *

if __name__ == '__main__':
    w = MTWindow()
    tb = toolbar()
    w.add_widget(tb)
    icon1 = MTImageButton(filename='gfx/icons/undo.png')
    icon2 = MTImageButton(filename='gfx/icons/undo.png')
    icon3 = MTImageButton(filename='gfx/icons/undo.png')
    icon4 = MTImageButton(filename='gfx/icons/undo.png')
    icon5 = MTImageButton(filename='gfx/icons/undo.png')
    icon6 = MTImageButton(filename='gfx/icons/undo.png')
    icon7 = MTImageButton(filename='gfx/icons/undo.png')
    icon8 = MTImageButton(filename='gfx/icons/undo.png')
    icon9 = MTImageButton(filename='gfx/icons/undo.png')
    tb.add_widget(icon1)
    tb.add_widget(icon2)
    tb.add_widget(icon3)
    tb.add_widget(icon4)
    tb.add_widget(icon5)
    tb.add_widget(icon6)
    tb.add_widget(icon7)
    tb.add_widget(icon8)
    tb.add_widget(icon9)
    runTouchApp()