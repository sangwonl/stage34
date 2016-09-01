def merge_dicts(d1, d2):
    if isinstance(d1, dict) and isinstance(d2, dict):
        for k, v in d2.iteritems():
            if k not in d1:
                d1[k] = v
            else:
                d1[k] = merge_dicts(d1[k],v)
    return d1
