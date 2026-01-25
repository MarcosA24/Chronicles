import sys,os
import json, numpy as np
sys.path.insert(0, R"E:\Py_glob_local\forestAria\forestAria\forest_3d_app\src")
from forest3D import lidar_IO,ground_removal,treeDetector,detection_tools,processLidar,inventory_tools,utilities
sys.path.insert(0, R"E:\Py_glob_local\forestAria\forestAria\Lib")

directory= R"E:\Universidad Alex\TFG\process\aéreo"
LidarPath= R"E:\Universidad Alex\TFG\Campo\instop_cloud0-las_2025-03-04_0909\cloud0.las"
photoRGB = None
#LidarPath= directory+"\cloud0_vegetacion.las"
#f= lasfile.File(LidarPath)
#fields= f.header
if photoRGB!= None:
    #RGB pointcloud
    xyz_data = lidar_IO.readFromLas(LidarPath, fields = ['x','y','z','red','green','blue'],convert_colours=True)
    xyz_data[:, 3:] /= 255.0 #normalize rgb
    xyz_data_gr = ground_removal.removeGround(xyz_data,offset=[0,0,0],thresh=2.0,proc_path='path/to/output_directory') #ground removal raw geometrical data
    ground_pts = ground_removal.load_ground_surface(directory+'/_ground_surface.ply') #get ground data
    
if LidarPath!= None:
    xyz_data= lidar_IO.readFromLas(LidarPath, fields = ['x','y','z','Intensity'])
    xyz_data[:, 3] /= 50000.0 #normalize intensity

    #xyz_data_gr,colour_gr = ground_removal.removeGround(xyz_data,returns=xyz_data[:,3:],offset=[0,0,0],thresh=2.0,proc_path=directory) #by number of returns
    xyz_data_gr = ground_removal.removeGround(xyz_data,offset=[0,0,0],thresh=2.0,proc_path='path/to/output_directory') #raw geometrical data
    ground_pts = ground_removal.load_ground_surface(directory+'/_ground_surface.ply') #get ground data

if False:
    #tree detector
    #json object with tree model reference
    detector_addr = 'path/to/detector/folder'
    with open(os.path.join(detector_addr, 'raster_config.json')) as json_file:
        config_dict = json.load(json_file)
    rasterTreeDetector = treeDetector.RasterDetector(**config_dict )

    labels = rasterTreeDetector.sliding_window(detector_addr,xyz_data_gr,ground_pts=ground_pts,windowSize = [100,100],stepSize = 80) 

if False: lidar_IO.writePly_labelled(os.path.join(directory,'detection.ply'),xyz_data_gr,labels,offset=[0,0,0,0]) #visualization export
if False: lidar_IO.writeLAS(os.path.join(output_dir,'detection.las'),xyz_data_gr,labels,offset=[0,0,0]) #treeId field export in a las file

#   ------- Inventory tools
if False:
    tree_tops = inventory_tools.get_tree_tops(xyz_data_gr,labels)
    heights = inventory_tools.get_tree_heights(tree_tops[:,:3],ground_pts)
    inventory = np.hstack((tree_tops,heights[:,np.newaxis]))
    utilities.write_csv(os.path.join(directory,'inventory.csv'),inventory,header='x,y,z,id,height')