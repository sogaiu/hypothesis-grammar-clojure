from hypothesis.strategies import characters, integers
from hypothesis.strategies import composite, lists

from label.comments import label
from verify.comments import verify

def build_comment_str(item):
    return item["inputs"]

# XXX: #! type of comment is not implemented yet
@composite
def comment_items(draw):
    n = draw(integers(min_value=0, max_value=100))
    #
    skip_chars = ["\n", "\r"] # XXX: possibly \r is ok
    #
    chars = \
        draw(lists(elements=characters(blacklist_characters=skip_chars,
                                       min_codepoint=32, max_codepoint=127),
                   min_size=n, max_size=n))
    #
    cmt_str = ';' + "".join(chars)
    #
    return {"inputs": cmt_str,
            "label": label,
            "to_str": build_comment_str,
            "verify": verify}
