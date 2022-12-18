from displayImages.functions import *
from pdfToImages.functions import *
import cv2
from imagesToOneNote.functions import imagesToOneNote


# pdfFilePath = selectPdfFile()

# pages = pdfToImages(pdfFilePath)

# selectPages(pages)

image = cv2.imread('image.png')

selected = selectQuestions(image)

imagesToOneNote(selected, './')

