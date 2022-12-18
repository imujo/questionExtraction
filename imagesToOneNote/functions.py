import imagesToOneNote.constants as c
import math
import cv2
import numpy as np


def placeImage(backgroundImageInput, imageInput, positionX='center', positionY='center'):
    x_offset = 0
    y_offset = 0

    backgroundImage = backgroundImageInput.copy()
    image = imageInput.copy()

    (backgroundHeight, backgroundWidth) = backgroundImage.shape[:2]
    (imageHeight, imageWidth) = image.shape[:2]

    if (positionX == 'center'):
        x_offset = int(backgroundWidth/2 - imageWidth / 2)
    elif (positionX == 'start'):
        x_offset = 0
    elif (positionX == 'end'):
        x_offset = backgroundWidth-imageWidth
    elif (type(positionX) == int):
        if (positionX + imageWidth > backgroundWidth):
            raise ValueError("Position x is out of range")
        x_offset = positionX
    else:
        raise TypeError(
            "Incorrect type for positionX (center, start, end or a small enought integer required")

    if (positionY == 'center'):
        y_offset = int(backgroundHeight/2 - imageHeight / 2)
    elif (positionY == 'start'):
        y_offset = 0
    elif (positionY == 'end'):
        y_offset = backgroundWidth-imageWidth
    elif (type(positionY) == int):
        if (positionY+imageHeight > backgroundWidth):
            raise ValueError("Position y is out of range")
        y_offset = positionY
    else:
        raise TypeError(
            "Incorrect type for positionY (center, start, end or a small enought integer required")

    backgroundImage[y_offset: y_offset + imageHeight,
                    x_offset: x_offset+imageWidth] = image

    return backgroundImage


def createBlank(width, height, backgroundColor=None):
    blankImage = np.zeros((height, width, 3), dtype='uint8')

    if (backgroundColor):
        blankImage[:] = backgroundColor

    return blankImage


def resizeImage(image, width, height, backgroundColor, progress = 0, progressHeight = 10, progressBackgroundColor=(255,255,255), progressColor=(0,0,0)):
    blankImage = createBlank(width, height+progressHeight, backgroundColor)

    (imageHeight, imageWidth) = image.shape[:2]

    wToHRatio = width / height
    wToHRatioImage = imageWidth / imageHeight

    if (wToHRatioImage > wToHRatio):
        scale = width / imageWidth
        outputWidth = width
        outputHeight = int(imageHeight*scale)
    else:
        scale = height / imageHeight
        outputWidth = int(imageWidth * scale)
        outputHeight = height

    image = cv2.resize(image, (outputWidth, outputHeight),
                       interpolation=cv2.INTER_AREA)

    blankImage[0:progressHeight, 0:width] = progressBackgroundColor
    blankImage[0:progressHeight, 0: int(width*progress)] = progressColor
    blankImage = placeImage(blankImage, image, 'center', 10)

    return blankImage


def imagesToOneNote(images, pathToSave):
    totalWidth = (c.IMAGE_WIDTH + c.X_GAP) * c.ZADATCI_PER_ROW
    numRows = math.ceil(len(images) / c.ZADATCI_PER_ROW)
    
    zadatciPerRow = []

    for i in range(numRows):
        if (i == numRows-1 and len(images) % c.ZADATCI_PER_ROW != 0):
            zadatciPerRow.append(len(images) % c.ZADATCI_PER_ROW)
        else:
            zadatciPerRow.append(c.ZADATCI_PER_ROW)


    for rowIndex in range(numRows):
        rowBlank = createBlank(totalWidth, c.IMAGE_HEIGHT+c.PROGRESS_HEIGHT, c.BACKGROUND_COLOR)

        for j in range(zadatciPerRow[rowIndex]):
            imageIndex = rowIndex*c.ZADATCI_PER_ROW + j
            image = images[imageIndex]
            cv2.imshow('image', image)
            cv2.waitKey()

            resizedImage = resizeImage(
                image, c.IMAGE_WIDTH, c.IMAGE_HEIGHT, c.BACKGROUND_COLOR, progress=(imageIndex+1)/len(images), progressBackgroundColor=c.PROGRESS_BACKGROUND_COLOR, progressColor=c.PROGRESS_COLOR)

            positionX = (c.IMAGE_WIDTH + c.X_GAP) * j
            rowBlank = placeImage(rowBlank, resizedImage, positionX, 'start')

        cv2.imwrite(f'{pathToSave}/row{rowIndex}.png', rowBlank)



