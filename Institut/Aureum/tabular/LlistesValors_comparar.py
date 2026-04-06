#https://pro.arcgis.com/en/pro-app/latest/arcpy/mapping/arcgisproject-class.htm
import arcpy
import os
import pandas as pd

wkspace= R'C:\Users\becari.alex.marcos\Downloads\espais-interes-geologic-v2r0-20230621'
arcpy.env.workspace= wkspace

aprx=None

def opSesame(route,separator='',sheet='',head=''):
    if route.endswith('.txt') or route.endswith('.ASC') or route.endswith('.csv'):
        estadillo= pd.read_csv(route,sep=separator,header=[0],index_col=None)
        estadillo= estadillo.replace(',','.', regex=True)
        return estadillo
    elif route.endswith('.xlsx'):
        if not sheet:
            sheet= input('Sheet_Name: ')
        if not head:
            head= int(input('Nºlines of headers(int)'))
        headers=[]
        for r in range(head):
            headers.append(r)
        estadillo= pd.read_excel(route,sheet_name=sheet,header=headers,names=None)
        estadillo= estadillo.replace(',','.', regex=True)
        return estadillo
    else:
        print('File type does not exist')

def OpenProject(aprx_route):
    #returns a dictionary with layers grouped by the map they're in.
    glob_layers={}
    nom_layers={}
    maps = aprx.listMaps()
    for map in maps:
        layers= map.listLayers()
        glob_layers[map.name]= layers
        map_layers=[]
        for layer in layers:
            map_layers.append(layer.name)
        nom_layers[map.name]= map_layers
    return glob_layers, nom_layers

def selShapes(inputNames=False):
    shapeslist=[]
    if inputNames!=False:
        print(arcpy.ListFeatureClasses())
        while True:
            shfile= input('Specify shapefile name:base (press intro once you"re finished: ')
            if shfile:
                shapefile = shfile+".shp"
                shapeslist.append(shapefile)
            else:
                break
    else:
        for shp in arcpy.ListFeatureClasses():
            shapeslist.append(shp)
    return shapeslist

def GetFields(fc):
    featureFields = arcpy.ListFields(fc)
    fcFields = []
    for field in featureFields:
        fcFields.append(field.name)
        #if instead of field.name you append field, all the object will be appended.
        #print(f"{field.name} has a type of {field.type} with a length of {field.length}")
    return fcFields

def IdSeparador(evo0,evo1):    
    if evo0.endswith(' ') and evo1.startswith(' '): return 1
    elif evo0.endswith(' ') and not evo1.startswith(' '): return 2
    elif not evo0.endswith(' ') and not evo1.startswith(' '): return 3
    elif not evo0.endswith(' ') and evo1.startswith(' '): return 4

if __name__=='__main__':
    shapefiles_tots= selShapes()
    d= {}
    for shp in shapefiles_tots: d[shp]= GetFields(shp)
    
    lespais= ['TIPUS_INTE', 'DOMINI_MEC', 'TEMPS_GEOL', 'TIPUS_ROCA', 'PROCES_GEO', 'DOMINI', 'UNITAT_REP', 'CONT_GEOL','IMPACT_NAT','AMENAC_NAT','IMPACT_ANT','AMENAC_ANT']
    lelem= ['TIPUS_INTE', 'DOMINI_MEC', 'TEMPS_GEOL', 'TIPUS_ROCA', 'PROCES_GEO', 'DOMINI', 'UNITAT_REP', 'CONT_GEOL']

    intEspais= {'TIPUS_INTE':'VTipusInt', 'DOMINI_MEC':'VDominiMEC', 'TEMPS_GEOL':'VTempsGeol', 'TIPUS_ROCA':'VTipusRoca', 'PROCES_GEO':'VProcesGeol', 'DOMINI':'VDomini', 'UNITAT_REP':'VUnitatRepr', 'CONT_GEOL':'VContGeol',
               'IMPACT_NAT':'VImpNat','AMENAC_NAT':'VAmenNat','IMPACT_ANT':'VImpAmAnt','AMENAC_ANT':'VImpAmAnt'}
    
    print('{CAPES: [atributs] --------------------',d,'\n-----------------------')

    if False:        
        # ----Procés per als dos shapefiles d'elements
        shapefiles=shapefiles_tots[:2]
        for f in lelem:
            df= opSesame(R'C:\Documents\LlistesValors_EIG.xlsx',sheet=intEspais[f],head=1)
            values= []
            for index, row in df.iterrows(): values.append(row[0])
            print(f,'-----------------\n-','Llistat de valors:', values,'\n')

            #fields = ['FID','TIPUS_ROCA']
            fields= ['FID',f]
            for shape in shapefiles:
                print('>>>',shape,'     <<<<')
                outlayers= []
                dispars=[]
                with arcpy.da.SearchCursor(shape,fields) as cursor:
                    for row in cursor:
                        if row[1]!=' ':
                            if not row[1] in values:
                                #print(u'{0}, {1}'.format(row[0], row[1]))
                                outlayers.append(row[0])
                                if row[1] not in dispars:
                                    dispars.append(row[1]) 
                print(outlayers,'\n-',dispars,'\n-Conteig Files afectades:',len(outlayers),'\n-Valors no registrats:',len(dispars),'\n\n')
    
    if True:
        # ----Mateix procés, per al shape d'espais. no cal bucle de shapes
        shape=shapefiles_tots[2]
        for f in lespais:
            df= opSesame(R'C:\Users\Documents\LlistesValors_EIG.xlsx',sheet=intEspais[f],head=1)
            values= []
            for index, row in df.iterrows(): values.append(row[0])
            #print(f,'-----------------\n-','Llistat de valors:', values,'\n')

            #fields = ['FID','TIPUS_ROCA']
            fields= ['FID',f]
        
            #print('>>>',shape,'     <<<<')
            #print(fields)
            outlayers= []
            dispars=[]
            separador={}
            print('sep'+fields[1])
            with arcpy.da.SearchCursor(shape,fields) as cursor:
                for row in cursor:
                    if row[1]!=' ':
                        if '/' in row[1]:
                            evo0= row[1].split('/')[0]
                            evo1= row[1].split('/')[1]
                        else: evo0= row[1]

                        if not evo0 in values:
                            #print(u'{0}, {1}'.format(row[0], row[1]))
                            outlayers.append(row[0])
                            if row[1] not in dispars:
                                dispars.append(row[1])
                            
                        elif not evo1 in values:
                            outlayers.append(row[0])
                            if row[1] not in dispars:
                                dispars.append(row[1])

            #print(outlayers,'\n-',dispars,'\n-Conteig Files afectades:',len(outlayers),'\n-Valors no registrats:',len(dispars),'\n\n')

