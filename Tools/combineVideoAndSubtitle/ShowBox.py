import tkinter as tk
from tkinterdnd2 import *
import re

# reference: https://stackoverflow.com/questions/4836710/is-there-a-built-in-function-for-string-natural-sort
def natural_sort(l): 
    convert = lambda text: int(text) if text.isdigit() else text.lower()
    alphanum_key = lambda key: [convert(c) for c in re.split('([0-9]+)', key)]
    return sorted(l, key=alphanum_key)

def convertDnDEventDataToArr(eventData):
    if eventData[0] == "{":
        return re.findall(r"[{](.*?)[}]", eventData)
    else:
        return eventData.split(" ")


class ShowBox:
    def __init__(self, window):
        self.label = None
        self.listBox = None
        self.removeButton = None
        self.maxCharSize = 0
        self.tkFrame = tk.Frame(window)
        self.listBoxInitSize = 32
        self.listBoxMaxSize = 100
        self.innerArr = []

    def initLabel(self, text, font):
        self.label = tk.Label(self.tkFrame, text=text, font=font)

    def initListBox(self, width, font):
        if width < self.listBoxInitSize:
            width = self.listBoxInitSize
        elif width > self.listBoxMaxSize:
            width = self.listBoxMaxSize
        else:
            self.listBoxInitSize = width

        self.listBox = tk.Listbox(
            self.tkFrame,
            width=width,
            font=font,
        )
        xsc = tk.Scrollbar(self.tkFrame, troughcolor="white", orient=tk.HORIZONTAL)
        ysc = tk.Scrollbar(self.tkFrame, troughcolor="white")
        self.listBox.configure(xscrollcommand=xsc.set, yscrollcommand=ysc.set)

        xsc.config(command=self.listBox.xview)
        ysc.config(command=self.listBox.yview)
        xsc.grid(row=1, column=0, sticky="ews")
        ysc.grid(row=1, column=0, sticky="nse")

    def initRemoveButton(self, text, font, command):
        self.removeButton = tk.Button(
            self.tkFrame, text=text, font=font, command=command
        )

    def setLabelGridLayout(self, row, column, sticky, pady, padx):
        self.label.grid(row=row, column=column, sticky=sticky, pady=pady, padx=padx)

    def setListBoxGridLayout(self, row, column, sticky, pady, padx):
        self.listBox.grid(row=row, column=column, sticky=sticky, pady=pady, padx=padx)

    def setRemoveButtonGridLayout(self, row, column, sticky, pady, padx):
        self.removeButton.grid(
            row=row, column=column, sticky=sticky, pady=pady, padx=padx
        )

    def setFrameGridLayout(self, row, column, sticky, pady, padx):
        self.tkFrame.grid(row=row, column=column, sticky=sticky, pady=pady, padx=padx)

    def configListBoxDnd(self, cb):
        self.listBox.drop_target_register(DND_FILES)
        self.listBox.dnd_bind("<<Drop>>", cb)
    
    def updateInnerArr(self, itemArr):        
        for i in itemArr:
            if i not in self.innerArr:
                self.innerArr.append(i)                    
        self.innerArr = natural_sort(self.innerArr)

    def addArrToListBoxDnd(self, itemArr):
        self.updateInnerArr(itemArr)
        self.listBox.delete(0, tk.END)
        idx = 0
        for i in self.innerArr:
            self.listBox.insert(idx, i)
            self.maxCharSize = len(i) if len(i) > self.maxCharSize else self.maxCharSize
            idx = idx + 1
        if self.maxCharSize > self.listBoxMaxSize:
            self.maxCharSize = self.listBoxMaxSize        

        self.listBox.insert(tk.END, "") # avoid horizon scrollbar cover last file item
        self.listBox.configure(width=self.maxCharSize + 2)

    def removeListBox(self):
        self.listBox.delete(0, tk.END)
        self.listBox.configure(width=self.listBoxInitSize)
        self.innerArr.clear()

    def getInnerArr(self):
        return self.innerArr


def getShowBox(window, labelText, labelFont, listBoxFont, gridRow, removeBtnFont):
    showBox = ShowBox(window)
    showBox.initLabel(text=labelText, font=labelFont)
    showBox.setLabelGridLayout(row=0, column=0, sticky=tk.W, pady=2, padx=20)
    showBox.initListBox(width=32, font=listBoxFont)
    showBox.setListBoxGridLayout(row=1, column=0, sticky=tk.W, pady=2, padx=40)


    def videoRemoveButtonCmd():
        showBox.removeListBox()


    showBox.initRemoveButton(
        text="Remove", font=removeBtnFont, command=videoRemoveButtonCmd
    )
    showBox.setRemoveButtonGridLayout(row=2, column=0, sticky=tk.E, pady=2, padx=2)


    def videoDragCb(event):
        showBox.addArrToListBoxDnd(convertDnDEventDataToArr(eventData=event.data))


    showBox.configListBoxDnd(cb=videoDragCb)
    showBox.setFrameGridLayout(row=gridRow, column=0, sticky=tk.W, pady=2, padx=2)
    return showBox