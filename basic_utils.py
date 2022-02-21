import pandas as pd
import numpy as np
import os
import matplotlib.image as img
import matplotlib.pyplot as plt
from tqdm import tqdm
import numpy as np_gpu
import pathlib
from astropy import units as u
from astropy.coordinates import SkyCoord
import re


global_definition_lit = "literature"


def get_class_dict(definition):
    """
    Returns the class definition for the galaxy images.
    :param definition: str, optional
        either literature
    :return: dict
    """
    if definition == global_definition_lit:
        return {0: "FRI",
                1: "FRII",
                2: "Compact",
                3: "Bent"}
    else:
        raise Exception("Definition: {} is not implemented.".format(definition))


def get_class_dict_rev(definition):
    """
    Returns the reverse class definition for the galaxy images.
    :param definition: str, optional
    :return: dict
    """
    class_dict = get_class_dict(definition)
    class_dict_rev = {v: k for k, v in class_dict.items()}
    return class_dict_rev
