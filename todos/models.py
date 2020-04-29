class Todo:
    def __init__(self, **kwargs):
        # TODO be more descriptive than kwargs; define a real model via Marshmallow
        for key, value in kwargs.items():
            setattr(self, key, value)

    def __repr__(self):
        return f"{self.description} – {self.tags}"
   
    def __str__(self):
        return f"{self.description} – {self.tags}"

