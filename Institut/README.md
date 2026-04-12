# Institut
This repository contains some tasks, python scripts and jupiter notebooks with tools and scripts that I developed during my time as an intern at Institut Cartogràfic i Geològic de Catalunya
The data used in this repository is not confidential, and is publicly available at the official website of the organization.

#### Modules
the python modules used in this repository are:
- Numpy
- pandas
- arcpy
- qgis.core
- geopandas

###### notes
> Python interpreter
    the interpreter that works with arcpy is the one integrated in Arcgis Pro
      - arcpy: 3.9.18

    for the other parts that don't use arcpy, any interpreter works, preferable the 3.12 version onwards


--*pandas tutorials and snippets are shown in the last part*

## Aureum
Aureum is the main directory of this repository that contains all the scripts and tools 
The python scripts are divided in subdirectories according to their environment.

- **arcpy_books**: they run in the ArcGis environment, either with the python interpreter originary from arcgis pro or via jupiter notebook
- **pyQgis_books**: they run in the QGIS environment. the python snippets are to be run in the python console integrated in QGIS.
- **geopandas**: these are sample scripts showcasing some of the geopandas library applications to manage and process geospatial data
- **tabular**: they run in a common python environment, on any IDE like visual studio or spyder. These scripts manage tabular data, mainly originary from excel files

#### Mementos
the mementos files work as personal basefiles, containing the the general functions that are used in many other files. 
these functions are then called to be used in the other files of the repository.

- */Aureum/Mementos_au.py*: it has general functions, like opening excel files and reading the data, or opening PDF files to read their contents.
- */Aureum/arcpy_books/Mementos_arc.py*: it has functions appliable to arcPy processes: 
        > opening an arcgis project, getting the attribute fields of a feature class, listing the files stored within a database,  converting files between raster, geopackage, geodatabase, shapefiles, exporting layouts...
- */Aureum/pyQgis_books/mementos_Qgis.py*: same as Mementos_arc but in pyQgis environment.


## guides
a directory with personal notes, guides and useful web links that help in the use of the libraries and python tools stored in this repository


