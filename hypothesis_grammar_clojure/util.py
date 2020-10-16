def make_form_with_metadata_str_builder(base_str_builder):
    def builder(item):
        # avoid circular dependency
        from .metadata import attach_metadata
        #
        form_str = base_str_builder(item)
        #
        md_items = item["metadata"]
        md_item_strs = [md_item["to_str"](md_item) for md_item in md_items]
        #
        return attach_metadata(md_item_strs, form_str)
    return builder

def to_ascii(n, cap):
    if n <= 9:
        return chr(n + 48)
    else:
        if cap:
            offset = 55
        else:
            offset = 87
        return chr(n + offset)
