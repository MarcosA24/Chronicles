lyname= 'cami_sant_jaume'
outfile= R'C:\Users\becari.alex.marcos\Documents\Alex\undik\buffLayer.shp'
dist= 0.01
#QgsProcessing.TEMPORARY_OUTPUT
ly= QgsProject.instance().mapLayersByName(lyname)[0]
fields= ly.fields()
feat= ly.getFeatures()

print(ly.name)
writer= QgsVectorFileWriter(outfile,'UTF-8',fields, QgsWkbTypes.Polygon, ly.sourceCrs(),'ESRI Shapefile')

for f in feat:
    geom= f.geometry()
    buffer= geom.buffer(dist,5)
    f.setGeometry(buffer)
    writer.addFeature(f)
iface.addVectorLayer(outfile,'','ogr')
del(writer)
