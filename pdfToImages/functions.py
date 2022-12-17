from tkinter.filedialog import askopenfilename
from pdf2image import convert_from_path
import numpy as np

def selectPdfFile() -> str:
    return askopenfilename(title="Select a PDF File", filetypes=(("pdf files", "*.pdf"),("all files", "*.*")))

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


