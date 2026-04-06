#!/usr/bin/env python3

# =================================================================
# =                  Author: Brad Heffernan                       =
# =================================================================

import gi
import Functions as fn
import GUI
import Support
import threading as th
import webbrowser
import sys

gi.require_version('Gtk', '4.0')
gi.require_version('GdkPixbuf', '2.0')
from gi.repository import Gtk, GdkPixbuf, Gdk, GLib, Gio  # noqa


class Main(Gtk.ApplicationWindow):
    def __init__(self, app):
        super().__init__(application=app, title="ArchLinux BetterLockScreen")
        self.set_default_size(1100, 700)
        self.connect("close-request", self.close)

        self.timeout_id = None
        self.image_path = None

        if not fn.os.path.isdir(fn.config):
            fn.os.mkdir(fn.config)

        if not fn.os.path.isfile(fn.config + fn.settings):
            with open(fn.config + fn.settings, "w") as f:
                f.write("path=")

        self.loc = Gtk.Entry()
        self.search = Gtk.Entry()
        self.status = Gtk.Label(label="")
        self.hbox3 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        scrolled = Gtk.ScrolledWindow()
        scrolled.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)

        self.fb = Gtk.FlowBox()
        self.fb.set_valign(Gtk.Align.START)
        self.fb.set_min_children_per_line(1)
        self.fb.set_max_children_per_line(30)
        self.fb.set_selection_mode(Gtk.SelectionMode.SINGLE)
        self.fb.connect("child-activated", self.on_item_clicked)

        scrolled.set_child(self.fb)
        self.hbox3.append(scrolled)
        scrolled.set_hexpand(True)
        scrolled.set_vexpand(True)

        GUI.GUI(self, Gtk, GdkPixbuf, Gdk, th, fn)

        with open("/tmp/archlinux-betterlock.lock", "w") as f:
            f.write("")

        # Defer flowbox loading so the window is shown first
        GLib.idle_add(self._load_initial_flowbox)

    def _load_initial_flowbox(self):
        t = th.Thread(target=self.create_flowbox, args=(self.loc.get_text(), False))
        t.daemon = True
        t.start()
        return False

    def on_default_clicked(self, widget, fb):
        self._clear_flowbox()
        t = th.Thread(target=self.create_flowbox, args=(self.loc.get_text(), True))
        t.daemon = True
        t.start()

    def on_support_clicked(self, widget):
        sup = Support.Support(self)
        sup.present()

    def on_apply_clicked(self, widget):
        if self.image_path is None:
            fn.show_in_app_notification(self, "You need to select an image first")
        else:
            self.btnset.set_sensitive(False)
            self.status.set_text("creating lockscreen images....wait for the message at the top")
            t = th.Thread(target=self.set_lockscreen)
            t.daemon = True
            t.start()

    def set_lockscreen(self):
        command = ["betterlockscreen", "-u", self.image_path,
                   "--blur", str(int(self.blur.get_value()) / 100)]
        try:
            fn.subprocess.call(command, shell=False)
            fn.show_in_app_notification(self, "Lockscreen set successfully")
            GLib.idle_add(self.btnset.set_sensitive, True)
            GLib.idle_add(self.status.set_text, "")
        except Exception:
            GLib.idle_add(self.status.set_text, "ERROR: is betterlockscreen installed?")
            GLib.idle_add(self.btnset.set_sensitive, True)

    def on_item_clicked(self, flowbox, child):
        image = child.get_child()
        if image:
            self.image_path = image.get_name()

    def on_load_clicked(self, widget, fb):
        self._clear_flowbox()
        t = th.Thread(target=self.create_flowbox, args=(self.loc.get_text(), False))
        t.daemon = True
        t.start()

    def on_search_clicked(self, widget):
        self._clear_flowbox()
        t = th.Thread(target=self.create_flowbox, args=(self.loc.get_text(), False))
        t.daemon = True
        t.start()

    def _clear_flowbox(self):
        while True:
            child = self.fb.get_child_at_index(0)
            if child is None:
                break
            self.fb.remove(child)

    def on_browse_clicked(self, widget):
        dialog = Gtk.FileDialog(title="Please choose a folder")
        dialog.set_initial_folder(Gio.File.new_for_path(fn.home))
        dialog.select_folder(self, None, self._on_browse_response)

    def _on_browse_response(self, dialog, result):
        try:
            folder = dialog.select_folder_finish(result)
            path = folder.get_path()
            self.loc.set_text(path)
            with open(fn.config + fn.settings, "w") as f:
                f.write("path=" + path)
        except Exception as e:
            print(f"[DEBUG]: Folder dialog: {e}")

    def create_flowbox(self, text, default):
        if not default:
            paths = fn.get_saved_path()
            if len(paths) < 1:
                if len(text) < 1:
                    paths = "/usr/share/archlinux-betterlockscreen/wallpapers/"
                    if not fn.os.path.isdir(paths):
                        return 0
                else:
                    paths = text
        else:
            paths = "/usr/share/archlinux-betterlockscreen/wallpapers/"
            if not fn.os.path.isdir(paths):
                return 0

        if paths.endswith("/"):
            paths = paths[:-1]

        if not fn.os.path.isdir(paths):
            GLib.idle_add(self.status.set_text, "That directory not found!")
            return 0
        try:
            ext = [".png", ".jpg", ".jpeg"]
            images = [x for x in fn.os.listdir(paths) for j in ext
                      if j in x.lower() if self.search.get_text() in x]
            GLib.idle_add(self.status.set_text, "Loading images...")
            for image in images:
                pb = GdkPixbuf.Pixbuf().new_from_file_at_size(
                    paths + "/" + image, 320, 180)
                pimage = Gtk.Picture()
                pimage.set_name(paths + "/" + image)
                pimage.set_pixbuf(pb)
                pimage.set_can_shrink(False)
                pimage.set_content_fit(Gtk.ContentFit.FILL)
                pimage.set_size_request(320, 180)
                GLib.idle_add(self.fb.append, pimage)
        except Exception as e:
            print(e)
        GLib.idle_add(self.status.set_text, "")

    def on_social_clicked(self, widget, link):
        t = th.Thread(target=self.weblink, args=(link,))
        t.daemon = True
        t.start()

    def weblink(self, link):
        webbrowser.open_new_tab(link)

    def tooltip_callback(self, widget, x, y, keyboard_mode, tooltip, text):
        tooltip.set_text(text)
        return True

    def close(self, widget):
        try:
            fn.os.unlink("/tmp/archlinux-betterlock.lock")
        except Exception:
            pass
        self.get_application().quit()
        return False


