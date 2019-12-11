import geopandas as gpd
import pandas as pd
from geo_functions import deg2num

def downloader(image_url, i, name):
    '''
    Downloads and names png images
    '''
    file_name = "name"+ str(i) + '.png'
    urllib.request.urlretrieve(image_url,file_name)

def tiles_lister(coordinate1, coordinate2):
    '''Creates geodataframe with list of tiles and corresponding center in degrees-coordinates.
    Useful to split a geographic area in squares.
    Coordinate1 and Coordinate2 correspond to top left and bottom right rectangle for selected area
    respectively.
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