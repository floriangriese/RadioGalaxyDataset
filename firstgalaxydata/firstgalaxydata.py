from __future__ import print_function
import os
import numpy as np
from PIL import Image
import h5py
import torch.utils.data as data
import matplotlib.pyplot as plt
from astropy import units as u
from astropy.coordinates import SkyCoord
from torchvision.datasets.utils import download_url
import zipfile


class FIRSTGalaxyData(data.Dataset):
    """
    FIRSTGalaxyData class provides FIRST images with labels from various different data catalogs

    Attributes
    ----------
    class_dict : dict key: str value: int
        Dictionary of Class defintion and numerial encoding
    urls : dict key: str value: str
        Dictionary of data file and its download link

    Methods
    -------
    __getitem__(index)
        returns data item at index
    __getcoords__(index)
        returns coordinate of data item at index
    __len__()
        return number of data items
    _check_files()
        checks whether the files in input_data_list are in the folder
    download()
        downloads all dataset and overwrites existing ones
    get_occurrences()
        get occurrences of images per class
    show_coords():
        shows the coordinates of the images in a Aitoff projection
    __repr__()
        presents import information about the dataset in the Repl
     """

    urls = {
        "galaxy_data.zip": "https://zenodo.org/record/7689127/files/galaxy_data.zip?download=1",
        "galaxy_data_h5.zip": "https://zenodo.org/record/7689127/files/galaxy_data_h5.zip?download=1",
        "galaxy_data_crossvalid_0_h5.zip": "https://zenodo.org/record/7689127/files/galaxy_data_crossvalid_0_h5.zip?download=1",
        "galaxy_data_crossvalid_1_h5.zip": "https://zenodo.org/record/7689127/files/galaxy_data_crossvalid_1_h5.zip?download=1",
        "galaxy_data_crossvalid_2_h5.zip": "https://zenodo.org/record/7689127/files/galaxy_data_crossvalid_2_h5.zip?download=1",
        "galaxy_data_crossvalid_3_h5.zip": "https://zenodo.org/record/7689127/files/galaxy_data_crossvalid_3_h5.zip?download=1",
        "galaxy_data_crossvalid_4_h5.zip": "https://zenodo.org/record/7689127/files/galaxy_data_crossvalid_4_h5.zip?download=1",
        "galaxy_data_crossvalid_test_h5.zip": "https://zenodo.org/record/7689127/files/galaxy_data_crossvalid_test_h5.zip?download=1"
    }

    def __init__(self, root, input_data_list=None, selected_split="train", selected_classes=None,
                 selected_catalogues=None, is_balanced=False, is_PIL=False, is_RGB=False, transform=None,
                 target_transform=None, is_download=False):
        """
        Parameters
        ----------
        :param root: str
            path directory to the data files
        :param input_data_list: list of str, optional
            list of data files for the data set with train, valid and test split within
        :param selected_split: str, optional (default is train)
            flag whether to use the train, valid or test set
        :param is_balanced: bool, optional (default is False)
            flag whether the dataset should be balanced,
            simplest balancing strategy, number data items determined by the class with the less data items
        :param selected_classes:  list (str), optional, default ["FRI", "FRII", "Compact", "Bent"]
        :param selected_catalogues:  list (str), optional (default is None)
            if None all possible catalogues are selected ["Gendre", "MiraBest", "Capetti2017a", "Capetti2017b", "Baldi2018",
            "Proctor_Tab1"]
        :param is_PIL: bool, optional (default is False)
            flag to return a PIL object
        :param is_RGB: bool, optional (default is False)
            flag to return a RGB image with 3 channels (default greyscale image)
        :param transform: torchvision.transforms.transforms, optional (default None)
            transformation of data
        :param target_transform: torchvision.transforms.transforms, optional (default None)
            transformation of labels
        :param is_download: bool, optional (default is False)
            flag, whether a download should be forced
        """
        self.root = os.path.expanduser(root)
        self.input_data_list = [os.path.join("galaxy_data_h5.h5")] if input_data_list is None else input_data_list
        self.selected_split = selected_split
        self.is_balanced = is_balanced
        self.class_dict = self.get_class_dict()
        self.class_dict_rev = self.get_class_dict_rev()
        self.selected_classes = selected_classes
        if selected_classes is None:
            self.class_labels = self.class_dict.keys()
            self.selected_classes = self.class_dict.values()
        else:
            self.class_labels = [self.class_dict_rev[c] for c in selected_classes]
        self.supported_catalogues = ["Gendre", "MiraBest", "Capetti2017a", "Capetti2017b", "Baldi2018", "Proctor_Tab1"]
        if selected_catalogues is None:
            self.selected_catalogues = self.supported_catalogues
        else:
            self.selected_catalogues = selected_catalogues
        self.is_PIL = is_PIL
        self.is_RGB = is_RGB
        self.transform = transform
        self.target_transform = target_transform

        if is_download:
            self.download()

        if not self._check_files():
            print("Dataset not found. Trying to download...")
            self.download()
            if not self._check_files():
                raise RuntimeError(
                    "Dataset not found (maybe custom dataset) or Dataset corrupted or downloading failed. Check data paths...")

        data_list = self.input_data_list

        self.data = []
        self.labels = []
        self.coordinates = []

        for file_name in data_list:
            file_path = os.path.join(self.root, file_name)
            with h5py.File(file_path, "r") as file:
                for key in file.keys():
                    # filter for selected split
                    if file[key + "/Split_literature"].asstr()[()] == self.selected_split:
                        data_entry = file[key + "/Img"]
                        label_entry = file[key + "/Label_literature"]
                        d = np.array(data_entry)
                        if data_entry.attrs["Source"] not in self.selected_catalogues:
                            continue
                        if data_entry.attrs.__contains__("RA") and data_entry.attrs.__contains__("DEC"):
                            coord = SkyCoord(data_entry.attrs["RA"], data_entry.attrs["DEC"], unit=(u.deg, u.deg))
                        else:
                            raise NotImplementedError("No coords in data_entry at key {}".format(key))

                        self.data.append(d)
                        self.labels.append(np.array(label_entry))
                        self.coordinates.append(coord)

        if self.selected_classes is not None:
            indices = [i for i, d in enumerate(self.labels) if int(d) in self.class_labels]
            self.data = [self.data[i] for i in indices]
            self.labels = [self.labels[i] for i in indices]
            self.coordinates = [self.coordinates[i] for i in indices]

        # simplest balancing strategy, take data occurrence with the least count and ignore more data of other classes
        if self.is_balanced:
            occ = [l for l in self.get_occurrences().values()]
            occ_min = np.min(occ)
            ind_list = []
            for cl in self.class_labels:
                ind = [i for i, d in enumerate(self.labels) if d == cl]
                ind_list = ind_list + ind[0:occ_min]
            self.data = [self.data[i] for i in ind_list]
            self.labels = [self.labels[i] for i in ind_list]
            self.coordinates = [self.coordinates[i] for i in ind_list]

    def __getitem__(self, index):
        img, labels = self.data[index], self.labels[index]

        if self.is_PIL:
            assert img.dtype == np.uint8
            img = Image.fromarray(img, mode="L")
            if self.is_RGB:
                img = img.convert("RGB")

        if self.transform is not None:
            img = self.transform(img)
        if self.target_transform is not None:
            img = self.target_transform(labels)

        return img, int(labels)

    def __getcoords__(self, index):
        return self.coordinates[index]

    def __len__(self):
        return len(self.data)

    def _check_files(self):
        root = self.root
        for data_file in self.input_data_list:
            path = os.path.join(root, data_file)
            if not os.path.exists(path):
                zip_path = "{}{}".format(os.path.splitext(data_file)[0], ".zip")
                if os.path.exists(zip_path):
                    with zipfile.ZipFile(os.path.join(root, zip_path), "r") as zip_ref:
                        zip_ref.extractall(path=root)
                    return True
                else:
                    return False
        return True

    def download(self):
        # download and extract file
        for key in self.urls.keys():
            download_url(self.urls[key], self.root, key)
            with zipfile.ZipFile(os.path.join(self.root, key), "r") as zip_ref:
                zip_ref.extractall(path=self.root)

    def get_occurrences(self):
        occ = {l: self.labels.count(l) for l in self.class_labels}
        return occ

    def show_coords(self):
        plt.figure(figsize=(8, 4.2))
        plt.subplot(111, projection="aitoff")
        plt.title("Aitoff projection of coordinates")
        plt.grid(True)
        for c in self.coordinates:
            if c is not None:
                ra_rad = c.ra.wrap_at(180 * u.deg).radian
                dec_rad = c.dec.radian
                plt.plot(ra_rad, dec_rad, 'o', markersize=1.5, color="red", alpha=0.3)

        plt.subplots_adjust(top=0.95, bottom=0.0)
        plt.show()

    def get_class_dict(self):
        """
        Returns the class definition for the galaxy images.
        :return: dict
        """
        return {0: "FRI",
                1: "FRII",
                2: "Compact",
                3: "Bent"}

    def get_class_dict_rev(self):
        """
        Returns the reverse class definition for the galaxy images.
        :return: dict
        """
        class_dict = self.get_class_dict()
        class_dict_rev = {v: k for k, v in class_dict.items()}
        return class_dict_rev

    def __repr__(self):
        fmt_str = 'Dataset ' + self.__class__.__name__ + '\n'
        fmt_str += '    Selected classes: {}'.format(self.selected_classes) + '\n'
        fmt_str += '    Number of datapoints in total: {}\n'.format(self.__len__())
        for c in self.selected_classes:
            fmt_str += '    Number of datapoint in class {}: {}\n'.format(c, self.labels.count(self.class_dict_rev[c]))
        tmp = self.selected_split
        fmt_str += '    Split: {}\n'.format(tmp)
        fmt_str += '    Root Location: {}\n'.format(self.root)
        tmp = '    Transforms (if any): '
        fmt_str += '{0}{1}\n'.format(tmp, self.transform.__repr__().replace('\n', '\n' + ' ' * len(tmp)))
        tmp = '    Target Transforms (if any): '
        fmt_str += '{0}{1}'.format(tmp, self.target_transform.__repr__().replace('\n', '\n' + ' ' * len(tmp)))
        return fmt_str

