from hypothesis.strategies import composite, just

from label.nils import label
from verify.nils import verify

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
