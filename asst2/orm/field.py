#!/usr/bin/python3
#
# fields.py
#
# Definitions for all the fields in ORM layer
#

from datetime import datetime
from datetime import timezone

class Integer:   
    
    inst_count = 0
    
    def __init__(self, blank=False, default=None, choices=None):
        
        #Check if given default
        if default is None:
            #Base default value
            self.default = 0
            self.blank = blank
        else:
            #Force blank true
            self.blank = True

            if callable(default) and isinstance(default(), int):
                self.default = default()
            elif isinstance(default, int):
                self.default = default
            else:
                raise TypeError('Default value wrong type')

        #Check if there is a choice list
        if choices is None:
            self.choices = choices
        else:
            #Check if iterable
            if not isinstance(choices, list) and not isinstance(choices, tuple):
                raise ValueError('choices not iterable')

            #Check values in choice list for type
            for choice in choices:
                if not isinstance(choice, int):
                    raise TypeError('Type Error in choice list')

            #Check if default value in choice list when blank=True
            if self.blank == True and self.default not in choices:
                raise TypeError('Default value not in choice list')

            self.choices = choices

        Integer.inst_count += 1
        self.id = Integer.inst_count

    def __get__(self, instance, owner):
        return getattr(instance, '_integer_value_' + str(self.id), None)

    def __set__(self, instance, value):
        if isinstance(value, int):
            setattr(instance, '_integer_value_' + str(self.id), value)
        else:
            raise TypeError('Type Error')


class Float: 
    
    inst_count = 0
    
    def __init__(self, blank=False, default=None, choices=None):
        
        #Check if given default
        if default is None:
            #Base default value
            self.default = 0.0
            self.blank = blank
        else:
            #Force blank true
            self.blank = True

            if callable(default) and isinstance(default(), float):
                self.default = default()
            elif isinstance(default, float):
                self.default = default
            else:
                raise TypeError('Default value wrong type')

        #Check if there is a choice list
        if choices is None:
            self.choices = choices
        else:
            #Check if iterable
            if not isinstance(choices, list) and not isinstance(choices, tuple):
                raise ValueError('choices not iterable')

            #Check values in choice list for type
            for choice in choices:
                if not isinstance(choice, float):
                    raise TypeError('Type Error in choice list')

            #Check if default value in choice list when blank=True
            if self.blank == True and self.default not in choices:
                raise TypeError('Default value not in choice list')

            self.choices = choices

        Float.inst_count += 1
        self.id = Float.inst_count

    def __get__(self, instance, owner):
        return getattr(instance, '_float_value_' + str(self.id), None)

    def __set__(self, instance, value):
        if isinstance(value, float) or isinstance(value, int):
            setattr(instance, '_float_value_' + str(self.id), value)
        else:
            raise TypeError('Type Error')

class String:

    inst_count = 0

    def __init__(self, blank=False, default=None, choices=None):
        
        #Check if given default
        if default is None:
            #Base default value
            self.default = ""
            self.blank = blank
        else:
            #Force blank true
            self.blank = True

            if callable(default) and isinstance(default(), str):
                self.default = default()
            elif isinstance(default, str):
                self.default = default
            else:
                raise TypeError('Default value wrong type')

        #Check if there is a choice list
        if choices is None:
            self.choices = choices
        else:
            #Check if iterable
            if not isinstance(choices, list) and not isinstance(choices, tuple):
                raise ValueError('choices not iterable')

            #Check values in choice list for type
            for choice in choices:
                if not isinstance(choice, str):
                    raise TypeError('Type Error in choice list')

            #Check if default value in choice list when blank=True
            if self.blank == True and self.default not in choices:
                raise TypeError('Default value not in choice list')

            self.choices = choices

        String.inst_count += 1
        self.id = String.inst_count

    def __get__(self, instance, owner):
        return getattr(instance, '_string_value_' + str(self.id), None)

    def __set__(self, instance, value):
        if isinstance(value, str):
            setattr(instance, '_string_value_' + str(self.id), value)
        else:
            raise TypeError('Type Error')

