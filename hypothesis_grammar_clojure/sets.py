from hypothesis.strategies import integers
from hypothesis.strategies import composite, lists

from .forms import form_items

from .separators import separator_strings

from custom.label.sets import label
from custom.verify.sets import verify, verify_with_metadata
from custom.parameters import coll_max, metadata_max

from .util import make_form_with_metadata_str_builder

marker = "#"
open_delim = "{"
close_delim = "}"

# XXX: could also have stuff before and after delimiters
def build_set_str(set_item):
    items = set_item["inputs"]
    seps = set_item["separators"]
    set_elts = []
    for i, s in zip(items, seps):
        set_elts += i["to_str"](i) + s
    return marker + open_delim + "".join(set_elts) + close_delim

@composite
def bare_set_items(draw,
                   elements=form_items(),
                   separators=separator_strings(),
                   label=label,
                   verify=verify):
    #
    n = draw(integers(min_value=0, max_value=coll_max))
    #
    items = draw(lists(elements=elements, min_size=n, max_size=n))
    #
    sep_strs = draw(lists(elements=separators,
                          min_size=n, max_size=n))
    if n > 0:
        sep_strs = sep_strs[:-1] + [""]
    #
    return {"inputs": items,
            "label": label,
            "to_str": build_set_str,
            "verify": verify,
            "separators": sep_strs,
            "marker": marker,
            "open": open_delim,
            "close": close_delim}

@composite
def set_with_metadata_items(draw,
                            elements=form_items(),
                            separators=separator_strings(),
                            metadata="metadata",
                            label=label,
                            verify=verify_with_metadata):
    # avoid circular dependency
    from .metadata import metadata_items, check_metadata_flavor
    #
    check_metadata_flavor(metadata)
    #
    set_item = draw(bare_set_items(elements=elements,
                                   separators=separators,
                                   label=label,
                                   verify=verify))
    #
    str_builder = make_form_with_metadata_str_builder(build_set_str)
    #
    m = draw(integers(min_value=1, max_value=metadata_max))
    #
    md_items = draw(lists(elements=metadata_items(flavor=metadata),
                          min_size=m, max_size=m))
    #
    set_item.update({"to_str": str_builder,
                     "metadata": md_items})
    #
    return set_item

@composite
def set_items(draw,
              elements=form_items(),
              separators=separator_strings(),
              metadata=False,
              label=label,
              verify=verify):
    #
    if not metadata:
        return draw(bare_set_items(elements=elements,
                                   separators=separators,
                                   label=label,
                                   verify=verify))
    else:
        return draw(set_with_metadata_items(elements=elements,
                                            separators=separators,
                                            metadata=metadata,
                                            label=label,
                                            verify=verify))
