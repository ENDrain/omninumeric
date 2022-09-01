# -*- coding: UTF-8 -*-
# For licensing information see LICENSE file included in the project's root directory.
"This module provides basic tools for reading and writing numbers in alphabetic numeral systems."

import re
from enum import Enum, unique


@unique
class Dictionary(Enum):
    """
    ABC for alphabetic numeral systems dictionaries.

    Derive from this class to define numeral dictionaries for alphabetic numeral systems.
    """

    @classmethod
    def get(cls, numeral):
        """
        Look a numeral up in dictionary.

        @numeral - str or int to look up. Returns int if str is found and vice versa, returns None if nothing found
        """

        try:
            return cls[numeral].value
        except:
            try:
                return cls(numeral).name
            except:
                return None


class NumberConverter:
    """
    ABC for number conversion.

    Derive from this class to define converters into and from alphabetic numeral systems.
    """

    def __init__(self, source, flags, target, dict_, const):
        self.source = source
        self.flags = flags
        self.target = target
        self.dict_ = dict_
        self.const = const
        self.groups = []

    def hasFlag(self, flag):
        "Check if a flag is set."

        return self.flags & flag

    def get(self):
        "Return the converted number."

        return self.target

    def build(self):
        "Build the converted number from groups of numerals."

        for k in self.groups:
            self.target = k + self.target
        return self

    def getNumeral(self, numeral, fallback):
        """
        Look a numeral up in dictionary.

        @numeral - numeral to look up
        @fallback - value to return if @numeral is not found
        """

        return self.dict_.get(numeral) or fallback

    def purgeEmptyGroups(self):
        "Remove empty groups from numeral groups collection."

        while self.groups.count(""):
            self.groups.remove("")  # Purge empty groups
        return self

    def convert(self):
        raise NotImplementedError


class IntConverter(NumberConverter):
    """
    ABC for number conversion into alphabetic numeral systems.

    Derive from this class to define converters into alphabetic numeral systems.
    """

    def __init__(self, source, flags, dict_, const=None):
        super().__init__(source, flags, "", dict_, const)

    def getNumeral(self, numeral):
        "Get alphabetic digit for given value."

        return super().getNumeral(numeral, "")


class StrConverter(NumberConverter):
    """
    ABC for number conversion from alphabetic numeral systems.

    Derive from this class to define converters from alphabetic numeral systems.
    """

    def __init__(self, source, flags, dict_, const=None):
        super().__init__(source, flags, 0, dict_, const)

    def prepare(self):
        "Prepare source number for further operations."

        self.source = str.strip(self.source)
        return self

    def getNumeral(self, numeral):
        "Get value for given alphabetic digit."

        return super().getNumeral(numeral, 0)