class Foreign:

    inst_count = 0

    def __init__(self, table, blank=False):
        self.table = table
        self.blank = blank
        self.default = None

        Foreign.inst_count += 1
        self.id = Foreign.inst_count

    def __get__(self, instance, owner):
        return getattr(instance, '_foreign_value_' + str(self.id), None)

    def __set__(self, instance, value):
        if self.blank == False and isinstance(value, self.table):
            setattr(instance, '_foreign_value_' + str(self.id), value)
        elif self.blank == True and (isinstance(value, self.table) or value is None):
            setattr(instance, '_foreign_value_' + str(self.id), value)
        else:
            raise TypeError('Type Error')

class DateTime:
    implemented = True

    inst_count = 0
    
    def __init__(self, blank=False, default=None, choices=None):
        
        #Check if given default
        if default is None:
            #Base default value
            self.default = datetime(1970, 1, 1, tzinfo=timezone.utc)
            self.blank = blank
        else:
            #Force blank true
            self.blank = True

            if callable(default) and isinstance(default(), datetime):
                self.default = default()
            elif isinstance(default, datetime):
                self.default = default
            else:
                raise TypeError('Default value wrong type')

        #Check if there is a choice list
        if choices is None:
            self.choices = choices
        else:
            #Check if iterable
            if not isinstance(choices, list) and not isinstance(choices, tuple):
                raise ValueError('choices not iterable')

            #Check values in choice list for type
            for choice in choices:
                if not isinstance(choice, datetime):
                    raise TypeError('Type Error in choice list')

            #Check if default value in choice list when blank=True
            if self.blank == True and self.default not in choices:
                raise TypeError('Default value not in choice list')

            self.choices = choices

        DateTime.inst_count += 1
        self.id = DateTime.inst_count

    def __get__(self, instance, owner):
        return getattr(instance, '_datetime_value_' + str(self.id), None)

    def __set__(self, instance, value):
        if isinstance(value, datetime):
            setattr(instance, '_datetime_value_' + str(self.id), value)
        else:
            raise TypeError('Type Error')

def is_valid_coord(coord):
    lat = coord[0]
    lon = coord[1]

    if not isinstance(lat, float) and not isinstance(lat, int):
        return False

    if not isinstance(lon, float) and not isinstance(lon, int):
        return False

    if lat < -90.0 or lat > 90.0:
        return False

    if lon < -180.0 or lon > 180.0:
        return False

    return True

class Coordinate:
    implemented = True

    inst_count = 0

    def __init__(self, blank=False, default=None, choices=None):
        
        #Check if given default
        if default is None:
            #Base default value
            self.default = (0.0, 0.0)
            self.blank = blank
        else:
            #Force blank true
            self.blank = True

            if callable(default) and isinstance(default(), tuple) and len(default()) == 2:
                if is_valid_coord(default()):
                    self.default = default()
                else:
                    raise ValueError('invalid coordinate')
            elif isinstance(default, tuple) and len(default) == 2:
                if is_valid_coord(default):
                    self.default = default
                else:
                    raise ValueError('invalid coordinate')
            else:
                raise TypeError('Default value wrong type')

        #Check if there is a choice list
        if choices is None:
            self.choices = choices
        else:
            #Check if iterable
            if not isinstance(choices, list) and not isinstance(choices, tuple):
                raise ValueError('choices not iterable')

            #Check values in choice list for type
            for choice in choices:
                if not isinstance(choice, tuple):
                    raise TypeError('Type Error in choice list')
                elif isinstance(choice, tuple) and not len(choice) == 2:
                    raise TypeError('Type Error in choice list')
                elif isinstance(choice, tuple) and len(choice) == 2 and not is_valid_coord(choice):
                    raise ValueError('invalid coordinate')

            #Check if default value in choice list when blank=True
            if self.blank == True and self.default not in choices:
                raise TypeError('Default value not in choice list')

            self.choices = choices

        Coordinate.inst_count += 1
        self.id = Coordinate.inst_count

    def __get__(self, instance, owner):
        return getattr(instance, '_coordinate_value_' + str(self.id), None)

    def __set__(self, instance, value):
        if isinstance(value, tuple) and len(value) == 2:
            if is_valid_coord(value):
                setattr(instance, '_coordinate_value_' + str(self.id), value)
            else:
                raise ValueError('invalid coordinate')
        else:
            raise TypeError('Type Error')
