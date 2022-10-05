from setuptools import setup

setup(name='firstgalaxydata',
      version='0.1',
      description='Package to load radio galaxy data',
      author='Florian Griese',
      packages=['firstgalaxydata'],
      install_requires=['numpy>=1.23.3', 'astropy~=5.0','h5py~=3.6.0','setuptools~=59.2.0','torch~=1.11.0','torchvision~=0.12.0','matplotlib~=3.5.1','Pillow>=9.2.0'],
      zip_safe=False)