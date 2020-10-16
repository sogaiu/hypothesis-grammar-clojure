from hypothesis.strategies import characters, integers
from hypothesis.strategies import composite, lists

from .loader import verify_fns, label_for
import os
name = os.path.splitext(os.path.basename(__file__))[0]
verify, _ = verify_fns(name)
label = label_for(name)

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
