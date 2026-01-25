import sys,os
#to import pyforestscan, first there must be installed gdal and pdal. to do so it was done via a 
import pyforestscan
import numpy as np
from pyforestscan.handlers import read_lidar, write_las, create_geotiff
from pyforestscan.filters import filter_hag, remove_outliers_and_clean, classify_ground_points,filter_select_ground
from pyforestscan.calculate import generate_dtm, calculate_chm, assign_voxels, calculate_pad, calculate_fhd, calculate_pai
from pyforestscan.visualize import plot_metric, plot_pad, plot_2d

#Functions for the program to compute
clean=True  #filter noise and SOR
DTM=False    #digital terrain model of the zone
ForestMetrics={#calculate forest Metrics
        'chm':True, #Canopy Height Model
        'pad':True, #Plant Area Density
        'fhd':True, #Foliage Height Diversity
        'pai':True # Plant Area Index
        } 

#export Options. activate when needed with ==True
visualize_plot=True
export_map=False
export_laz=False

def noiseFilter(PointCloud,clean_bool,mean_k=6,multiplier=1.4):
    if clean==True: return remove_outliers_and_clean(PointCloud, mean_k=mean_k, multiplier=multiplier)
    else: return PointCloud

def exportData(map,route,lidar=False,crs='EPSG:32631'):
    if export_map==True: 
        create_geotiff(map,str(route)+'.tif',crs=crs,spatial_extent=extent)
        print(str(route)+' map exported')
    if export_laz==True: 
        write_las(lidar, str(route)+".laz", srs=crs, compress=True)
        print(str(route)+' lidar exported')
    
    
if __name__=='__main__':
    #import datasets
    #[0]:original .las cloud, [1]:vegetation filtered .las, [2]:ground classification -las
    lidar_paths=[R'E:\Universidad Alex\TFG\Campo\instop_cloud0-las_2025-03-04_0909\cloud0.las',
              R'E:\Universidad Alex\TFG\process\aéreo\cloud0.terreno.las',R'E:\ArcGIS\JorbaForest\lidar-territorial-v3r0-full1km329648-2021-2023.laz']
    photo_paths=[R'E:\Universidad Alex\TFG\process\fotog\forest_MMA.las']
    tls_paths= [R'E:\Universidad Alex\TFG\process\blk\blk_py.las',
                R'E:\Universidad Alex\TFG\process\blk\blk_groundpy.las']
    
    lidar_airborn=read_lidar(lidar_paths[2],'EPSG:25831',hag=True)[0]  #airborn_lidar origin
    #lidar_airborn=read_lidar(photo_paths[0],'EPSG:32631',hag=True)[0] #photogrammetry origin
    
    if visualize_plot is True: plot_2d(lidar_airborn)
    #lidar_clean= noiseFilter(lidar_aerial,clean)
            
    #for computing ForestMetrics, the original pointcloud must be used, not the vegetation classified one.    
    if any(b == True for b in ForestMetrics.values()):
        voxel_res=(1,1,1)
        lidar_voxel, extent= assign_voxels(lidar_airborn,voxel_res)
        if ForestMetrics['chm'] is True: #Canopy Height Model
            chm, extent= calculate_chm(lidar_airborn,voxel_res)
            if visualize_plot is True: plot_metric('Canopy height model',chm,extent,metric_name='Height (m)',cmap='viridis', fig_size=None)
            exportData(chm,'chm',lidar=False,crs='EPSG:32631')
            
        if ForestMetrics['pad'] is True:
            pad = calculate_pad(lidar_voxel, voxel_res[-1])
            if visualize_plot==True: plot_pad(pad, 5, axis='y', cmap='viridis')
            #exportData(pad,'pad',lidar=False,crs='EPSG:32631')
        
        if ForestMetrics['fhd'] is True:
            fhd= calculate_fhd(lidar_voxel)
            if visualize_plot is True: plot_metric('Foliage Height Diversity', fhd, extent, metric_name='FHD', cmap='viridis', fig_size=None)
            exportData(fhd,'fhd',lidar=False,crs='EPSG:32631')
            
        if ForestMetrics['pai'] is True:
            pad= calculate_pad(lidar_voxel,voxel_res[-1])
            pai= calculate_pai(pad)
            if visualize_plot is True: plot_metric('Plant Area Index', pai, extent, metric_name='PAI', cmap='viridis', fig_size=None)
            exportData(pai,'pai',lidar=False,crs='EPSG:32631')
        
    if DTM==True:
        print('-DTM processing. --Ongoing')
        #classified_pcd = classify_ground_points(aerial_cloud)
        #ground_points= filter_select_ground(classified_pcd)
        ground_points=read_lidar(lidar_paths[1],'EPSG:32631')[0]
        dtm, extent= generate_dtm(ground_points=ground_points) #modification of points X,Y,Z arrays in original code. generate_DTM function
        if visualize_plot is True: plot_metric('Digital Terrain Model',dtm,extent,metric_name='Elevation (m)',cmap='viridis', fig_size=None)
        exportData(dtm,'dtm',lidar=False,crs='EPSG:32631')
    
