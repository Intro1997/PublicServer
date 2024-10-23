import tkinter as tk
from tkinter.filedialog import askdirectory
from tkinterdnd2 import *
import ctypes
import platform
from Core import core
import threading
from ShowBox import getShowBox

# https://stackoverflow.com/questions/25427347/how-to-install-and-use-tkdnd-with-python-tkinter-on-osx

WIN_LOGICAL_WIDTH = 800
WIN_LOGICAL_HEIGHT = 900
GLOBAL_FONT = "Consolas"


def getRatio():
    if platform.system() == "Windows":
        ctypes.windll.shcore.SetProcessDpiAwareness(1)
        return ctypes.windll.shcore.GetScaleFactorForDevice(0) / 100
    return 1.0


window = TkinterDnD.Tk()
window.title = "add subtitle to video"
pixRatio = getRatio()
window.tk.call("tk", "scaling", pixRatio)

winWidth = int(WIN_LOGICAL_WIDTH * pixRatio)
winHeight = int(WIN_LOGICAL_HEIGHT * pixRatio)


window.geometry(f"{winWidth}x{winHeight}")

videoShowBox = getShowBox(
    window=window,
    labelText="video files:",
    labelFont=(GLOBAL_FONT, 12),
    listBoxFont=(GLOBAL_FONT, 14),
    gridRow=0,
    removeBtnFont=(GLOBAL_FONT, 12),
)
subtitleShowBox = getShowBox(
    window=window,
    labelText="subtitle files:",
    labelFont=(GLOBAL_FONT, 12),
    listBoxFont=(GLOBAL_FONT, 14),
    gridRow=1,
    removeBtnFont=(GLOBAL_FONT, 12),
)

# window.rowconfigure(0, weight=2)
# window.rowconfigure(1, weight=2)
# window.rowconfigure(2, weight=2)
# window.rowconfigure(3, weight=1)
# window.columnconfigure(0, weight=1)
# window.columnconfigure(1, weight=1)


resPath = tk.StringVar()
tk.Label(window, text="res path:", font=(GLOBAL_FONT, 12)).grid(
    row=2, column=0, sticky="W", padx=10 * pixRatio
)
tk.Entry(window, textvariable=resPath, font=(GLOBAL_FONT, 12), width=80).grid(
    row=3, column=0, sticky="W", padx=20 * pixRatio, pady=0
)


def selectPath():
    resPath.set(askdirectory())


tk.Button(window, text="select path", command=selectPath, font=(GLOBAL_FONT, 12)).grid(
    row=3, column=0, sticky="W", padx=680 * pixRatio
)

stateMsg = tk.Text(window, font=(GLOBAL_FONT, 12), width=90, height=15)
stateMsg.grid(row=4, column=0, sticky="W", padx=20 * pixRatio, pady=40 * pixRatio)

def coreFinishCb():
    startButton["state"] = "normal"

def startButtonCmd():
    stateMsg.config(state=tk.NORMAL)
    stateMsg.delete("1.0", tk.END)
    stateMsg.config(state=tk.DISABLED)
    startButton["state"] = "disabled"
    threading.Thread(
        target=core,
        args=(
            videoShowBox.getInnerArr(),
            subtitleShowBox.getInnerArr(),
            resPath.get(),
            stateMsg,
            coreFinishCb,
        ),
    ).start()


startButton = tk.Button(
    window, text="Start!", font=(GLOBAL_FONT, 12), command=startButtonCmd
)
startButton.grid(row=5, column=0, sticky="W", padx=pixRatio * 15, pady=pixRatio * 15)
window.mainloop()
