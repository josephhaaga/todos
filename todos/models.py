class Todo:
    def __init__(self, **kwargs):
        # TODO be more descriptive than kwargs; define a real model via Marshmallow
        for key, value in kwargs.items():
            setattr(self, key, value)

    def __repr__(self):
        return f"#{self.id}: {self.description} – {self.tags}"

    def format_description(self):
        # In Progress tasks should blink
        if self.status == 2:
            return "\033[5m" + self.description + "\033[0m"
        return self.description

   
    def __str__(self):
        return f"#{self.id} {self.format_description()} - {self.tags}" 
        # \033[5m\033\0m

