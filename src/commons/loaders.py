# pylint: skip-file
from importlib import import_module
from importlib.util import find_spec
from pathlib import Path
from pkgutil import iter_modules


def autodiscovery(root_module, _globals, *, condition, resolver=lambda x: x):
    """
    Autodiscovery module.

    Args:
        root_module (str, required): Dotted module path.
        _globals (str, required): Base module globals reference.
        condition (func, required): Condition test to load the module.
        resolver (func, optional): Module name resolver.
    """
    package_dir = Path(import_module(root_module).__file__).resolve().parent

    for (_, module_name, _) in iter_modules([str(package_dir)]):
        try:
            module = find_spec(resolver(f"{root_module}.{module_name}"))

            if not module:
                # ignore when no module was found.
                continue

        except ModuleNotFoundError:
            continue

        else:
            module = module.loader.load_module()

        for attribute in filter(
            condition, map(lambda x: getattr(module, x), dir(module))
        ):
            _globals[attribute.__name__] = attribute
