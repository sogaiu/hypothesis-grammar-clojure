from hypothesis.strategies import composite, just, one_of

from .loader import verify_fns, label_for
import os
name = os.path.splitext(os.path.basename(__file__))[0]
verify, _ = verify_fns(name)
label = label_for(name)

def build_boolean_str(item):
    return item["inputs"]

@composite
def boolean_items(draw):
    bool_str = draw(one_of(just("false"), just("true")))
    #
    return {"inputs": bool_str,
            "label": label,
            "to_str": build_boolean_str,
            "verify": verify}
