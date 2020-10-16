from hypothesis.strategies import composite

from .strings import string_items

from .loader import verify_fns, label_for
import os
name = os.path.splitext(os.path.basename(__file__))[0]
verify, _ = verify_fns(name)
label = label_for(name)

marker = '#'

def build_regex_str(item):
    str_item = item["inputs"]
    return marker + str_item["to_str"](str_item)

@composite
def regex_items(draw):
    str_item = draw(string_items())
    #
    return {"inputs": str_item,
            "label": label,
            "to_str": build_regex_str,
            "verify": verify,
            "marker": marker}
