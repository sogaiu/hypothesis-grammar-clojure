from hypothesis.strategies import characters, integers
from hypothesis.strategies import composite, lists

@composite
def string_as_str(draw):
    n = draw(integers(min_value=0, max_value=100))
    #
    not_tween_delims = ['"', '\\']
    #
    chars = \
        draw(lists(elements=characters(blacklist_characters=not_tween_delims,
                                       min_codepoint=32, max_codepoint=127),
                   min_size=n, max_size=n))
    #
    # XXX: what about escape sequences? e.g. \", \\, etc.
    return f'"{"".join(chars)}"'
