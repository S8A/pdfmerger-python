import PyPDF2
        

class Document():
    """Represents a document entry."""
    def __init__(self, file = None):
        super().__init__()
        self.path = ""
        self.start = 1
        self.end = 1
        if file is not None:
            self.path = file
            self.pdf = PyPDF2.PdfFileReader(open(file, 'rb'))
            self.end = self.pdf.numPages
