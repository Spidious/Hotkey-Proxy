import win32api, win32con, win32gui

def main():
    # get instance handle
    hinstance = win32api.GetModuleHandle()


    # Initialize window class
    wndClass = win32gui.WNDCLASS()
    wndClass.style = win32con.CS_HREDRAW | win32con.CS_VREDRAW
    wndClass.lpfnWndProc = wndProc # Define this
    wndClass.hInstance = hinstance
    wndClass.hIcon = win32gui.LoadIcon(0, 0)
    wndClass.hCursor = win32gui.LoadCursor(0, win32con.IDC_ARROW)
    wndClass.hbrBackground = win32gui.GetStockObject(win32con.WHITE_BRUSH)
    wndClass.lpszClassName = 'SimpleWin32'

    # register window class
    wndClassAtom = None
    try:
        wndClassAtom = win32gui.RegisterClass(wndClass)
    except Exception as e:
        print(e)
        raise e

    hWindow = win32gui.CreateWindow(wndClassAtom, 'Python Win32 Window')


def wndProc(hWnd, message, wParam, lParam):
    return win32gui.DefWindowProc(hWnd, message, wParam, lParam)
    