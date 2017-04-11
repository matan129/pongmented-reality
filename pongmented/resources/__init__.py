import os


def get_resource_path(*resource):
    return os.path.join(__file__, '..', *resource)
