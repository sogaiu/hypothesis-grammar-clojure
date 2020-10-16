from hypothesis.strategies import composite, one_of

from .booleans import boolean_items
from .characters import character_items
from .keywords import keyword_items
from .nils import nil_items
from .numbers import number_items
from .regex import regex_items
from .strings import string_items
from .symbolic_values import symbolic_value_items
from .symbols import symbol_items

@composite
def atom_items(draw):
    atm_item = draw(one_of(boolean_items(),
                           character_items(),
                           keyword_items(),
                           nil_items(),
                           number_items(),
                           regex_items(),
                           string_items(),
                           symbol_items(), # XXX: metadata?
                           symbolic_value_items()))
    return atm_item
