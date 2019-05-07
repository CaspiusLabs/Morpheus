# Morpheus Chat Bot Assistant Framework v0.1 by Caspius Labs © 2019 - All Rights Reserved.
# GUI based on Chromium web browser full html/css/javascript compatible.
# https://www.caspiuslabs.com


from __future__ import print_function
from infi.systray import SysTrayIcon
from cefpython3 import cefpython as cef
import platform
import os
import sys
import math
import win32api
import win32con
import win32gui
import ctypes


AppName = "░▒▓█[ Morpheus v0.1 ]█▓▒░"
WindowUtils = cef.WindowUtils()


def main():
    check_versions()
    sys.excepthook = cef.ExceptHook

    gui_url = "file:///gui/index.html"

    settings = {
        "user_agent": AppName,
        "product_version": AppName,
        "context_menu": {"enabled": False}
    }

    switches = {
        "disable-gpu": "",
        "disable-web-security": "",
    }

    cef.Initialize(settings=settings, switches=switches)

    window_proc = {
        win32con.WM_CLOSE: close_window,
        win32con.WM_DESTROY: exit_app,
        win32con.WM_SIZE: WindowUtils.OnSize,
        win32con.WM_SETFOCUS: WindowUtils.OnSetFocus,
        win32con.WM_ERASEBKGND: WindowUtils.OnEraseBackground
    }

    window_handle = create_window(title=AppName,
                                  class_name="chromium_window",
                                  width=400,
                                  height=500,
                                  window_proc=window_proc,
                                  icon="chromium.ico")

    window_info = cef.WindowInfo()
    window_info.SetAsChild(window_handle)

    chromium = cef.CreateBrowserSync(window_info=window_info,url=gui_url)

    # chromium.ShowDevTools()

    cef.MessageLoop()
    cef.Shutdown()


def create_window(title, class_name, width, height, window_proc, icon):

    # Register window class
    wndclass = win32gui.WNDCLASS()
    wndclass.hInstance = win32api.GetModuleHandle(None)
    wndclass.lpszClassName = class_name
    wndclass.style = win32con.CS_VREDRAW | win32con.CS_HREDRAW
    wndclass.hbrBackground = win32con.COLOR_WINDOW
    wndclass.hCursor = win32gui.LoadCursor(0, win32con.IDC_ARROW)
    wndclass.lpfnWndProc = window_proc
    atom_class = win32gui.RegisterClass(wndclass)
    assert(atom_class != 0)

    # Center window on screen.
    screenx = win32api.GetSystemMetrics(win32con.SM_CXSCREEN)
    screeny = win32api.GetSystemMetrics(win32con.SM_CYSCREEN)
    xpos = int(math.floor((screenx - width) + 10))
    ypos = int(math.floor((screeny - height) - 30))
    if xpos < 0:
        xpos = 0
    if ypos < 0:
        ypos = 0

    # Create window
    window_style = (win32con.WS_CAPTION | win32con.WS_SYSMENU | win32con.WS_MINIMIZEBOX | win32con.WS_VISIBLE)
    window_handle = win32gui.CreateWindow(class_name, title, window_style,
                                          xpos, ypos, width, height,
                                          0, 0, wndclass.hInstance, None)
    assert(window_handle != 0)

    # Window icon
    icon = os.path.abspath(icon)
    if not os.path.isfile(icon):
        icon = None
    if icon:

        bigx = win32api.GetSystemMetrics(win32con.SM_CXICON)
        bigy = win32api.GetSystemMetrics(win32con.SM_CYICON)
        big_icon = win32gui.LoadImage(0, icon, win32con.IMAGE_ICON,
                                      bigx, bigy,
                                      win32con.LR_LOADFROMFILE)
        smallx = win32api.GetSystemMetrics(win32con.SM_CXSMICON)
        smally = win32api.GetSystemMetrics(win32con.SM_CYSMICON)
        small_icon = win32gui.LoadImage(0, icon, win32con.IMAGE_ICON,
                                        smallx, smally,
                                        win32con.LR_LOADFROMFILE)
        win32api.SendMessage(window_handle, win32con.WM_SETICON,
                             win32con.ICON_BIG, big_icon)
        win32api.SendMessage(window_handle, win32con.WM_SETICON,
                             win32con.ICON_SMALL, small_icon)

    return window_handle


def close_window(window_handle, message, wparam, lparam):
    browser = cef.GetBrowserByWindowHandle(window_handle)
    browser.CloseBrowser(True)

    return win32gui.DefWindowProc(window_handle, message, wparam, lparam)


def exit_app(*_):
    win32gui.PostQuitMessage(0)
    return 0


def check_versions():
    if platform.system() != "Windows":
        print("ERROR: This example is for Windows platform only")
        sys.exit(1)

    ver = cef.GetVersion()
    print("[tutorial.py] CEF Python {ver}".format(ver=ver["version"]))
    print("[tutorial.py] Chromium {ver}".format(ver=ver["chrome_version"]))
    print("[tutorial.py] CEF {ver}".format(ver=ver["cef_version"]))
    print("[tutorial.py] Python {ver} {arch}".format(
           ver=platform.python_version(),
           arch=platform.architecture()[0]))

    assert cef.__version__ >= "57.0", "CEF Python v57.0+ required to run this"


if __name__ == '__main__':
    main()

icon_path = os.path.join(os.path.dirname(__file__), "test.ico")
shutdown_called = False
def on_quit(systray):
    print("Bye")
def do_example(systray):
    print("Example")
def on_about(systray):
    ctypes.windll.user32.MessageBoxW(None, u"This is a test of infi.systray", u"About", 0)

menu_options = (("Example", None, do_example),
                ("About", None, on_about))
systray = SysTrayIcon(icon_path, "Systray Test", menu_options, on_quit)
systray.start()
