# Radio Galaxy Dataset
This Radio Galaxy Dataset is a collection and combination of several catalogues using the FIRST radio galaxy survey.
The following catalogues are included in this dataset:
* MiraBest [Catalog](https://academic.oup.com/mnras/article/466/4/4346/2843096), [Source](https://zenodo.org/record/4288837#.YFSBEdwxlaT)
* Gendre [Catalog](https://academic.oup.com/mnras/article/404/4/1719/1081038?login=true), Supplementary Data: mnras0404-1719-SD1.pdf, data tables CoNFIG-1 to CoNFIG-4
* Capetti 2017a [Catalog](https://www.aanda.org/articles/aa/full_html/2017/02/aa29287-16/aa29287-16.html), [Table](https://www.aanda.org/articles/aa/full_html/2017/02/aa29287-16/T1.html)
* Capette 2017b [Catalog](https://www.aanda.org/articles/aa/full_html/2017/05/aa30247-16/aa30247-16.html), [Table](http://cdsarc.u-strasbg.fr/viz-bin/qcat?J/A+A/601/A81)
* Balid 2018 [Catalog](https://www.aanda.org/articles/aa/full_html/2018/01/aa31333-17/aa31333-17.html), [Table](https://www.aanda.org/articles/aa/full_html/2018/01/aa31333-17/T1.html)
* Proctor [Catalog](https://ui.adsabs.harvard.edu/abs/2011ApJS..194...31P/abstract), [Table](https://iopscience.iop.org/article/10.1088/0067-0049/194/2/31#apjs390184t1), data from Table 1 with label “WAT” and “NAT”

When using the literature class definition of FRI, FRII, Compact and Bent as schown below, 
![image](img/Classification_Scheme.png)
the dataset contains the following number of samples per class.

| classes/split     | FRI |   FRII |     Compact |    Bent |   Total     |
| ----------- | ----------- |----------- |----------- |-----------       |-----------|
| train     | 395       |824       |291       |248       |1758       |
| valid   | 50        | 50       | 50       | 50      |200       |
| test   | 50        | 50       | 50       | 50      |200       |
| total   | 495        |924       |391       |348       |2158       |

# Installation
If you want to use the dataset via the dataset class `FIRSTGalaxyData` with pytorch, install the necessary packages with

`pip3 install -r requirements.txt`

first, otherwise you will find the corredponding folder sturcture with images in the
`galaxy_data.zip'
file.

# Basic usage
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
With `selected_split` the data split is selcted. Choose either `"train"` or `"valid"` or `"test"`.

With `selected_catalogues` the dataset uses only the selected catalogues. All possible catalogues are listed here:

`selected_catalogues= ["Gendre", "MiraBest", "Capetti2017a", "Capetti2017b", "Baldi2018", "Proctor_Tab1"]`

```data = FIRSTGalaxyData(root="./", selected_split="train", input_data_list=["galaxy_data_h5.h5"], selected_catalogues=selected_catalogues, is_PIL=True, is_RGB=True, transform=transformRGB)```

With `class_definition` the class defintions of the dataset is selected. Choose either between `"literature"` or `"CDL1"`.
```
data = FIRSTGalaxyData(root="./", selected_split="train", input_data_list=["galaxy_data_h5.h5"], class_definition="CDL1", is_PIL=True, is_RGB=True, transform=transformRGB)
```
With CDL1 the classes FRI and Bent are subdivided into the three classes FRI-Sta, FRI-Nat and FRI-Wat as you can see in the following scheme:
![image](img/Classification_Scheme_CDL1.png)