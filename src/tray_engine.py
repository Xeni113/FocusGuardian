import pystray
from pystray import MenuItem as item
from PIL import Image
import threading
import os


def create_image():
    return Image.open("docs/assets/icon.png")


def quit_app(icon):
    icon.stop()
    os._exit(0)


def start_tray():
    icon = pystray.Icon(
        "FocusGuardian",
        create_image(),
        "FocusGuardian",
        menu=pystray.Menu(
            item("Exit", quit_app)
        )
    )

    threading.Thread(
        target=icon.run,
        daemon=True
    ).start()