from firstgalaxydata import FIRSTGalaxyData
import torchvision.transforms as transforms


if __name__ == "__main__":
    transformRGB = transforms.Compose(
        [transforms.ToTensor(),
         transforms.Normalize(mean=[0.5, 0.5, 0.5], std=[0.5, 0.5, 0.5])])

    # Basic usage of splitting train, valid and test

    data = FIRSTGalaxyData(root="./", selected_split="train", input_data_list=["galaxy_data_h5.h5"],
                           is_PIL=True, is_RGB=True, transform=transformRGB)

    img, label = data.__getitem__(0)

    print(data)
    data = FIRSTGalaxyData(root="./", selected_split="valid", input_data_list=["galaxy_data_h5.h5"],
                           is_PIL=True, is_RGB=True, transform=transformRGB)

    print(data)

    data = FIRSTGalaxyData(root="./", selected_split="test", input_data_list=["galaxy_data_h5.h5"],
                           selected_classes=["FRI", "FRII", "Compact", "Bent"],
                           selected_catalogues=["Gendre", "MiraBest", "Capetti2017a", "Capetti2017b",
                                                "Baldi2018", "Proctor_Tab1"],
                           is_PIL=True, is_RGB=True, transform=transformRGB)
    print(data)

    # Usage of 5-fold cross validation set

    data = FIRSTGalaxyData(root="./", selected_split="train", input_data_list=["galaxy_data_crossvalid_0_h5.h5"],
                           is_PIL=True, is_RGB=True, transform=transformRGB)

    print(data)

    data = FIRSTGalaxyData(root="./", selected_split="valid", input_data_list=["galaxy_data_crossvalid_0_h5.h5"],
                           is_PIL=True, is_RGB=True, transform=transformRGB)

    print(data)

    data = FIRSTGalaxyData(root="./", selected_split="test", input_data_list=["galaxy_data_crossvalid_test_h5.h5"],
                           selected_classes=["FRI", "FRII", "Compact", "Bent"],
                           selected_catalogues=["Gendre", "MiraBest", "Capetti2017a", "Capetti2017b",
                                                "Baldi2018", "Proctor_Tab1"],
                           is_PIL=True, is_RGB=True, transform=transformRGB)
    print(data)



