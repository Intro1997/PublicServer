## 说明

使用 python reportlab 库拼接 png 图片，参考 https://github.com/mrbeann/jpg2pdf。
应该也可以拼接 jpg 图片，目前没有测试。

## 用法

目前不支持 CLI 直接填写参数使用，可修改 img2pdf 函数内参数进行调用，参数和使用示例如下：

```python
'''
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
'''
img2pdf(imgDir="./test/srcPng",
            pictureType=['png'],
            saveDir='./test/dstPdf')
```
