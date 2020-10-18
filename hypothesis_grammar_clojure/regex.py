from hypothesis.strategies import composite

from .strings import string_items

from custom.label.regex import label
from custom.verify.regex import verify

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
