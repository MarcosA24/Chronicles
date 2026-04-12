## FME GUIDE FOR FUNCTIONS AND USE

>>Basic FME workflows: 
  - reader : read any source
  - writer : export FME data into any source
  - transformer: apply calculations and transformations, managing and defining data

>> Reaers, writers

--Autocad, DGN, ESRI ArcGis, IBM, Mojang Minecraft(PointCloud), MongoDB, OGC, PointCloud, PostGis, PNG, PostgreSQL, RADAR, Landsat, 
SAR, Sentinel, SQLite, TIFF, 



>> Functions Inventory  (transformer functions)

#### Tables and data management
- AttributeCreator:
- AttributeCopier: 
- AttributeExploder: similar to transpose in excel, it explodes a row attributes into a list
- AttributeFileReader: reads a csv and adds the info into an attribute
- AttributeFileWriter: writes the info of a feature into a csv
- AttributeKeeper: from the source, it keeps only the attributes that you define
- AttributeManager: an all-around feature to edit table frames, attributes and features
- AttributeSplitter: Splits attribute values into parts, based on a delimiter or fixed-width pattern, and creates a list attribute containing one list element for each part.
- AttributeRounder: rounds numerical field

- Counter:
- FileNamePartExtractor: works with filename path
- FeatureJoiner: join columns by common field

- JSONExctractor: extracts parts of a JSON file into attributes
- JSONUpdater: modifies a JSON

- ListHistogrammer: plots a histogram from data on a list

- OneDriveConnector:
- PDFPageFormatter:
- PDFStyler: to style the export to pdf

- RandomNumberGenerator: 
- Sorter: order by
- StatisticsCalculator: calculates statistics of an attribute or a set of attributes. And Adds the results as attributes into a new column (max,min, count, sum, mean, median, range...)
- StringReplacer: str.replace()
- SummaryReporter: writes a summary of the input features and attributes
- Tester: IF condition
- TestFilter: multiple IF, ELIF conditions to filter values from a source

- SVGreader
- 

#### Geometry functions
- AreaOnAreaOverlayer: extracts a feature with the overlapped area of polygons as a result. it can inherit attributes from both overlapping features
- AreaCalculator : gets area of polygons
- AreaBuilder: builds polýgons by using enclosed lines
- Bufferer: buffer zone
- ContourGenerator: constructs a Delaunay triangulation from points
- ConvexityFilter: returns convex or concave from an input geometry
- Coordinate.->
- Curvefitter: line smoothing
- DEMGenerator: constructs a Delaunay triangulation and turns it into a DEM from source points
- Densifier: from source point cloud, it densifies the number of points by interpolating close coordinates
- DensityCalculator: index to evaluate density
- DGNstyles: exports DGN
- Dissolver:
- Feature.-> Merger/Reader/Joiner/Holder/Writer/TypeFilter

- LengthCalculator: calculates length of a feature, and adds it as an attribute
- LineBuilder: connects input points with a line, in the order they are in the tableframe
- LineCloser: encloses the lines by marking start=end point and creates an area

- MeasureExtractor: depending on the type of geometry, it returns its corresponding measure values
- NeighborFinder:
- NeighborhoodAggregator:
- NetworkCostCalculator: computes and assigns the cost of the shortest path as an M-Value
- NetworkFlowOrientor: Fixes the flow of each edge or linear feature in the network tofith the direction to the destination node. Used to later on calculate the cost

- OffsetCurveGenerator: builds an offset line of a curve object

- PointOnAreaOverlayer: spatial join Point-Polygon to inherit attributes
- PointOnLineOverlayer
- PointOnPointOverlayer
- PointOnRasterValueExtractor: extracts the info of the raster that corresponds to the Point coordinate.
  
- Scaler: scales x,y values
- SpatialFilter: filters values using spatial relations
- SpatialRelator: specifies the spatial relations of two inputs

- TINGenerator:
- VertexCounter
- VertexCreator:
- VolumeCalculator:
- VoronoiCellGenerator: outputs circles of area of influence for each geometry
- VoronoiDiagrammer: generates a voronoi diagram, Thiessen polygons
- 
### FME SERVER
- FMEFunctionCaller
- FMEServerJobSubmitter:
- FMEServerJobWaiter:
- FMEServerNotifier: 
- FMEServerLogFileRetriever:

- HTTPCaller
- HTTPUploader
- HTTPSHeader

#### PointCloud 

### PROJ
- PROJAttributeReprojector: reprojects coordinates stored as attributes to the defined coord.system Using the PROJ library
- Reprojector: reprojects X,Y, from a coord.system to another
  
### PYTHON
- PythonCaller: executes a python script (user provided by FME)
  >>> EXAMPLE
       import fme
       import fmeobjects
      
      class FeatureProcessor(object):
          def __init__(self):
              self.sondejos = []
              self.fulls= []
              self.count= 0
              
          def input(self, feature):
              s= feature.clone()
              self.sondejos.append(feature)
              self.count += 1
              full = feature.getAttribute('id_full')
              
              s.setAttribute('full', full)
              s.setAttribute('count',self.count)
              self.pyoutput(s)
              
          def close(self):
              pass 
                  
          def process_group(self):
              pass
  Python caller uses a class structure to process FME objects.
  Tips to take into account while using python caller:
    . Make sure the pytoutput(feature) is different from the input one, if not it will show the initial one without the changes.
    . specify any new variables in the init function, and the FME input layer is referenced in the input() function
    . Only 1 input can be processed at a time. We can't compare two layer sources from 2 sources. For it to work they must be merged beforehand.
    . To reference table attributs from FME objects, use the helper. It follows a structure like feature.getAttrubute(), feature.setAttribute()

- PythonCreator: creates features using python script

#### RASTER
- RasterAspectCalculator: process to get direction of slope
- RasterBand.> /Adder/Combiner
- RasterCellValueCalculator
- RasterCheckpointer: Forces accumulated raster operations to be processed, saving the state to disk and releasing resources to tune performance or assist with memory limitations.
- RasterDEMGenerator:
- RasterGeoreferencer:
- RasterHillshade: generates agrayscaled shaded relief of the raster, based on elevation values of the DEM
- RasterMosaicker: merge multiple rasters into a mosaic
- RasterSlopeCalculator:
- RasterStatisticsCalculator:

### SQL
- SQLCreator:
- SQLExecutor:
  


