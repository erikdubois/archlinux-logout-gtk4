# =====================================================
#        Authors Brad Heffernan and Erik Dubois
# =====================================================


def GUI(self, Gtk, GdkPixbuf, working_dir, os, Gdk, fn):
    mainbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
    mainbox2 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    lblbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)

    lbl = Gtk.Label(label="")

    self.lbl_stat = Gtk.Label()

    lblbox.append(lbl)
    lblbox.append(self.lbl_stat)

    overlayFrame = Gtk.Overlay()
    overlayFrame.set_child(lblbox)
    overlayFrame.add_overlay(mainbox)

    self.set_child(overlayFrame)

    # --- Settings button (gear icon) ---
    self.Eset = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
    self.Eset.set_name("settings")

    eset_click = Gtk.GestureClick()
    eset_click.connect(
        "pressed",
        lambda g, n, x, y: self.on_click(self.Eset, self.binds["settings"]),
    )
    self.Eset.add_controller(eset_click)

    eset_motion = Gtk.EventControllerMotion()
    eset_motion.connect(
        "enter", lambda c, x, y: self.on_mouse_in(self.Eset, self.binds["settings"])
    )
    eset_motion.connect(
        "leave", lambda c: self.on_mouse_out(self.Eset, self.binds["settings"])
    )
    self.Eset.add_controller(eset_motion)

    pset = GdkPixbuf.Pixbuf().new_from_file_at_size(
        os.path.join(working_dir, "configure.svg"), 48, 48
    )
    self.imageset = Gtk.Image()
    self.imageset.set_from_pixbuf(pset)
    self.Eset.append(self.imageset)

    # --- Light/wallpaper button ---
    self.Elig = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
    self.Elig.set_name("light")

    elig_click = Gtk.GestureClick()
    elig_click.connect(
        "pressed", lambda g, n, x, y: self.on_click(self.Elig, "light")
    )
    self.Elig.add_controller(elig_click)

    elig_motion = Gtk.EventControllerMotion()
    elig_motion.connect("enter", lambda c, x, y: self.on_mouse_in(self.Elig, "light"))
    elig_motion.connect("leave", lambda c: self.on_mouse_out(self.Elig, "light"))
    self.Elig.add_controller(elig_motion)

    plig = GdkPixbuf.Pixbuf().new_from_file_at_size(
        os.path.join(working_dir, "light.svg"), 48, 48
    )
    self.imagelig = Gtk.Image()
    self.imagelig.set_from_pixbuf(plig)
    self.Elig.append(self.imagelig)

    # --- Per-button boxes ---
    vbox1 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
    vbox2 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
    vbox3 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
    vbox4 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
    vbox5 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
    vbox6 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
    vbox7 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
    hbox17 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)

    hbox1 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=30)

    # --- Shutdown ---
    self.Esh = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
    esh_click = Gtk.GestureClick()
    esh_click.connect(
        "pressed",
        lambda g, n, x, y: self.on_click(self.Esh, self.binds["shutdown"]),
    )
    self.Esh.add_controller(esh_click)
    esh_motion = Gtk.EventControllerMotion()
    esh_motion.connect(
        "enter", lambda c, x, y: self.on_mouse_in(self.Esh, self.binds["shutdown"])
    )
    esh_motion.connect(
        "leave", lambda c: self.on_mouse_out(self.Esh, self.binds["shutdown"])
    )
    self.Esh.add_controller(esh_motion)

    # --- Restart ---
    self.Er = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
    er_click = Gtk.GestureClick()
    er_click.connect(
        "pressed",
        lambda g, n, x, y: self.on_click(self.Er, self.binds["restart"]),
    )
    self.Er.add_controller(er_click)
    er_motion = Gtk.EventControllerMotion()
    er_motion.connect(
        "enter", lambda c, x, y: self.on_mouse_in(self.Er, self.binds["restart"])
    )
    er_motion.connect(
        "leave", lambda c: self.on_mouse_out(self.Er, self.binds["restart"])
    )
    self.Er.add_controller(er_motion)

    # --- Suspend ---
    self.Es = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
    es_click = Gtk.GestureClick()
    es_click.connect(
        "pressed",
        lambda g, n, x, y: self.on_click(self.Es, self.binds["suspend"]),
    )
    self.Es.add_controller(es_click)
    es_motion = Gtk.EventControllerMotion()
    es_motion.connect(
        "enter", lambda c, x, y: self.on_mouse_in(self.Es, self.binds["suspend"])
    )
    es_motion.connect(
        "leave", lambda c: self.on_mouse_out(self.Es, self.binds["suspend"])
    )
    self.Es.add_controller(es_motion)

    # --- Lock ---
    self.Elk = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
    elk_click = Gtk.GestureClick()
    elk_click.connect(
        "pressed",
        lambda g, n, x, y: self.on_click(self.Elk, self.binds["lock"]),
    )
    self.Elk.add_controller(elk_click)
    elk_motion = Gtk.EventControllerMotion()
    elk_motion.connect(
        "enter", lambda c, x, y: self.on_mouse_in(self.Elk, self.binds["lock"])
    )
    elk_motion.connect(
        "leave", lambda c: self.on_mouse_out(self.Elk, self.binds["lock"])
    )
    self.Elk.add_controller(elk_motion)

    # --- Logout ---
    self.El = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
    el_click = Gtk.GestureClick()
    el_click.connect(
        "pressed",
        lambda g, n, x, y: self.on_click(self.El, self.binds["logout"]),
    )
    self.El.add_controller(el_click)
    el_motion = Gtk.EventControllerMotion()
    el_motion.connect(
        "enter", lambda c, x, y: self.on_mouse_in(self.El, self.binds["logout"])
    )
    el_motion.connect(
        "leave", lambda c: self.on_mouse_out(self.El, self.binds["logout"])
    )
    self.El.add_controller(el_motion)

    # --- Cancel ---
    self.Ec = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
    ec_click = Gtk.GestureClick()
    ec_click.connect(
        "pressed",
        lambda g, n, x, y: self.on_click(self.Ec, self.binds["cancel"]),
    )
    self.Ec.add_controller(ec_click)
    ec_motion = Gtk.EventControllerMotion()
    ec_motion.connect(
        "enter", lambda c, x, y: self.on_mouse_in(self.Ec, self.binds["cancel"])
    )
    ec_motion.connect(
        "leave", lambda c: self.on_mouse_out(self.Ec, self.binds["cancel"])
    )
    self.Ec.add_controller(ec_motion)

    # --- Hibernate ---
    self.Eh = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
    eh_click = Gtk.GestureClick()
    eh_click.connect(
        "pressed",
        lambda g, n, x, y: self.on_click(self.Eh, self.binds["hibernate"]),
    )
    self.Eh.add_controller(eh_click)
    eh_motion = Gtk.EventControllerMotion()
    eh_motion.connect(
        "enter", lambda c, x, y: self.on_mouse_in(self.Eh, self.binds["hibernate"])
    )
    eh_motion.connect(
        "leave", lambda c: self.on_mouse_out(self.Eh, self.binds["hibernate"])
    )
    self.Eh.add_controller(eh_motion)

    # --- Load icons per active button ---
    for button in self.buttons:
        if button == "shutdown":
            psh = GdkPixbuf.Pixbuf().new_from_file_at_size(
                os.path.join(working_dir, "themes/" + self.theme + "/shutdown.svg"),
                self.icon,
                self.icon,
            )
            self.imagesh = Gtk.Image()
            self.imagesh.set_from_pixbuf(psh)
            self.Esh.append(self.imagesh)
        if button == "cancel":
            pc = GdkPixbuf.Pixbuf().new_from_file_at_size(
                os.path.join(working_dir, "themes/" + self.theme + "/cancel.svg"),
                self.icon,
                self.icon,
            )
            self.imagec = Gtk.Image()
            self.imagec.set_from_pixbuf(pc)
            self.Ec.append(self.imagec)
        if button == "restart":
            pr = GdkPixbuf.Pixbuf().new_from_file_at_size(
                os.path.join(working_dir, "themes/" + self.theme + "/restart.svg"),
                self.icon,
                self.icon,
            )
            self.imager = Gtk.Image()
            self.imager.set_from_pixbuf(pr)
            self.Er.append(self.imager)
        if button == "suspend":
            ps = GdkPixbuf.Pixbuf().new_from_file_at_size(
                os.path.join(working_dir, "themes/" + self.theme + "/suspend.svg"),
                self.icon,
                self.icon,
            )
            self.images = Gtk.Image()
            self.images.set_from_pixbuf(ps)
            self.Es.append(self.images)
        if button == "lock":
            plk = GdkPixbuf.Pixbuf().new_from_file_at_size(
                os.path.join(working_dir, "themes/" + self.theme + "/lock.svg"),
                self.icon,
                self.icon,
            )
            self.imagelk = Gtk.Image()
            self.imagelk.set_from_pixbuf(plk)
            self.Elk.append(self.imagelk)
        if button == "logout":
            plo = GdkPixbuf.Pixbuf().new_from_file_at_size(
                os.path.join(working_dir, "themes/" + self.theme + "/logout.svg"),
                self.icon,
                self.icon,
            )
            self.imagelo = Gtk.Image()
            self.imagelo.set_from_pixbuf(plo)
            self.El.append(self.imagelo)
        if button == "hibernate":
            ph = GdkPixbuf.Pixbuf().new_from_file_at_size(
                os.path.join(working_dir, "themes/" + self.theme + "/hibernate.svg"),
                self.icon,
                self.icon,
            )
            self.imageh = Gtk.Image()
            self.imageh.set_from_pixbuf(ph)
            self.Eh.append(self.imageh)

    # --- Labels ---
    self.lbl1 = Gtk.Label()
    self.lbl1.set_markup(
        f'<span size="{str(self.font)}000">Shutdown ({self.binds["shutdown"]})</span>'
    )
    self.lbl1.set_name("lbl")

    self.lbl2 = Gtk.Label()
    self.lbl2.set_markup(
        f'<span size="{str(self.font)}000">Reboot ({self.binds["restart"]})</span>'
    )
    self.lbl2.set_name("lbl")

    self.lbl3 = Gtk.Label()
    self.lbl3.set_markup(
        f'<span size="{str(self.font)}000">Suspend ({self.binds["suspend"]})</span>'
    )
    self.lbl3.set_name("lbl")

    self.lbl4 = Gtk.Label()
    self.lbl4.set_markup(
        f'<span size="{str(self.font)}000">Lock ({self.binds["lock"]})</span>'
    )
    self.lbl4.set_name("lbl")

    self.lbl5 = Gtk.Label()
    self.lbl5.set_markup(
        f'<span size="{str(self.font)}000">Logout ({self.binds["logout"]})</span>'
    )
    self.lbl5.set_name("lbl")

    self.lbl6 = Gtk.Label()
    self.lbl6.set_markup(
        f'<span size="{str(self.font)}000">Cancel ({self.binds["cancel"]})</span>'
    )
    self.lbl6.set_name("lbl")

    self.lbl7 = Gtk.Label()
    self.lbl7.set_markup(
        f'<span size="{str(self.font)}000">Hibernate ({self.binds["hibernate"]})</span>'
    )
    self.lbl7.set_name("lbl")

    vbox1.append(self.Esh)
    vbox1.append(self.lbl1)
    vbox2.append(self.Er)
    vbox2.append(self.lbl2)
    vbox3.append(self.Es)
    vbox3.append(self.lbl3)
    vbox4.append(self.Elk)
    vbox4.append(self.lbl4)
    vbox5.append(self.El)
    vbox5.append(self.lbl5)
    vbox6.append(self.Ec)
    vbox6.append(self.lbl6)
    vbox7.append(self.Eh)
    vbox7.append(self.lbl7)

    for button in self.buttons:
        if button == "shutdown":
            hbox1.append(vbox1)
            vbox1.set_margin_start(20)
            vbox1.set_margin_end(20)
        if button == "cancel":
            hbox1.append(vbox6)
            vbox6.set_margin_start(20)
            vbox6.set_margin_end(20)
        if button == "restart":
            hbox1.append(vbox2)
            vbox2.set_margin_start(20)
            vbox2.set_margin_end(20)
        if button == "suspend":
            hbox1.append(vbox3)
            vbox3.set_margin_start(20)
            vbox3.set_margin_end(20)
        if fn.sessionw != True:
            if button == "lock":
                hbox1.append(vbox4)
                vbox4.set_margin_start(20)
                vbox4.set_margin_end(20)
        if button == "logout":
            hbox1.append(vbox5)
            vbox5.set_margin_start(20)
            vbox5.set_margin_end(20)
        if button == "hibernate":
            hbox1.append(vbox7)
            vbox7.set_margin_start(20)
            vbox7.set_margin_end(20)

    mainbox2.set_halign(Gtk.Align.CENTER)
    mainbox2.append(hbox1)

    # spacers row (settings + light icons top-left)
    hbox17.append(self.Elig)
    hbox17.append(self.Eset)
    mainbox.append(hbox17)

    mainbox.set_valign(Gtk.Align.CENTER)
    mainbox.append(mainbox2)

    # --- Settings popover ---
    self.popover = Gtk.Popover()
    self.popover2 = Gtk.Popover()

    vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
    vbox.set_margin_start(10)
    vbox.set_margin_end(10)
    vbox.set_margin_top(10)
    vbox.set_margin_bottom(10)

    lbl_opacity = Gtk.Label()
    lbl_opacity.set_markup("<b>Opacity:</b>")
    lbl_opacity.set_halign(Gtk.Align.START)
    lbl_opacity.set_valign(Gtk.Align.END)

    lbl_icon_size = Gtk.Label()
    lbl_icon_size.set_markup("<b>Icon size:</b>")
    lbl_icon_size.set_halign(Gtk.Align.START)
    lbl_icon_size.set_valign(Gtk.Align.END)

    lbl_theme = Gtk.Label()
    lbl_theme.set_markup("<b>Theme:</b>")
    lbl_theme.set_halign(Gtk.Align.START)
    lbl_theme.set_valign(Gtk.Align.CENTER)

    lbl_font_size = Gtk.Label()
    lbl_font_size.set_markup("<b>Font size:</b>")
    lbl_font_size.set_halign(Gtk.Align.START)
    lbl_font_size.set_valign(Gtk.Align.END)

    try:
        vals = self.opacity * 100
        ad1 = Gtk.Adjustment(value=vals, lower=0, upper=100, step_increment=5, page_increment=10, page_size=0)
    except Exception:
        ad1 = Gtk.Adjustment(value=60, lower=0, upper=100, step_increment=5, page_increment=10, page_size=0)

    self.hscale = Gtk.Scale(orientation=Gtk.Orientation.HORIZONTAL, adjustment=ad1)
    self.hscale.set_digits(0)
    self.hscale.set_hexpand(True)
    self.hscale.set_size_request(150, 0)
    self.hscale.set_valign(Gtk.Align.START)

    try:
        vals = self.font
        ad1f = Gtk.Adjustment(value=vals, lower=0, upper=80, step_increment=5, page_increment=10, page_size=0)
    except Exception:
        ad1f = Gtk.Adjustment(value=60, lower=0, upper=80, step_increment=5, page_increment=10, page_size=0)

    self.fonts = Gtk.Scale(orientation=Gtk.Orientation.HORIZONTAL, adjustment=ad1f)
    self.fonts.set_digits(0)
    self.fonts.set_hexpand(True)
    self.fonts.set_size_request(150, 0)
    self.fonts.set_valign(Gtk.Align.START)

    try:
        valsi = self.icon
        ad1i = Gtk.Adjustment(value=valsi, lower=0, upper=300, step_increment=5, page_increment=10, page_size=0)
    except Exception:
        ad1i = Gtk.Adjustment(value=60, lower=0, upper=300, step_increment=5, page_increment=10, page_size=0)

    self.icons = Gtk.Scale(orientation=Gtk.Orientation.HORIZONTAL, adjustment=ad1i)
    self.icons.set_digits(0)
    self.icons.set_hexpand(True)
    self.icons.set_size_request(150, 0)
    self.icons.set_valign(Gtk.Align.START)

    self.themes = Gtk.ComboBoxText()

    lists = fn._get_themes()
    active = 0
    for x in range(len(lists)):
        self.themes.append_text(lists[x])
        if lists[x] == self.theme:
            active = x
    self.themes.set_active(active)

    btn_save_settings = Gtk.Button(label="Save Settings")
    btn_save_settings.connect("clicked", self.on_save_clicked)

    hbox_opacity = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=5)
    hbox_opacity.append(lbl_opacity)
    hbox_opacity.append(self.hscale)

    hbox_icon_size = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=5)
    hbox_icon_size.append(lbl_icon_size)
    hbox_icon_size.append(self.icons)

    hbox_font_size = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=5)
    hbox_font_size.append(lbl_font_size)
    hbox_font_size.append(self.fonts)

    hbox_theme = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=20)
    hbox_theme.append(lbl_theme)
    hbox_theme.append(self.themes)

    hbox_buttons = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=5)
    hbox_buttons.append(btn_save_settings)

    grid_settings = Gtk.Grid()
    grid_settings.set_row_spacing(20)

    grid_settings.attach(hbox_opacity, 0, 1, 1, 1)
    grid_settings.attach(hbox_icon_size, 0, 2, 1, 1)
    grid_settings.attach(hbox_font_size, 0, 3, 1, 1)
    grid_settings.attach(hbox_theme, 0, 4, 1, 1)
    grid_settings.attach(hbox_buttons, 0, 6, 1, 1)

    vbox.append(grid_settings)

    self.popover.set_child(vbox)
    self.popover.set_position(Gtk.PositionType.TOP)

    hbox8 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=20)

    plbl = Gtk.Label()
    plbl.set_markup(
        '<span size="large">You can change the lockscreen wallpaper\nwith <b>Archlinux BetterLockScreen</b></span>'
    )
    plbl.set_halign(Gtk.Align.END)
    hbox8.append(plbl)

    self.popover2.set_child(hbox8)
    self.popover2.set_position(Gtk.PositionType.TOP)

    # Set popover parents (GTK4 replaces set_relative_to)
    self.popover.set_parent(self.Eset)
    self.popover2.set_parent(self.Elig)
