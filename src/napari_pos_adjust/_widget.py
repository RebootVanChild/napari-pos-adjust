"""
This module is an example of a barebones QWidget plugin for napari

It implements the Widget specification.
see: https://napari.org/stable/plugins/guides.html?#widgets

Replace code below according to your needs.
"""
from typing import TYPE_CHECKING

import numpy as np
from qtpy.QtCore import Qt
from qtpy.QtWidgets import QFormLayout, QSlider, QWidget

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
    translate_x = 0
    translate_y = 0
    translate_z = 0
    rotation_x = 0
    rotation_y = 0
    rotation_z = 0

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
        self.sl_translate_x.valueChanged.connect(
            self.translate_x_value_changed
        )
        self.sl_translate_y = QSlider(Qt.Horizontal)
        self.sl_translate_y.setMinimum(-5000)
        self.sl_translate_y.setMaximum(5000)
        self.sl_translate_y.setValue(0)
        self.sl_translate_y.valueChanged.connect(
            self.translate_y_value_changed
        )
        self.sl_translate_z = QSlider(Qt.Horizontal)
        self.sl_translate_z.setMinimum(-2500)
        self.sl_translate_z.setMaximum(2500)
        self.sl_translate_z.setValue(0)
        self.sl_translate_z.valueChanged.connect(
            self.translate_z_value_changed
        )
        # Rotation sliders
        self.sl_rotate_x = QSlider(Qt.Horizontal)
        self.sl_rotate_x.setMinimum(-180)
        self.sl_rotate_x.setMaximum(180)
        self.sl_rotate_x.setValue(0)
        self.sl_rotate_x.valueChanged.connect(self.rotate_x_value_changed)
        self.sl_rotate_y = QSlider(Qt.Horizontal)
        self.sl_rotate_y.setMinimum(-180)
        self.sl_rotate_y.setMaximum(180)
        self.sl_rotate_y.setValue(0)
        self.sl_rotate_y.valueChanged.connect(self.rotate_y_value_changed)
        self.sl_rotate_z = QSlider(Qt.Horizontal)
        self.sl_rotate_z.setMinimum(-180)
        self.sl_rotate_z.setMaximum(180)
        self.sl_rotate_z.setValue(0)
        self.sl_rotate_z.valueChanged.connect(self.rotate_z_value_changed)

        layout = QFormLayout()
        layout.addRow("translate x:", self.sl_translate_x)
        layout.addRow("translate y:", self.sl_translate_y)
        layout.addRow("translate z:", self.sl_translate_z)
        layout.addRow("rotate x:", self.sl_rotate_x)
        layout.addRow("rotate y:", self.sl_rotate_y)
        layout.addRow("rotate z:", self.sl_rotate_z)
        self.setLayout(layout)
        # self.layout().addWidget(self.btn)
        # self.layout().addWidget(self.sl_translate_x)
        # self.layout().addWidget(self.sl_translate_y)
        # self.layout().addWidget(self.sl_translate_z)

    # def _on_click(self):
    #     print("napari has", len(self.viewer.layers), "layers")
    #     print("test")
    #     print("layer translate:", self.viewer.layers["0"].translate)
    #     translate_val = self.viewer.layers["0"].translate
    #     translate_val[2] = 1000
    #     self.viewer.layers["0"].translate = translate_val

    def translate_x_value_changed(self):
        self.affine_matrix[2][3] = self.sl_translate_x.value()
        self.viewer.layers["0"].affine = self.affine_matrix
        print(self.viewer.layers["0"].extent["data"][1][2])
        print(self.viewer.layers["0"].extent["step"][2])

    def translate_y_value_changed(self):
        self.affine_matrix[1][3] = self.sl_translate_y.value()
        self.viewer.layers["0"].affine = self.affine_matrix

    def translate_z_value_changed(self):
        self.affine_matrix[0][3] = self.sl_translate_z.value()
        self.viewer.layers["0"].affine = self.affine_matrix

    def rotate_x_value_changed(self):
        # TODO
        return

    def rotate_y_value_changed(self):
        # TODO
        return

    def rotate_z_value_changed(self):
        # TODO
        return

    def calculate_affine(self):
        # rot_mat_x = np.array(
        #     [
        #         [np.cos(self.rotation_x), np.sin(self.rotation_x), 0],
        #         [-np.sin(self.rotation_x), np.cos(self.rotation_x), 0],
        #         [0, 0, 1],
        #     ]
        # )
        # rot_mat_y = np.array(
        #     [
        #         [np.cos(self.rotation_y), 0, np.sin(self.rotation_y)],
        #         [0, 1, 0],
        #         [-np.sin(self.rotation_y), 0, np.cos(self.rotation_y)],
        #     ]
        # )
        # rot_mat_z = np.array(
        #     [
        #         [1, 0, 0],
        #         [0, np.cos(self.rotation_z), np.sin(self.rotation_z)],
        #         [0, -np.sin(self.rotation_z), np.cos(self.rotation_z)],
        #     ]
        # )
        return
