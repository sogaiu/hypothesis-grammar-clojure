from hypothesis.strategies import composite, just

from custom.label.nils import label
from custom.verify.nils import verify

def build_nil_str(item):
    return item["inputs"]

@composite
def nil_items(draw,
              label=label,
              verify=verify):
    #
    nil_str = draw(just("nil"))
    #
    return {"inputs": nil_str,
            "label": label,
            "to_str": build_nil_str,
            "verify": verify}
