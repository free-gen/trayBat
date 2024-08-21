import wx
import wx.adv
import os
import ctypes
import webbrowser
import json

class TrayApp(wx.adv.TaskBarIcon):
    def __init__(self):
        super(TrayApp, self).__init__()

        self.app_name = "trayBat"
        self.app_version = "1.0"
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
        self.load_bat_files(menu)
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
        except Exception:
            return False

    def load_menu_config(self, config_path):
        with open(config_path, 'r') as file:
            return json.load(file)

    def load_bat_files(self, menu):
        config_path = os.path.join(os.getcwd(), 'include', 'menu_config.json')
        if not os.path.exists(config_path):
            print(f"Config file not found: {config_path}")
            return
        
        config = self.load_menu_config(config_path)
        bat_folder = os.path.join(os.getcwd(), 'include')

        if not os.path.exists(bat_folder):
            print(f"Directory 'include' does not exist at path: {bat_folder}")
            return

        for item in config.get("items", []):
            if item["type"] == "item":
                action_text = item.get("label", "")
                bat_file_name = item.get("file", "")
                bat_file_path = os.path.join(bat_folder, bat_file_name)
                
                if os.path.exists(bat_file_path):
                    action = menu.Append(wx.ID_ANY, action_text)
                    self.Bind(wx.EVT_MENU, lambda evt, file=bat_file_path: self.run_bat_file(file), action)
                else:
                    print(f"Batch file not found: {bat_file_path}")

        for section in config.get("sections", []):
            section_name = section.get("name", "")
            section_menu = wx.Menu()
            for item in section.get("items", []):
                if item["type"] == "item":
                    action_text = item.get("label", "")
                    bat_file_name = item.get("file", "")
                    bat_file_path = os.path.join(bat_folder, bat_file_name)
                    
                    if os.path.exists(bat_file_path):
                        action = section_menu.Append(wx.ID_ANY, action_text)
                        self.Bind(wx.EVT_MENU, lambda evt, file=bat_file_path: self.run_bat_file(file), action)
                    else:
                        print(f"Batch file not found: {bat_file_path}")
            if section_menu.GetMenuItemCount() > 0:
                menu.AppendSubMenu(section_menu, section_name)

    def run_bat_file(self, bat_file):
        if os.path.exists(bat_file):
            ctypes.windll.shell32.ShellExecuteW(None, "runas", bat_file, None, None, 0)
        else:
            print(f"Batch file not found: {bat_file}")

    def open_website(self, event):
        webbrowser.open("https://github.com/free-gen/traybat")

    def quit(self, event):
        wx.CallAfter(self.Destroy)
        wx.Exit()

def main():
    app = wx.App(False)
    tray_app = TrayApp()
    app.MainLoop()

if __name__ == "__main__":
    main()
