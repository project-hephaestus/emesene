# -*- coding: utf-8 -*-

#    This file is part of emesene.
#
#    emesene is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; either version 3 of the License, or
#    (at your option) any later version.
#
#    emesene is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with emesene; if not, write to the Free Software
#    Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

import sys
import gtk
import gobject

import utils

from gui.gtkui import check_gtk3

if check_gtk3():
    import TinyButtonNew as TinyButton
else:
    import TinyButton

if check_gtk3():
    import RenderersNew as Renderers
else:
    import Renderers


CLOSE_ON_LEFT = 0

#FIXME: find correct GSettings value and replace this in gtk3
if not check_gtk3():
    try:
        import gconf
        gclient = gconf.client_get_default()
        val = gclient.get("/apps/metacity/general/button_layout")
        if val.get_string().startswith("close"):
            CLOSE_ON_LEFT = 1
    except:
        pass

if sys.platform == 'darwin':
    CLOSE_ON_LEFT = 1

class TabWidget(gtk.HBox):
    '''a widget that is placed on the tab on a notebook'''
    NAME = 'Tab Widget'
    DESCRIPTION = 'A widget to display the tab information'
    AUTHOR = 'Mariano Guerra'
    WEBSITE = 'www.emesene.org'

    def __init__(self, text, on_tab_menu, 
                 on_close_clicked, conversation):
        '''constructor'''
        gtk.HBox.__init__(self)
        self.set_border_width(0)
        self.set_spacing(4)

        self.config = conversation.session.config
        self.image = gtk.Image()
        label = gtk.EventBox()
        label.connect('button-press-event', self.on_tab_clicked,
                           on_close_clicked, conversation)
        label.set_visible_window(False)
        self._label = Renderers.SmileyLabel()
        self._label.set_ellipsize(True)
        self._label.set_text(text)
        label.add(self._label)
        self.close = TinyButton.TinyButton(gtk.STOCK_CLOSE)
        self.close.set_tooltip_text(_('Close Tab (Ctrl+W)'))
        self.close.connect('clicked', on_close_clicked,
            conversation)

        if CLOSE_ON_LEFT:
            self.pack_start(self.close, False, False, 0)
            self.pack_start(self.image, False, False, 0)
            self.pack_start(label, True, True, 0)
        else:
            self.pack_start(self.image, False, False, 0)
            self.pack_start(label, True, True, 0)
            self.pack_start(self.close, False, False, 0)

        self.config.subscribe(self._on_close_button_on_tabs_visible,
            'b_close_button_on_tabs')
        self._on_close_button_on_tabs_visible(
              self.config.get_or_set('b_close_button_on_tabs', True))


        if self.config.i_tab_position > 1:
            self.set_orientation(gtk.ORIENTATION_VERTICAL)
            self._label.set_angle(90)
        else:
            self.set_orientation(gtk.ORIENTATION_HORIZONTAL)
            self._label.set_angle(0)

        self.config.subscribe(self.on_tab_position_change, 
                                      'i_tab_position')

        self.image.show()
        label.show()
        self._label.show()

    def remove_subscriptions(self):
        self.config.unsubscribe(self.on_tab_position_change, 
                                        'i_tab_position')
        self.config.unsubscribe(self._on_close_button_on_tabs_visible,
                                        'b_close_button_on_tabs')

    def set_image(self, path):
        '''set the image from path'''
        if utils.file_readable(path):
            self.image.set_from_file(path)
            self.image.show()

            return True

        return False

    def set_text(self, text):
        '''set the text of the label'''
        self._label.set_markup(gobject.markup_escape_text(text))

    def _on_close_button_on_tabs_visible(self, value):
        '''callback called when b_close_button_on_tabs changes'''
        self.close.set_visible(value)

    def on_tab_position_change(self, position):
        if self.config.i_tab_position > 1:
            self.set_orientation(gtk.ORIENTATION_VERTICAL)
            self._label.set_angle(90)
        else:
            self.set_orientation(gtk.ORIENTATION_HORIZONTAL)
            self._label.set_angle(0)

    def on_tab_clicked(self, widget, event, close_function, conv):
        if event.button == 2:
            close_function(widget, conv)
