from hypothesis.strategies import composite, just

from custom.label.auto_res_markers import label
from custom.verify.auto_res_markers import verify

def build_auto_res_marker_str(item):
    # this is just "::"
    return item["inputs"]

@composite
def auto_res_marker_items(draw,
                          label=label,
                          verify=verify):
    #
    arm_item = draw(just("::"))
    #
    return {"inputs": arm_item,
            "label": label,
            "to_str": build_auto_res_marker_str,
            "verify": verify}
