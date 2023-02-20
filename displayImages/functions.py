import cv2
import displayImages.key_mapping as k


def displayImage(window_name: str, image, width=0, height=0, positionX: int = 0, positionY: int = 0):
    image = image.copy()
    h, w, _ = image.shape

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


def higlightImage(image, borderColor=(0, 0, 255), borderThickness=10):
    image = image.copy()

    height, width, _ = image.shape

    cv2.rectangle(image, (0, 0), (width, height),
                  color=borderColor, thickness=borderThickness)

    return image


def selectPages(pages: list):

    currentPage = 0
    selectedPages = set()

    while True:
        page = pages[currentPage]
        windowName = f"Page {currentPage+1} :: LEFT / RIGHT for navigation :: SPACE for selecting :: ENTER for done"

        if (currentPage in selectedPages):
            displayImage(windowName, higlightImage(page))
        else:
            displayImage(windowName, page)

        navigation = selectPagesNavigation(
            currentPage=currentPage, numOfPages=len(pages))

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
                cv2.destroyAllWindows()
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


def drawContours(image, contours, higlightedContourIndex, higlightedContourColor=(0, 0, 255), contourColor=(255, 0, 0), thickness=2):
    image = image.copy()
    # blank = np.zeros(image.shape, dtype="uint8")
    cv2.drawContours(image, contours, -1, contourColor, thickness)
    cv2.drawContours(
        image, contours, higlightedContourIndex, higlightedContourColor, thickness+2)
    return image


def selectQuestionsNavigation(currentIterations, higlightedContourIndex, contoursLen, kernelSize):
    key = cv2.waitKey()

    if (key == k.UP):
        return 'increaseI'
    elif (key == k.DOWN and currentIterations != -1):
        return 'decreaseI'

    elif (key == k.D):
        return 'increaseK0'
    elif (key == k.A and kernelSize[0] != 3):
        return 'decreaseK0'

    elif (key == k.W):
        return 'increaseK1'
    elif (key == k.S and kernelSize[1] != 3):
        return 'decreaseK1'

    elif (key == k.RIGHT and higlightedContourIndex != -1):
        return 'left'
    elif (key == k.LEFT and higlightedContourIndex != contoursLen-1):
        return 'right'

    elif (key == k.ESC):
        return 'exit'
    elif (key == k.ENTER):
        return 'done'
    elif (key == k.SPACE):
        if currentIterations == -1:
            return 'doneAll'
        else:
            return 'select'


def applyMask(image, maskCoordinates, color=(255, 255, 255)):
    image = image.copy()

    for coordinates in maskCoordinates:
        cv2.rectangle(image, coordinates[0], coordinates[1], color, -1)

    return image


def drawRectangles(image, rectangleCoordinates, borderColor=(0, 255, 0), thickness=2):
    image = image.copy()

    for rectangleCoordinates in rectangleCoordinates:
        cv2.rectangle(
            image, rectangleCoordinates[0], rectangleCoordinates[1], borderColor, thickness)

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
    imH, imW, imC = image.shape
    pageCoordinates = ((0, 0), (imW, imH))

    selectedCoordinates = []
    kernelSize = [12, 12]
    iterations = 1
    higlightedContourIndex = -1

    while True:
        # to stop contouring that part of the image
        maskedImage = applyMask(image, selectedCoordinates)
        contours = getContours(maskedImage, kernelSize,
                               iterations if iterations != -1 else 0)

        # set higlighted contour to be the first in image
        if (higlightedContourIndex == -1):
            higlightedContourIndex = len(contours)-1

        # reset higlighted contour if it's out of range
        while higlightedContourIndex >= len(contours):
            higlightedContourIndex -= 1

        contoursImage = drawContours(image, contours, higlightedContourIndex, higlightedContourColor=(
            27, 27, 153), contourColor=(157, 90, 23))
        contoursImage = drawRectangles(
            contoursImage, selectedCoordinates, borderColor=(71, 48, 2))

        if (iterations == -1):
            displayImage("Contours", cv2.rectangle(
                image.copy(), (0, 0), (imW-2, imH-2), (27, 27, 153), 10))
        else:
            displayImage('Contours', contoursImage)

        navigation = selectQuestionsNavigation(
            iterations, higlightedContourIndex, len(contours), kernelSize)

        match navigation:
            case 'increaseI':
                iterations += 1
            case 'decreaseI':
                iterations -= 1

            case 'increaseK0':
                kernelSize[0] += 1
            case 'decreaseK0':
                kernelSize[0] -= 1

            case 'increaseK1':
                kernelSize[1] += 1
            case 'decreaseK1':
                kernelSize[1] -= 1

            case 'left':
                higlightedContourIndex -= 1
            case 'right':
                higlightedContourIndex += 1
            case 'select':
                x, y, w, h = cv2.boundingRect(contours[higlightedContourIndex])
                selectedCoordinates.append(((x, y), (x+w, y+h)))
            case 'done':
                cv2.destroyAllWindows()
                return getImagesFromCoordinates(page, selectedCoordinates)
            case 'doneAll':
                cv2.destroyAllWindows()
                return getImagesFromCoordinates(page, [pageCoordinates])
            case 'exit':
                exit()

        cv2.destroyWindow('Contours')
