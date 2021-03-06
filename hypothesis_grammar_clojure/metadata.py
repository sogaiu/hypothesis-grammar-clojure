from hypothesis.strategies import integers
from hypothesis.strategies import composite, just, one_of

from .keywords import unqualified_keyword_items, \
    qualified_keyword_items
from .maps import map_items
from .read_conds import read_cond_items
from .strings import string_items
from .symbols import symbol_items

from custom.label.metadata import label as md_label
from custom.label.old_metadata import label as old_md_label
from custom.verify.metadata_atom import verify as verify_atom
from custom.verify.metadata_coll import verify as verify_coll

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
def keyword_metadata_items(draw,
                           label=md_label,
                           verify=verify_atom):
    #
    keyword_item = draw(one_of(unqualified_keyword_items(),
                               qualified_keyword_items()))
    #
    return {"inputs": keyword_item,
            "label": label,
            "to_str": build_metadata_str,
            "verify": verify,
            "marker": marker_for_label[label]}

@composite
def map_metadata_items(draw,
                       label=md_label,
                       verify=verify_coll):
    #
    map_item = draw(map_items())
    #
    return {"inputs": map_item,
            "label": label,
            "to_str": build_metadata_str,
            "verify": verify,
            "marker": marker_for_label[label]}

@composite
def read_cond_metadata_items(draw,
                             label=md_label,
                             verify=verify_coll):
    #
    read_cond_item = draw(read_cond_items())
    #
    return {"inputs": read_cond_item,
            "label": label,
            "to_str": build_metadata_str,
            "verify": verify,
            "marker": marker_for_label[label]}

@composite
def string_metadata_items(draw,
                          label=md_label,
                          verify=verify_atom):
    #
    string_item = draw(string_items())
    #
    return {"inputs": string_item,
            "label": label,
            "to_str": build_metadata_str,
            "verify": verify,
            "marker": marker_for_label[label]}

@composite
def symbol_metadata_items(draw,
                          label=md_label,
                          verify=verify_atom):
    #
    symbol_item = draw(symbol_items())
    #
    return {"inputs": symbol_item,
            "label": label,
            "to_str": build_metadata_str,
            "verify": verify,
            "marker": marker_for_label[label]}

@composite
def metadata_items(draw,
                   flavor="metadata",
                   verify_atom=verify_atom,
                   verify_coll=verify_coll):
    #
    assert (flavor != None) and (flavor != False), \
        f'flavor must not be {flavor}'
    #
    if flavor == "any":
        label = draw(one_of(just(md_label),
                            just(old_md_label)))
    elif flavor == "metadata":
        label = md_label
    elif flavor == "old_metadata":
        label = old_md_label
    #
    assert label in [md_label, old_md_label], \
        f'unexpected label value: {label}'
    #
    metadata_item = \
        draw(one_of(map_metadata_items(label=label,
                                       verify=verify_coll),
                    keyword_metadata_items(label=label,
                                           verify=verify_atom),
                    read_cond_metadata_items(label=label,
                                             verify=verify_coll),
                    string_metadata_items(label=label,
                                          verify=verify_atom),
                    symbol_metadata_items(label=label,
                                          verify=verify_atom)))
    return metadata_item

def check_metadata_flavor(metadata):
    # n.b. some strings here coincide with what tree-sitter-clojure
    #      uses, but that is a "coincidence"
    assert metadata in ["any", "metadata", "old_metadata", False, None], \
        f'unexepected metadata specifier: {metadata}'
