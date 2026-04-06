# =================================================================
# =                  Author: Brad Heffernan                       =
# =================================================================

from Functions import base_dir, os


def GUI(self, Gtk, GdkPixbuf, Gdk, th, fn):

    self.vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=15)
    self.vbox.set_margin_start(10)
    self.vbox.set_margin_end(10)
    self.vbox.set_margin_top(10)
    self.vbox.set_margin_bottom(10)
    self.set_child(self.vbox)

    hbox1 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    hbox2 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    hbox5 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    hbox6 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
    hbox7 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    hbox8 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)

    # =======================================================
    #                       App Notifications
    # =======================================================

    self.notification_revealer = Gtk.Revealer()
    self.notification_revealer.set_reveal_child(False)

    self.notification_label = Gtk.Label()

    pb_panel = GdkPixbuf.Pixbuf().new_from_file(base_dir + '/images/panel.png')
    panel = Gtk.Image()
    panel.set_from_pixbuf(pb_panel)

    overlayFrame = Gtk.Overlay()
    overlayFrame.set_child(panel)
    overlayFrame.add_overlay(self.notification_label)

    self.notification_revealer.set_child(overlayFrame)

    hbox1.append(self.notification_revealer)
    self.notification_revealer.set_hexpand(True)

    # ==========================================================
    #                       LOCATIONS
    # ==========================================================
    lbl = Gtk.Label(label="Enter Location")
    self.loc.set_size_request(280, 0)
    btnbrowse = Gtk.Button(label="...")
    btnsearch = Gtk.Button(label="Load")
    btndefault = Gtk.Button(label="Default")

    btnsearch.connect("clicked", self.on_load_clicked, self.fb)
    btndefault.connect("clicked", self.on_default_clicked, self.fb)
    btnbrowse.connect("clicked", self.on_browse_clicked)

    btnsearch.set_size_request(130, 0)

    lbl.set_margin_start(10)
    lbl.set_margin_end(0)
    hbox6.append(lbl)
    hbox6.append(self.loc)
    btnbrowse.set_margin_start(5)
    hbox6.append(btnbrowse)
    hbox6.append(btnsearch)

    btndefault.set_halign(Gtk.Align.END)
    btndefault.set_hexpand(True)
    hbox6.append(btndefault)

    # ==========================================================
    #                       SEARCH
    # ==========================================================
    lblS = Gtk.Label(label="Search: ")
    self.search.set_size_request(180, 0)
    btnsearcher = Gtk.Button(label="Search")

    btnsearcher.connect("clicked", self.on_search_clicked)
    btnsearcher.set_size_request(130, 0)

    hbox8.append(lblS)
    hbox8.append(self.search)
    hbox8.append(btnsearcher)

    # ==========================================================
    #                       APPLY BUTTON
    # ==========================================================
    self.btnset = Gtk.Button(label="Apply Image")
    self.btnset.connect("clicked", self.on_apply_clicked)
    self.btnset.set_halign(Gtk.Align.END)
    self.btnset.set_hexpand(True)
    hbox2.append(self.btnset)

    # ==========================================================
    #                       CREDITS
    # ==========================================================
    credits = Gtk.Button(label="Credits")
    credits.connect("clicked", self.on_support_clicked)
    hbox2.prepend(credits)

    # ==========================================================
    #                       STATUS
    # ==========================================================
    hbox5.append(self.status)
    self.status.set_hexpand(True)

    # ==========================================================
    #                       BLUR SLIDER
    # ==========================================================
    ad1 = Gtk.Adjustment(value=100, lower=0, upper=100,
                         step_increment=1, page_increment=100, page_size=0)

    self.blur = Gtk.Scale(orientation=Gtk.Orientation.HORIZONTAL, adjustment=ad1)
    self.blur.set_digits(0)
    self.blur.set_hexpand(True)
    self.blur.set_draw_value(True)
    self.blur.set_size_request(100, 0)
    self.blur.set_valign(Gtk.Align.START)

    label = Gtk.Label(label="Blur intensity")
    hbox7.append(label)
    hbox7.append(self.blur)
    self.blur.set_hexpand(True)

    hbox2.prepend(hbox7)

    # ==========================================================
    #                       PACK TO WINDOW
    # ==========================================================

    self.vbox.append(hbox1)          # notify
    self.vbox.append(hbox6)          # load row
    self.vbox.append(hbox8)          # search row
    self.vbox.append(self.hbox3)     # images
    self.hbox3.set_vexpand(True)
    self.hbox3.set_hexpand(True)
    self.vbox.append(hbox5)          # status
    self.vbox.append(hbox2)          # settings row
