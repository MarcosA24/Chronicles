#https://docs.qgis.org/3.34/en/docs/pyqgis_developer_cookbook/vector.html#retrieving-information-about-attributes
#https://gis.stackexchange.com/questions/54057/reading-attribute-values-using-pyqgis
import pandas as pd

def ExcelExport(df, excel_route, hoja=''):
    with pd.ExcelWriter(excel_route) as writer:
        if hoja:
            df.to_excel(writer, sheet_name=hoja)
        else:
            df.to_excel(writer, sheet_name='pred1')

def getFields(source,lyname=''):
    def getSc(source,lyname=''):
        #lyname must be a list, even if it's only 1 layer
        if source=='layer_name': #by calling the name, then marking with instance
            if len(lyname)==1: ly= QgsProject.instance().mapLayersByName(lyname[0])[0]
            elif len(lyname)>1: 
                ly=[]
                for l in lyname: 
                    layer= QgsProject.instance().mapLayersByName(l)[0]
                    print(layer.name)
                    ly.append(layer)
            return ly
        elif source =='activeLayer': #or by choosing the current active layer
            ly= iface.activeLayer()
            return ly
        elif source=='externalFile': #by choosing an external file, not necessarily uploaded in the QGIS map
            ly = QgsVectorLayer(".shp", "airports", "ogr")
            return ly
    layers= getSc(source,lyname)
    df= pd.DataFrame({'layer':[],'field':[],'type':[],'values':[]})
    
    if type(layers)==list:
        if True: #to get the attribute fields names
            for l in layers:
                for field in l.fields(): 
                    #print(field.name(), field.typeName())
                    nrow={'layer':l.name(),'field':field.name(),'type':field.typeName()}
                    df.loc[len(df)] = nrow
                    df = df.reset_index(drop=True)
        if False: #to get all the geometries(features), and work with them
            for l in layers: 
                for feat in l.getFeatures(): print(feat)                
    elif type(layers)!=list:
        l=layers
        if True: #to get the attribute fields names
            for field in l.fields(): 
                #print(field.name(), field.typeName())
                nrow={'layer':l.name(),'field':field.name(),'type':field.typeName()}
                df.loc[len(df)] = nrow
                df = df.reset_index(drop=True)
        if False: #to get all the geometries(features), and work with them
            for feat in l.getFeatures(): print(feat)     
    return df
lyname= ['espais-interes-geologic-v2r0-espais-20230621','espais-interes-geologic-v2r0-elements-punts-20230621','espais-interes-geologic-v2r0-elements-poligons-20230621']
#lyname= ['espais-interes-geologic-v2r0-espais-20230621']
DF= getFields(source='layer_name',lyname=lyname)
print(DF)
#DF.to_csv(R'C:\Users\becari.alex.marcos\Documents\Alex\undik\practices\dataframe.csv')


#export the file to excel, do it in external IDE because pyQGIS doesn't detect Openpyxl
#so, open the csv with OpSesame from the Omni file and then change it into excel
#import pandas as pd
#import sys
#sys.path.insert(1,R'C:\Users\becari.alex.marcos\Documents\Alex\py_carto')
#import Omni

#file= Omni.opSesame(R'C:\Users\becari.alex.marcos\Documents\Alex\undik\practices\dataframe.csv',separator=',',sheet='fields',head=1)
#print(file)
#ExcelExport(file,R'C:\Users\becari.alex.marcos\Documents\Alex\undik\practices\dades.xlsx')


    