# GEOPANDAS GUIDES

##### read files 
>> gdf= geopandas.read_file(R'.gpkg',layer='')
>>   layer is only needed in case we open geopackage.


##### calculate new columns in the same geodataframe <br>
>>amb['area']=amb.area <br>
>>amb['centroid']=amb.centroid <br>

##### set active geometry type, from one of the columns. this way we can have a column with areas, another with distance, another with points, and we choose which to plot depending on the case <br>
>>amb.set_geometry('centroid')
>>ax= amb['geometry'/'centroid'/...].plot() #plot according to column values, without following the default

##### Plot functions
amb.plot(column="area",legend=True,cmap='OrRd'scheme='quantiles , zorder=1) <br>
  >> column is the basis from which defines color values
  >> cmap selects the colormap
  >> scheme is the distribution of color based on proportion. (equal, quantles, percentiles)
  >> zorder marks the order in which functions are plotted in the figure.
  >>amb.boundary.plot()
  >>plt.show() #it's necessary while working outside of Jupyter notebook

##### Projections
  >> gdf.crs              : get the current Coordinate reference system of the geodataframe <br>
  >> gdf['geometry'].crs   : same as above, working with pandas geoseries
  >> gdf['geometry'].set_crs(epsg=25831) : set the crs, like ST_SetSRID()
>  > gdf['geometry'].set_crs("EPSG:25831")
>  > newdf = gdf.to_crs('EPSG:4326')
     
##### Intersects. only works with 1 polygon as reference

#### Spatial Joins
>>cross= gdf1.overlay(gdf2,how='intersection') <br>
>>cross.plot(cmap='pink',ax=ax,legend=True) <br>
>>>how= ['intersection', 'union','identity','symmetric_difference','difference'] <br>

##### ADD BASEMAP
>>import contextily as cx
>>cx.add_basemap(ax=ax,crs=cross.crs,source='')
