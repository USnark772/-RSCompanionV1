

# TODO: Figure out if subclassing with this is worth it right now.
class DeviceController:
    def __init__(self):
        self.__tab = None

    def cleanup(self):
        pass

    def create_new_save_file(self, new_filename):
        pass

    def start_exp(self):
        """ Required function for all device controllers. """
        pass

    def end_exp(self):
        """ Required function for all device controllers. """
        pass

    def start_block(self):
        """ Required function for all device controllers. """
        pass

    def end_block(self):
        """ Required function for all device controllers. """
        pass

    def get_tab_obj(self):
        return self.__tab

    @staticmethod
    def get_save_file_hdr():
        return ''

    @staticmethod
    def get_note_spacer():
        return ''
