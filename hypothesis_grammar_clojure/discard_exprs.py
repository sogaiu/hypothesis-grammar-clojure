from hypothesis.strategies import composite

from .forms import form_items

from custom.label.discard_exprs import label
from custom.verify.discard_exprs import verify

marker = '#_'

def build_discard_expr_str(item):
    some_item = item["inputs"]
    # XXX: space here should really be separator, but can
    #      also be empty string
    return marker + " " + some_item["to_str"](some_item)

# XXX: make another key-value pair for the repeat non_form?
@composite
def discard_expr_items(draw, elements=form_items()):
    some_item = draw(elements)
    #
    return {"inputs": some_item,
            "label": label,
            "to_str": build_discard_expr_str,
            "verify": verify,
            "marker": marker}
