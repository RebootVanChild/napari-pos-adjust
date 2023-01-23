"""
This module is an example of a barebones QWidget plugin for napari

It implements the Widget specification.
see: https://napari.org/stable/plugins/guides.html?#widgets

Replace code below according to your needs.
"""
from typing import TYPE_CHECKING

import numpy as np
from qtpy.QtCore import Qt
from qtpy.QtWidgets import QHBoxLayout, QSlider, QWidget

if TYPE_CHECKING:
    pass


class Widget(QWidget):
    # your QWidget.__init__ can optionally request the napari viewer instance
    # in one of two ways:
    # 1. use a parameter called `napari_viewer`, as done here
    # 2. use a type annotation of 'napari.viewer.Viewer' for any parameter
    affine_matrix = np.array(
        [[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]]
    )

    def __init__(self, napari_viewer):
        super().__init__()
        self.viewer = napari_viewer
        # buttons
        # self.btn = QPushButton("Click me!")
        # self.btn.clicked.connect(self._on_click)
        # Translation sliders
        self.sl_translate_x = QSlider(Qt.Horizontal)
        self.sl_translate_x.setMinimum(-5000)
        self.sl_translate_x.setMaximum(5000)
        self.sl_translate_x.setValue(0)
        self.sl_translate_x.valueChanged.connect(self.x_value_changed)
        self.sl_translate_y = QSlider(Qt.Horizontal)
        self.sl_translate_y.setMinimum(-5000)
        self.sl_translate_y.setMaximum(5000)
        self.sl_translate_y.setValue(0)
        self.sl_translate_y.valueChanged.connect(self.y_value_changed)
        self.sl_translate_z = QSlider(Qt.Horizontal)
        self.sl_translate_z.setMinimum(-2500)
        self.sl_translate_z.setMaximum(2500)
        self.sl_translate_z.setValue(0)
        self.sl_translate_z.valueChanged.connect(self.z_value_changed)

        self.setLayout(QHBoxLayout())
        # self.layout().addWidget(self.btn)
        self.layout().addWidget(self.sl_translate_x)

    # def _on_click(self):
    #     print("napari has", len(self.viewer.layers), "layers")
    #     print("test")
    #     print("layer translate:", self.viewer.layers["0"].translate)
    #     translate_val = self.viewer.layers["0"].translate
    #     translate_val[2] = 1000
    #     self.viewer.layers["0"].translate = translate_val

    def x_value_changed(self):
        self.affine_matrix[2][3] = self.sl_translate_x.value()
        # self.viewer.layers["0"].translate =
        # [0, 0, self.sl_translate_x.value()]
        self.viewer.layers["0"].affine = self.affine_matrix

    def y_value_changed(self):
        self.affine_matrix[1][3] = self.sl_translate_y.value()
        # self.viewer.layers["0"].translate =
        # [0, 0, self.sl_translate_x.value()]
        self.viewer.layers["0"].affine = self.affine_matrix

    def z_value_changed(self):
        self.affine_matrix[0][3] = self.sl_translate_z.value()
        # self.viewer.layers["0"].translate =
        # [0, 0, self.sl_translate_x.value()]
        self.viewer.layers["0"].affine = self.affine_matrix
