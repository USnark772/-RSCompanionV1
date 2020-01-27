from abc import ABC, abstractmethod


# TODO: Figure out if subclassing with this is worth it right now.
class ABCDeviceController(ABC):
    def __init__(self, tab):
        self.tab = tab
        self.active = True

    @abstractmethod
    def cleanup(self):
        pass

    def create_new_save_file(self, new_filename):
        pass

    def start_exp(self):
        pass

    def end_exp(self):
        pass

    def start_block(self):
        pass

    def end_block(self):
        pass

    # TODO: Figure out if we don't always need a tab obj.
    def get_tab_obj(self):
        return self.tab

    # TODO: Figure out if can pass instead of return ''
    @staticmethod
    def get_save_file_hdr():
        return ''

    # TODO: Figure out if can pass instead of return ''
    @staticmethod
    def get_note_spacer():
        return ''
