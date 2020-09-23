from hypothesis import assume
from hypothesis.strategies import booleans, characters, integers, text
from hypothesis.strategies import composite, just, lists, one_of

from .utils import to_ascii

@composite
def any_character_as_str(draw):
    # XXX: will include surrogates which seem to lead to problems
    #      but unclear whether that's in tree-sitter or python...
    #character = draw(characters())
    character = draw(text(min_size=1, max_size=1))
    #
    return f'\\{character}'

@composite
def named_character_as_str(draw):
    named_char = draw(one_of(just("backspace"),
                             just("formfeed"),
                             just("newline"),
                             just("return"),
                             just("space"),
                             just("tab")))
    #
    return f'\\{named_char}'

@composite
def octal_character_as_str(draw):
    n = draw(integers(min_value=1, max_value=3))
    #
    if n == 3:
        first_digit = draw(integers(min_value=0, max_value=3))
    else:
        first_digit = draw(integers(min_value=0, max_value=7))
    rest_digits = map(to_ascii,
                      draw(lists(elements=integers(min_value=0,
                                                   max_value=7),
                                 min_size=n-1, max_size=n-1)),
                      draw(lists(elements=booleans(),
                                 min_size=n-1, max_size=n-1)))
    #
    return f'\\o{to_ascii(first_digit, False)}{"".join(rest_digits)}'

@composite
def unicode_quad_character_as_str(draw):
    pre_digits = draw(lists(elements=integers(min_value=0,
                                              max_value=15),
                            min_size=4, max_size=4))
    caps = draw(lists(elements=booleans(),
                      min_size=4, max_size=4))
    quad = map(to_ascii, pre_digits, caps)
    #
    return f'\\u{"".join(quad)}'

@composite
def character_as_str(draw):
    character = draw(one_of(any_character_as_str(),
                            named_character_as_str(),
                            octal_character_as_str(),
                            unicode_quad_character_as_str()))
    #
    return character
