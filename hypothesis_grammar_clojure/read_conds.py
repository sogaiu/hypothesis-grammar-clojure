from hypothesis.strategies import integers
from hypothesis.strategies import composite, lists

from math import floor

from .forms import form_items
from .keywords import keyword_items

from .separators import separator_strings

from custom.label.read_conds import label
from custom.verify.read_conds import verify, verify_with_metadata
from custom.parameters import coll_max, metadata_max

from .util import make_form_with_metadata_str_builder

marker = "#?"
open_delim = "("
close_delim = ")"

# XXX: could also have stuff before and after delimiters
def build_read_cond_str(read_cond_item):
    items = read_cond_item["inputs"]
    seps = read_cond_item["separators"]
    read_cond_elts = []
    for i, s in zip(items, seps):
        read_cond_elts += i["to_str"](i) + s
    # XXX: there can be whitespace between #? and (
    return marker + "" + open_delim + "".join(read_cond_elts) + close_delim

@composite
def read_cond_items(draw,
                    elements=form_items(),
                    separators=separator_strings(),
                    metadata=False):
    # avoid circular dependency
    from .metadata import metadata_items, check_metadata_flavor
    #
    check_metadata_flavor(metadata)
    #
    n = draw(integers(min_value=0, max_value=floor(coll_max/2)))
    # XXX: may be auto-resolved are not allowed?
    kwd_items = draw(lists(elements=keyword_items(),
                           min_size=n, max_size=n))
    #
    frm_items = draw(lists(elements=elements,
                           min_size=n, max_size=n))
    #
    sep_strs = draw(lists(elements=separators,
                          min_size=2*n, max_size=2*n))
    if n > 0:
        sep_strs = sep_strs[:-1] + [""]
    #
    items = [item
             for pair in zip(kwd_items, frm_items)
             for item in pair]
    #
    if not metadata:
        return {"inputs": items,
                "label": label,
                "to_str": build_read_cond_str,
                "verify": verify,
                "separators": sep_strs,
                "marker": marker,
                "open": open_delim,
                "close": close_delim}
    else:
        str_builder = \
            make_form_with_metadata_str_builder(build_read_cond_str)
        #
        m = draw(integers(min_value=1, max_value=metadata_max))
        #
        md_items = draw(lists(elements=metadata_items(flavor=metadata),
                              min_size=m, max_size=m))
        return {"inputs": items,
                "label": label,
                "to_str": str_builder,
                "verify": verify_with_metadata,
                "metadata": md_items,
                "separators": sep_strs,
                "marker": marker,
                "open": open_delim,
                "close": close_delim}
