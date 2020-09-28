from hypothesis.strategies import characters, integers
from hypothesis.strategies import composite, lists

# XXX: not going to bother with the #! type of comment for now
@composite
def comment_as_str(draw):
    n = draw(integers(min_value=0, max_value=100))
    #
    skip_chars = ["\n", "\r"] # XXX: possibly \r is ok
    #
    chars = \
        draw(lists(elements=characters(blacklist_characters=skip_chars,
                                       min_codepoint=32, max_codepoint=127),
                   min_size=n, max_size=n))
    #
    return ';' + "".join(chars)
