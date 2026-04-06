# =====================================================
#        Authors Brad Heffernan, Fennec and Erik Dubois
# =====================================================

import gi
import shutil
import GUI
import Functions as fn
import threading
import signal
import os
import sys
from distro import id

gi.require_version("Gtk", "4.0")
gi.require_version("GdkPixbuf", "2.0")

from gi.repository import Gtk, GdkPixbuf, Gdk, GLib  # noqa


class TransparentWindow(Gtk.ApplicationWindow):
    distr = id()

    cmd_shutdown = "systemctl poweroff"
    cmd_restart = "systemctl reboot"
    cmd_suspend = "systemctl suspend"
    cmd_hibernate = "systemctl hibernate"

    if distr == "artix":
        if os.path.isfile("/usr/bin/loginctl"):
            cmd_shutdown = "loginctl poweroff"
            cmd_restart = "loginctl reboot"
            cmd_suspend = "loginctl suspend"
            cmd_hibernate = "loginctl hibernate"

    cmd_lock = 'betterlockscreen -l dim -- --time-str="%H:%M"'
    wallpaper = "/usr/share/archlinux-betterlockscreen/wallpapers/wallpaper.jpg"
    d_buttons = [
        "cancel",
        "shutdown",
        "restart",
        "suspend",
        "hibernate",
        "lock",
        "logout",
    ]
    binds = {
        "lock": "K",
        "restart": "R",
        "shutdown": "S",
        "suspend": "U",
        "hibernate": "H",
        "logout": "L",
        "cancel": "Escape",
        "settings": "P",
    }
    theme = "candy"
    hover = "#ffffff"
    icon = 96
    font = 11
    buttons = None
    active = False
    opacity = 0.8
    main_icon_size = 96
    aux_icon_size = 48

    def __init__(self, app):
        super().__init__(application=app, title="ArchLinux Logout")

        self.set_decorated(False)

        self.connect("close-request", self.on_close)

        key_controller = Gtk.EventControllerKey()
        key_controller.set_propagation_phase(Gtk.PropagationPhase.CAPTURE)
        key_controller.connect("key-pressed", self.on_keypress)
        self.add_controller(key_controller)

        self.connect("notify::fullscreened", self.on_window_state_changed)
        self.__is_fullscreen = False

        if not fn.os.path.isdir(fn.home + "/.config/archlinux-logout"):
            fn.os.mkdir(fn.home + "/.config/archlinux-logout")

        if not fn.os.path.isfile(
            fn.home + "/.config/archlinux-logout/archlinux-logout.conf"
        ):
            shutil.copy(
                fn.root_config,
                fn.home + "/.config/archlinux-logout/archlinux-logout.conf",
            )

        self.width = 0
        self.display = Gdk.Display.get_default()

        fn.get_config(self, Gdk, Gtk, fn.config)

        if self.buttons is None or self.buttons == [""]:
            self.buttons = self.d_buttons

        self.main_icon_size = self.icon
        self.aux_icon_size = max(32, self.icon // 2)

        self._apply_background_css()

        self.display_on_monitor()

        GUI.GUI(self, Gtk, GdkPixbuf, fn.working_dir, fn.os, Gdk, fn)

        self.set_focusable(True)
        self.grab_focus()

        if not fn.os.path.isfile("/tmp/archlinux-logout.lock"):
            with open("/tmp/archlinux-logout.lock", "w") as f:
                f.write("")

        self.present()

    def _apply_background_css(self):
        css = f"window {{ background-color: rgba(0, 0, 0, {self.opacity}); }}"
        provider = Gtk.CssProvider()
        provider.load_from_data(css.encode())
        Gtk.StyleContext.add_provider_for_display(
            self.display,
            provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION + 1,
        )

    def _cleanup_runtime_files(self):
        for path in ("/tmp/archlinux-logout.lock", "/tmp/archlinux-logout.pid"):
            try:
                fn.os.unlink(path)
            except FileNotFoundError:
                pass
            except Exception:
                pass

    def _set_scaled_icon_sizes(self, geometry):
        monitor_min = min(geometry.width, geometry.height)
        scaled_main = int(round(monitor_min * 0.044))
        scaled_aux = int(round(monitor_min * 0.03))
        self.main_icon_size = max(48, min(160, scaled_main))
        self.aux_icon_size = max(32, min(72, scaled_aux))

    def display_on_monitor(self):
        print("#### Archlinux Logout ####")
        desktop = fn._detect_desktop()
        print(f"[DEBUG]: Desktop session = {desktop}")

        session_type = os.environ.get("XDG_SESSION_TYPE", "").lower()

        if session_type == "wayland":
            print("[WARN]: Session type = wayland, mouse position can't be tracked")
            self.display_on_default()
            return

        if session_type == "x11":
            print("[DEBUG]: Session type = x11")
            try:
                import subprocess

                result = subprocess.run(
                    ["xdotool", "getmouselocation", "--shell"],
                    capture_output=True,
                    text=True,
                    timeout=1,
                )
                if result.returncode == 0:
                    lines = result.stdout.strip().split("\n")
                    x_vals = [line.split("=")[1] for line in lines if line.startswith("X=")]
                    y_vals = [line.split("=")[1] for line in lines if line.startswith("Y=")]
                    if x_vals and y_vals:
                        x = int(x_vals[0])
                        y = int(y_vals[0])
                        print(f"[DEBUG]: Mouse position x={x} y={y}")
                        monitor = self._get_monitor_at_point(x, y)
                        if monitor:
                            geometry = monitor.get_geometry()
                            print(
                                f"[DEBUG]: Monitor: Primary={monitor.is_primary()}, "
                                f"Dimension={geometry.width}x{geometry.height}"
                            )
                            self.set_size_request(geometry.width, geometry.height)
                            self.fullscreen_on_monitor(monitor)
                            return
            except Exception as e:
                print(f"[DEBUG]: Could not get mouse position via xdotool: {e}")

        self.display_on_default()

    def _get_monitor_at_point(self, x, y):
        monitors = self.display.get_monitors()
        for i in range(monitors.get_n_items()):
            monitor = monitors.get_item(i)
            geom = monitor.get_geometry()
            if (
                geom.x <= x < geom.x + geom.width
                and geom.y <= y < geom.y + geom.height
            ):
                return monitor
        return monitors.get_item(0)

    def display_on_default(self):
        monitors = self.display.get_monitors()
        monitor = monitors.get_item(0)
        if monitor:
            geometry = monitor.get_geometry()
            print("[DEBUG]: Showing on first monitor")
            print(f"[DEBUG]: Dimension: {geometry.width}x{geometry.height}")
            self.set_size_request(geometry.width, geometry.height)
            self.fullscreen_on_monitor(monitor)

    def on_save_clicked(self, widget):
        try:
            with open(
                fn.home + "/.config/archlinux-logout/archlinux-logout.conf", "r"
            ) as f:
                lines = f.readlines()

            pos_opacity = fn._get_position(lines, "opacity")
            pos_size = fn._get_position(lines, "icon_size")
            pos_theme = fn._get_position(lines, "theme=")
            pos_font = fn._get_position(lines, "font_size=")

            lines[pos_opacity] = "opacity=" + str(int(self.hscale.get_value())) + "\n"
            lines[pos_size] = "icon_size=" + str(int(self.icons.get_value())) + "\n"
            lines[pos_theme] = "theme=" + self.themes.get_active_text() + "\n"
            lines[pos_font] = "font_size=" + str(int(self.fonts.get_value())) + "\n"

            with open(
                fn.home + "/.config/archlinux-logout/archlinux-logout.conf", "w"
            ) as f:
                f.writelines(lines)
            self.popover.popdown()
        except Exception:
            fn.os.unlink(fn.home + "/.config/archlinux-logout/archlinux-logout.conf")
            if not fn.os.path.isfile(
                fn.home + "/.config/archlinux-logout/archlinux-logout.conf"
            ):
                shutil.copy(
                    fn.root_config,
                    fn.home + "/.config/archlinux-logout/archlinux-logout.conf",
                )
            with open(
                fn.home + "/.config/archlinux-logout/archlinux-logout.conf", "r"
            ) as f:
                lines = f.readlines()

            pos_opacity = fn._get_position(lines, "opacity")
            pos_size = fn._get_position(lines, "icon_size")
            pos_theme = fn._get_position(lines, "theme=")
            pos_font = fn._get_position(lines, "font_size=")

            lines[pos_opacity] = "opacity=" + str(int(self.hscale.get_value())) + "\n"
            lines[pos_size] = "icon_size=" + str(int(self.icons.get_value())) + "\n"
            lines[pos_theme] = "theme=" + self.themes.get_active_text() + "\n"
            lines[pos_font] = "font_size=" + str(int(self.fonts.get_value())) + "\n"

            with open(
                fn.home + "/.config/archlinux-logout/archlinux-logout.conf", "w"
            ) as f:
                f.writelines(lines)
            self.popover.popdown()

    def on_mouse_in(self, widget, data):
        widget.set_cursor(Gdk.Cursor.new_from_name("pointer"))

        if data == self.binds.get("shutdown"):
            psh = GdkPixbuf.Pixbuf().new_from_file_at_size(
                fn.os.path.join(
                    fn.working_dir, "themes/" + self.theme + "/shutdown_blur.svg"
                ),
                self.main_icon_size,
                self.main_icon_size,
            )
            fn.set_widget_pixbuf(self.imagesh, psh)
            self.lbl1.set_markup(
                f'<span size="{str(self.font)}000" foreground="{self.hover}">Shutdown ({data})</span>'
            )
        elif data == self.binds.get("restart"):
            pr = GdkPixbuf.Pixbuf().new_from_file_at_size(
                fn.os.path.join(
                    fn.working_dir, "themes/" + self.theme + "/restart_blur.svg"
                ),
                self.main_icon_size,
                self.main_icon_size,
            )
            fn.set_widget_pixbuf(self.imager, pr)
            self.lbl2.set_markup(
                f'<span size="{str(self.font)}000" foreground="{self.hover}">Reboot ({data})</span>'
            )
        elif data == self.binds.get("suspend"):
            ps = GdkPixbuf.Pixbuf().new_from_file_at_size(
                fn.os.path.join(
                    fn.working_dir, "themes/" + self.theme + "/suspend_blur.svg"
                ),
                self.main_icon_size,
                self.main_icon_size,
            )
            fn.set_widget_pixbuf(self.images, ps)
            self.lbl3.set_markup(
                f'<span size="{str(self.font)}000" foreground="{self.hover}">Suspend ({data})</span>'
            )
        elif data == self.binds.get("lock"):
            plk = GdkPixbuf.Pixbuf().new_from_file_at_size(
                fn.os.path.join(
                    fn.working_dir, "themes/" + self.theme + "/lock_blur.svg"
                ),
                self.main_icon_size,
                self.main_icon_size,
            )
            fn.set_widget_pixbuf(self.imagelk, plk)
            self.lbl4.set_markup(
                f'<span size="{str(self.font)}000" foreground="{self.hover}">Lock ({data})</span>'
            )
        elif data == self.binds.get("logout"):
            plo = GdkPixbuf.Pixbuf().new_from_file_at_size(
                fn.os.path.join(
                    fn.working_dir, "themes/" + self.theme + "/logout_blur.svg"
                ),
                self.main_icon_size,
                self.main_icon_size,
            )
            fn.set_widget_pixbuf(self.imagelo, plo)
            self.lbl5.set_markup(
                f'<span size="{str(self.font)}000" foreground="{self.hover}">Logout ({data})</span>'
            )
        elif data == self.binds.get("cancel"):
            plo = GdkPixbuf.Pixbuf().new_from_file_at_size(
                fn.os.path.join(
                    fn.working_dir, "themes/" + self.theme + "/cancel_blur.svg"
                ),
                self.main_icon_size,
                self.main_icon_size,
            )
            fn.set_widget_pixbuf(self.imagec, plo)
            self.lbl6.set_markup(
                f'<span size="{str(self.font)}000" foreground="{self.hover}">Cancel ({data})</span>'
            )
        elif data == self.binds.get("hibernate"):
            plo = GdkPixbuf.Pixbuf().new_from_file_at_size(
                fn.os.path.join(
                    fn.working_dir, "themes/" + self.theme + "/hibernate_blur.svg"
                ),
                self.main_icon_size,
                self.main_icon_size,
            )
            fn.set_widget_pixbuf(self.imageh, plo)
            self.lbl7.set_markup(
                f'<span size="{str(self.font)}000" foreground="{self.hover}">Hibernate ({data})</span>'
            )
        elif data == self.binds.get("settings"):
            pset = GdkPixbuf.Pixbuf().new_from_file_at_size(
                fn.os.path.join(fn.working_dir, "configure_blur.svg"),
                self.aux_icon_size,
                self.aux_icon_size,
            )
            fn.set_widget_pixbuf(self.imageset, pset)
        elif data == "light":
            pset = GdkPixbuf.Pixbuf().new_from_file_at_size(
                fn.os.path.join(fn.working_dir, "light_blur.svg"),
                self.aux_icon_size,
                self.aux_icon_size,
            )
            fn.set_widget_pixbuf(self.imagelig, pset)

    def on_mouse_out(self, widget, data):
        widget.set_cursor(None)

        if not self.active:
            if data == self.binds.get("shutdown"):
                psh = GdkPixbuf.Pixbuf().new_from_file_at_size(
                    fn.os.path.join(
                        fn.working_dir, "themes/" + self.theme + "/shutdown.svg"
                    ),
                    self.main_icon_size,
                    self.main_icon_size,
                )
                fn.set_widget_pixbuf(self.imagesh, psh)
                self.lbl1.set_markup(
                    f'<span size="{str(self.font)}000">Shutdown ({data})</span>'
                )
            elif data == self.binds.get("restart"):
                pr = GdkPixbuf.Pixbuf().new_from_file_at_size(
                    fn.os.path.join(
                        fn.working_dir, "themes/" + self.theme + "/restart.svg"
                    ),
                    self.main_icon_size,
                    self.main_icon_size,
                )
                fn.set_widget_pixbuf(self.imager, pr)
                self.lbl2.set_markup(
                    f'<span size="{str(self.font)}000">Reboot ({data})</span>'
                )
            elif data == self.binds.get("suspend"):
                ps = GdkPixbuf.Pixbuf().new_from_file_at_size(
                    fn.os.path.join(
                        fn.working_dir, "themes/" + self.theme + "/suspend.svg"
                    ),
                    self.main_icon_size,
                    self.main_icon_size,
                )
                fn.set_widget_pixbuf(self.images, ps)
                self.lbl3.set_markup(
                    f'<span size="{str(self.font)}000">Suspend ({data})</span>'
                )
            elif data == self.binds.get("lock"):
                plk = GdkPixbuf.Pixbuf().new_from_file_at_size(
                    fn.os.path.join(
                        fn.working_dir, "themes/" + self.theme + "/lock.svg"
                    ),
                    self.main_icon_size,
                    self.main_icon_size,
                )
                fn.set_widget_pixbuf(self.imagelk, plk)
                self.lbl4.set_markup(
                    f'<span size="{str(self.font)}000">Lock ({data})</span>'
                )
            elif data == self.binds.get("logout"):
                plo = GdkPixbuf.Pixbuf().new_from_file_at_size(
                    fn.os.path.join(
                        fn.working_dir, "themes/" + self.theme + "/logout.svg"
                    ),
                    self.main_icon_size,
                    self.main_icon_size,
                )
                fn.set_widget_pixbuf(self.imagelo, plo)
                self.lbl5.set_markup(
                    f'<span size="{str(self.font)}000">Logout ({data})</span>'
                )
            elif data == self.binds.get("cancel"):
                plo = GdkPixbuf.Pixbuf().new_from_file_at_size(
                    fn.os.path.join(
                        fn.working_dir, "themes/" + self.theme + "/cancel.svg"
                    ),
                    self.main_icon_size,
                    self.main_icon_size,
                )
                fn.set_widget_pixbuf(self.imagec, plo)
                self.lbl6.set_markup(
                    f'<span size="{str(self.font)}000">Cancel ({data})</span>'
                )
            elif data == self.binds.get("hibernate"):
                plo = GdkPixbuf.Pixbuf().new_from_file_at_size(
                    fn.os.path.join(
                        fn.working_dir, "themes/" + self.theme + "/hibernate.svg"
                    ),
                    self.main_icon_size,
                    self.main_icon_size,
                )
                fn.set_widget_pixbuf(self.imageh, plo)
                self.lbl7.set_markup(
                    f'<span size="{str(self.font)}000">Hibernate ({data})</span>'
                )
            elif data == self.binds.get("settings"):
                pset = GdkPixbuf.Pixbuf().new_from_file_at_size(
                    fn.os.path.join(fn.working_dir, "configure.svg"),
                    self.aux_icon_size,
                    self.aux_icon_size,
                )
                fn.set_widget_pixbuf(self.imageset, pset)
            elif data == "light":
                pset = GdkPixbuf.Pixbuf().new_from_file_at_size(
                    fn.os.path.join(fn.working_dir, "light.svg"),
                    self.aux_icon_size,
                    self.aux_icon_size,
                )
                fn.set_widget_pixbuf(self.imagelig, pset)

    def on_click(self, widget, data):
        self.click_button(widget, data)

    def on_window_state_changed(self, window, pspec):
        self.__is_fullscreen = window.is_fullscreen()

    def on_keypress(self, controller, keyval, keycode, state):
        if keyval == Gdk.KEY_Escape:
            self.click_button(None, self.binds.get("cancel"))
            return True

        self.shortcut_keys = [
            self.binds.get("cancel"),
            self.binds.get("shutdown"),
            self.binds.get("restart"),
            self.binds.get("suspend"),
            self.binds.get("logout"),
            self.binds.get("lock"),
            self.binds.get("hibernate"),
            self.binds.get("settings"),
        ]

        for key in self.shortcut_keys:
            if keyval == Gdk.keyval_to_lower(Gdk.keyval_from_name(key)):
                self.click_button(None, key)
                return True

        return False

    def click_button(self, widget, data=None):
        if data != self.binds.get("settings") and data != "light":
            self.active = True
            fn.button_toggled(self, data)
            fn.button_active(self, data, GdkPixbuf)

        if data == self.binds.get("logout"):
            command = fn._get_logout()
            if not command:
                self.message_box(
                    "No logout command could be detected for this desktop session.",
                    "Logout command not found",
                )
                self.active = False
                return
            self._cleanup_runtime_files()
            self.__exec_cmd(command)
            self.get_application().quit()

        elif data == self.binds.get("restart"):
            self._cleanup_runtime_files()
            self.__exec_cmd(self.cmd_restart)
            self.get_application().quit()

        elif data == self.binds.get("shutdown"):
            self._cleanup_runtime_files()
            self.__exec_cmd(self.cmd_shutdown)
            self.get_application().quit()

        elif data == self.binds.get("suspend"):
            self._cleanup_runtime_files()
            self.__exec_cmd(self.cmd_suspend)
            self.get_application().quit()

        elif data == self.binds.get("hibernate"):
            self._cleanup_runtime_files()
            self.__exec_cmd(self.cmd_hibernate)
            self.get_application().quit()

        elif data == self.binds.get("lock"):
            if self.cmd_lock.startswith("betterlockscreen") and not fn.os.path.isdir(
                fn.home + "/.cache/betterlockscreen"
            ):
                if fn.os.path.isfile(self.wallpaper):
                    self.lbl_stat.set_markup(
                        '<span size="x-large"><b>Caching lockscreen images for a faster locking next time</b></span>'
                    )
                    t = threading.Thread(target=fn.cache_bl, args=(self, GLib))
                    t.daemon = True
                    t.start()
                else:
                    self.lbl_stat.set_markup(
                        '<span size="x-large"><b>Choose a wallpaper with archlinux-betterlockscreen</b></span>'
                    )
                    self.Ec.set_sensitive(True)
                    self.active = False
            else:
                self._cleanup_runtime_files()
                self.__exec_cmd(self.cmd_lock)
                self.get_application().quit()

        elif data == self.binds.get("settings"):
            self.themes.grab_focus()
            self.popover.popup()

        elif data == "light":
            self.popover2.popup()

        else:
            self._cleanup_runtime_files()
            self.get_application().quit()

    def __exec_cmd(self, cmdline):
        fn.os.system(cmdline)

    def on_close(self, widget):
        self._cleanup_runtime_files()
        self.get_application().quit()
        return False

    def message_box(self, message, title):
        dialog = Gtk.AlertDialog(message=title, detail=message)
        dialog.show(self)


class ArchLinuxLogoutApp(Gtk.Application):
    def __init__(self):
        super().__init__(application_id="org.archlinux.logout")

    def do_activate(self):
        TransparentWindow(self)


def signal_handler(sig, frame):
    print("\nArchLinux-Logout is Closing.")
    for path in ("/tmp/archlinux-logout.lock", "/tmp/archlinux-logout.pid"):
        try:
            fn.os.unlink(path)
        except Exception:
            pass
    app = Gtk.Application.get_default()
    if app:
        app.quit()


if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)
    if not fn.os.path.isfile("/tmp/archlinux-logout.lock"):
        try:
            with open("/tmp/archlinux-logout.pid", "w") as f:
                f.write(str(fn.os.getpid()))
        except PermissionError:
            print("[WARN]: Could not write /tmp/archlinux-logout.pid (permission denied)")
        app = ArchLinuxLogoutApp()
        app.run(sys.argv)
    else:
        print(
            "ArchLinux-logout did not close properly. Remove /tmp/archlinux-logout.lock with sudo."
        )
