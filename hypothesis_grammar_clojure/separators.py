from hypothesis.strategies import integers
from hypothesis.strategies import composite, lists, one_of

from .parameters import sep_max

from .whitespace import whitespace_items
from .comments import comment_items
from .discard_exprs import discard_expr_items

@composite
def whitespace_strings(draw):
    ws_item = draw(whitespace_items())
    #
    return ws_item["to_str"](ws_item)

# newline is appended so result can be used as a separator
@composite
def comment_and_nl_strings(draw):
    cmt_item = draw(comment_items())
    #
    return cmt_item["to_str"](cmt_item) + "\n"

# space is appended so result can be used safely as a separator
@composite
def discard_expr_and_ws_strings(draw):
    de_item = draw(discard_expr_items())
    # XXX: prepend a space because it turns out that although for
    #      numbers (and collections?) it is not necessary, for
    #      keywords, symbols, characters, and possibly other things,
    #      it appears to be
    #return de_item["to_str"](de_item) + " "
    return " " + de_item["to_str"](de_item) + " "

@composite
def separator_strings(draw):
    n = draw(integers(min_value=1, max_value=sep_max))
    #
    seps = \
        draw(lists(elements=one_of(whitespace_strings(),
                                   comment_and_nl_strings(),
                                   discard_expr_and_ws_strings()),
                   min_size=n, max_size=n))
    #
    sep_str = "".join(seps)
    #
    return sep_str
