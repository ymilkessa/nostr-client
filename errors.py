class FileNonExistentError(Exception):
    """
    Called when some action involves loading from or saving to a file
    that has not been created yet.
    """
    def __init__(self, file_name):
        self.file_name = file_name
        self.message = f"{file_name} has not been created yet."
        super().__init__(self.message)
    
    note = "Note: relays won't be saved since there is no relay file."