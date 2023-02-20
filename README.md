# Qestion Extraction

This is a python app used for extracting questions from PDF documents. It's intended to be used for Math, Physics and similar subjects. It returns images intended to be imported into OneNote or similar programs and solved using a graphic tablet.

## Requirements

```txt
opencv-contrib-python==4.6.0.66
pdf2image==1.16.0
tk==0.1.0
```

## Usage

Run the app with the following commands

```bash
python fromPDF.py
```
or
```
python fromImages.py
```

### From PDF
- select a PDF file you want to select questions from
- go through the PDF's pages and select ones with your questions
- go through the pages and select the questions

### From Images
- select a number of images
- select question from the images

## Licence

MIT License

Copyright (c) [2022] [questionextraction]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.