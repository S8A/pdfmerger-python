import PyPDF2


class Document():
    """Represents a document entry."""
    def __init__(self, file, path, start = 1, end = file.numPages):
        super().__init__()
        self.pdf = PyPDF2.PdfFileReader(file)
        self.path = path
        self.start = start
        self.end = end
