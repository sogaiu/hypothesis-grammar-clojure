from hypothesis.strategies import integers
from hypothesis.strategies import composite, just, one_of

from .keywords import unqualified_keyword_items, \
    qualified_keyword_items
from .maps import map_items
from .read_conds import read_cond_items
from .strings import string_items
from .symbols import symbol_items

from .separators import separator_strings

from .loader import verify_fns, label_for
verify_atom, _ = verify_fns("metadata_atom")
verify_coll, _ = verify_fns("metadata_coll")
md_label = label_for("metadata")
old_md_label = label_for("old_metadata")
# XXX: kind of hacky...
if md_label is None:
    md_label = "metadata"
if old_md_label is None:
    old_md_label = "old_metadata"

marker_for_label = \
    {md_label: "^",
     old_md_label: '#^'}

# XXX: there is one separator of interest and that is potentially
#      between ^ / #^ and the rest of the form.  the default here is
#      no separator.
def build_metadata_str(md_item):
    inner_item = md_item["inputs"]
    #
    marker = md_item["marker"]
    body_str = inner_item["to_str"](inner_item)
    #
    return f'{marker}{body_str}'

def attach_metadata(metadata_strs, metadatee_str):
    # XXX: another "what to do about separator" location
    return " ".join(metadata_strs + [metadatee_str])

# XXX: only non-auto-resolved-keywords are valid
@composite
def keyword_metadata_items(draw, label=md_label):
    keyword_item = draw(one_of(unqualified_keyword_items(),
                               qualified_keyword_items()))
    #
    return {"inputs": keyword_item,
            "label": label,
            "to_str": build_metadata_str,
            "verify": verify_atom,
            "marker": marker_for_label[label]}

@composite
def map_metadata_items(draw, label=md_label):
    map_item = draw(map_items())
    #
    return {"inputs": map_item,
            "label": label,
            "to_str": build_metadata_str,
            "verify": verify_coll,
            "marker": marker_for_label[label]}

@composite
def read_cond_metadata_items(draw, label=md_label):
    read_cond_item = draw(read_cond_items())
    #
    return {"inputs": read_cond_item,
            "label": label,
            "to_str": build_metadata_str,
            "verify": verify_coll,
            "marker": marker_for_label[label]}

@composite
def string_metadata_items(draw, label=md_label):
    string_item = draw(string_items())
    #
    return {"inputs": string_item,
            "label": label,
            "to_str": build_metadata_str,
            "verify": verify_atom,
            "marker": marker_for_label[label]}

@composite
def symbol_metadata_items(draw, label=md_label):
    symbol_item = draw(symbol_items())
    #
    return {"inputs": symbol_item,
            "label": label,
            "to_str": build_metadata_str,
            "verify": verify_atom,
            "marker": marker_for_label[label]}

@composite
def metadata_items(draw, flavor="metadata"):
    if flavor == "any":
        label = draw(one_of(just(md_label),
                            just(old_md_label)))
    #
    assert label in [md_label, old_md_label], \
        f'unexpected label value: {label}'
    #
    metadata_item = \
        draw(one_of(map_metadata_items(label=label),
                    keyword_metadata_items(label=label),
                    read_cond_metadata_items(label=label),
                    string_metadata_items(label=label),
                    symbol_metadata_items(label=label)))
    return metadata_item

def check_metadata_flavor(metadata):
    # n.b. some strings here coincide with what tree-sitter-clojure
    #      uses, but that is a "coincidence"
    assert metadata in ["any", "metadata", "old_metadata", False, None], \
        f'unexepected metadata specifier: {metadata}'
