
# import the needed libraries;
import xarray
import geopandas 
import rioxarray
from shapely.geometry import mapping
import os
import pandas as pd
import numpy as np
import pdb

def clip_era5(catchment_area_file,era5file_pet,era5file_p,catchment_name):
    #open the shapefile with the catchment area

    sf = geopandas.read_file(catchment_area_file)
    #reproject the catchment area shapefile to the MESCAN-SURFEX grid
    sf_reproj = sf.to_crs('+proj=lcc +lat_1=50 +lat_2=50 +lat_0=50 +lon_0=8 +x_0=2937018.5829291 +y_0=2937031.41074803 +a=6371229 +b=6371229')


    #open the era5 evapotranspiration dataset
    xds_pet = rioxarray.open_rasterio(era5file_pet)
        #select the evaporation data from the era5 dataset
    evap_data = xds_pet.pet

    #define the projection of the era5
    evap_data= evap_data.rio.write_crs('+proj=lcc +lat_1=50 +lat_2=50 +lat_0=50 +lon_0=8 +x_0=2937018.5829291 +y_0=2937031.41074803 +a=6371229 +b=6371229')

    #clip the evapitation data on the reprofected shapefile
    clipped = evap_data.rio.clip(sf_reproj.geometry.apply(mapping), sf_reproj.crs)
    
    path=r'C:\Users\mmazzolini\OneDrive - Scientific Network South Tyrol\Documents\conda\clip_era5\monthly_budget\evap/'+ catchment_name[:-4]+'.nc'
    clipped.to_netcdf(path)   
    #group the data by time and compute the mean.
    monthly_total_evap_avg = clipped.groupby('time').mean(...)

    #multiply the average evapitation (mm/day) by the total area (in squared meters), save it into a dataframe
    monthly_total_evap = (monthly_total_evap_avg*0.001*sf_reproj.area[0]).to_dataframe()

    #rename the column with a proper name
    monthly_total_evap=monthly_total_evap.rename(columns={'pet':'total_month_evap_m3'})


    #define the name of the new file where monthly evap is saved, make the path
    path = os.path.join('C:/Users/mmazzolini/OneDrive - Scientific Network South Tyrol/Documents/conda/monthly_data_evap/',catchment_name)

    #save into a csv file.
    # if file does not exist write header 
    if not os.path.isfile(path):
       monthly_total_evap.to_csv(path)
    else: # else print the problem
       print('evap file already exists')
    
                                 
                                 
    #open the era5 precipitation dataset
    xds_p= rioxarray.open_rasterio(era5file_p)
    #select the precipitation data from the era5 dataset
    precip_data = xds_p.tp
    
    #clip the precipitation data on the reprofected shapefile
    clipped_p = precip_data.rio.clip(sf_reproj.geometry.apply(mapping), sf_reproj.crs)
    path_p=r'C:\Users\mmazzolini\OneDrive - Scientific Network South Tyrol\Documents\conda\clip_era5\monthly_budget\precip/'+ catchment_name[:-4] +'.nc'
    clipped_p.to_netcdf(path_p)   

    
    #group the data by time and compute the mean.
    monthly_total_precip_avg = clipped_p.groupby('time').mean(...)

    #multiply the average precipitation by the total area (in squared meters), save it into a dataframe
    monthly_total_precip = (monthly_total_precip_avg*0.001*sf_reproj.area[0]).to_dataframe()

    #rename the column with a proper name
    monthly_total_precip=monthly_total_precip.rename(columns={'tp':'total_month_precip_m3'})


    #define the name of the new file where monthly precip is saved, make the path
    path = os.path.join('C:/Users/mmazzolini/OneDrive - Scientific Network South Tyrol/Documents/conda/monthly_data_precip/',catchment_name)
    
    #save into a csv file.
    # if file does not exist write header 
    if not os.path.isfile(path):
       monthly_total_precip.to_csv(path)
    else: # else print the problem
       print('precip file already exists')



def compute_monthly_discharge(path,filename):
    #read the csv file with the daily discharge
    filepath=path+filename
    df = pd.read_csv(filepath,
                     header=0)
 
    
    #set the date in a proper format
    df.index = pd.to_datetime(df.date, format='%Y-%m-%d')

    #compute the monthly total discharge by summing the average daily discharge (m^3/s) multiplied by the seconds in a day (60*60*24)
    monthly_tot_discharge = (df.discharge_m3_s.groupby(pd.Grouper(freq='M')).sum()*60*60*24).to_frame(name = 'total_discharge_m_3')

    #count the measured days in the month (to check if data are missing)
    n = df.iloc[:,0].groupby(pd.Grouper(freq='M')).count().to_frame(name= 'number')

    #merge the two columns
    df2= pd.concat([monthly_tot_discharge, n], axis=1)
    #save the computed data on a csv file
    path2 = os.path.join('C:/Users/mmazzolini/OneDrive - Scientific Network South Tyrol/Documents/conda/monthly_data_discharge/',filename)
    

    #save into a csv file.
    # if file does not exist write header 
    if not os.path.isfile(path2):
       df2.to_csv(path2)
    else: # else print the problem
       print('discharge file already exists')



           