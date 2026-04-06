import gi
from Functions import os

gi.require_version('Gtk', '4.0')
gi.require_version('GdkPixbuf', '2.0')
from gi.repository import Gtk, GdkPixbuf  # noqa

base_dir = os.path.dirname(os.path.realpath(__file__))


class splashScreen(Gtk.Window):
    def __init__(self):
        super().__init__(title='')
        self.set_decorated(False)
        self.set_resizable(False)
        self.set_default_size(600, 400)

        main_vbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=1)
        self.set_child(main_vbox)

        self.image = Gtk.Image()
        pimage = GdkPixbuf.Pixbuf().new_from_file_at_size(
            base_dir + "/images/splash.png", 600, 400
        )
        self.image.set_from_pixbuf(pimage)

        main_vbox.append(self.image)

        self.present()
