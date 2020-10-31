from hypothesis.strategies import integers
from hypothesis.strategies import composite, lists

from .forms import form_items

from .separators import separator_strings

from custom.label.anon_funcs import label
from custom.verify.anon_funcs import verify, verify_with_metadata
from custom.parameters import coll_max, metadata_max

from .util import make_form_with_metadata_str_builder

marker = "#"
open_delim = "("
close_delim = ")"

# XXX: could also have stuff after delimiters
def build_anon_func_str(anon_func_item):
    items = anon_func_item["inputs"]
    seps = anon_func_item["separators"]
    anon_func_elts = []
    for i, s in zip(items, seps):
        anon_func_elts += i["to_str"](i) + s
    return marker + open_delim + "".join(anon_func_elts) + close_delim

@composite
def bare_anon_func_items(draw,
                         elements=form_items(),
                         separators=separator_strings(),
                         label=label,
                         verify=verify):
    #
    n = draw(integers(min_value=0, max_value=coll_max))
    #
    items = draw(lists(elements=elements,
                       min_size=n, max_size=n))
    #
    sep_strs = draw(lists(elements=separators,
                          min_size=n, max_size=n))
    if n > 0:
        sep_strs = sep_strs[:-1] + [""]
    #
    return {"inputs": items,
            "label": label,
            "to_str": build_anon_func_str,
            "verify": verify,
            "separators": sep_strs,
            "marker": marker,
            "open": open_delim,
            "close": close_delim}

@composite
def anon_func_with_metadata_items(draw,
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
    af_item = draw(bare_anon_func_items(elements=elements,
                                        separators=separators,
                                        label=label,
                                        verify=verify))
    #
    str_builder = make_form_with_metadata_str_builder(build_anon_func_str)
    #
    m = draw(integers(min_value=1, max_value=metadata_max))
    #
    md_items = draw(lists(elements=metadata_items(flavor=metadata),
                          min_size=m, max_size=m))
    #
    af_item.update({"to_str": str_builder,
                    "metadata": md_items})
    #
    return af_item

@composite
def anon_func_items(draw,
                    elements=form_items(),
                    separators=separator_strings(),
                    metadata=False,
                    label=label,
                    verify=verify):
    if not metadata:
        return draw(bare_anon_func_items(elements=elements,
                                         separators=separators,
                                         label=label,
                                         verify=verify))
    else:
        return draw(anon_func_with_metadata_items(elements=elements,
                                                  separators=separators,
                                                  metadata=metadata,
                                                  label=label,
                                                  verify=verify))
