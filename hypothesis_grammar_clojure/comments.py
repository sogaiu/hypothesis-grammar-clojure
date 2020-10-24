from hypothesis.strategies import characters, integers
from hypothesis.strategies import composite, lists

from custom.label.comments import label
from custom.verify.comments import verify

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
    # XXX: comment as last line in file does not end in newline, but not
    #      handling that case
    cmt_str = ';' + "".join(chars) + "\n"
    #
    return {"inputs": cmt_str,
            "label": label,
            "to_str": build_comment_str,
            "verify": verify}
