#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import gtk, cairo, gobject

from canaimainstalador.clases.common import floatify, givemeswap
from canaimainstalador.clases.common import set_color, process_color
from canaimainstalador.clases.common import hex_to_rgb, draw_rounded
from canaimainstalador.config import *

class BarraTodo(gtk.DrawingArea):
    def __init__(self, parent):
        super(BarraTodo, self).__init__()
        self.set_events(
            gtk.gdk.POINTER_MOTION_MASK | gtk.gdk.POINTER_MOTION_HINT_MASK |
            gtk.gdk.BUTTON_PRESS_MASK | gtk.gdk.BUTTON_RELEASE_MASK
            )
        self.connect("expose-event", self.expose)
        self.connect("button-press-event", self.press)
        self.connect("button-release-event", self.release)
        self.connect("motion-notify-event", self.draw_cursor)
        self.p = parent
        self.presionado = False

    def cambiar(self, forma):
        self.p.forma = forma
        self.forma = forma
        self.expose()

    def expose(self, widget = None, event = None):
        self.metodo = self.p.metodo
        self.ini = self.p.metodo['part'][1]
        self.fin = self.p.metodo['part'][2]
        self.primarias = self.p.metodo['disco'][3]
        self.extendidas = self.p.metodo['disco'][4]
        self.particiones = self.p.particiones
        self.minimo = self.p.minimo
        self.forma = self.p.forma
        self.nuevas = self.p.nuevas
        self.libre = self.p.libre
        self.total = self.fin - self.ini
        self.current = self.total - self.libre
        self.factor = self.current / ESPACIO_TOTAL
        self.swap = ESPACIO_SWAP
        self.p.acciones = []

        self.ancho = self.get_size_request()[0]
        self.alto = self.get_size_request()[1]

        if self.window:
            cr = self.window.cairo_create()
            cr.set_source_rgb(0.925490196, 0.91372549, 0.847058824)
            cr.rectangle(0, 0, self.ancho, self.alto)
            cr.fill()

        if self.forma == 'ROOT:SWAP:LIBRE':
            ini_1 = 0
            fin_1 = self.current - self.swap
            ini_2 = fin_1
            fin_2 = self.current
            ini_3 = fin_2
            fin_3 = self.total
            p_1 = [self.forma.split(':')[0], ini_1, fin_1, 0, 'ext4', 'primary', '', 0, 0, 0, 1]
            p_2 = [self.forma.split(':')[1], ini_2, fin_2, 0, 'swap', 'primary', '', 0, 0, 0, 1]
            p_3 = [self.forma.split(':')[2], ini_3, fin_3, 0, 'free', 'primary', '', 0, 0, 0, 1]
            self.p.nuevas = [p_1,p_2,p_3]

        elif self.forma == 'ROOT:HOME:SWAP:LIBRE':
            ini_1 = 0
            fin_1 = (ESPACIO_ROOT + ESPACIO_BOOT + ESPACIO_VAR + ESPACIO_USR) * self.factor
            ini_2 = fin_1
            fin_2 = self.current - self.swap
            ini_3 = fin_2
            fin_3 = self.current
            ini_4 = fin_3
            fin_4 = self.total
            p_1 = [self.forma.split(':')[0], ini_1, fin_1, 0, 'ext4', 'primary', '', 0, 0, 0, 1]
            p_2 = [self.forma.split(':')[1], ini_2, fin_2, 0, 'xfs', 'primary', '', 0, 0, 0, 1]
            p_3 = [self.forma.split(':')[2], ini_3, fin_3, 0, 'swap', 'primary', '', 0, 0, 0, 1]
            p_4 = [self.forma.split(':')[3], ini_4, fin_4, 0, 'free', 'primary', '', 0, 0, 0, 1]
            self.p.nuevas = [p_1,p_2,p_3,p_4]

        elif self.forma == 'BOOT:ROOT:HOME:SWAP:LIBRE':
            ini_1 = 0
            fin_1 = ESPACIO_BOOT * self.factor
            ini_2 = fin_1
            fin_2 = fin_1 + (ESPACIO_ROOT + ESPACIO_VAR + ESPACIO_USR) * self.factor
            ini_3 = fin_2
            fin_3 = self.current - self.swap
            ini_4 = fin_3
            fin_4 = self.current
            ini_5 = fin_4
            fin_5 = self.total
            p_1 = [self.forma.split(':')[0], ini_1, fin_1, 0, 'ext4', 'primary', '', 0, 0, 0, 1]
            p_2 = [self.forma.split(':')[1], ini_2, fin_2, 0, 'ext4', 'primary', '', 0, 0, 0, 1]
            p_3 = [self.forma.split(':')[2], ini_3, fin_3, 0, 'xfs', 'primary', '', 0, 0, 0, 1]
            p_4 = [self.forma.split(':')[3], ini_4, fin_4, 0, 'swap', 'primary', '', 0, 0, 0, 1]
            p_5 = [self.forma.split(':')[4], ini_5, fin_5, 0, 'free', 'primary', '', 0, 0, 0, 1]
            self.p.nuevas = [p_1,p_2,p_3,p_4,p_5]

        elif self.forma == 'BOOT:ROOT:VAR:USR:HOME:SWAP:LIBRE':
            ini_1 = 0
            fin_1 = ESPACIO_BOOT * self.factor
            ini_2 = fin_1
            fin_2 = fin_1 + (ESPACIO_ROOT * self.factor)
            ini_3 = fin_2
            fin_3 = fin_2 + (ESPACIO_VAR * self.factor)
            ini_4 = fin_3
            fin_4 = fin_3 + (ESPACIO_USR * self.factor)
            ini_5 = fin_4
            fin_5 = self.current - self.swap
            ini_6 = fin_5
            fin_6 = self.current
            ini_7 = fin_6
            fin_7 = self.total
            p_1 = [self.forma.split(':')[0], ini_1, fin_1, 0, 'ext4', 'primary', '', 0, 0, 0, 1]
            p_2 = [self.forma.split(':')[1], ini_2, fin_2, 0, 'ext4', 'primary', '', 0, 0, 0, 1]
            p_3 = [self.forma.split(':')[2], ini_3, fin_3, 0, 'ext4', 'primary', '', 0, 0, 0, 1]
            p_4 = [self.forma.split(':')[3], ini_4, fin_4, 0, 'ext4', 'primary', '', 0, 0, 0, 1]
            p_5 = [self.forma.split(':')[4], ini_5, fin_5, 0, 'xfs', 'primary', '', 0, 0, 0, 1]
            p_6 = [self.forma.split(':')[5], ini_6, fin_6, 0, 'swap', 'primary', '', 0, 0, 0, 1]
            p_7 = [self.forma.split(':')[6], ini_7, fin_7, 0, 'free', 'primary', '', 0, 0, 0, 1]
            self.p.nuevas = [p_1,p_2,p_3,p_4,p_5,p_6,p_7]

        else:
            pass

        for p in self.p.nuevas:
            ini = p[1]
            fin = p[2]
            tipo = p[5]
            fs = p[4]

            if tipo == 'logical':
                y1 = 3
                y2 = self.alto - 3
            elif tipo == 'extended' or tipo == 'primary':
                y1 = 0
                y2 = self.alto

            x1 = ((ini * self.ancho) / self.total)
            x2 = ((fin * self.ancho) / self.total)
            r = 1

            if x2 - x1 > 12:
                x1 = x1 + 1
                x2 = x2 - 1
                r = 5

            if self.window:
                draw_rounded(cr, (x1, y1, x2, y2), r)
                cr.set_source(set_color(fs, self.alto))
                cr.fill()

        xsel1 = (self.current * self.ancho / self.total) - 5
        ysel1 = 10
        xsel2 = (self.current * self.ancho / self.total) + 5
        ysel2 = self.alto - 10
        self.pos = [xsel1, ysel1, xsel2, ysel2]

        if self.window:
            cr.set_source_rgb(0, 0, 0)
            draw_rounded(cr, self.pos, 3)

            for i in range(int(ysel1 + 3), int(ysel2 - 2), 3):
                cr.move_to(xsel1 + 1, i)
                cr.rel_line_to(8, 0)
                cr.stroke()

        if self.metodo['tipo'] == 'TODO':
            for w in self.particiones:
                if w[4] != 'free':
                    self.p.acciones.append(
                        ['borrar', w[0], None, 0, 0, None, None]
                        )

            if len(self.p.nuevas) - 1 > 4:
                self.p.acciones.append(
                    ['crear', None, None, self.ini, self.ini + self.current, 'extended', 'extended']
                    )
                a_tipo = 'logical'
            else:
                a_tipo = 'primary'

        elif self.metodo['tipo'] == 'LIBRE':
            if self.metodo['part'][5] == 'logical':
                a_tipo = 'logical'
            else:
                if self.extendidas < 1:
                    if self.primarias + self.extendidas + len(self.p.nuevas) - 1 > 4:
                        self.p.acciones.append(
                            ['crear', None, None, self.ini, self.ini + self.current, 'extended', 'extended']
                            )
                        a_tipo = 'logical'
                    else:
                        a_tipo = 'primary'
                else:
                    if self.primarias + self.extendidas + len(self.p.nuevas) - 1 > 4:
                        a_tipo = 'FAIL'
                    else:
                        a_tipo = 'primary'

        for k in range(0, len(self.p.nuevas)):
            if self.p.nuevas[k][0] == 'ROOT':
                a_mount = '/'
                a_fs = 'ext4'
            elif self.p.nuevas[k][0] == 'SWAP':
                a_mount = 'swap'
                a_fs = 'swap'
            elif self.p.nuevas[k][0] == 'HOME':
                a_mount = '/home'
                a_fs = 'xfs'
            elif self.p.nuevas[k][0] == 'USR':
                a_mount = '/usr'
                a_fs = 'ext4'
            elif self.p.nuevas[k][0] == 'BOOT':
                a_mount = '/boot'
                a_fs = 'ext4'
            elif self.p.nuevas[k][0] == 'VAR':
                a_mount = '/var'
                a_fs = 'ext4'

            a_ini = self.ini + self.p.nuevas[k][1]
            a_fin = self.ini + self.p.nuevas[k][2]

            if self.p.nuevas[k][0] != 'LIBRE':
                self.p.acciones.append(
                    ['crear', None, a_mount, a_ini, a_fin, a_fs, a_tipo]
                    )

    def press(self, widget, event):
        if event.x >= self.pos[0] and event.x <= self.pos[2] and event.y >= self.pos[1] and event.y <= self.pos[3]:
            self.presionado = True

    def release(self, widget, event):
        self.presionado = False

    def draw_cursor(self, widget, event):
        if event.x >= self.pos[0] and event.x <= self.pos[2] and event.y >= self.pos[1] and event.y <= self.pos[3]:
            cursor = gtk.gdk.Cursor(gtk.gdk.HAND2)
            self.window.set_cursor(cursor)
        else:
            cursor = gtk.gdk.Cursor(gtk.gdk.LEFT_PTR)
            self.window.set_cursor(cursor)

        if self.presionado == True:
            x = float((event.x * self.total) / self.ancho)
            if x <= self.total and x >= self.minimo:
                self.libre = self.total - x
                self.p.libre = self.total - x
                self.p.barra.cambiar(self.forma)
                self.p.leyenda.cambiar(self.forma)
                self.queue_draw()
