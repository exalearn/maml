"""
Dummy test systems
"""
from pymatgen.core import Composition, Structure, Lattice, Molecule

from ._inspect import get_param_types
from ._data_conversion import to_array


DUMMY_OBJECTS = {
    'str': 'H2O',
    'Composition': Composition('H2O'),
    'Structure': Structure(Lattice.cubic(3.167),
                           ['Mo', 'Mo'],
                           [[0, 0, 0], [0.5, 0.5, 0.5]]),
    'Molecule': Molecule(['C', 'O'], [[0, 0, 0], [1, 0, 0]])
}


def get_describer_dummy_obj(instance):
    """
    For a describer, get a dummy object for transform_one.
    This relies on the type hint.

    Args:
        instance (BaseDescriber): describer instance
    """
    obj_type = getattr(instance, "obj_type", None)
    if obj_type is not None:
        return DUMMY_OBJECTS[obj_type]
    arg_types = get_param_types(instance.transform_one)
    arg_type = list(arg_types.values())[0]
    str_t = str(arg_type)
    if '.' in str_t:
        str_t = str_t.split('.')[-1]
    return DUMMY_OBJECTS[str_t]


def feature_dim_from_test_system(describer):
    """
    Get feature size from a test system

    Args:
        describer (BaseDescriber): describer instance
    """
    dummy_obj = get_describer_dummy_obj(describer)
    features = to_array(describer.transform_one(dummy_obj))
    if features.ndim == 1:
        return None
    else:
        return features.shape[-1]