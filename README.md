# Radio Galaxy Dataset
This Radio Galaxy Dataset is a collection and combination of several catalogues using the FIRST radio galaxy survey.
The following catalogues are included in this dataset:
* MiraBest [Catalogue](https://academic.oup.com/mnras/article/466/4/4346/2843096), [Source](https://zenodo.org/record/4288837#.YFSBEdwxlaT)
* Gendre [Catalogue](https://academic.oup.com/mnras/article/404/4/1719/1081038?login=true), Supplementary Data: mnras0404-1719-SD1.pdf, data tables CoNFIG-1 to CoNFIG-4
* Capetti 2017a [Catalogue](https://www.aanda.org/articles/aa/full_html/2017/02/aa29287-16/aa29287-16.html), [Table](https://www.aanda.org/articles/aa/full_html/2017/02/aa29287-16/T1.html)
* Capetti 2017b [Catalogue](https://www.aanda.org/articles/aa/full_html/2017/05/aa30247-16/aa30247-16.html), [Table](http://cdsarc.u-strasbg.fr/viz-bin/qcat?J/A+A/601/A81)
* Baldi 2018 [Catalogue](https://www.aanda.org/articles/aa/full_html/2018/01/aa31333-17/aa31333-17.html), [Table](https://www.aanda.org/articles/aa/full_html/2018/01/aa31333-17/T1.html)
* Proctor [Catalogue](https://ui.adsabs.harvard.edu/abs/2011ApJS..194...31P/abstract), [Table](https://iopscience.iop.org/article/10.1088/0067-0049/194/2/31#apjs390184t1), data from Table 1 with label “WAT” and “NAT”

When using the literature class definition of FRI, FRII, Compact and Bent as schown below, 
![image](img/Classification_Scheme.png)
the dataset contains the following number of samples per class.

| classes/split     | FRI |   FRII |     Compact |    Bent |   Total     |
| ----------- | ----------- |----------- |----------- |-----------       |-----------|
| train     | 395       |824       |291       |248       |1758       |
| valid   | 50        | 50       | 50       | 50      |200       |
| test   | 50        | 50       | 50       | 50      |200       |
| total   | 495        |924       |391       |348       |2158       |

# Installation usage with pytorch
If you want to use the dataset via the dataset class `FIRSTGalaxyData` with pytorch, install the necessary packages with

`pip3 install -r requirements.txt`

first, otherwise you can use the dataset
* directly with *.png files on disk or
* load the dataset directly from the HDF5 file.

Both options are descibed further below.

# usage with pytorch
```
from firstgalaxydata import FIRSTGalaxyData
import torchvision.transforms as transforms
```
```
transformRGB = transforms.Compose(
        [transforms.ToTensor(),
         transforms.Normalize(mean=[0.5, 0.5, 0.5], std=[0.5, 0.5, 0.5])])
```
```
data = FIRSTGalaxyData(root="./", selected_split="train", input_data_list=["galaxy_data_h5.h5"],
                           is_PIL=True, is_RGB=True, transform=transformRGB)
```
```print(data)```

This will print out the following output:
```Dataset FIRSTGalaxyData
    Selected classes: dict_values(['FRI', 'FRII', 'Compact', 'Bent'])
    Number of datapoints in total: 1758
    Number of datapoint in class FRI: 395
    Number of datapoint in class FRII: 824
    Number of datapoint in class Compact: 291
    Number of datapoint in class Bent: 248
    Split: train
    Root Location: ./
    Transforms (if any): Compose(
                             ToTensor()
                             Normalize(mean=[0.5, 0.5, 0.5], std=[0.5, 0.5, 0.5])
                         )
    Target Transforms (if any): None
```

## Options
With `selected_split` the data split is selected. Choose either `"train"` or `"valid"` or `"test"`.

With `selected_classes` only data containing the chosen classes is returned. e.g. `["FRI",FRII"]` returns only FRI and FRII images.

With `selected_catalogues` the dataset uses only the selected catalogues. All possible catalogues are listed here:

`selected_catalogues= ["Gendre", "MiraBest", "Capetti2017a", "Capetti2017b", "Baldi2018", "Proctor_Tab1"]`

```data = FIRSTGalaxyData(root="./", selected_split="train", input_data_list=["galaxy_data_h5.h5"], selected_catalogues=selected_catalogues, is_PIL=True, is_RGB=True, transform=transformRGB)```

# basic usage with files on disk
You will also find the dataset in the 'galaxy_data' folder by unzipping `galaxy_data.zip`.
It contains the following folder sturcture with *.png images. The most import information will also be part of the file name separated by underscores:
`RA_DEC_Label_Source.png`
E.g. `14.084_-9.608_3_MiraBest.png`
```
galaxy_data  
│
└───all
│   │   Bent
|   |       *.png  
│   │   Compact
|   |       *.png  
|   |   FRI
|   |       *.png  
│   │   FRII
|   |       *.png  
│   
└───test
│   │   Bent
|   |       *.png  
│   │   Compact
|   |       *.png  
|   |   FRI
|   |       *.png  
│   │   FRII
|   |       *.png
│   
└───train
│   │   Bent
|   |       *.png  
│   │   Compact
|   |       *.png  
|   |   FRI
|   |       *.png  
│   │   FRII
|   |       *.png
│   
└───valid
│   │   Bent
|   |       *.png  
│   │   Compact
|   |       *.png  
|   |   FRI
|   |       *.png  
│   │   FRII
|   |       *.png
```
 

# basic usage with HDF5 file 
The dataset can also be accessed via the HDF5 file `galaxy_data_h5.h5`. 
Every data entry consists of a group named `data_$(i)` with `i=1...n` where `n` is the total number of data entries.`
Each group consists of the following data:
* `Img`: two-dimensional uint8 array with (300,300)
  * Attributes of `Img`:
  * `RA` right ascension equatorial  coordinate  system (J2000): double
  * `DEC` declination equatorial  coordinate  system (J2000): double 
  * `Source`: string, ["Gendre", "MiraBest", "Capetti2017a", "Capetti2017b", "Baldi2018", "Proctor_Tab1"]
  * `Filepath_literature`: string, relative path to the *.png file in the folder `galaxy_data`
* `Label_literature`: double scalar, 0: ”FRI”, 1: ”FRII”, 2: ”Compact”, 3: ”Bent”
* `Split_literature`: string, ["train","test","valid"]





