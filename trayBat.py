import wx
import wx.adv
import os
import ctypes
import webbrowser
import xml.etree.ElementTree as ET

class TrayApp(wx.adv.TaskBarIcon):
    def __init__(self):
        super(TrayApp, self).__init__()

        self.app_name = "trayBat"
        self.app_version = "1.0.1"
        self.light_icon_path = "src/icon_light.png"
        self.dark_icon_path = "src/icon_dark.png"

        self.update_icon()

        self.Bind(wx.adv.EVT_TASKBAR_RIGHT_UP, self.on_right_click)
        self.Bind(wx.adv.EVT_TASKBAR_LEFT_UP, self.on_left_click)

        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.check_and_update, self.timer)
        self.timer.Start(1000)

    def update_icon(self):
        dark_mode = self.is_dark_mode()
        icon_path = self.dark_icon_path if dark_mode else self.light_icon_path
        icon = wx.Icon(icon_path)
        self.SetIcon(icon, f"{self.app_name}")

    def on_right_click(self, event):
        menu = wx.Menu()
        about_action1 = menu.Append(wx.ID_ANY, f"{self.app_name} ver. {self.app_version}")
        about_action1.Enable(False)
        
        about_action2 = menu.Append(wx.ID_ANY, "Assembled by freegen")
        self.Bind(wx.EVT_MENU, self.open_website, about_action2)
        
        menu.AppendSeparator()
        
        quit_action = menu.Append(wx.ID_EXIT, "Exit")
        self.Bind(wx.EVT_MENU, self.quit, quit_action)

        self.PopupMenu(menu)
        menu.Destroy()

    def on_left_click(self, event):
        menu = wx.Menu()
        self.load_menu_from_config(menu)
        self.PopupMenu(menu)
        menu.Destroy()

    def check_and_update(self, event):
        current_mode = self.is_dark_mode()
        if not hasattr(self, 'last_mode') or self.last_mode != current_mode:
            self.update_icon()
        self.last_mode = current_mode

    def is_dark_mode(self):
        try:
            import winreg
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Themes\Personalize") as key:
                value, _ = winreg.QueryValueEx(key, "SystemUsesLightTheme")
                return value == 0
        except Exception as e:
            return False

    def load_menu_from_config(self, menu):
        config_file = os.path.join('include', 'menu_config.xml')
        
        try:
            tree = ET.parse(config_file)
            root = tree.getroot()

            # Обработка элементов меню
            for element in root:
                if element.tag == 'item':
                    label = element.attrib['label']
                    file = element.attrib['file']
                    action = menu.Append(wx.ID_ANY, label)
                    self.Bind(wx.EVT_MENU, lambda evt, file_path=file: self.run_bat_file(file_path), action)
                elif element.tag == 'separator':
                    menu.AppendSeparator()
                elif element.tag == 'section':
                    section_name = element.attrib['name']
                    submenu = wx.Menu()
                    for item in element:
                        if item.tag == 'item':
                            label = item.attrib['label']
                            file = item.attrib['file']
                            action = submenu.Append(wx.ID_ANY, label)
                            self.Bind(wx.EVT_MENU, lambda evt, file_path=file: self.run_bat_file(file_path), action)
                        elif item.tag == 'separator':
                            submenu.AppendSeparator()
                    menu.AppendSubMenu(submenu, section_name)

        except Exception as e:
            print(f"Error loading menu config: {e}")

    def run_bat_file(self, bat_file):
        if os.path.exists(bat_file):
            ctypes.windll.shell32.ShellExecuteW(None, "runas", bat_file, None, None, 0)

    def open_website(self, event):
        webbrowser.open("https://free-gen.github.io")

    def quit(self, event):
        wx.CallAfter(self.Destroy)
        wx.Exit()

def main():
    app = wx.App(False)
    tray_app = TrayApp()
    app.MainLoop()

if __name__ == "__main__":
    main()
