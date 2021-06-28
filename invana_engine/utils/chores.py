from importlib import import_module


def import_klass(klass_path_string):
    components = klass_path_string.split('.')
    module = import_module(".".join(components[0: (components.__len__() - 1)]))
    return getattr(module, components[-1])
