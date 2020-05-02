ID_PADDING = 3

class Todo:
    def __init__(self, **kwargs):
        # TODO be more descriptive than kwargs; define a real model via Marshmallow
        for key, value in kwargs.items():
            setattr(self, key, value)

    def short_description(self):
        """Return a concise one-line str."""
        return f"{self._padded_id()}. {self.format_description()} {self.format_tags()}"

    def long_description(self):
        """Returns a multi-line description str."""
        return f"{self.description}\n{self._padded_id()}\t{self.format_tags()}"

    def format_tags(self):
        """Return a string of formatted tags (including ASCII escape sequences)."""
        return ''

    def format_description(self):
        if self.status == 2:
            return _make_input_blink(self.description)
        return self.description
    
    def _padded_id(self):
        return str(self.id).rjust(ID_PADDING, ' ')

def _make_input_blink(message):
    return "\033[5m" + message + "\033[0m" 

