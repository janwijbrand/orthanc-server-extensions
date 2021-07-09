
def hashable(k):
    try:
        return hash(k)
    except TypeError:
        return False


def create_reverse_type_dict(py_type):
    return {v: k for k, v in py_type.__dict__.items() if hashable(v)}
