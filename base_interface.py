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

    def get_comma_sep_list(self, item_name):
        str_input = self.get_input(f"Enter a comma-separated list of {item_name}:\n>")
        input_array = str_input.split(",")
        return [item.strip() for item in input_array if item.strip()]