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

import gtk

from gui.gtkui import check_gtk3

if check_gtk3():
    import RenderersNew as Renderers
else:
    import Renderers

class Header(gtk.HBox):
    '''a widget used to display some information about the conversation'''
    INFO_TPL = '%s[$nl]'
    INFO_TPL += '[$small]%s[$/small]'

    NAME = 'Header'
    DESCRIPTION = 'The widget that displays information about the conversation'
    AUTHOR = 'Mariano Guerra, Ivan25'
    WEBSITE = 'www.emesene.org'

    def __init__(self, session, members):
        '''constructor'''
        gtk.HBox.__init__(self)
        self.set_border_width(2)
        self._information = Renderers.SmileyLabel()

        eventBox = gtk.EventBox()
        eventBox.set_visible_window(False)
        eventBox.add(self._information)
        eventBox.connect('button-press-event', self.on_clicked)

        self.pack_start(eventBox, True, True)

        self.session = session
        self.members = members

        self.menu = gtk.Menu()
        copynick = gtk.ImageMenuItem(_('Copy nick to clipboard'))
        copynick.set_image(gtk.image_new_from_stock(gtk.STOCK_COPY, gtk.ICON_SIZE_MENU))
        copypm = gtk.ImageMenuItem(_('Copy personal message to clipboard'))
        copypm.set_image(gtk.image_new_from_stock(gtk.STOCK_COPY, gtk.ICON_SIZE_MENU))
        copymail = gtk.ImageMenuItem(_('Copy mail to clipboard'))
        copymail.set_image(gtk.image_new_from_stock(gtk.STOCK_COPY, gtk.ICON_SIZE_MENU))
        self.menu.append(copynick)
        self.menu.append(copypm)
        self.menu.append(copymail)
        copynick.connect('activate', self.copy_nick)
        copypm.connect('activate', self.copy_pm)
        copymail.connect('activate', self.copy_mail)
        copynick.show()
        copypm.show()
        copymail.show()

    def _set_information(self, lines):
        '''set the text on the information, lines is a tuple of size 3 with 3
        strings that will be replaced on the template'''
        self._information.set_markup(Header.INFO_TPL % lines)
        
    def _get_information(self):
        '''return the text on the information'''
        return self._information.get_markup()

    def copy_nick(self, data, widget=None):
        nick_list = []
        for member in self.members:
            contact = self.session.contacts.safe_get(member)
            nick_list.append(contact.nick)

        clipboard = gtk.clipboard_get(gtk.gdk.SELECTION_CLIPBOARD)
        clipboard.set_text(', '.join(nick_list))

    def copy_pm(self, data, widget=None):
        pm_list = []
        for member in self.members:
            contact = self.session.contacts.safe_get(member)
            pm_list.append(contact.message)

        clipboard = gtk.clipboard_get(gtk.gdk.SELECTION_CLIPBOARD)
        clipboard.set_text(', '.join(pm_list))

    def copy_mail(self, data, widget=None):
        mail_list = []
        for member in self.members:
            mail_list.append(member)

        clipboard = gtk.clipboard_get(gtk.gdk.SELECTION_CLIPBOARD)
        clipboard.set_text(', '.join(mail_list))

    def on_clicked(self, widget, event):
        '''called when the header clicked'''
        if event.button == 3:
            self.menu.popup(None, None, None, event.button, event.time, None)

    information = property(fget=_get_information, fset=_set_information)
