import cv2
import displayImages.key_mapping as k
import numpy as np

def displayImage(window_name:str, image, positionX:int = 0 , positionY:int = 0):
    cv2.namedWindow(window_name)
    cv2.moveWindow(window_name, positionX, positionY)
    cv2.imshow(window_name, image)


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


    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    _, thresh1 = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU |
                               cv2.THRESH_BINARY_INV)

    rect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, kernel_size)

    dilation = cv2.dilate(thresh1, rect_kernel, iterations=dilation_iterations)

    contours, _ = cv2.findContours(dilation, cv2.RETR_EXTERNAL,
                                   cv2.CHAIN_APPROX_NONE)

    return contours

def drawContours(image, contours, higlightedContourIndexes):
    blank = np.zeros(image.shape, dtype="uint8")
    cv2.drawContours(blank, contours, -1, (255, 255, 255), 2)

    for higlightedContourIndex in higlightedContourIndexes:
        cv2.drawContours(
            blank, contours, higlightedContourIndex, (0, 255, 255), 2)

    return blank

def selectQuestions(page):

    while True:
        contours = getContours(page, (20, 20), 1)

        contoursImage = drawContours(page, contours, [])

        cv2.imshow('contours', contoursImage)

        cv2.waitKey()
