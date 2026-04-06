import arcpy 
import os 
import sys 

#UNIQUE VALUE RENDERER: https://pro.arcgis.com/en/pro-app/3.1/arcpy/mapping/uniquevaluerenderer-class.htm
# ITEM GROUP: https://pro.arcgis.com/en/pro-app/3.1/arcpy/mapping/item-class.htm
# SYMBOL:   https://pro.arcgis.com/en/pro-app/3.1/arcpy/mapping/symbol-class.htm
arcpy.env.overwriteOutput = True

wkspace= R'C:\Users\becari.alex.marcos\Documents\ArcGIS\Projects\testing\testing.gdb'
project= R'C:\Users\becari.alex.marcos\Documents\ArcGIS\Projects\testing\testing.aprx'
arcpy.env.workspace= wkspace

aprx= arcpy.mp.ArcGISProject(project)
relpath = os.path.dirname(sys.argv[0])


def OpenProject(aprx_route):
    #returns a dictionary with layers grouped by the map they're in.
    glob_layers={}
    nom_layers={}
    aprx= arcpy.mp.ArcGISProject(project)
    maps = aprx.listMaps()
    for map in maps:
        layers= map.listLayers()
        glob_layers[map.name]= layers
        map_layers=[]
        for layer in layers:
            map_layers.append(layer.name)
        nom_layers[map.name]= map_layers
    return glob_layers, nom_layers

def InspectStyleitem(aprx_route,style_route):
    #returns a list with all the style items of that stylx file
    aprx= arcpy.mp.ArcGISProject(project)
    geologia_territorial_250000_styles= []
    for styleClass in ['Point', 'Line', 'Polygon']:
        #print(f'Style Class:{styleClass}')
        customStylePath = style_route
        if styleClass == 'Polygon':
            for styleItem in aprx.listStyleItems(customStylePath, styleClass):
    #           if styleItem.category == 'Capitol Forest':
                #print(f' StyleItem Name: {styleItem.name}')
                geologia_territorial_250000_styles.append(styleItem)
    return geologia_territorial_250000_styles

def getSymbology(aprx_route, layer_obj, stylesList):
    #only prints the info stored in a symbology
    aprx= arcpy.mp.ArcGISProject(aprx_route)
    layers= OpenProject(aprx_route)[0]
    m_layers= layers['Map']
    lyr= m_layers[0]
    sym= lyr.symbology
    print(sym.renderer.type())
    sym.renderer.fields = ['ORDRE']
    print(lyr.name, '--%--------------\nRenderer:',sym.renderer,'\nSymbol Field:',sym.renderer.fields)
    if sym.renderer.type() == 'UniqueValueRenderer':
        print('type: ', sym.renderer.type())
        for group in sym.renderer.groups:
            for item in group.items:
                item.label= item.values[0][0]       # in case there are more than 1 fields, this chooses the first one as label
                print(item.label,item.symbol, item.values, item.symbol.color, item.description)
                print('angle:',item.symbol.angle,'color:',item.symbol.color,'name:',item.symbol.name,'Outline:',item.symbol.outlineColor,item.symbol.outlineWidth,'size:',item.symbol.size)

def changeSymbology(aprx_route, layer_obj, stylesList):
    aprx= arcpy.mp.ArcGISProject(aprx_route)
    layers= OpenProject(aprx_route)[0]
    m_layers= layers['Map']
    lyr= m_layers[0]
    sym= lyr.symbology
    sym.updateRenderer('UniqueValueRenderer')
    sym.renderer.fields = ['ORDRE']

    for group in sym.renderer.groups:
        for item in group.items:
            transVal = item.values[0][0]
            Gallery= item.symbol.listSymbolsFromGallery(item.label) #checks if there's a symbol with the key: item.label in the gallery styles
            item.symbol.color = {'RGB' : [255, 0, int(transVal), int(transVal)]}    #defines a new color for the symbol
            item.symbol.applySymbolFromGallery(item.label) # applies the symbol from the gallery to the category item
            print('symbol:', item.symbol.color)
            print('updatedSymbol',item.label)

    #save the changes
    lyr.symbology= sym
    aprx.save()

#---directamente en el arcgis notebook
if True:
    #---directamente en el arcgis notebook
    #Usando CURRENT PROJECT Y ACTUALIZANDO CAPA AL MOMENTO
    aprx= arcpy.mp.ArcGISProject("CURRENT")
    m = aprx.listMaps('Map')[0]
    lyr = m.listLayers('_05_unitats_geologiques')[0]

    sym= lyr.symbology
    sym.updateRenderer('UniqueValueRenderer')
    sym.renderer.fields = ['ORDRE','CODI_CAS']
    print(lyr.name, '--%--------------\nRenderer:',sym.renderer,'\nSymbol Field:',sym.renderer.fields)

    exceptions= {}
    for group in sym.renderer.groups:
        for item in group.items:
            item.label = item.values[0][1]
            Gallery= item.symbol.listSymbolsFromGallery(item.label)
            print(item.label, len(Gallery))

            if len(Gallery)==1: 
                item.symbol.applySymbolFromGallery(item.label)
            else: 
                exceptions[item.label] = len(Gallery)
                ind=-1
                for s in Gallery:
                    ind+=1
                    if s.name == item.label:
                        print(s.name,'index:', ind)
                        item.symbol.applySymbolFromGallery(item.label,ind)
                        print('updatedSymbol',item.label)
                continue
                
            #print('symbol:', item.symbol.color)
            print('updatedSymbol',item.label)
            
    print(exceptions)
    print(len(exceptions))
    #save the changes
    lyr.symbology= sym
    aprx.save()
        

if __name__=='__main__':
    #get the layers of the project, sorted by the map they're in.
    layers_name= OpenProject(project)[1]
    layers= OpenProject(project)[0]
    m_layers= layers['Map']

    #we have all the styles that we will have to apply later on in the new layer
    styles= InspectStyleitem(project,R'C:\Users\becari.alex.marcos\OneDrive - Institut Cartogràfic i Geològic de Catalunya\geologia-territorial-250000\geologia-territorial-250000-geologic.stylx' )
    for st in styles: 
        print(st.name)




