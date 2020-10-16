from hypothesis.strategies import integers
from hypothesis.strategies import composite, lists

from .parameters import metadata_max

from .forms import form_items

from .loader import verify_fns, label_for
import os
name = os.path.splitext(os.path.basename(__file__))[0]
verify, verify_with_metadata = verify_fns(name)
label = label_for(name)

from .util import make_form_with_metadata_str_builder

marker = "`"

# XXX: there is one separator of interest and that is potentially
#      between ` and the rest of the form.  the default here is
#      no separator.
def build_syntax_quote_form_str(item):
    inputs = item["inputs"]
    return marker + inputs["to_str"](inputs)

@composite
def syntax_quote_form_items(draw, metadata=False):
    # avoid circular dependency
    from .metadata import metadata_items, check_metadata_flavor
    #
    check_metadata_flavor(metadata)
    #
    form_item = draw(form_items())
    #
    if not metadata:
        return {"inputs": form_item,
                "label": label,
                "to_str": build_syntax_quote_form_str,
                "verify": verify,
                "marker": marker}
    else:
        str_builder = \
            make_form_with_metadata_str_builder(build_syntax_quote_form_str)
        #
        n = draw(integers(min_value=1, max_value=metadata_max))
        #
        md_items = draw(lists(elements=metadata_items(flavor=metadata),
                              min_size=n, max_size=n))
        #
        return {"inputs": form_item,
                "label": label,
                "to_str": str_builder,
                "verify": verify_with_metadata,
                "metadata": md_items,
                "marker": marker}
