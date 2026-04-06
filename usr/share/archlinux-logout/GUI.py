# =====================================================
#        Authors Brad Heffernan and Erik Dubois
# =====================================================


def GUI(self, Gtk, GdkPixbuf, working_dir, os, Gdk, fn):
    def apply_icon_widget_size(container, image, size):
        container.set_size_request(size, size)
        container.set_halign(Gtk.Align.CENTER)
        container.set_valign(Gtk.Align.START)
        container.set_margin_bottom(0)
        image.set_size_request(size, size)
        image.set_halign(Gtk.Align.CENTER)
        image.set_valign(Gtk.Align.START)
        image.set_can_shrink(False)

    def build_icon_widget(pixbuf):
        picture = Gtk.Picture()
        picture.set_content_fit(Gtk.ContentFit.CONTAIN)
        fn.set_widget_pixbuf(picture, pixbuf)
        return picture

    def normalize_button_label(label):
        label.set_halign(Gtk.Align.CENTER)
        label.set_justify(Gtk.Justification.CENTER)
        label.set_xalign(0.5)
        label.set_wrap(False)
        label.set_single_line_mode(True)
        label.set_margin_top(-138)

    def normalize_button_card(card):
        card_width = max(self.main_icon_size + 48, 150)
        card.set_halign(Gtk.Align.CENTER)
        card.set_valign(Gtk.Align.START)
        card.set_size_request(card_width, -1)
        card.set_margin_top(0)
        card.set_margin_bottom(0)

    mainbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
    mainbox2 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=24)
    topbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    lblbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)

    lbl = Gtk.Label(label="")

    self.lbl_stat = Gtk.Label()

    lblbox.append(lbl)
    lblbox.append(self.lbl_stat)

    overlayFrame = Gtk.Overlay()
    overlayFrame.set_child(lblbox)
    overlayFrame.add_overlay(topbox)
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
        os.path.join(working_dir, "configure.svg"),
        self.aux_icon_size,
        self.aux_icon_size,
    )
    self.imageset = build_icon_widget(pset)
    apply_icon_widget_size(self.Eset, self.imageset, self.aux_icon_size)
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
        os.path.join(working_dir, "light.svg"),
        self.aux_icon_size,
        self.aux_icon_size,
    )
    self.imagelig = build_icon_widget(plig)
    apply_icon_widget_size(self.Elig, self.imagelig, self.aux_icon_size)
    self.Elig.append(self.imagelig)

    # --- Per-button boxes ---
    vbox1 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
    vbox2 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
    vbox3 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
    vbox4 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
    vbox5 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
    vbox6 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
    vbox7 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
    hbox1 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=18)
    hbox2 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=18)

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
                self.main_icon_size,
                self.main_icon_size,
            )
            self.imagesh = build_icon_widget(psh)
            apply_icon_widget_size(self.Esh, self.imagesh, self.main_icon_size)
            self.Esh.append(self.imagesh)
        if button == "cancel":
            pc = GdkPixbuf.Pixbuf().new_from_file_at_size(
                os.path.join(working_dir, "themes/" + self.theme + "/cancel.svg"),
                self.main_icon_size,
                self.main_icon_size,
            )
            self.imagec = build_icon_widget(pc)
            apply_icon_widget_size(self.Ec, self.imagec, self.main_icon_size)
            self.Ec.append(self.imagec)
        if button == "restart":
            pr = GdkPixbuf.Pixbuf().new_from_file_at_size(
                os.path.join(working_dir, "themes/" + self.theme + "/restart.svg"),
                self.main_icon_size,
                self.main_icon_size,
            )
            self.imager = build_icon_widget(pr)
            apply_icon_widget_size(self.Er, self.imager, self.main_icon_size)
            self.Er.append(self.imager)
        if button == "suspend":
            ps = GdkPixbuf.Pixbuf().new_from_file_at_size(
                os.path.join(working_dir, "themes/" + self.theme + "/suspend.svg"),
                self.main_icon_size,
                self.main_icon_size,
            )
            self.images = build_icon_widget(ps)
            apply_icon_widget_size(self.Es, self.images, self.main_icon_size)
            self.Es.append(self.images)
        if button == "lock":
            plk = GdkPixbuf.Pixbuf().new_from_file_at_size(
                os.path.join(working_dir, "themes/" + self.theme + "/lock.svg"),
                self.main_icon_size,
                self.main_icon_size,
            )
            self.imagelk = build_icon_widget(plk)
            apply_icon_widget_size(self.Elk, self.imagelk, self.main_icon_size)
            self.Elk.append(self.imagelk)
        if button == "logout":
            plo = GdkPixbuf.Pixbuf().new_from_file_at_size(
                os.path.join(working_dir, "themes/" + self.theme + "/logout.svg"),
                self.main_icon_size,
                self.main_icon_size,
            )
            self.imagelo = build_icon_widget(plo)
            apply_icon_widget_size(self.El, self.imagelo, self.main_icon_size)
            self.El.append(self.imagelo)
        if button == "hibernate":
            ph = GdkPixbuf.Pixbuf().new_from_file_at_size(
                os.path.join(working_dir, "themes/" + self.theme + "/hibernate.svg"),
                self.main_icon_size,
                self.main_icon_size,
            )
            self.imageh = build_icon_widget(ph)
            apply_icon_widget_size(self.Eh, self.imageh, self.main_icon_size)
            self.Eh.append(self.imageh)

    # --- Labels ---
    self.lbl1 = Gtk.Label()
    self.lbl1.set_markup(
        f'<span size="{str(self.font)}000">Shutdown ({self.binds["shutdown"]})</span>'
    )
    self.lbl1.set_name("lbl")
    normalize_button_label(self.lbl1)

    self.lbl2 = Gtk.Label()
    self.lbl2.set_markup(
        f'<span size="{str(self.font)}000">Reboot ({self.binds["restart"]})</span>'
    )
    self.lbl2.set_name("lbl")
    normalize_button_label(self.lbl2)

    self.lbl3 = Gtk.Label()
    self.lbl3.set_markup(
        f'<span size="{str(self.font)}000">Suspend ({self.binds["suspend"]})</span>'
    )
    self.lbl3.set_name("lbl")
    normalize_button_label(self.lbl3)

    self.lbl4 = Gtk.Label()
    self.lbl4.set_markup(
        f'<span size="{str(self.font)}000">Lock ({self.binds["lock"]})</span>'
    )
    self.lbl4.set_name("lbl")
    normalize_button_label(self.lbl4)

    self.lbl5 = Gtk.Label()
    self.lbl5.set_markup(
        f'<span size="{str(self.font)}000">Logout ({self.binds["logout"]})</span>'
    )
    self.lbl5.set_name("lbl")
    normalize_button_label(self.lbl5)

    self.lbl6 = Gtk.Label()
    self.lbl6.set_markup(
        f'<span size="{str(self.font)}000">Cancel ({self.binds["cancel"]})</span>'
    )
    self.lbl6.set_name("lbl")
    normalize_button_label(self.lbl6)

    self.lbl7 = Gtk.Label()
    self.lbl7.set_markup(
        f'<span size="{str(self.font)}000">Hibernate ({self.binds["hibernate"]})</span>'
    )
    self.lbl7.set_name("lbl")
    normalize_button_label(self.lbl7)

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

    button_widgets = []
    for button in self.buttons:
        if button == "shutdown":
            button_widgets.append(vbox1)
        if button == "cancel":
            button_widgets.append(vbox6)
        if button == "restart":
            button_widgets.append(vbox2)
        if button == "suspend":
            button_widgets.append(vbox3)
        if fn.sessionw != True and button == "lock":
            button_widgets.append(vbox4)
        if button == "logout":
            button_widgets.append(vbox5)
        if button == "hibernate":
            button_widgets.append(vbox7)

    split_index = (len(button_widgets) + 1) // 2
    first_row = button_widgets[:split_index]
    second_row = button_widgets[split_index:]

    for widget in button_widgets:
        normalize_button_card(widget)
        widget.set_margin_start(10)
        widget.set_margin_end(10)

    for widget in first_row:
        hbox1.append(widget)

    for widget in second_row:
        hbox2.append(widget)

    hbox1.set_halign(Gtk.Align.CENTER)
    hbox2.set_halign(Gtk.Align.CENTER)

    mainbox2.set_halign(Gtk.Align.CENTER)
    mainbox2.append(hbox1)
    if second_row:
        mainbox2.append(hbox2)

    mainbox.set_valign(Gtk.Align.CENTER)
    mainbox.append(mainbox2)

    topbox.set_halign(Gtk.Align.START)
    topbox.set_valign(Gtk.Align.START)
    topbox.set_margin_top(16)
    topbox.set_margin_start(16)
    topbox.append(self.Elig)
    topbox.append(self.Eset)

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
