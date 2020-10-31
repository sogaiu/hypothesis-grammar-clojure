from hypothesis.strategies import integers
from hypothesis.strategies import composite, lists

from .forms import form_items

from custom.label.syntax_quote_forms import label
from custom.verify.syntax_quote_forms import verify, verify_with_metadata
from custom.parameters import metadata_max

from .util import make_form_with_metadata_str_builder

marker = "`"

# XXX: there is one separator of interest and that is potentially
#      between ` and the rest of the form.  the default here is
#      no separator.
def build_syntax_quote_form_str(item):
    inputs = item["inputs"]
    return marker + inputs["to_str"](inputs)

@composite
def bare_syntax_quote_form_items(draw,
                                 forms=form_items()):
    form_item = draw(forms)
    #
    return {"inputs": form_item,
            "label": label,
            "to_str": build_syntax_quote_form_str,
            "verify": verify,
            "marker": marker}

@composite
def syntax_quote_form_with_metadata_items(draw,
                                          forms=form_items(),
                                          metadata="metadata"):
    # avoid circular dependency
    from .metadata import metadata_items, check_metadata_flavor
    #
    check_metadata_flavor(metadata)
    #
    str_builder = \
        make_form_with_metadata_str_builder(build_syntax_quote_form_str)
    #
    n = draw(integers(min_value=1, max_value=metadata_max))
    #
    md_items = draw(lists(elements=metadata_items(flavor=metadata),
                          min_size=n, max_size=n))
    #
    sq_form = draw(bare_syntax_quote_form_items(forms))
    #
    sq_form.update({"to_str": str_builder,
                    "verify": verify_with_metadata,
                    "metadata": md_items})
    #
    return sq_form

@composite
def syntax_quote_form_items(draw,
                            forms=form_items(),
                            metadata=False):
    if not metadata:
        return draw(bare_syntax_quote_form_items(forms=forms))
    else:
        return draw(syntax_quote_form_with_metadata_items(forms=forms,
                                                          metadata=metadata))
