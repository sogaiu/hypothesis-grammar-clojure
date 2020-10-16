import importlib, os

def verify_fns(path):
    cur_dir = os.path.dirname(__file__)
    if os.path.exists(f'{cur_dir}/../verify'):
        module_dict = \
            importlib.import_module(f'..verify.{path}', __package__).__dict__
        verify = module_dict["verify"]
        if "verify_with_metadata" in module_dict:
            verify_with_metadata = \
                module_dict["verify_with_metadata"]
        else:
            verify_with_metadata = None
    else:
        verify = lambda ctx, item: True
        verify_with_metadata = lambda ctx, item: True
    return verify, verify_with_metadata

def label_for(path):
    cur_dir = os.path.dirname(__file__)
    if os.path.exists(f'{cur_dir}/../label'):
        module_dict = \
            importlib.import_module(f'..label.{path}', __package__).__dict__
        label = module_dict["label"]
    else:
        label = None
    return label
