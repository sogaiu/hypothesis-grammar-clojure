from hypothesis.strategies import composite, just, one_of

from .symbols import symbol_items

from label.symbolic_values import label
from verify.symbolic_values import verify

marker = '##'

def build_symbolic_value_str(item):
    sym_item = item["inputs"]
    # XXX: there can be one or more non_forms between the marker and symbol...
    return marker + sym_item["to_str"](sym_item)

@composite
def symbolic_value_items(draw):
    sym_val_str = draw(one_of(just("Inf"), just("-Inf"), just("NaN")))
    #
    # XXX: a bit of a hack?
    sym_item = draw(symbol_items())
    sym_item["inputs"] = sym_val_str
    #
    return {"inputs": sym_item,
            "label": label,
            "to_str": build_symbolic_value_str,
            "verify": verify,
            "marker": marker}
