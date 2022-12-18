from displayImages.functions import *
from pdfToImages.functions import *
import cv2



# pdfFilePath = selectPdfFile()

# pages = pdfToImages(pdfFilePath)

# selectPages(pages)

image = cv2.imread('image.png')

selected = selectQuestions(image)




for i in range (len(selected)):
    cv2.imshow(f'Image {i}', selected[i])
    cv2.waitKey()


