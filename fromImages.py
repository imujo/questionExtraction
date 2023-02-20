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

    images = []

    for pilImage in pilImages:
        page = pilToCv2Image(pilImage)
        images.append(page)

    imagesToOneNote(images, outputPath)

    print('\n\n')
    print("All done!")
