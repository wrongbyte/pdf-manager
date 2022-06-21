import os
from PyPDF2 import PdfFileReader, PdfFileWriter

# TODO: raise errors for encrypted PDFS
# TODO: fix fixed range (it counts one page more than expected)
# TODO: raise error for invalid intervals on custom range


outputPath = os.path.join(os.getcwd() + '\pdfs')

# Split PDF in a regular interval
def splitFixed(pagesInterval, filename):
    if filename == None:
        return 'No PDF selected'

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
            lis.append(num)
            if num >= numPages:
                # Pages that are left from the interval (just like the remainder of a division)
                for page in lis:
                    PDFWriter.addPage(inputPDF.getPage(page))
                    outputFilename = '{}_interval.pdf'.format(count)
                    with open(outputFilename, 'wb') as output:
                        PDFWriter.write(output)
                        print('Created: {}'.format(count))
                return

        for page in lis:
            PDFWriter.addPage(inputPDF.getPage(page))
            outputFilename = '{}_interval.pdf'.format(count)
            with open(outputFilename, 'wb') as output:
                PDFWriter.write(output)
                # print('Created: {}'.format(count))

# Create a new file from a custom range
def splitCustom(startPage, endPage, filename):
    startPage = startPage - 1

    if startPage >= endPage:
        return 'Invalid interval'

    inputPDF = PdfFileReader(filename)
    numPages = inputPDF.getNumPages()
    PDFWriter = PdfFileWriter()

    listPages = [page for page in range(numPages)]
    interval = listPages[startPage:endPage]
    for page in interval:
        PDFWriter.addPage(inputPDF.getPage(page))
        outputFilename = 'splitted.pdf'
        with open(outputFilename, 'wb') as output:
            PDFWriter.write(output)
    return 

