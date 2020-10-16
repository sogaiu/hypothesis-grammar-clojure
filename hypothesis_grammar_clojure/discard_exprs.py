from hypothesis.strategies import composite

from .loader import verify_fns, label_for
import os
name = os.path.splitext(os.path.basename(__file__))[0]
verify, _ = verify_fns(name)
label = label_for(name)

marker = '#_'

def build_discard_expr_str(item):
    form_item = item["inputs"]
    # XXX: space here should really be separator, but can
    #      also be empty string
    return marker + " " + form_item["to_str"](form_item)

# XXX: make another key-value pair for the repeat non_form?
@composite
def discard_expr_items(draw):
    # avoid circular dependency
    from .forms import form_items
    #
    form_item = draw(form_items())
    #
    return {"inputs": form_item,
            "label": label,
            "to_str": build_discard_expr_str,
            "verify": verify,
            "marker": marker}
