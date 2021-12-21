from firstgalaxydata import FIRSTGalaxyData
import torchvision.transforms as transforms



if __name__ == "__main__":
    transformRGB = transforms.Compose(
        [transforms.ToTensor(),
         transforms.Normalize(mean=[0.5, 0.5, 0.5], std=[0.5, 0.5, 0.5])])

    data = FIRSTGalaxyData(root="./", selected_split="train", input_data_list=["galaxy_data_h5.h5"],

                           is_PIL=True, is_RGB=True, transform=transformRGB)

    print(data)

    data = FIRSTGalaxyData(root="./", selected_split="train", input_data_list=["galaxy_data_h5.h5"],
                           selected_catalogues=["Gendre", "MiraBest", "Capetti2017a", "Capetti2017b", "Baldi2018", "Proctor_Tab1"],
                           is_PIL=True, is_RGB=True, transform=transformRGB)

    print(data)