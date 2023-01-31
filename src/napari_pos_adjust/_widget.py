"""
This module is an example of a barebones QWidget plugin for napari

It implements the Widget specification.
see: https://napari.org/stable/plugins/guides.html?#widgets

Replace code below according to your needs.
"""
from typing import TYPE_CHECKING

import napari
import napari.layers
import numpy as np
from qtpy.QtCore import Qt
from qtpy.QtWidgets import (
    QComboBox,
    QFormLayout,
    QHBoxLayout,
    QLineEdit,
    QPushButton,
    QSlider,
    QWidget,
)

if TYPE_CHECKING:
    pass


class Widget(QWidget):
    tissue_block_names = ["A1.czi", "A2.czi", "A3.czi", "A4.czi"]
    # the selected tissue block's index now
    current_tissue_block_index = 0
    # each parameter is a array of size 4 (blocks)
    affine_matrix = [
        np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]]),
        np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]]),
        np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]]),
        np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]]),
    ]
    translation_x = [0, 0, 0, 0]
    translation_y = [0, 0, 0, 0]
    translation_z = [0, 0, 0, 0]
    rotation_x = [0, 0, 0, 0]
    rotation_y = [0, 0, 0, 0]
    rotation_z = [0, 0, 0, 0]

    # image_center = [
    # np.array([0, 0, 0]),
    # np.array([0, 0, 0]),
    # np.array([0, 0, 0]),
    # np.array([0, 0, 0])]

    def __init__(self, napari_viewer):
        super().__init__()
        self.viewer = napari_viewer
        print(self.viewer.layers)
        print(napari.layers)
        # transformation file path text box
        self.tb_trans_file_path = QLineEdit(self)
        # transformation file browse button
        self.btn_browse_trans_file = QPushButton("browse", self)
        # transformation file apply button
        self.btn_apply_trans_file = QPushButton("apply", self)
        # Select tissue block to work on
        self.cb_tissue_block = QComboBox()
        self.cb_tissue_block.addItems(self.tissue_block_names)
        self.cb_tissue_block.currentIndexChanged.connect(
            self.tissue_block_selection_changed
        )
        # button save transformation to file
        self.btn_print_affine = QPushButton(
            "save transformation to file", self
        )
        self.btn_print_affine.clicked.connect(self.btn_print_affine_clicked)

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

        # self.image_select = create_widget(
        #     annotation=napari.layers.Image, label="image_layer"
        # )

        layout = QFormLayout()
        layout.addRow("tissue block:", self.cb_tissue_block)
        # hbox_layer_select = QHBoxLayout()
        # hbox_layer_select.addWidget(self.image_select.native)
        hbox_load_file = QHBoxLayout()
        hbox_load_file.addWidget(self.tb_trans_file_path)
        hbox_load_file.addWidget(self.btn_browse_trans_file)
        # layout.addRow("tissue block:", hbox_layer_select)
        layout.addRow(hbox_load_file)
        layout.addRow(self.btn_apply_trans_file)
        layout.addRow("translate x:", self.sl_translate_x)
        layout.addRow("translate y:", self.sl_translate_y)
        layout.addRow("translate z:", self.sl_translate_z)
        layout.addRow("rotate x:", self.sl_rotate_x)
        layout.addRow("rotate y:", self.sl_rotate_y)
        layout.addRow("rotate z:", self.sl_rotate_z)
        layout.addRow(self.btn_print_affine)
        self.setLayout(layout)

    def tissue_block_selection_changed(self, index):
        self.current_tissue_block_index = index
        # block signals: not to trigger valueChanged()
        self.sl_translate_x.blockSignals(True)
        self.sl_translate_y.blockSignals(True)
        self.sl_translate_z.blockSignals(True)
        self.sl_rotate_x.blockSignals(True)
        self.sl_rotate_y.blockSignals(True)
        self.sl_rotate_z.blockSignals(True)
        self.sl_translate_x.setValue(
            self.translation_x[self.current_tissue_block_index]
        )
        self.sl_translate_y.setValue(
            self.translation_y[self.current_tissue_block_index]
        )
        self.sl_translate_z.setValue(
            self.translation_z[self.current_tissue_block_index]
        )
        self.sl_rotate_x.setValue(
            self.rotation_x[self.current_tissue_block_index]
        )
        self.sl_rotate_y.setValue(
            self.rotation_y[self.current_tissue_block_index]
        )
        self.sl_rotate_z.setValue(
            self.rotation_z[self.current_tissue_block_index]
        )
        self.sl_translate_x.blockSignals(False)
        self.sl_translate_y.blockSignals(False)
        self.sl_translate_z.blockSignals(False)
        self.sl_rotate_x.blockSignals(False)
        self.sl_rotate_y.blockSignals(False)
        self.sl_rotate_z.blockSignals(False)

    def translate_x_value_changed(self):
        self.translation_x[
            self.current_tissue_block_index
        ] = self.sl_translate_x.value()
        self.calculate_and_set_affine()

    def translate_y_value_changed(self):
        self.translation_y[
            self.current_tissue_block_index
        ] = self.sl_translate_y.value()
        self.calculate_and_set_affine()

    def translate_z_value_changed(self):
        self.translation_z[
            self.current_tissue_block_index
        ] = self.sl_translate_z.value()
        self.calculate_and_set_affine()

    def rotate_x_value_changed(self):
        self.rotation_x[
            self.current_tissue_block_index
        ] = self.sl_rotate_x.value()
        self.calculate_and_set_affine()

    def rotate_y_value_changed(self):
        self.rotation_y[
            self.current_tissue_block_index
        ] = self.sl_rotate_y.value()
        self.calculate_and_set_affine()

    def rotate_z_value_changed(self):
        self.rotation_z[
            self.current_tissue_block_index
        ] = self.sl_rotate_z.value()
        self.calculate_and_set_affine()

    def calculate_and_set_affine(self):
        # get dimensions and pixel size to find center (in microns)
        image_center = (
            np.array(
                self.viewer.layers[
                    self.tissue_block_names[self.current_tissue_block_index]
                ].extent[0][1]
            )
            * np.array(
                self.viewer.layers[
                    self.tissue_block_names[self.current_tissue_block_index]
                ].extent[2]
            )
            / 2
        )
        rot_mat_x = np.array(
            [
                [
                    np.cos(
                        np.deg2rad(
                            self.rotation_x[self.current_tissue_block_index]
                        )
                    ),
                    np.sin(
                        np.deg2rad(
                            self.rotation_x[self.current_tissue_block_index]
                        )
                    ),
                    0,
                ],
                [
                    -np.sin(
                        np.deg2rad(
                            self.rotation_x[self.current_tissue_block_index]
                        )
                    ),
                    np.cos(
                        np.deg2rad(
                            self.rotation_x[self.current_tissue_block_index]
                        )
                    ),
                    0,
                ],
                [0, 0, 1],
            ]
        )
        rot_mat_y = np.array(
            [
                [
                    np.cos(
                        np.deg2rad(
                            self.rotation_y[self.current_tissue_block_index]
                        )
                    ),
                    0,
                    np.sin(
                        np.deg2rad(
                            self.rotation_y[self.current_tissue_block_index]
                        )
                    ),
                ],
                [0, 1, 0],
                [
                    -np.sin(
                        np.deg2rad(
                            self.rotation_y[self.current_tissue_block_index]
                        )
                    ),
                    0,
                    np.cos(
                        np.deg2rad(
                            self.rotation_y[self.current_tissue_block_index]
                        )
                    ),
                ],
            ]
        )
        rot_mat_z = np.array(
            [
                [1, 0, 0],
                [
                    0,
                    np.cos(
                        np.deg2rad(
                            self.rotation_z[self.current_tissue_block_index]
                        )
                    ),
                    np.sin(
                        np.deg2rad(
                            self.rotation_z[self.current_tissue_block_index]
                        )
                    ),
                ],
                [
                    0,
                    -np.sin(
                        np.deg2rad(
                            self.rotation_z[self.current_tissue_block_index]
                        )
                    ),
                    np.cos(
                        np.deg2rad(
                            self.rotation_z[self.current_tissue_block_index]
                        )
                    ),
                ],
            ]
        )
        rot_mat = rot_mat_x.dot(rot_mat_y).dot(rot_mat_z)
        translate_arr = (
            -rot_mat.dot(image_center.T)
            + image_center
            + np.array(
                [
                    self.translation_z[self.current_tissue_block_index],
                    self.translation_y[self.current_tissue_block_index],
                    self.translation_x[self.current_tissue_block_index],
                ]
            )
        )
        self.affine_matrix[self.current_tissue_block_index] = np.append(
            np.hstack((rot_mat, translate_arr[..., None])),
            [[0, 0, 0, 1]],
            axis=0,
        )
        self.viewer.layers[
            self.tissue_block_names[self.current_tissue_block_index]
        ].affine = self.affine_matrix[self.current_tissue_block_index]

    def btn_print_affine_clicked(self):
        print(self.affine_matrix[self.current_tissue_block_index])
        print(self.image_select)
        # self.viewer.open("F:/HT442PI/visualization/442PI-A1-5x-small.czi")
