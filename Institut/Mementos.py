# coding= UTF-8
import os
import arcpy


def selShp(): #seleccionar fichers d'un workspace. cal haver definit un workspace d'ArcGis prèviament
    catalog= {}
    features= arcpy.ListFeatureClasses()
    n=0
    for fin in features:
       n+=1
       catalog[n] = fin
    print(catalog)
    print(len(catalog))
    shapesList=[]
    while True:
        #shfile= input('Specify shapefile name:base (press intro once you"re finished: ')
        order= input('write nºshape(press intro once you"re finished: ')
        if order.isnumeric():
            ord= int(order)
            shapesList.append(catalog[ord])
        else:
            break
        
    return shapesList

def hasSpatialRef(fc_list,workspace):#check if a feature class is referenced, and which.
    if type(fc_list) == list() and len(fc_list)> 1:
        for f in fc_list:
            desc = arcpy.Describe(workspace+'/'+f)
            spat_ref= desc.spatialReference
            if spat_ref.name == "Unknown":
                print("{} has an unknown spatial reference".format(f))
            # Otherwise, print out the feature class name and spatial reference
            else:
                print("{} : {}".format(f, spat_ref.name))
                
    elif type(fc_list) == list() and len(fc_list)== 1:
        desc = arcpy.Describe(workspace+'/'+f)
        spat_ref= desc.spatialReference
        if spat_ref.name == "Unknown":
            print("{} has an unknown spatial reference".format(f))
        # Otherwise, print out the feature class name and spatial reference
        else:
            print("{} : {}".format(f, spat_ref.name))
    elif type(fc_list) == str:
        desc = arcpy.Describe(workspace+'/'+f)
        spat_ref= desc.spatialReference
        if spat_ref.name == "Unknown":
            print("{} has an unknown spatial reference".format(f))
        # Otherwise, print out the feature class name and spatial reference
        else:
            print("{} : {}".format(f, spat_ref.name))
  
def definePrj(fc_list,workspace):    #define projection of a feature class.
    newList=[]
    for f in fc_list:
        desc = arcpy.Describe(workspace+'/'+f)
        if desc.spatialReference.name =='Unknown':
            arcpy.management.DefineProjection(f,coor_system=25831)
            newList.append(f)
        else:
            newList.append(f)
            continue
    return newList


def Project(fc_list,workspace): #project a feature class into another coordinate system. similar to ArcGis tool.
    newList=[]
    for f in fc_list:
        newName= 'UTM30'+f
        print(workspace+newName)
        if os.path.isfile(workspace+'/'+newName):
            newList.append(newName)
            continue
        else:
            arcpy.management.Project(f,newName,in_coor_system=25831,out_coor_system=25830)
            newList.append(newName)
    return newList


def filterby(type):#choose how something will be filtered. type: [attribute/element]
    if type== 'attribute':
        filFields=[]
        while True:
            field= str(input("Camp a filtrar(press intro to finish): "))
            if field:
                filFields.append(field)
            else:
                break
        return filFields
    elif type== 'element':
        filElement=[]
        while True:
            elem= str(input("Nom de l'element a filtrar(press intro to finish): "))
            if elem:
                filElement.append(elem)
            else:
                break
        return filElement


def ListProjects(directoryRoute,type=''):#List the project files that are inside a directory.
    #listar elementos en un directorio y los subdirectorios de dentro
    #arcpy.env.workspace = directoryRoute
    try:
        files = os.listdir(directoryRoute)
        for file in files:
            try:
                #if file.split(".")[1] == "%s" %(type):
                if file.endswith("%s" %(type)):
                    #print(directoryRoute)
                    print(file)
                    fRoute= "%s\\%s" % (directoryRoute,file)
                    #colFiles.extend(file)
                    #filesRoutes.extend(fRoute)
                elif os.path.isdir(file) == True:
                    subdirectory = "%s\\%s" % (directoryRoute, file)
                    #listDirect.append(subdirectory)
                    print('subdir',subdirectory)
                    subfiles = os.listdir(subdirectory)

                    ListProjects(subdirectory, type)

            except IndexError:
                continue
        #print('allroutes:', filesRoutes)


    except FileNotFoundError:
        directoryRoute = input('Specify route: ')
        type = input('File extension: ')

#
def extractPol(shp,camps,filtre):
    with arcpy.da.SearchCursor(shp[0],camps, filtre) as cursor:
        for row in cursor:
            print(u'{0}, {1}'.format(row[0], row[1]))

        camps2= filterby(shp[1],type='attribute')
        with arcpy.da.UpdateCursor(shp[1],camps2 ) as cursor2:
                for row2 in cursor2:
                    if row[1].contains(row2[2]):
                        print(u'{0}, {1}'.format(row2[0], row2[1]))
                        row2[3] = comarca
                        cursor2.updateRow(row2)
        return camps2


#Inspects a project in ArcGis. defines the maps in it, the layers in each map
class Project_analyzing:
    def __init__(self,route= ''):
        self.route = route
        self.aprx = arcpy.mp.ArcGISProject(self.route) 
        
    def FindMaps(self):
        aprx = self.aprx
        maps = aprx.listMaps()
        print('Number of maps:',len(maps))
        #we define two variables that will help us later while indexing our list of objects
        i=0
        #we callback all the maps of the project
        for map in maps:
            i+=1
            map_md = map.metadata
            print('map',i,':',map.name)
            print('Metadata:','title:',map_md.title,'\n','descr:',map_md.description,'\n','credits:',map_md.credits)
        #aprx.save()
    def FindLayers(self,map):
        aprx = self.aprx
        maps = aprx.listMaps()
        for m in maps:
            if m.name == map:
                j=0
                #a call for all the layers that each of the maps have
                layers = m.listLayers()
                print('map---<',m.name,'>---')
                for layer in layers:
                    j+=1
                    if layer.name == 'JPN_Country':
                        print(' -Layer',j,':',layer.name)
                        print('Metadata does not exist')
                    else:
                        layer_md = layer.metadata
                        print(' -Layer',j,':',layer.name)
                        print('Metadata:','title:',layer_md.title,'\n','descr:',layer_md.description,'\n','credits:',layer_md.credits)

def findNodes(tobeprocDir):
    #tobeprocDir.append(startrt)
    files = os.listdir(tobeprocDir[0])
    for file in files:
        fileRoute= "%s%s/" % (tobeprocDir[0],file)
        #print('frot',fileRoute)
        if os.path.isdir(fileRoute):
            tobeprocDir.append(fileRoute)
    procDir.append(tobeprocDir[0])
    tobeprocDir.pop(0)