class BetterLockScreenApp(Gtk.Application):
    def __init__(self):
        super().__init__(application_id="org.archlinux.betterlockscreen")

    def do_activate(self):
        if not fn.os.path.isfile("/tmp/archlinux-betterlock.lock"):
            try:
                with open("/tmp/archlinux-betterlock.pid", "w") as f:
                    f.write(str(fn.os.getpid()))
            except PermissionError:
                print("[WARN]: Could not write /tmp/archlinux-betterlock.pid")
            win = Main(self)
            win.present()
        else:
            dialog = Gtk.AlertDialog(
                message="Lock File Found",
                detail=(
                    "The lock file has been found. This indicates there is already "
                    "an instance of ArchLinux Betterlockscreen GUI running.\n"
                    "Click Yes to remove the lock file and try running again."
                ),
                buttons=["No", "Yes"],
                default_button=1,
                cancel_button=0,
            )
            dialog.choose(None, None, self._on_lock_dialog_response)

    def _on_lock_dialog_response(self, dialog, result):
        try:
            button = dialog.choose_finish(result)
        except Exception:
            return
        if button == 1:  # Yes
            pid = ""
            try:
                with open("/tmp/archlinux-betterlock.pid", "r") as f:
                    pid = f.read().strip()
            except Exception:
                pass
            if pid and fn.checkIfProcessRunning(int(pid)):
                alert = Gtk.AlertDialog(
                    message="Application Running!",
                    detail="You first need to close the existing application",
                )
                alert.show(None)
            else:
                fn.os.unlink("/tmp/archlinux-betterlock.lock")
                # Re-activate now that lock is cleared
                self.do_activate()


if __name__ == "__main__":
    app = BetterLockScreenApp()
    app.run(sys.argv)
