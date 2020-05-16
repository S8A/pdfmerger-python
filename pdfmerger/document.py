import PyPDF2
        

class Document():
    """Represents a PDF document entry."""
    def __init__(self, file = None):
        super().__init__()
        self.path = ""
        self.start = 1
        self.end = 1
        if file is not None:
            self.path = file
            self.pdf = PyPDF2.PdfFileReader(open(file, 'rb'))
            self.end = self.pdf.numPages

    def __repr__(self):
        return f"{self.__class__.__name__}({self.path})"

    def set_interval(self, start, end):
        self.start = start
        self.end = end
