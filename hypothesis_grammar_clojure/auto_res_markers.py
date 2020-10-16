from hypothesis.strategies import composite, just

from .loader import verify_fns, label_for
import os
name = os.path.splitext(os.path.basename(__file__))[0]
verify, _ = verify_fns(name)
label = label_for(name)

def build_auto_res_marker_str(item):
    # this is just "::"
    return item["inputs"]

@composite
def auto_res_marker_items(draw):
    arm_item = draw(just("::"))
    #
    return {"inputs": arm_item,
            "label": label,
            "to_str": build_auto_res_marker_str,
            "verify": verify}
