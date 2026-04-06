#https://opensourceoptions.com/pyqgis-calculate-geometry-and-field-values-with-the-qgis-python-api/

lyname= 'ABS'
layer= QgsProject.instance().mapLayersByName(lyname)[0]


    #adding new fields


def addField(fields={}):
    #{name:type, name:type}
    pv = layer.dataProvider()
    for f in fields:
        pv.addAttributes([QgsField(f,QVariant.Double),QgsField('percentage',QVariant.Double)])
        layer.updateFields()
    
def calculateFields(addons=False):
    #addons tell if other fields are used or not
    if addons==False:
        ex1= QgsExpression('$area')
        ex2= QgsExpression('"area"/10000')
        context = QgsExpressionContext()
        context.appendScopes(QgsExpressionContextUtils.globalProjectLayerScopes(layer))

        with edit(layer):
            for f in layer.getFeatures():
                context.setFeature(f)
                f['area'] = ex2.evaluate(context)
                layer.updateFeature(f)
        
        
addField(fields={'new':'string','song':'int','names':'string'})        
#calculateFields()
