import getpass

class BaseInterface:
    """
    Contains rudimentary versions for input/output methods used
    to interact with the user.
    """
    def __init__(self):
        pass
    
    def get_input(self, prompt=">"):
        return input(prompt)
    
    def get_password(self, prompt=">"):
        return getpass.getpass(prompt)