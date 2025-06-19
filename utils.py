import ctypes
from ctypes import wintypes
from windows_toasts import Toast, WindowsToaster

class WindowsAPIBS():
    def is_desktop_visible(self):
        try:
            desktop_hwnd = ctypes.windll.user32.GetDesktopWindow()
            foreground_hwnd = ctypes.windll.user32.GetForegroundWindow()

            if not foreground_hwnd:
                return True
            
            class_name = ctypes.create_unicode_buffer(256)
            ctypes.windll.user32.GetClassNameW(foreground_hwnd, class_name, 256)
            desktop_classes = ['Progman', 'WorkerW', 'Shell_TrayWnd']

            if class_name.value in desktop_classes:
                return True
            
            if ctypes.windll.user32.IsIconic(foreground_hwnd):
                return True
            
            desktop_point = wintypes.POINT(100, 100)
            hwnd_at_point = ctypes.windll.user32.WindowFromPoint(desktop_point)
            
            root_hwnd = hwnd_at_point
            while True:
                parent = ctypes.windll.user32.GetParent(root_hwnd)
                if parent == 0:
                    break
                root_hwnd = parent
            
            if root_hwnd == desktop_hwnd:
                return True
                
            return False
            
        except Exception:
            return False
    
    def check_desktop_visibility(self):
        if self.is_desktop_visible():
            if not self.isVisible():
                self.show()
        else:
            if self.isVisible():
                self.hide()
                
                

def show_toast(title="Email Alert", message="You have a new high priority email!"):
    toaster = WindowsToaster(title)
    newToast = Toast()
    newToast.text_fields = [message]
    toaster.show_toast(newToast)