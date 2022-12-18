import cv2
import displayImages.key_mapping as k
import numpy as np
from displayImages.constants import SCREEN_WIDTH


def displayImage(window_name:str, image, width = 0, height = 0, positionX:int = 0 , positionY:int = 0):
    image = image.copy()
    h,w,_ = image.shape
    ratio = w/h

    if (width == 0 and height == 0):
        width = w
        height = h
    elif (width == 0):
        width = (w * height) // h
    elif (height == 0):
        height = (h * width) // w

    resized = cv2.resize(image, (width, height), interpolation=cv2.INTER_AREA)    

    cv2.namedWindow(window_name)
    cv2.moveWindow(window_name, positionX, positionY) 
    cv2.imshow(window_name, resized)

def selectPagesNavigation(currentPage, numOfPages):
    key = cv2.waitKey()

    if key == k.RIGHT and currentPage < numOfPages-1: 
        return 'next'
    elif key == k.LEFT and currentPage > 0: 
        return 'prev'
    elif key == k.SPACE: 
        return 'select'
    elif key == k.ENTER: 
        return 'done'
    elif key == k.ESC:
        return 'exit'

    return

def higlightImage (image, borderColor=(0, 0, 255), borderThickness = 10):
    image = image.copy()

    height, width, _ = image.shape

    cv2.rectangle(image, (0,0), (width, height), color=borderColor, thickness= borderThickness)

    return image

def selectPages(pages:list):

    currentPage = 0
    selectedPages = set()

    while True:
        print(selectedPages)
        page = pages[currentPage]
        windowName = f"Page {currentPage+1} :: LEFT / RIGHT for navigation :: SPACE for selecting :: ENTER for done"



        if (currentPage in selectedPages):
            displayImage(windowName, higlightImage(page))
        else:
            displayImage(windowName, page)



        navigation = selectPagesNavigation(currentPage=currentPage, numOfPages=len(pages))

        match navigation:
            case 'prev':
                currentPage -= 1
            case 'next':
                currentPage += 1
            case 'select': 
                if (currentPage in selectedPages):
                    selectedPages.remove(currentPage)
                else:
                    selectedPages.add(currentPage)
            case 'done': 
                return selectedPages
            case 'exit':
                exit()
        
        cv2.destroyWindow(windowName)

def getContours(image, kernel_size, dilation_iterations):
    image = image.copy()


    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)


    _, thresh1 = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU |
                               cv2.THRESH_BINARY_INV)

    rect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, kernel_size)

    dilation = cv2.dilate(thresh1, rect_kernel, iterations=dilation_iterations)

    contours, _ = cv2.findContours(dilation, cv2.RETR_EXTERNAL,
                                   cv2.CHAIN_APPROX_NONE)

    return contours

def drawContours(image, contours, higlightedContourIndex, higlightedContourColor = (0,0,255), contourColor=(255,0,0), thickness = 2):
    image = image.copy()
    # blank = np.zeros(image.shape, dtype="uint8")
    cv2.drawContours(image, contours, -1, contourColor, thickness)
    cv2.drawContours(
        image, contours, higlightedContourIndex, higlightedContourColor, thickness)
    return image

def selectQuestionsNavigation(currentIterations, higlightedContourIndex, contoursLen):
    key = cv2.waitKey()

    if (key == k.UP): return 'increase'
    elif (key == k.DOWN and currentIterations != 0): return 'decrease'
    elif (key == k.ESC): return 'exit'
    elif (key == k.ENTER): return 'done'
    elif (key == k.SPACE): return 'select'
    elif (key == k.RIGHT and higlightedContourIndex != -1): return 'left'
    elif (key == k.LEFT and higlightedContourIndex != contoursLen-1): return 'right'

def applyMask(image, maskCoordinates, color=(255, 255, 255)):
    image = image.copy()

    for coordinates in maskCoordinates:
        cv2.rectangle(image, coordinates[0], coordinates[1], color, -1)
    
    return image

def drawRectangles(image, rectangleCoordinates, borderColor = (0,255,0), thickness = 2):
    image = image.copy()

    for rectangleCoordinates in rectangleCoordinates:
        cv2.rectangle(image, rectangleCoordinates[0], rectangleCoordinates[1], borderColor, thickness)
    
    return image

def getImagesFromCoordinates(image, coordinates):
    images = []
    for coordinate in coordinates:
        x1 = coordinate[0][0]
        y1 = coordinate[0][1]
        x2 = coordinate[1][0]
        y2 = coordinate[1][1]
        
        croppedImage = image[y1:y2, x1:x2]
        images.append(croppedImage)

    return images


def selectQuestions(page):
    image = page.copy()

    selectedCoordinates = []
    kernelSize = (15, 15)
    iterations = 1
    higlightedContourIndex = 0


    while True:
        maskedImage = applyMask(image, selectedCoordinates)
        contours = getContours(maskedImage, kernelSize, iterations)

        contoursImage = drawContours(image, contours, higlightedContourIndex, contourColor=(255, 210, 162))
        contoursImage = drawRectangles(contoursImage, selectedCoordinates, borderColor=(71,48,2))

        displayImage('Contours', contoursImage, width=SCREEN_WIDTH//2)

        navigation = selectQuestionsNavigation(iterations, higlightedContourIndex, len(contours))

        match navigation:
            case 'increase':
                iterations += 1
                higlightedContourIndex = 0
            case 'decrease':
                iterations -= 1
                higlightedContourIndex = 0
            case 'left':
                higlightedContourIndex -=1
            case 'right':
                higlightedContourIndex +=1
            case 'select':
                x, y, w, h = cv2.boundingRect(contours[higlightedContourIndex])
                selectedCoordinates.append(((x,y), (x+w, y+h)))
            case 'done':
                return getImagesFromCoordinates(page, selectedCoordinates)
            case 'exit':
                exit()
        
        cv2.destroyWindow('Contours')
