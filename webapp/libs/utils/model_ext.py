from itertools import chain


def model_to_dict(instance, fields=None, exclude=None):
    data = {}

    # populate model fields
    opts = instance._meta
    for f in chain(opts.concrete_fields, opts.private_fields, opts.many_to_many):
        if not getattr(f, 'editable', False):
            continue
        if fields and f.name not in fields:
            continue
        if exclude and f.name in exclude:
            continue
        data[f.name] = f.value_from_object(instance)

    # populate property decorated
    model_cls = type(instance)
    properties = [name for name, val in vars(model_cls).items() if isinstance(val, property)]
    for prop_name in properties:
        data[prop_name] = getattr(instance, prop_name)

    return data