#!/usr/bin/python3
# -*- coding: utf-8 -*-

import gi
gi.require_version("Gtk", "3.0")

from gi.repository import Gtk
from gi.repository import Gdk

from BarraProgreso import BarraProgreso


class ColorTable(Gtk.Table):

    def __init__(self):
        Gtk.Table.__init__(self, rows=3, columns=14, homogeneous=True)

        self.redScale = BarraProgreso()
        self.redScale.escala.set_value(0)
        self.redimg = Gtk.Image()
        self.redimg.get_style_context().add_class("miniview")
        self.redimg.modify_bg(0, Gdk.Color(0,0,0))
        self.attach(self.redScale, 0, 7, 0, 1)
        self.attach(self.redimg, 7, 8, 0, 1)

        self.greenScale = BarraProgreso()
        self.greenScale.escala.set_value(0)
        self.greenimg = Gtk.Image()
        self.greenimg.get_style_context().add_class("miniview")
        self.greenimg.modify_bg(0, Gdk.Color(0,0,0))
        self.attach(self.greenScale, 0, 7, 1, 2)
        self.attach(self.greenimg, 7, 8, 1, 2)

        self.blueScale = BarraProgreso()
        self.blueScale.escala.set_value(0)
        self.blueimg = Gtk.Image()
        self.blueimg.get_style_context().add_class("miniview")
        self.blueimg.modify_bg(0, Gdk.Color(0,0,0))
        self.attach(self.blueScale, 0, 7, 2, 3)
        self.attach(self.blueimg, 7, 8, 2, 3)

        self.img = Gtk.Image()
        self.img.get_style_context().add_class("miniview")
        self.img.modify_bg(0, Gdk.Color(0,0,0))
        self.attach(self.img, 8, 11, 0, 3)

        self.btn = Gtk.Button("Enviar")
        self.attach(self.btn, 11, 14, 0, 3)

        self.btnchk = Gtk.CheckButton("Monocromo")
        self.attach(self.btnchk, 1, 5, 3, 4)

        self.show_all()
