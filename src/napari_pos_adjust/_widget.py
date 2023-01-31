"""
This module is an example of a barebones QWidget plugin for napari

It implements the Widget specification.
see: https://napari.org/stable/plugins/guides.html?#widgets

Replace code below according to your needs.
"""
from typing import TYPE_CHECKING

import numpy as np
from qtpy.QtCore import Qt
from qtpy.QtWidgets import (
    QComboBox,
    QFileDialog,
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
    tissue_block_dict = {}

    def __init__(self, napari_viewer):
        super().__init__()
        self.viewer = napari_viewer
        # transformation file path text box
        self.tb_trans_file_path = QLineEdit(self)
        # transformation file browse button
        self.btn_browse_trans_file = QPushButton("browse", self)
        # transformation file apply button
        self.btn_apply_trans_file = QPushButton("apply", self)
        # Select tissue block to work on
        self.cb_tissue_block = QComboBox()
        self.cb_tissue_block.currentTextChanged.connect(
            self.tissue_block_selection_changed
        )
        # button save transformation to file
        self.btn_save_transformation = QPushButton(
            "save transformation to file", self
        )
        self.btn_save_transformation.clicked.connect(
            self.transformation_save_to_file
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

        for x in self.viewer.layers:
            self.tissue_block_dict[x.name] = {
                "image_center": np.array(
                    self.viewer.layers[x.name].extent[0][1]
                )
                * np.array(self.viewer.layers[x.name].extent[2])
                / 2,
                "translation": [0, 0, 0],
                "rotation": [0, 0, 0],
            }
            self.cb_tissue_block.addItem(x.name)

        layout = QFormLayout()
        layout.addRow("tissue block:", self.cb_tissue_block)
        hbox_load_file = QHBoxLayout()
        hbox_load_file.addWidget(self.tb_trans_file_path)
        hbox_load_file.addWidget(self.btn_browse_trans_file)
        layout.addRow(hbox_load_file)
        layout.addRow(self.btn_apply_trans_file)
        layout.addRow("translate x:", self.sl_translate_x)
        layout.addRow("translate y:", self.sl_translate_y)
        layout.addRow("translate z:", self.sl_translate_z)
        layout.addRow("rotate x:", self.sl_rotate_x)
        layout.addRow("rotate y:", self.sl_rotate_y)
        layout.addRow("rotate z:", self.sl_rotate_z)
        layout.addRow(self.btn_save_transformation)
        self.setLayout(layout)

    def tissue_block_selection_changed(self, name):
        # block signals: not to trigger valueChanged()
        self.sl_translate_x.blockSignals(True)
        self.sl_translate_y.blockSignals(True)
        self.sl_translate_z.blockSignals(True)
        self.sl_rotate_x.blockSignals(True)
        self.sl_rotate_y.blockSignals(True)
        self.sl_rotate_z.blockSignals(True)
        self.sl_translate_x.setValue(
            self.tissue_block_dict[name]["translation"][0]
        )
        self.sl_translate_y.setValue(
            self.tissue_block_dict[name]["translation"][1]
        )
        self.sl_translate_z.setValue(
            self.tissue_block_dict[name]["translation"][2]
        )
        self.sl_rotate_x.setValue(self.tissue_block_dict[name]["rotation"][0])
        self.sl_rotate_y.setValue(self.tissue_block_dict[name]["rotation"][1])
        self.sl_rotate_z.setValue(self.tissue_block_dict[name]["rotation"][2])
        self.sl_translate_x.blockSignals(False)
        self.sl_translate_y.blockSignals(False)
        self.sl_translate_z.blockSignals(False)
        self.sl_rotate_x.blockSignals(False)
        self.sl_rotate_y.blockSignals(False)
        self.sl_rotate_z.blockSignals(False)

    def translate_x_value_changed(self):
        self.tissue_block_dict[self.cb_tissue_block.currentText()][
            "translation"
        ][0] = self.sl_translate_x.value()
        self.calculate_and_set_affine()

    def translate_y_value_changed(self):
        self.tissue_block_dict[self.cb_tissue_block.currentText()][
            "translation"
        ][1] = self.sl_translate_y.value()
        self.calculate_and_set_affine()

    def translate_z_value_changed(self):
        self.tissue_block_dict[self.cb_tissue_block.currentText()][
            "translation"
        ][2] = self.sl_translate_z.value()
        self.calculate_and_set_affine()

    def rotate_x_value_changed(self):
        self.tissue_block_dict[self.cb_tissue_block.currentText()]["rotation"][
            0
        ] = self.sl_rotate_x.value()
        self.calculate_and_set_affine()

    def rotate_y_value_changed(self):
        self.tissue_block_dict[self.cb_tissue_block.currentText()]["rotation"][
            1
        ] = self.sl_rotate_y.value()
        self.calculate_and_set_affine()

    def rotate_z_value_changed(self):
        self.tissue_block_dict[self.cb_tissue_block.currentText()]["rotation"][
            2
        ] = self.sl_rotate_z.value()
        self.calculate_and_set_affine()

    def calculate_and_set_affine(self):
        # get dimensions and pixel size to find center (in microns)
        rot_mat_x = np.array(
            [
                [
                    np.cos(
                        np.deg2rad(
                            self.tissue_block_dict[
                                self.cb_tissue_block.currentText()
                            ]["rotation"][0]
                        )
                    ),
                    np.sin(
                        np.deg2rad(
                            self.tissue_block_dict[
                                self.cb_tissue_block.currentText()
                            ]["rotation"][0]
                        )
                    ),
                    0,
                ],
                [
                    -np.sin(
                        np.deg2rad(
                            self.tissue_block_dict[
                                self.cb_tissue_block.currentText()
                            ]["rotation"][0]
                        )
                    ),
                    np.cos(
                        np.deg2rad(
                            self.tissue_block_dict[
                                self.cb_tissue_block.currentText()
                            ]["rotation"][0]
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
                            self.tissue_block_dict[
                                self.cb_tissue_block.currentText()
                            ]["rotation"][1]
                        )
                    ),
                    0,
                    np.sin(
                        np.deg2rad(
                            self.tissue_block_dict[
                                self.cb_tissue_block.currentText()
                            ]["rotation"][1]
                        )
                    ),
                ],
                [0, 1, 0],
                [
                    -np.sin(
                        np.deg2rad(
                            self.tissue_block_dict[
                                self.cb_tissue_block.currentText()
                            ]["rotation"][1]
                        )
                    ),
                    0,
                    np.cos(
                        np.deg2rad(
                            self.tissue_block_dict[
                                self.cb_tissue_block.currentText()
                            ]["rotation"][1]
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
                            self.tissue_block_dict[
                                self.cb_tissue_block.currentText()
                            ]["rotation"][2]
                        )
                    ),
                    np.sin(
                        np.deg2rad(
                            self.tissue_block_dict[
                                self.cb_tissue_block.currentText()
                            ]["rotation"][2]
                        )
                    ),
                ],
                [
                    0,
                    -np.sin(
                        np.deg2rad(
                            self.tissue_block_dict[
                                self.cb_tissue_block.currentText()
                            ]["rotation"][2]
                        )
                    ),
                    np.cos(
                        np.deg2rad(
                            self.tissue_block_dict[
                                self.cb_tissue_block.currentText()
                            ]["rotation"][2]
                        )
                    ),
                ],
            ]
        )
        rot_mat = rot_mat_x.dot(rot_mat_y).dot(rot_mat_z)
        translate_arr = (
            -rot_mat.dot(
                self.tissue_block_dict[self.cb_tissue_block.currentText()][
                    "image_center"
                ].T
            )
            + self.tissue_block_dict[self.cb_tissue_block.currentText()][
                "image_center"
            ]
            + np.array(
                [
                    self.tissue_block_dict[self.cb_tissue_block.currentText()][
                        "translation"
                    ][2],
                    self.tissue_block_dict[self.cb_tissue_block.currentText()][
                        "translation"
                    ][1],
                    self.tissue_block_dict[self.cb_tissue_block.currentText()][
                        "translation"
                    ][0],
                ]
            )
        )
        affine_matrix = np.append(
            np.hstack((rot_mat, translate_arr[..., None])),
            [[0, 0, 0, 1]],
            axis=0,
        )
        self.viewer.layers[
            self.cb_tissue_block.currentText()
        ].affine = affine_matrix

    def transformation_save_to_file(self):
        fileName, _ = QFileDialog.getSaveFileName(
            self, "Save Transformation", "", "CSV Files (*.csv)"
        )
        file = open(fileName, "w")
        info = self.tissue_block_dict[self.cb_tissue_block.currentText()]
        text = (
            str(info["translation"][0])
            + str(info["translation"][1])
            + str(info["translation"][2])
            + "\n"
            + str(info["rotation"][0])
            + str(info["rotation"][1])
            + str(info["rotation"][2])
        )
        file.write(text)
        file.close()
