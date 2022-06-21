import os
from PyPDF2 import PdfFileReader, PdfFileWriter

# TODO: raise errors for encrypted PDFS
# TODO: get name of file and use it to save

outputPath = os.path.join(os.getcwd() + '\pdfs')

# Split PDF in a regular interval
def splitFixed(pagesInterval, filename):
    if filename == None:
        return 'Choose a PDF file'

    count = 0
    pagesInterval = int(pagesInterval)
    inputPDF = PdfFileReader(filename)
    numPages = inputPDF.getNumPages()

    if pagesInterval >= numPages or pagesInterval == 0:
        return 'Invalid interval!'

    listPages = [page for page in range(numPages)]
    
    listIntervals = listPages[0:numPages:pagesInterval]

    # Add each interval's pages
    for i in listIntervals:
        lis = [] # Contains the indexes of the first page of each interval
        count += 1
        PDFWriter = PdfFileWriter()
        for j in range(pagesInterval):
            num = i + j
            if num < numPages:
                lis.append(num)
                
            if num > numPages:
                for page in lis:
                    PDFWriter.addPage(inputPDF.getPage(page))
                    outputFilename = '{}_interval.pdf'.format(count)
                    with open(outputFilename, 'wb') as output:
                        PDFWriter.write(output)
                        
                return

        for page in lis:
            PDFWriter.addPage(inputPDF.getPage(page))
            outputFilename = '{}_interval.pdf'.format(count)
            with open(outputFilename, 'wb') as output:
                PDFWriter.write(output)
                

# Create a new file from a custom range
def splitCustom(startPage, endPage, filename):
    if filename == None:
        return 'No PDF selected'

    inputPDF = PdfFileReader(filename)
    numPages = inputPDF.getNumPages()
    
    if startPage >= endPage or startPage == 0 or endPage > numPages:
        return 'Invalid interval'

    startPage = startPage - 1
    PDFWriter = PdfFileWriter()

    listPages = [page for page in range(numPages)]
    interval = listPages[startPage:endPage]
    for page in interval:
        PDFWriter.addPage(inputPDF.getPage(page))
        outputFilename = 'splitted.pdf'
        with open(outputFilename, 'wb') as output:
            PDFWriter.write(output)
    return 

