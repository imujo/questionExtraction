from displayImages.functions import selectPages, selectQuestions
from inputFilesFunctions.functions import pdfToImages, pilToCv2Image, selectPdfFile
from imagesToOneNote.functions import imagesToOneNote


if __name__ == '__main__':

    print("*--- WELCOME TO THE QUESTION SELECTION APP ---*")
    print('\n\n')

    print("Select a PDF file")

    pathToPdfFile = selectPdfFile()

    print('\n\n')

    # outputPath = selectOutputDir()
    outputPath = './images/'

    print('Processing PDF file...')
    pilImages = pdfToImages(pathToPdfFile)

    pages = []

    for pilImage in pilImages:
        page = pilToCv2Image(pilImage)
        pages.append(page)

    print('\n\n')

    print("Select pages")
    selectedPageIndexes = selectPages(pages)

    print('\n\n')

    allQuestions = []

    print("Select questions")
    for pageIndex in sorted(selectedPageIndexes):
        page = pages[pageIndex]

        questions = selectQuestions(page)
        allQuestions += questions

    print('\n\n')

    print("Converting images to Onenote friendly type")

    imagesToOneNote(allQuestions, outputPath)

    print('\n\n')
    print("All done!")
