import sys
import win32api
import pywintypes

def get_res():
    modes = []
    i = 0
    try:
        while True:
            mode = win32api.EnumDisplaySettings(None, i)
            modes.append((
                int(mode.PelsWidth),
                int(mode.PelsHeight),
                int(mode.BitsPerPel),
                ))
            i += 1
    except pywintypes.error:
        pass
    finally:
        for w, h, b in modes:
            print "%d %d %d" % (w, h, b)

def set_res():
    width, height, depth = list(map(int, sys.argv[2:5]))

    mode = win32api.EnumDisplaySettings()
    mode.PelsWidth = width
    mode.PelsHeight = height
    mode.BitsPerPel = depth

    win32api.ChangeDisplaySettings(mode, 0)

if __name__ == "__main__":
    if sys.argv[1] == "set":
        set_res()
    elif sys.argv[1] == "get":
        get_res()
    else:
        exit(-1)

