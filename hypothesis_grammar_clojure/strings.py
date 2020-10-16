from hypothesis.strategies import characters, integers
from hypothesis.strategies import composite, lists

from .loader import verify_fns, label_for
import os
name = os.path.splitext(os.path.basename(__file__))[0]
verify, _ = verify_fns(name)
label = label_for(name)

def build_string_str(item):
    return item["inputs"]

@composite
def string_items(draw):
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
    str_str = f'"{"".join(chars)}"'
    #
    return {"inputs": str_str,
            "label": label,
            "to_str": build_string_str,
            "verify": verify}
