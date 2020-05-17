import PyPDF2
        

class Document():
    """Representation of a PDF document entry."""

    def __init__(self, file = None):
        super().__init__()
        self.path = ""
        self.start = 1
        self.end = 1
        self.num_pages = 1
        if file is not None:
            self.path = file
            pdf = PyPDF2.PdfFileReader(open(file, 'rb'))
            self.num_pages = pdf.numPages + 0
            self.end = pdf.numPages + 0

    def __repr__(self):
        return f"{self.__class__.__name__}({self.path})"

    def set_interval(self, start, end):
        """Sets the start and end page of the document."""
        self.start = start
        self.end = end
    
    def copy(self):
        """Creates a copy of the document."""
        copy = Document(self.path)
        copy.set_interval(self.start, self.end)
        return copy
