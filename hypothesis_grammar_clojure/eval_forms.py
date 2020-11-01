from hypothesis.strategies import integers
from hypothesis.strategies import composite, lists, one_of

from .forms import form_items

from .lists import list_items
from .read_conds import read_cond_items
from .symbols import symbol_items

from custom.label.eval_forms import label
from custom.verify.eval_forms import verify, verify_with_metadata
from custom.parameters import metadata_max

from .util import make_form_with_metadata_str_builder

marker = '#='

# XXX: there is one separator of interest and that is potentially
#      between #= and the rest of the form.  the default here is
#      no separator.
def build_eval_form_str(item):
    inputs = item["inputs"]
    return marker + inputs["to_str"](inputs)

# XXX: doesn't have parameterization of label or verify...impractical?
@composite
def evalee_items(draw):
    return draw(one_of(list_items(elements=form_items()),
                       read_cond_items(),
                       symbol_items()))

@composite
def bare_eval_form_items(draw,
                         form=evalee_items(),
                         label=label,
                         verify=verify):
    #
    evalee_item = draw(form)
    #
    return {"inputs": evalee_item,
            "label": label,
            "to_str": build_eval_form_str,
            "verify": verify,
            "marker": marker}

@composite
def eval_form_with_metadata_items(draw,
                                  form=evalee_items(),
                                  metadata="metadata",
                                  label=label,
                                  verify=verify_with_metadata):
    # avoid circular dependency
    from .metadata import metadata_items, check_metadata_flavor
    #
    check_metadata_flavor(metadata)
    #
    evl_form = draw(bare_eval_form_items(form=form,
                                         label=label,
                                         verify=verify))
    #
    str_builder = \
        make_form_with_metadata_str_builder(build_eval_form_str)
    #
    n = draw(integers(min_value=1, max_value=metadata_max))
    #
    md_items = draw(lists(elements=metadata_items(flavor=metadata),
                          min_size=n, max_size=n))
    #
    evl_form.update({"to_str": str_builder,
                     "metadata": md_items})
    #
    return evl_form

@composite
def eval_form_items(draw,
                    form=evalee_items(),
                    metadata=False,
                    label=label,
                    verify=verify):
    if not metadata:
        return draw(bare_eval_form_items(form=form,
                                         label=label,
                                         verify=verify))
    else:
        return draw(eval_form_with_metadata_items(form=form,
                                                  metadata=metadata,
                                                  label=label,
                                                  verify=verify))
