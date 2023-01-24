"""
This module is an example of a barebones QWidget plugin for napari

It implements the Widget specification.
see: https://napari.org/stable/plugins/guides.html?#widgets

Replace code below according to your needs.
"""
from typing import TYPE_CHECKING

import numpy as np
from qtpy.QtCore import Qt
from qtpy.QtWidgets import QComboBox, QFormLayout, QSlider, QWidget

if TYPE_CHECKING:
    pass


class Widget(QWidget):
    affine_matrix = np.array(
        [[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]]
    )
    translation_x = 0
    translation_y = 0
    translation_z = 0
    rotation_x = 0
    rotation_y = 0
    rotation_z = 0
    image_center = np.array([0, 0, 0])

    def __init__(self, napari_viewer):
        super().__init__()
        self.viewer = napari_viewer
        # botton
        # self.btn = QPushButton()
        # self.btn.clicked.connect(self.btn_clicked)
        # Select tissue block to work on
        self.cb_tissue_block = QComboBox()
        self.cb_tissue_block.addItems(["A1", "A2", "A3", "A4"])
        self.cb_tissue_block.currentIndexChanged.connect(
            self.tissue_block_selection_changed
        )

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
        # layout.addRow("test:", self.btn)
        layout.addRow("tissue block:", self.cb_tissue_block)
        layout.addRow("translate x:", self.sl_translate_x)
        layout.addRow("translate y:", self.sl_translate_y)
        layout.addRow("translate z:", self.sl_translate_z)
        layout.addRow("rotate x:", self.sl_rotate_x)
        layout.addRow("rotate y:", self.sl_rotate_y)
        layout.addRow("rotate z:", self.sl_rotate_z)
        self.setLayout(layout)

    # def btn_clicked(self):
    #     self.viewer.open("F:/HT442PI/visualization/442PI-A1-5x-small.czi")

    def tissue_block_selection_changed(self, index):
        print(index, self.cb_tissue_block.currentText())

    def translate_x_value_changed(self):
        self.translation_x = self.sl_translate_x.value()
        self.calculate_and_set_affine()

    def translate_y_value_changed(self):
        self.translation_y = self.sl_translate_y.value()
        self.calculate_and_set_affine()

    def translate_z_value_changed(self):
        self.translation_z = self.sl_translate_z.value()
        self.calculate_and_set_affine()

    def rotate_x_value_changed(self):
        self.rotation_x = np.deg2rad(self.sl_rotate_x.value())
        self.calculate_and_set_affine()

    def rotate_y_value_changed(self):
        self.rotation_y = np.deg2rad(self.sl_rotate_y.value())
        self.calculate_and_set_affine()

    def rotate_z_value_changed(self):
        self.rotation_z = np.deg2rad(self.sl_rotate_z.value())
        self.calculate_and_set_affine()

    def calculate_and_set_affine(self):
        self.image_center = (
            np.array(self.viewer.layers["0"].extent[0][1])
            * np.array(self.viewer.layers["0"].extent[2])
            / 2
        )
        rot_mat_x = np.array(
            [
                [np.cos(self.rotation_x), np.sin(self.rotation_x), 0],
                [-np.sin(self.rotation_x), np.cos(self.rotation_x), 0],
                [0, 0, 1],
            ]
        )
        rot_mat_y = np.array(
            [
                [np.cos(self.rotation_y), 0, np.sin(self.rotation_y)],
                [0, 1, 0],
                [-np.sin(self.rotation_y), 0, np.cos(self.rotation_y)],
            ]
        )
        rot_mat_z = np.array(
            [
                [1, 0, 0],
                [0, np.cos(self.rotation_z), np.sin(self.rotation_z)],
                [0, -np.sin(self.rotation_z), np.cos(self.rotation_z)],
            ]
        )
        rot_mat = rot_mat_x.dot(rot_mat_y).dot(rot_mat_z)
        translate_arr = (
            -rot_mat.dot(self.image_center.T)
            + self.image_center
            + np.array(
                [self.translation_z, self.translation_y, self.translation_x]
            )
        )
        self.affine_matrix = np.append(
            np.hstack((rot_mat, translate_arr[..., None])),
            [[0, 0, 0, 1]],
            axis=0,
        )
        self.viewer.layers["0"].affine = self.affine_matrix
