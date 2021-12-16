import pandas as pd
import numpy as np
import os
import matplotlib.image as img
import matplotlib.pyplot as plt
from tqdm import tqdm
# import cupy as np_gpu
import numpy as np_gpu
import pathlib
from astropy import units as u
from astropy.coordinates import SkyCoord
import re


global_definition_lit = "literature"
global_definition_cdl1 = "CDL1"


def get_class_dict(definition=global_definition_lit):
    """
    Returns the class definition for the galaxy images.
    :param definition: str, optional
        either literature or CDL1
    :return: dict
    """
    if definition == global_definition_lit:
        return {0: "FRI",
                1: "FRII",
                2: "Compact",
                3: "Bent"}
    elif definition == global_definition_cdl1:
        return {0: "FRI-Sta",
                1: "FRII",
                2: "Compact",
                3: "FRI-WAT",
                4: "FRI-NAT"}
    else:
        raise Exception("Definition: {} is not implemented.".format(definition))


def get_class_dict_rev(definition=global_definition_lit):
    """
    Returns the reverse class definition for the galaxy images.
    :param definition: str, optional
    :return: dict
    """
    class_dict = get_class_dict(definition)
    class_dict_rev = {v: k for k, v in class_dict.items()}
    return class_dict_rev


def generate_type_column(definition=global_definition_lit):
    """
    Returns column name for type label depending on class definitions.
    :param definition: str, optional (default=literature)
        other definition CLD1.
    :return: str
    """
    dict_classes = get_class_dict(definition)
    return gen_type_column(dict_classes)


def gen_type_column(dict_classes):
    definition_str = ["{}={}".format(v, k) for k, v in dict_classes.items()]
    type_column_name = "Type ({})".format(",".join(definition_str))
    return type_column_name


def generate_file_name_coords(coords, galaxy_type_label, source):
    """
    :param coords: SkyCoord
        ra and dec
    :param galaxy_type_label: str
        label name
    :param source: str
        source catalog
    :return: str
        combined name for file
    """
    return generate_file_name(round(coords.ra.degree, 3), round(coords.dec.degree, 3), galaxy_type_label, source)


def generate_file_name(ra, dec, galaxy_type_label, source):
    """
    :param ra: float
        Right ascension in degree
    :param dec: float
        Decliniation in degree
    :param galaxy_type_label: str
        label name
    :param source: str
        source catalog
    :return: str
        combined name for file
    """
    return "{}_{}_{}_{}.png".format(round(ra, 3), round(dec, 3), galaxy_type_label, source)


def generate_filepath_column(definition=global_definition_lit):
    """
        Returns column name for filepath depending on class definitions.
        :param definition: str, optional (default=literature)
            other definition CLD1.
        :return: str
        """
    return "filepath_{}".format(definition)


def generate_split_column(definition=global_definition_lit):
    """
        Returns column name for filepath depending on class definitions.
        :param definition: str, optional (default=literature)
            other definition CLD1.
        :return: str
        """
    return "split_{}".format(definition)


def generate_LOFAR_FIRST_column():
    """
    Returns column name for flag whether the item with coordinates is within LOFAR and FIRST catalog.
    :return: str
    """
    return "included_LOFAR_FIRST"


def get_empty_df():
    """
    Create empty dataframe for galaxy data.
    :return: DataFrame
    """
    return pd.DataFrame({"RA (J2000) degree": [],
                         "DEC (J2000) degree": [],
                         generate_type_column(definition=global_definition_lit): [],
                         generate_type_column(definition=global_definition_cdl1): [],
                         "Source": [],
                         generate_filepath_column(definition=global_definition_lit): [],
                         generate_filepath_column(definition=global_definition_cdl1): [],
                         "coord_str": []})


def parse_filename_to_RA_DEC(filename):
    #filename, file_extension = os.path.splitext(filename)
    # be aware of different "-" characters
    minus_str = '−'
    #print("numeric code of {} {}".format(minus_str, ord(minus_str)))
    #print("numeric code of {} {}".format('-', ord('-')))
    splits_plus = filename[1:].split("+", 2)
    splits_minus = re.split(minus_str+'|-', filename[1:], 2)
    if len(splits_plus) == 2:
        ra_str = "{0} {1} {2}".format(splits_plus[0][0:2], splits_plus[0][2:4], splits_plus[0][4:])
        dec_str = "+{0} {1} {2}".format(splits_plus[1][0:2], splits_plus[1][2:4], splits_plus[1][4:])
        return ra_str, dec_str
    elif len(splits_minus) == 2:
        ra_str = "{0} {1} {2}".format(splits_minus[0][0:2], splits_minus[0][2:4], splits_minus[0][4:])
        dec_str = "-{0} {1} {2}".format(splits_minus[1][0:2], splits_minus[1][2:4], splits_minus[1][4:])
        return ra_str, dec_str
    else:
        raise NameError("Unexpected filename...format not expected")


