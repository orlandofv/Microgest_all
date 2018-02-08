# -*- coding: latin-1 -*-
"""
Created on Fri Mar 02 23:18:43 2012

@author: lims
"""

from PyQt5.QtWidgets import QDoubleSpinBox
from PyQt5.QtCore import Qt


class price(QDoubleSpinBox):
    def __init__(self, parent=None):
        super(price, self).__init__(parent)

        self.setRange(0.0000, 999999999999.0000)
        self.setSingleStep(10.0000)
        self.setAlignment(Qt.AlignRight)
        self.setMaximumWidth(130)

    def focusInEvent(self, evt):
        self.selectAll()

