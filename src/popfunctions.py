import geopandas as gpd
import pandas as pd
from geofunctions import deg2num, num2deg
import requests
import os 
from dotenv import load_dotenv
import urllib.request


def downloader(image_url, name):
    '''
    Downloads and names png images
    '''
    file_name = str(name) + '.png'
    urllib.request.urlretrieve(image_url,file_name)

def tiles_lister(coordinate1, coordinate2):
    '''Creates geodataframe with list of tiles and corresponding center in degrees-coordinates.
    Useful to split a geographic area in squares.
    Coordinate1 and Coordinate2 correspond to top left and bottom right rectangle for selected area
    respectively, task for which www.geojson.io might be the best place.
    Input of each coordinate must be in (longitude, latitude) tuple format.
    '''
    chosen_tiles = deg2num(*coordinate1), deg2num(*coordinate2)
    tiles = []
    longitudes = []
    latitudes = []
    for i in range(chosen_tiles[0][1], chosen_tiles[1][1]):
        for j in range(chosen_tiles[0][0], chosen_tiles[1][0]):
            tiles.append([j, i])
            coords = num2deg(j+0.5, i+0.5)
            longitudes.append(coords[0])
            latitudes.append(coords[1])
    df = pd.DataFrame(data={'tiles': tiles, 'Longitude': longitudes, 'Latitude': latitudes})
    gdf = gpd.GeoDataFrame(
        df, geometry=gpd.points_from_xy(df.Longitude, df.Latitude))
    return gdf

def download_tiles(gdf, path, name="image-", column="geometry"):
    '''
    Downloads and saves 256x256 png images from Google Static Maps API
    for each Point coordinate in a provided geodataframe
    '''
    load_dotenv()
    key = 'GOOGLETOKEN'
    value = os.getenv(key)
    fullfilename = os.path.join(path, name)
    for index, row in gdf.iterrows():
        y_coord= row[column].y
        x_coord = row[column].x
        url = f"https://maps.googleapis.com/maps/api/staticmap?center={y_coord},{x_coord}&zoom=20&size=256x256&maptype=satellite&key={value}"
        downloader(url, fullfilename+"-"+str(index)+"-"+str(x_coord)+"-"+str(y_coord))