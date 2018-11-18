#!/usr/bin/python3
# -*- coding: utf-8 -*-

import gi
gi.require_version("Gtk", "3.0")

from gi.repository import Gtk


class BarraProgreso(Gtk.EventBox):

    def __init__(self):

        Gtk.EventBox.__init__(self)

        self.escala = Gtk.Scale(orientation=Gtk.Orientation.HORIZONTAL)
        self.escala.set_adjustment(Gtk.Adjustment(0.0, 0.0, 256.0, 0.1, 1.0, 1.0))
        self.escala.set_digits(0)
        self.escala.set_draw_value(True)

        self.add(self.escala)
        self.show_all()

        # NOTA: Necesario para que funcione la escala
        self.set_size_request(-1, 24)
        