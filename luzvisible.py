#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import serial
import sys

import gi
gi.require_version("Gtk", "3.0")

from gi.repository import Gtk
from gi.repository import GLib
from gi.repository import Gdk

from ColorTable import ColorTable

BASE_PATH = os.path.dirname(__file__)

screen = Gdk.Screen.get_default()
css_provider = Gtk.CssProvider()
style_path = os.path.join(BASE_PATH, "Estilo.css")
css_provider.load_from_path(style_path)
context = Gtk.StyleContext()
context.add_provider_for_screen(screen, css_provider, Gtk.STYLE_PROVIDER_PRIORITY_SETTINGS)

'''
KY-016 RGB FULL COLOR LED MODULE: https://arduinomodules.info/ky-016-rgb-full-color-led-module/
'''

class Ventana(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self)

        #self.set_icon_from_file(os.path.join(BASE_PATH, "Iconos", "?.svg"))
        self.set_title("Luz Visible")
        self.set_resizable(True)
        self.set_position(Gtk.WindowPosition.CENTER)
        self.set_size_request(640, 480)

        self.arduino = None
        self.color = {"RED": 0, "GREEN": 0, "BLUE": 0}

        try:
            self.arduino = serial.Serial('/dev/ttyUSB0', 9600, timeout=0.1)
            self.arduino.flushInput()
        except:
            pass

        vbox = Gtk.VBox()
        vbox.get_style_context().add_class("boxcontainer")

        self.tabla = ColorTable()
        
        vbox.pack_start(self.tabla, False, False, 3)

        self.label = Gtk.Label("...")
        vbox.pack_start(self.label, False, False, 3)

        image = Gtk.Image().new_from_file("Electromagnetic_spectrum-es.png")
        vbox.pack_start(image, False, False, 3)

        self.add(vbox)
        self.show_all()

        self.tabla.btn.connect("clicked", self.__send)
        self.tabla.redScale.escala.connect("change-value", self.__moveSlider, "RED")
        self.tabla.greenScale.escala.connect("change-value", self.__moveSlider, "GREEN")
        self.tabla.blueScale.escala.connect("change-value", self.__moveSlider, "BLUE")
        #self.tabla.btnchk.connect("toggled", self.__togledButton)

        self.connect("delete-event", self.__exit)

        #GLib.timeout_add(200, self.update)

    #def __togledButton(self, button):
    #    print(button, button.get_active())

    def __moveSlider(self, widget, scroll, value, color):
        ret = value
        if value < 0.0:
            ret = 0.0
            adj = widget.get_adjustment()
            GLib.idle_add(adj.set_value, ret)
        elif value > 255.0:
            ret = 255.0
            adj = widget.get_adjustment()
            GLib.idle_add(adj.set_value, ret)

        if self.tabla.btnchk.get_active():
            for key in self.color.keys():
                self.color[key] = int(ret)
                self.__paintMiniPreview(ret, key)
            for scale in [self.tabla.redScale.escala, self.tabla.greenScale.escala, self.tabla.blueScale.escala]:
                if scale != widget:
                    adj = scale.get_adjustment()
                    GLib.idle_add(adj.set_value, ret)
        else:
            self.color[color] = int(ret)
            self.__paintMiniPreview(ret, color)
    
        self.__paintMiniPreview2()

    def __paintMiniPreview(self, ret, canal):
        col = 100*ret/255
        col = 65535*col/100
        if canal == "RED":
            self.tabla.redimg.modify_bg(0, Gdk.Color(col,0,0))
        elif canal == "GREEN":
            self.tabla.greenimg.modify_bg(0, Gdk.Color(0,col,0))
        elif canal == "BLUE":
            self.tabla.blueimg.modify_bg(0, Gdk.Color(0,0,col))
    
    def __paintMiniPreview2(self):
        ret = self.color["RED"]
        col = 100*ret/255
        r = 65535*col/100
        ret = self.color["GREEN"]
        col = 100*ret/255
        g = 65535*col/100
        ret = self.color["BLUE"]
        col = 100*ret/255
        b = 65535*col/100
        self.tabla.img.modify_bg(0, Gdk.Color(r,g,b))

    def __send(self, widget):
        try:
            r = "{:3d}".format(self.color["RED"]).replace(" ", "0")
            g = "{:3d}".format(self.color["GREEN"]).replace(" ", "0")
            b = "{:3d}".format(self.color["BLUE"]).replace(" ", "0")
            self.arduino.write("r:%s g:%s b:%s" % (r,g,b))
            self.arduino.flush()
        except:
            print("Los colores no pudieron enviarse")

    def __exit(self, widget=False, event=False):
        try:
            self.arduino.write("r:%s g:%s b:%s" % (0,0,0))
            self.arduino.close()
        except:
            print("No se pudo cerrar el puerto")
        Gtk.main_quit()
        sys.exit(0)

    '''def update(self):
        try:
            texto = self.arduino.readline().strip().replace("\n", "")
            if texto: self.label.set_text(texto)
        except:
            print("No se pudo leer en el serial")
        return True'''


if __name__=="__main__":
    Ventana()
    Gtk.main()
