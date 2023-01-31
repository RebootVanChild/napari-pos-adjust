"""
This module is an example of a barebones QWidget plugin for napari

It implements the Widget specification.
see: https://napari.org/stable/plugins/guides.html?#widgets

Replace code below according to your needs.
"""
from pathlib import Path
from typing import TYPE_CHECKING, Sequence

import napari.layers
import numpy as np
from magicgui import magic_factory
from magicgui.widgets import create_widget
from napari import Viewer
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

        layout = QFormLayout()
        layout.addRow("tissue block:", self.cb_tissue_block)
        hbox_load_file = QHBoxLayout()
        hbox_load_file.addWidget(self.tb_trans_file_path)
        hbox_load_file.addWidget(self.btn_browse_trans_file)

        image_select = create_widget(
            annotation=napari.layers.Image, label="image_layer"
        )
        hbox_load_file.addWidget(image_select.native)

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
        # self.viewer.open("F:/HT442PI/visualization/442PI-A1-5x-small.czi")


# landmarks file has coordinates in microns,
# while Napari takes in transformation matrix in pixels.
# landmarks file in xyz order,
# while Napari takes in transformation matrix in zyx order.
def Matrix_to_napari_affine_input(
    matrix, source_physical_pixel_sizes, target_physical_pixel_sizes
):
    # convert unit: microns to pixels
    support_matrix = [
        [
            source_physical_pixel_sizes.X / target_physical_pixel_sizes.X,
            source_physical_pixel_sizes.Y / target_physical_pixel_sizes.Y,
            source_physical_pixel_sizes.Z / target_physical_pixel_sizes.Z,
            1 / target_physical_pixel_sizes.X,
        ],
        [
            source_physical_pixel_sizes.X / target_physical_pixel_sizes.X,
            source_physical_pixel_sizes.Y / target_physical_pixel_sizes.Y,
            source_physical_pixel_sizes.Z / target_physical_pixel_sizes.Z,
            1 / target_physical_pixel_sizes.Y,
        ],
        [
            source_physical_pixel_sizes.X / target_physical_pixel_sizes.X,
            source_physical_pixel_sizes.Y / target_physical_pixel_sizes.Y,
            source_physical_pixel_sizes.Z / target_physical_pixel_sizes.Z,
            1 / target_physical_pixel_sizes.Z,
        ],
        [1, 1, 1, 1],
    ]
    matrixXYZ = matrix * support_matrix
    # convert order: XYZ to ZYX
    matrixZYX = matrixXYZ
    matrixZYX[:3, :3] = np.rot90(matrixXYZ[:3, :3], 2)
    matrixZYX[:3, 3] = np.flip(matrixXYZ[:3, 3])
    return matrixZYX


# Input: landmarks pairs of source and target points.
# Output: 4x4 rigid body transformation matrix.
def GetRigidMatrixFromLandmarks(
    source_points_landmarks, target_points_landmarks
):
    centroid_source = np.mean(source_points_landmarks, axis=0)
    centroid_target = np.mean(target_points_landmarks, axis=0)
    P = source_points_landmarks - centroid_source
    Q = target_points_landmarks - centroid_target
    M = np.dot(P.T, Q)
    U, W, V = np.linalg.svd(M)
    R = np.dot(V.T, U.T)
    matrix = np.append(
        np.append(
            R,
            np.vstack(-np.dot(R, centroid_source.T) + centroid_target.T),
            axis=1,
        ),
        [[0.0, 0.0, 0.0, 1.0]],
        axis=0,
    )
    print(matrix)
    return matrix


# Input: landmarks pairs of source and target points.
# Output: 4x4 affine transformation matrix.
def GetAffineMatrixFromLandmarks(
    source_points_landmarks, target_points_landmarks
):
    pts_count = len(source_points_landmarks)
    A = np.zeros((pts_count * 3, 12))
    b = np.zeros(pts_count * 3)
    for i in range(pts_count):
        # build A
        A[i * 3][0] = source_points_landmarks[i][0]
        A[i * 3][1] = source_points_landmarks[i][1]
        A[i * 3][2] = source_points_landmarks[i][2]
        A[i * 3][3] = 1
        A[i * 3 + 1][4] = source_points_landmarks[i][0]
        A[i * 3 + 1][5] = source_points_landmarks[i][1]
        A[i * 3 + 1][6] = source_points_landmarks[i][2]
        A[i * 3 + 1][7] = 1
        A[i * 3 + 2][8] = source_points_landmarks[i][0]
        A[i * 3 + 2][9] = source_points_landmarks[i][1]
        A[i * 3 + 2][10] = source_points_landmarks[i][2]
        A[i * 3 + 2][11] = 1
        # build b
        b[i * 3] = target_points_landmarks[i, 0]
        b[i * 3 + 1] = target_points_landmarks[i, 1]
        b[i * 3 + 2] = target_points_landmarks[i, 2]
    x = np.linalg.solve(np.dot(A.T, A), np.dot(A.T, b.T))
    matrix = np.append(x.reshape(3, 4), [[0.0, 0.0, 0.0, 1.0]], axis=0)
    print(matrix)
    return matrix


@magic_factory(
    call_button="btn1",
    transformation_file={
        "label": "transformation file",
        "filter": "*.csv",
        "tooltip": "Select the transformation file",
    },
    translate_x_slider={
        "widget_type": "FloatSlider",
        "min": -5000,
        "max": 5000,
    },
    extra_button=dict(widget_type="PushButton"),
)
def example_magic_widget(
    viewer: Viewer,
    img: "napari.layers.Image",
    transformation_file: Sequence[Path],
    translate_x_slider=0,
):
    transformation_file_path = str(transformation_file[0])
    print(transformation_file_path)
