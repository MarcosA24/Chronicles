#https://pro.arcgis.com/en/pro-app/latest/arcpy/mapping/arcgisproject-class.htm
import arcpy
import os
import pandas as pd

wkspace= R'C:\Users\Documents\espais-interes-geologic-vr0-20230621'
arcpy.env.workspace= wkspace

aprx=None

def ExcelExport(df, excel_route, hoja=''):    
    with pd.ExcelWriter(excel_route) as writer:
        if hoja:
            df.to_excel(writer, sheet_name=hoja)
        else:
            df.to_excel(writer, sheet_name='pred1')

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

def synth_arcdf(shp,fields=''):
    #synthesize a df from a shp table
    if fields=='': fields= GetFields(shp)
    else: pass
    table=[]
    with arcpy.da.SearchCursor(shp,fields) as cursor:
        for row in cursor:
            table.append(row)
    df= pd.DataFrame(table,columns=fields)
    return df

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
    
    #print('{CAPES: [atributs] --------------------',d,'\n-----------------------')

    if True:
        # ----Mateix procés, per al shape d'espais. no cal bucle de shapes
        shape=shapefiles_tots[1]
        camps= lelem
        cols= camps.copy()
        sep= ['FID','sep_TIPUS_INTE', 'sep_DOMINI_MEC', 'sep_TEMPS_GEOL', 'sep_TIPUS_ROCA', 'sep_PROCES_GEO', 'sep_DOMINI', 'sep_UNITAT_REP', 'sep_CONT_GEOL','sep_IMPACT_NAT','sep_IMPACT_NAT','sep_AMENAC_NAT','sep_IMPACT_ANT','sep_AMENAC_ANT']
        #sep= ['FID','sep_TIPUS_INTE', 'sep_DOMINI_MEC', 'sep_TEMPS_GEOL', 'sep_TIPUS_ROCA', 'sep_PROCES_GEO', 'sep_DOMINI', 'sep_UNITAT_REP', 'sep_CONT_GEOL']
        cols= cols+sep
        result= pd.DataFrame(columns=cols)
        for f in camps:
            df= opSesame(R'C:\Users\becari.alex.marcos\Downloads\LlistesValors_EIG.xlsx',sheet=intEspais[f],head=1)
            values= []
            for index, row in df.iterrows(): 
                t= row[0].replace('.',',')
                values.append(t)
            #print(f,'-----------------\n-','Llistat de valors:', values,'\n')
            if f=='AMENAC_ANT': print(values)
            fields= ['FID',f]
    
            with arcpy.da.SearchCursor(shape,fields) as cursor:
                for row in cursor:
                    FID= row[0]+1
                    result.loc[row[0],'FID']= FID      
                  
                    #identificar el separador, i fer un split per el separador
                    if '/' in row[1]:
                        evo= row[1].split('/')
                        evo0= evo[0]
                        evo1= evo[1]
                        if len(evo)==3: evo2= evo[2]
                        else: evo2=None
                        
                        separador= IdSeparador(evo0,evo1)
                    else: 
                        evo0= row[1]
                        separador= None
                    
                    if row[1]!=' ':               
                        if evo0!=row[1]:
                            evo0= evo0.rstrip()
                            if evo2!=None: 
                                evo1= evo1.rstrip()
                                evo1= evo1.removeprefix(' ')
                                evo2= evo2.removeprefix(' ')
                                if not evo0 in values and not evo1 in values and not evo2 in values: result.loc[row[0],fields[1]]=row[1]
                                elif not evo0 in values and evo1 in values and evo2 in values: result.loc[row[0],fields[1]]= evo0
                                elif evo0 in values and not evo1 in values and evo2 in values: result.loc[row[0],fields[1]]= evo1
                                elif evo0 in values and evo1 in values and not evo2 in values: result.loc[row[0],fields[1]]= evo2

                            else: 
                                evo1= evo1.removeprefix(' ')
                                if not evo0 in values and not evo1 in values: result.loc[row[0],fields[1]]=row[1]
                                elif not evo0 in values and evo1 in values: result.loc[row[0],fields[1]]= evo0
                                elif evo0 in values and not evo1 in values: result.loc[row[0],fields[1]]= evo1
                        else:
                            if not row[1] in values: result.loc[row[0],fields[1]]=row[1]
                            #print(u'{0}, {1}'.format(row[0], row[1]))

                    if separador!=None: result.loc[row[0],'sep_'+fields[1]]= separador


        print('Final Dataframe:\n',result)
        ExcelExport(result,R'C:\Users\Documents\persona\llist_sep_es.xlsx',hoja='elements')
    
    
