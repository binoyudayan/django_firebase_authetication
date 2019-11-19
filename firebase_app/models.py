from django.db import models

# Create your models here.


class User:
    """
    Temporary user object have user attributes(mainly 'is_authenticated' for now).
    TODO: additional attributes and methods can be added.
    """
    is_authenticated = False
    is_anonymous = True
    _attr = ['name', 'email', 'uid', 'picture']
    
    def set_attributes(self, attr_dict):
        self.is_anonymous = False
        self.is_authenticated = True
        for attr in self._attr:
            setattr(self, attr, attr_dict.get(attr, ""))
