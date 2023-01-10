from tkinter.filedialog import askopenfilename, askdirectory, askopenfilenames
from pdf2image import convert_from_path
import numpy as np
import cv2


def selectPdfFile() -> str:
    return askopenfilename(title="Select a PDF File", filetypes=(("pdf files", "*.pdf"), ("all files", "*.*")))


def selectImageFiles() -> str:
    return askopenfilenames(title="Select Image Files", filetypes=(("image files", "*.png"), ("all files", "*.*")))


def selectOutputDir() -> str:
    return askdirectory(title="Select the save directory")


def pilToCv2Image(pilImage):
    cv2Image = np.array(pilImage)
    # Convert RGB to BGR
    cv2Image = cv2Image[:, :, ::-1].copy()

    return cv2Image


def pdfToImages(pdfPath: str):
    # convert PDF to PIL Images
    pilImages = convert_from_path(pdf_path=pdfPath)

    # convert PIL Images to CV2 Images
    cv2Images = []
    for pilImage in pilImages:
        cv2Images.append(pilToCv2Image(pilImage))

    return cv2Images


def imagePathsToImages(imagePaths: list):
    return [cv2.imread(imgPath) for imgPath in imagePaths]