def add_data(df, label_lit, label_cdl1, source, target_df):
    for index, row in df.iterrows():
        try:
            coords_raw = row.iloc[0].split(" ")[1]
            ra_str, dec_str = parse_filename_to_RA_DEC(coords_raw)
            coord_str = str(ra_str) + " " + str(dec_str)
            c = SkyCoord(coord_str, unit=(u.hourangle, u.deg))
            file_path_lit = pathlib.Path(os.path.join(get_class_dict()[label_lit],
                                                      generate_file_name_coords(c, label_lit, source)))
            file_path_cdl1 = pathlib.Path(os.path.join(get_class_dict()[label_cdl1],
                                                       generate_file_name_coords(c, label_cdl1, source)))
            target_df = add_element(target_df, round(c.ra.degree, 3), round(c.dec.degree, 3), label_lit, label_cdl1,
                                    source, file_path_lit, file_path_cdl1, coord_str)

        except (ValueError, IndexError):
            print("problem with number: " + str(index))
            print(c)
    return target_df


def add_element(df, ra, dec, label_lit, label_cdl1, source, file_path_lit, file_path_cdl1, coord_str):
    df = df.append({"RA (J2000) degree": ra, #round(c.ra.degree, 3)
                    "DEC (J2000) degree": dec, #round(c.dec.degree, 3)
                    generate_type_column(definition=global_definition_lit): label_lit,
                    generate_type_column(definition=global_definition_cdl1): label_cdl1,
                    "Source": source,
                    generate_filepath_column(definition=global_definition_lit): file_path_lit.as_posix(),
                    generate_filepath_column(definition=global_definition_cdl1): file_path_cdl1.as_posix(),
                    "coord_str": coord_str}, ignore_index=True)
    return df


def set_nan_to_zero(img):
    """
    Set nan values to zero.
    :param img:
    :return:
    """
    nan = np.isnan(img)
    img[nan] = 0
    return img


def preprocess_clip_normalize(img, std, sigma=3.0):
    """ Clips the image with respect to sigma * standard deviation.
    :param img: numpy.ndarray (float)
        image
    :param std: float
        standard deviation
    :param sigma: float
        factor of how many std should be clipped
    :return: numpy.ndarray (float)
        normalized image between 0 and 1
    """
    # clip with 3 sigma (local_rms)
    img_clip = np.clip(img, sigma * std, np.inf)
    # normalize to 0 and 1
    img_norm = (img_clip - np.min(img_clip)) / (np.max(img_clip) - np.min(img_clip))
    return img_norm


def convert_to_unit8(img):
    """
    Convert to range 0 to 255 and uint8 in order to make convertible to PIL object
    :param img: numpy.ndarray (float)
        img should be normalized between 0 and 1
    :return: numpy.ndarray (uint8)
        img is between 0 and 255
    """
    img = 255 * img
    img = img.astype(np.uint8)
    return img


def rgb2gray(I):
    return (np_gpu.mean(I, -1) if I.ndim == 3 else I)


def grad(f):
    g = np_gpu.zeros(f.shape + (2,))
    # gy
    g[:-1, :, 0] = f[1:, :] - f[:-1, :]
    # gx
    g[:, :-1, 1] = f[:, 1:] - f[:, :-1]
    return g


def div(f):
    d = np_gpu.zeros(f.shape[:-1])
    d[1:, :] = f[1:, :, 0] - f[:-1, :, 0]
    d[:, 1:] += f[:, 1:, 1] - f[:, :-1, 1]
    return d


def rof(f, sigma=0.5, tau=0.25, l=0.4, iterations=200):
    """
    # the following function implements the primal-dual optimisation for the ROF denosing
    # consider a problem
    # > min_{x} F(Ax) + G(x)
    # and its convex conjugate w.r.t. F** (min_{x} <y,Ax> - F*(y))
    # > min_{x} sup_{y} <y,Ax> - F*(y) + G(x)
    # for A find a corresponding ajoint operator A* s.t. <y,Ax> = <A*y,x>
    # > sup_{y} min_{x} <A*y,x> + G(x) - F*(y)
    # which can further be reformulated as (knowning that G(x) = G**(x) = sup_{x} <y,x> - G(x) ) we arrive to
    # this is a dual formulation of the original primal problem,
    # sup_{y} -G*(-A*y) - F*(y)
    #
    # We want to minimize the primal dual gap
    # G(x,y) = F(Ax) + G(x) - (-G*(-A*y) - F*(y))
    # by maximizing w.r.t the dual and minimizing with respect to primal we exploit the most fucking amazing algorithm
    # ever
    :param f:
    :param sigma:
    :param tau:
    :param l:
    :param iterations:
    :return:
    """
    M, N = f.shape
    u = np_gpu.zeros((M, N))
    uq = np_gpu.zeros((M, N))
    p = np_gpu.zeros((M, N, 2))
    for i in tqdm(range(iterations)):
        p = p + sigma * grad(uq)
        n = np_gpu.maximum(1, np_gpu.sqrt(np_gpu.sum(p ** 2, -1)))
        p[..., 0] = p[..., 0] / n
        p[..., 1] = p[..., 1] / n
        unew = (l * (u + tau * div(p)) + tau * f) / (l + tau)
        uq = 2.0 * unew - u;
        u = np_gpu.maximum(0, np_gpu.minimum(1, unew))

        if i % 50 == 0:
            # img.imsave('/img' + str(i).zfill(5) + '.png',u)
            plt.imshow(u)
            plt.show()

    return u


if __name__ == "__main__":
    generate_type_column()
