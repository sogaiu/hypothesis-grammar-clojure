from hypothesis.strategies import composite, just

from .loader import verify_fns, label_for
import os
name = os.path.splitext(os.path.basename(__file__))[0]
verify, _ = verify_fns(name)
label = label_for(name)

def build_nil_str(item):
    return item["inputs"]

@composite
def nil_items(draw):
    nil_str = draw(just("nil"))
    #
    return {"inputs": nil_str,
            "label": label,
            "to_str": build_nil_str,
            "verify": verify}
