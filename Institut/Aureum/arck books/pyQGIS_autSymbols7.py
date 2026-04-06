#sources:   https://qgis.org/pyqgis/3.0/core/Symbol/QgsSymbol.html
#           https://subscription.packtpub.com/book/programming/9781783984664/7/ch07lvl1sec50/using-the-layer-editing-mode
#           https://www.reddit.com/r/QGIS/comments/17sqsx1/need_help_with_qgis_python_script_for_updating/
#           https://gis.stackexchange.com/questions/454312/save-a-layers-renderer-to-undo-the-changes-in-style
from qgis.core import QgsProject, QgsVectorLayer, QgsFeature, QgsGeometry, QgsLayerTreeLayer

#set the layer where we will work
layer = QgsProject.instance().mapLayersByName("_12_unitats_geologiques_basament_25000")[0]
iface.setActiveLayer(layer) 

feat = QgsFeature()
geom = QgsGeometry()
print('Layer: ----', layer.name())

#this part works with LayerTrees, it's another way to extract the layers of a project rather than directly
root= QgsProject.instance().layerTreeRoot()
print('LayerTree: ----', root.children())
print('Layer: ----', layer.name())

#get properties of all the symbol categories
if False:
    categorized_renderer = QgsCategorizedSymbolRenderer()
    # Add a few categories
    cat1 = QgsRendererCategory('1', QgsMarkerSymbol(), 'category 1')
    cat2 = QgsRendererCategory('2', QgsMarkerSymbol(), 'category 2')
    categorized_renderer.addCategory(cat1)
    categorized_renderer.addCategory(cat2)

#this part extracts the simbology and shows which type it is, and the properties of it
renderer = layer.renderer()
print("Type:--", renderer.type())
#the table column by which the symbols are categorized
print("Symbol_Attribute:--", layer.renderer().legendClassificationAttribute())
#print(layer.renderer().dump())
#Here we begin to work with the symbology, and it's a categorized Symbol, where each code has its own symbol
#Qgs style manager
print("Style -- ",QgsMapLayerStyleManager(layer).currentStyle())
#Here we begin to work with the symbology, and it's a categorized Symbol, where each code has its own symbol


indexs_lines= []
if renderer.type()=="categorizedSymbol":
    if True:
        if n<100:
            n= -1
            for cat in layer.renderer().categories():
                csymbol= cat.symbol().clone()    #cloning symbol
                index= renderer.categoryIndexForValue(cat.value())
                n+=1
                if n<10:
                    #print("index:",n, cat.value())
                    #check if there are more than 1 symbols in a category
                    if csymbol.symbolLayerCount()>1:
                        #print("index:",index,"\n C2(before delete)",csymbol.symbolLayerCount())
                        if False:
                            #option1: filter using QgisObjects and do depending on the type, without referring to the num of layers.
                            for sl in csymbol.symbolLayers():
                            #print(i, 'type:', symbol.symbolLayer(i).type())                        
                                if isinstance(sl, QgsSimpleLineSymbolLayer):
                                    indexs_lines.append((index,cat.value()))
                                    #print("{}: {} :: {}".format(cat.value(), cat.label(), csymbol.symbolLayer(2)))
                                    csymbol.deleteSymbolLayer(2)
                                    cat.setSymbol(csymbol)
                        
                        if True:
                                #option2: loop through range(symbolLayerscount) and work with i == integer
                            for i in range( csymbol.symbolLayerCount()):
                                #checks all the symbol layers in the category
                                print(i, 'type:', csymbol.symbolLayer(i).type())
                                if csymbol.symbolLayer(i).type()==2:
                                    csymbol.symbolLayer(i).setLocked(i)
                                    print("{}: {} :: {}".format(cat.value(), cat.label(), csymbol.symbolLayer(i)))
                                elif csymbol.symbolLayer(i).type()==1:
                                    indexs_lines.append((index,cat.value()))
                                    print("{}: {} :: {}".format(cat.value(), cat.label(), csymbol.symbolLayer(i)))
                                    csymbol.deleteSymbolLayer(i)
                                    #cat.symbol().symbolLayer(0).setStrokStyle(Qt.Penstyle.NoPen)
                                    #cat.symbol().setStrokeStyle(Qt.Penstyle.NoPen)
                                    #print("index:",index,"\n C3(after delete)",csymbol.symbolLayerCount())
                                    #defining new symbol for the category
                                    cat.setSymbol(csymbol)
                                
        
        #Updating all the symbols together
        renderer.updateSymbols(cat.symbol())

        print('length',len(indexs_lines), indexs_lines)
        # Save changes to the renderer and update the layer
        layer.setRenderer(renderer)
        layer.triggerRepaint()
        iface.layerTreeView().refreshLayerSymbology(layer.id())
        print("Layer updated")
                            
            


