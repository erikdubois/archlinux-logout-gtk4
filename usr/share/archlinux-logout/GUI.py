# =====================================================
#        Authors Brad Heffernan and Erik Dubois
# =====================================================


def GUI(self, Gtk, GdkPixbuf, working_dir, os, Gdk, fn):
    def apply_icon_widget_size(container, image, size):
        container.set_halign(Gtk.Align.CENTER)
        container.set_valign(Gtk.Align.START)
        container.set_vexpand(False)
        container.set_hexpand(False)
        image.set_size_request(size, size)
        image.set_halign(Gtk.Align.CENTER)
        image.set_valign(Gtk.Align.START)
        image.set_vexpand(False)
        image.set_hexpand(False)

    def build_icon_widget(svg_path, size):
        picture = Gtk.Picture()
        picture.set_content_fit(Gtk.ContentFit.CONTAIN)
        picture.set_can_shrink(True)
        picture.set_size_request(size, size)
        self._pending_pixbufs.append((svg_path, picture, size))
        return picture

    def normalize_button_label(label):
        label.set_halign(Gtk.Align.CENTER)
        label.set_justify(Gtk.Justification.CENTER)
        label.set_xalign(0.5)
        label.set_wrap(False)
        label.set_single_line_mode(True)
        label.set_margin_top(0)

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

    self.imageset = build_icon_widget(
        os.path.join(working_dir, "configure.svg"), self.aux_icon_size)
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

    self.imagelig = build_icon_widget(
        os.path.join(working_dir, "light.svg"), self.aux_icon_size)
    apply_icon_widget_size(self.Elig, self.imagelig, self.aux_icon_size)
    self.Elig.append(self.imagelig)

    # --- Button cards: each card IS the gesture target (no inner wrapper box) ---
    # self.Esh/Er/etc. point directly to the card so set_sensitive works on the whole card

    def make_card(bind_key):
        card = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        click = Gtk.GestureClick()
        click.connect("pressed", lambda g, n, x, y: self.on_click(card, bind_key))
        card.add_controller(click)
        motion = Gtk.EventControllerMotion()
        motion.connect("enter", lambda c, x, y: self.on_mouse_in(card, bind_key))
        motion.connect("leave", lambda c: self.on_mouse_out(card, bind_key))
        card.add_controller(motion)
        return card

    self.Esh  = make_card(self.binds["shutdown"])
    self.Er   = make_card(self.binds["restart"])
    self.Es   = make_card(self.binds["suspend"])
    self.Elk  = make_card(self.binds["lock"])
    self.El   = make_card(self.binds["logout"])
    self.Ec   = make_card(self.binds["cancel"])
    self.Eh   = make_card(self.binds["hibernate"])

    hbox1 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=18)
    hbox2 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=18)

    # Map button names to (card, image_attr, label_attr, label_text, svg_name)
    button_defs = {
        "shutdown": (self.Esh,  "imagesh",  "lbl1", f'Shutdown ({self.binds["shutdown"]})', "shutdown"),
        "restart":  (self.Er,   "imager",   "lbl2", f'Reboot ({self.binds["restart"]})',    "restart"),
        "suspend":  (self.Es,   "images",   "lbl3", f'Suspend ({self.binds["suspend"]})',   "suspend"),
        "lock":     (self.Elk,  "imagelk",  "lbl4", f'Lock ({self.binds["lock"]})',         "lock"),
        "logout":   (self.El,   "imagelo",  "lbl5", f'Logout ({self.binds["logout"]})',     "logout"),
        "cancel":   (self.Ec,   "imagec",   "lbl6", f'Cancel ({self.binds["cancel"]})',     "cancel"),
        "hibernate":(self.Eh,   "imageh",   "lbl7", f'Hibernate ({self.binds["hibernate"]})', "hibernate"),
    }

    for button in self.buttons:
        if button not in button_defs:
            continue
        card, img_attr, lbl_attr, lbl_text, svg = button_defs[button]

        img = build_icon_widget(
            os.path.join(working_dir, "themes/" + self.theme + f"/{svg}.svg"),
            self.main_icon_size)
        apply_icon_widget_size(card, img, self.main_icon_size)
        setattr(self, img_attr, img)

        lbl = Gtk.Label()
        lbl.set_markup(f'<span size="{str(self.font)}000">{lbl_text}</span>')
        lbl.set_name("lbl")
        normalize_button_label(lbl)
        lbl.set_valign(Gtk.Align.CENTER)
        setattr(self, lbl_attr, lbl)
        lbl.set_visible(self.show_text)

        icon_overlay = Gtk.Overlay()
        icon_overlay.set_child(img)
        icon_overlay.add_overlay(lbl)
        icon_overlay.set_size_request(self.main_icon_size, self.main_icon_size)
        icon_overlay.set_halign(Gtk.Align.CENTER)
        icon_overlay.set_valign(Gtk.Align.START)
        card.append(icon_overlay)

    # Convenience references for labels used in on_mouse_in/out
    # (set to empty label if button not shown, to avoid AttributeError)
    _dummy = Gtk.Label()
    for attr in ("lbl1","lbl2","lbl3","lbl4","lbl5","lbl6","lbl7"):
        if not hasattr(self, attr):
            setattr(self, attr, _dummy)

    card_map = {
        "shutdown": self.Esh,
        "cancel":   self.Ec,
        "restart":  self.Er,
        "suspend":  self.Es,
        "lock":     self.Elk,
        "logout":   self.El,
        "hibernate":self.Eh,
    }

    button_widgets = []
    for button in self.buttons:
        if button == "lock" and fn.sessionw:
            continue
        if button in card_map:
            button_widgets.append(card_map[button])

    split_index = len(button_widgets) if len(button_widgets) <= 5 else (len(button_widgets) + 1) // 2
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
    self.hscale.set_draw_value(True)
    self.hscale.set_value_pos(Gtk.PositionType.TOP)
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
    self.fonts.set_draw_value(True)
    self.fonts.set_value_pos(Gtk.PositionType.TOP)
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
    self.icons.set_draw_value(True)
    self.icons.set_value_pos(Gtk.PositionType.TOP)
    self.icons.set_hexpand(True)
    self.icons.set_size_request(150, 0)
    self.icons.set_valign(Gtk.Align.START)

    lists = fn._get_themes()
    theme_model = Gtk.StringList.new(lists)
    self.themes = Gtk.DropDown(model=theme_model)
    active = lists.index(self.theme) if self.theme in lists else 0
    self.themes.set_selected(active)

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

    lbl_show_text = Gtk.Label()
    lbl_show_text.set_markup("<b>Show text:</b>")
    lbl_show_text.set_halign(Gtk.Align.START)
    lbl_show_text.set_valign(Gtk.Align.CENTER)

    self.chk_show_text = Gtk.CheckButton()
    self.chk_show_text.set_active(self.show_text)

    hbox_show_text = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=20)
    hbox_show_text.append(lbl_show_text)
    hbox_show_text.append(self.chk_show_text)

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
    grid_settings.attach(hbox_show_text, 0, 4, 1, 1)
    grid_settings.attach(hbox_theme, 0, 5, 1, 1)
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
