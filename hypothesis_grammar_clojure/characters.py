from hypothesis import assume
from hypothesis.strategies import booleans, characters, integers, text
from hypothesis.strategies import composite, just, lists, one_of

from .util import to_ascii

from custom.label.characters import label
from custom.verify.characters import verify

def build_chr_str(item):
    return item["inputs"]

@composite
def any_character_items(draw,
                        label=label,
                        verify=verify):
    # XXX: will include surrogates which seem to lead to problems
    #      but unclear whether that's in tree-sitter or python...
    #character = draw(characters())
    character = draw(text(min_size=1, max_size=1))
    #
    chr_str = f'\\{character}'
    # XXX: tree-sitter cannot handle null byte (0)
    assume(chr_str != '\\\x00')
    #
    return {"inputs": chr_str,
            "label": label,
            "to_str": build_chr_str,
            "verify": verify}

@composite
def named_character_items(draw,
                          label=label,
                          verify=verify):
    #
    named_char = draw(one_of(just("backspace"),
                             just("formfeed"),
                             just("newline"),
                             just("return"),
                             just("space"),
                             just("tab")))
    #
    chr_str = f'\\{named_char}'
    #
    return {"inputs": chr_str,
            "label": label,
            "to_str": build_chr_str,
            "verify": verify}

@composite
def octal_character_items(draw,
                          label=label,
                          verify=verify):
    #
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
    chr_str = f'\\o{to_ascii(first_digit, False)}{"".join(rest_digits)}'
    #
    return {"inputs": chr_str,
            "label": label,
            "to_str": build_chr_str,
            "verify": verify}

@composite
def unicode_quad_character_items(draw,
                                 label=label,
                                 verify=verify):
    #
    pre_digits = draw(lists(elements=integers(min_value=0,
                                              max_value=15),
                            min_size=4, max_size=4))
    caps = draw(lists(elements=booleans(),
                      min_size=4, max_size=4))
    quad = map(to_ascii, pre_digits, caps)
    #
    chr_str = f'\\u{"".join(quad)}'
    #
    return {"inputs": chr_str,
            "label": label,
            "to_str": build_chr_str,
            "verify": verify}

@composite
def character_items(draw,
                    label=label,
                    verify=verify):
    #
    chr_item = draw(one_of(any_character_items(label=label,
                                               verify=verify),
                           named_character_items(label=label,
                                                 verify=verify),
                           octal_character_items(label=label,
                                                 verify=verify),
                           unicode_quad_character_items(label=label,
                                                        verify=verify)))
    return chr_item
