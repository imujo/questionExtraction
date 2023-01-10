from displayImages.functions import selectPages, selectQuestions
from inputFilesFunctions.functions import pilToCv2Image, selectImageFiles, imagePathsToImages
from imagesToOneNote.functions import imagesToOneNote


if __name__ == '__main__':

    print("*--- WELCOME TO THE QUESTION SELECTION APP ---*")
    print('\n\n')

    print("Select a Image files")

    imagePaths = selectImageFiles()

    print('\n\n')

    # outputPath = selectOutputDir()
    outputPath = './images/'

    print('Processing Image files...')
    pilImages = imagePathsToImages(imagePaths)

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
