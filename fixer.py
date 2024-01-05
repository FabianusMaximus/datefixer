import os.path
import shutil

import pyexiv2
from pprint import pprint
from datetime import datetime


def convertNameToDate(filename: str) -> datetime:
    if ".trashed" in filename:
        date = filename.split("-")[3]
    elif "-" in filename:
        date = filename.split("-")[1]
    else:
        date = filename.split("_")[1]
    print(date)
    date = datetime.strptime(date, "%Y%m%d")
    print(date)
    return date


def convertDateTimeToString(date: datetime) -> str:
    str = date.strftime("%Y") + ":" + date.strftime("%m") + ":" + date.strftime("%d")
    print(str)
    return str


def readMetaData(image: pyexiv2.Image):
    exif = image.read_exif()
    xmp = image.read_xmp()
    icc = image.read_icc()
    iptc = image.read_iptc()
    comment = image.read_comment()
    raw_xmp = image.read_raw_xmp()
    thumbnail = image.read_thumbnail()
    pprint(f'{exif, xmp, icc, iptc, comment, raw_xmp, thumbnail}')
    pprint(icc)


def copyImage(path: str):
    pass


def modifyExif(image: pyexiv2.Image, dateTime: datetime):
    image.modify_exif({"Exif.Image.DateTime": convertDateTimeToString(dateTime)})


def getFilePathsFromDirectory(path: str):
    filelist = []
    for root, dirs, files in os.walk(path):
        for file in files:
            filelist.append(os.path.join(root, file))
    pprint(filelist)
    return filelist


def fixDateImage(path: str, debug=False):
    filename = os.path.basename(path)
    try:
        image = pyexiv2.Image(path)
        pprint(filename)
        if debug:
            readMetaData(image)
        date = convertNameToDate(filename)
        modifyExif(image, date)
        if debug:
            readMetaData(image)
    except Exception as e:
        shutil.move(path, "./broken")
        print("Broken Image: " + filename)



testImages = ["./out/IMG_20181115_094607__02.jpg", "./in/IMG-20170517-WA0006.jpg"]
images = getFilePathsFromDirectory("./in")
for image in images:
    fixDateImage(image, True)
