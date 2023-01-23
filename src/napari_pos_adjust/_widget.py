"""
This module is an example of a barebones QWidget plugin for napari

It implements the Widget specification.
see: https://napari.org/stable/plugins/guides.html?#widgets

Replace code below according to your needs.
"""
from typing import TYPE_CHECKING

from qtpy.QtCore import Qt
from qtpy.QtWidgets import QHBoxLayout, QPushButton, QSlider, QWidget

if TYPE_CHECKING:
    pass


class ExampleQWidget(QWidget):
    # your QWidget.__init__ can optionally request the napari viewer instance
    # in one of two ways:
    # 1. use a parameter called `napari_viewer`, as done here
    # 2. use a type annotation of 'napari.viewer.Viewer' for any parameter
    def __init__(self, napari_viewer):
        super().__init__()
        self.viewer = napari_viewer

        self.btn = QPushButton("Click me!")
        self.btn.clicked.connect(self._on_click)

        self.sl_translate_x = QSlider(Qt.Horizontal)
        self.sl_translate_x.setMinimum(-5000)
        self.sl_translate_x.setMaximum(5000)
        self.sl_translate_x.setValue(0)
        self.sl_translate_x.valueChanged.connect(self.value_changed)

        self.setLayout(QHBoxLayout())
        self.layout().addWidget(self.btn)
        self.layout().addWidget(self.sl_translate_x)

    def _on_click(self):
        print("napari has", len(self.viewer.layers), "layers")
        print("test")
        print("layer translate:", self.viewer.layers["0"].translate)
        translate_val = self.viewer.layers["0"].translate
        translate_val[2] = 1000
        self.viewer.layers["0"].translate = translate_val

    def value_changed(self):
        print("value changed", self.sl_translate_x.value())
        self.viewer.layers["0"].translate = [0, 0, self.sl_translate_x.value()]
        # if self.timer_id != -1:
        #     self.killTimer(self.timer_id)
        #
        # self.timer_id = self.startTimer(3000)
