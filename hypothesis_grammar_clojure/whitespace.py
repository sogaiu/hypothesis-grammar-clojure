from hypothesis.strategies import integers, lists
from hypothesis.strategies import composite, sampled_from

from .loader import verify_fns, label_for
import os
name = os.path.splitext(os.path.basename(__file__))[0]
verify, _ = verify_fns(name)
label = label_for(name)

def build_whitespace_str(item):
    return item["inputs"]

@composite
def whitespace_items(draw):
    # XXX: java.lang.Character isWhitespace has more...
    allowed = ["\f", "\n", "\r", "\t", ",", " "]
    #
    n = draw(integers(min_value=1, max_value=19))
    #
    ws_chars = \
        draw(lists(elements=sampled_from(allowed),
                   min_size=n, max_size=n))
    #
    ws_str = "".join(ws_chars)
    #
    return {"inputs": ws_str,
            "label": label,
            "to_str": build_whitespace_str,
            "verify": verify}
