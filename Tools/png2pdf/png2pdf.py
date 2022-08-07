from curses.ascii import isdigit
from cv2 import sort
# refer https://stackoverflow.com/questions/4836710/is-there-a-built-in-function-for-string-natural-sort
from natsort import natsorted
import os
import glob
import platform
import time

from reportlab.lib.pagesizes import letter
from reportlab.platypus import Image
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas

from PIL import Image


def sort_by(rule, img_dir, i):
    if rule == 1:
        return natsorted(glob.glob(os.path.join(img_dir, '*.' + i)),
                         key=lambda x: x.lower())
    return sorted(glob.glob(os.path.join(img_dir, '*.' + i)),
                  key=lambda x: x.lower())


def img2pdf(imgDir,
            recursion=None,
            pictureType=None,
            sizeMode=None,
            width=None,
            height=None,
            fit=None,
            saveDir=None,
            pdfName=None,
            rule=1):
    """
    Parameters
    ----------
    imgDir : string
           directory of the source pictures
    recursion : boolean
                None or False for no recursion
                True for recursion to children folder
                wether to recursion or not
    pictureType : list
                  type of pictures,for example :jpg,png...
    sizeMode : int
           None or 0 for pdf's pagesize is the biggest of all the pictures
           1 for pdf's pagesize is the min of all the pictures
           2 for pdf's pagesize is the given value of width and height
           to choose how to determine the size of pdf
    width : int
            width of the pdf page
    height : int
            height of the pdf page
    fit : boolean
           None or False for fit the picture size to pagesize
           True for keep the size of the pictures
           wether to keep the picture size or not
    saveDir : directory to save the pdf
    pdfName : aim pdf file name, if None, use timestamp
    """
    if platform.system() == 'Windows':
        imgDir = imgDir.replace('\\', '/')
    if imgDir[-1] != '/':
        imgDir = (imgDir + '/')
    if recursion == True:
        for i in os.listdir(imgDir):
            if os.path.isdir(os.path.abspath(os.path.join(imgDir, i))):
                img2pdf(imgDir + i, recursion, pictureType, sizeMode, width,
                        height, fit, saveDir)
    filelist = []

    if pictureType == None:
        print("default use jpg image format!")
        filelist = glob.glob(os.path.join(imgDir, '*.jpg'))
    else:
        for i in pictureType:
            # sort by name
            # filelist.extend(sorted(glob.glob(os.path.join(imgDir, '*.' + i))))
            filelist.extend(sort_by(rule, imgDir, i))

    maxw = 0
    maxh = 0

    print('pdf order is:\n')
    for i in filelist:
        print("Page:%d %s" % (filelist.index(i), i))
    print('is that order correct? [y:n]')
    name = input()
    if name != 'y' and name != 'Y':
        print(
            'file order not correct, please fix code or modify your file name!'
        )
        quit()
    '''
    change order of files
    file1 = filelist[0]
    filelist[0] = filelist[3]
    filelist[3] = file1
    file1 = filelist[1]
    filelist[1] = filelist[2]
    filelist[2] = file1
    print(filelist)
    '''

    if sizeMode == None or sizeMode == 0:
        for i in filelist:
            im = Image.open(i)
            if maxw < im.size[0]:
                maxw = im.size[0]
            if maxh < im.size[1]:
                maxh = im.size[1]
    elif sizeMode == 1:
        maxw = 999999
        maxh = 999999
        for i in filelist:
            im = Image.open(i)
            if maxw > im.size[0]:
                maxw = im.size[0]
            if maxh > im.size[1]:
                maxh = im.size[1]
    else:
        if width == None or height == None:
            raise Exception("no width or height provid")
        maxw = width
        maxh = height

    maxsize = (maxw, maxh)

    if pdfName == None:
        print('[WARN] pdfName is None, use timestamp as pdf file name')
        pdfName = str(time.time())

    if pdfName.find('.pdf') == -1:
        pdfName = pdfName + '.pdf'

    if saveDir == None or not os.path.exists(saveDir):
        print(
            '[WARN] saveDir is None or not exist, save pdf file to source image directory'
        )
        filename_pdf = imgDir + pdfName
    else:
        if saveDir[-1] != '/':
            saveDir = (saveDir + '/')
        filename_pdf = saveDir + pdfName
    '''
    pdfgen.canvas detail parameters check 
    https://www.reportlab.com/docs/reportlab-userguide.pdf
    '''
    c = canvas.Canvas(filename_pdf, pagesize=maxsize)

    l = len(filelist)
    for i in range(l):
        (w, h) = maxsize
        width, height = letter
        if fit == True:
            c.drawImage(filelist[i], 0, 0)
        else:
            c.drawImage(filelist[i], 0, 0, maxw, maxh)
        c.showPage()
    c.save()
    print('pdf has been save in %s' % (filename_pdf))


def main():
    print(
        "common sort:\n - before sort:['1','2','3','4','10','20','21']\n - after sort['1','10','2','20','21','3','4']"
    )
    print(
        "nature sort:\n - before sort:['1','2','3','4','10','20','21']\n - after sort['1','2','3','4','10','20','21']"
    )
    print("please choose sort rule:\n 0: common\n 1: nature")
    sort_rule = input()
    if isdigit(sort_rule) and (int(sort_rule) == 0 or int(sort_rule) == 1):
        sort_rule = int(sort_rule)
    else:
        print("unknown input, defult use nature")
        sort_rule = 1

    img2pdf(imgDir="../",
            pictureType=['png', 'jpg'],
            saveDir='./dstPdf',
            rule=sort_rule)


if __name__ == '__main__':
    main()