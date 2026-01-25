## TFG_Forestal
This folder contains the code used in my bachelor's thesis:

**ESTUDIO DE DIFERENTES TÉCNICAS GEOMÁTICAS APLICADAS EN INVENTARIO FORESTAL**
*Study of different survey techniques applied to forest inventories*

The thesis is published at the University's repository: https://hdl.handle.net/2117/444578

---
This repository contains part of the thesis work, the one corresponding to the Zonal Analysis section.
Unlike the individual analysis, that was performed using open source software such as [3DForest](https://www.3dforest.eu) and [3DFIN](https://github.com/3DFIN/3DFIN), the Zonal analysis was done using the python library of **[pyforestscan](https://pyforestscan.sefa.ai)**. 

#### PyForestScan
**PyforestScan** already has a github repo: https://github.com/iosefa/PyForestScan
I applied this library into my case of study, using my own data and adapting the script to the dataset. 

#### forestAria
3DForest is a C++ developed interface that performs individual analysis to extract metrics from trees point cloud datasets.
It also has its python version,[Forest_3d_app](https://github.com/lloydwindrim/forest_3d_app), and in this folder I've applied this processing to my project dataset. 

##### Libraries and resources Installation
- pyforestscan
    - gdal
    - pdal
- numpy

##### Results

<img src="PyForestScan\fhd.png" alt="Foliage Height Diversity" width="650" />
<img src="PyForestScan\pai.png" alt="Plant Area Index" width="650" />
<img src="PyForestScan\chm.png" alt="Canopy Height Model" width="650" />
