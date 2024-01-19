import geopandas as gpd
import pandas as pd
from src.data_process import transform_crs, preprocess
from src.point_cloud import gen_point_cloud


def read_mask(mask_path, target_crs="EPSG:3006"):
    """
    Reads the mask GeoDataFrame from a file and ensures it has the correct CRS.

    Parameters:
    - mask_path (str): The file path to the mask GeoDataFrame.
    - target_crs (str): The target CRS for the mask. Defaults to "EPSG:3006".

    Returns:
    - gpd.GeoDataFrame: The mask GeoDataFrame with the correct CRS.
    """
    mask = gpd.read_file(mask_path, crs=target_crs)
    if mask.crs != target_crs:
        mask = transform_crs(mask, target_crs=target_crs)
    return mask


def generate_test_point_cloud(mask, settings):
    """
    Generates a test point cloud based on the provided mask and settings.

    Parameters:
    - mask (gpd.GeoDataFrame): The mask GeoDataFrame.
    - settings (dict): Settings for generating the test point cloud.

    Returns:
    - pd.DataFrame: The generated test point cloud.
    """
    gen_point_cloud(mask, settings)
    point_cloud_path = "./data/input/point_cloud/"
    test_point_cloud = pd.read_csv(point_cloud_path + "test_point_cloud.csv")
    return test_point_cloud


def read_point_cloud(file_path):
    """
    Reads a point cloud from a CSV file.

    Parameters:
    - file_path (str): The file path to the CSV file containing the point cloud.

    Returns:
    - pd.DataFrame: The point cloud DataFrame.
    """
    return pd.read_csv(file_path)


def preprocess_point_cloud(point_cloud, epsg_code):
    """
    Preprocesses the point cloud by creating a GeoDataFrame with Point geometries.

    Parameters:
    - point_cloud (pd.DataFrame): The point cloud DataFrame.
    - epsg_code (str): The EPSG code representing the Coordinate Reference System (CRS) for the point cloud data.

    Returns:
    - gpd.GeoDataFrame: The preprocessed GeoDataFrame containing Point geometries.
    """
    return preprocess(point_cloud, epsg_code)


def save_pc_inside_mask(df: gpd.GeoDataFrame, filename: str) -> None:
    """
    Saves a GeoDataFrame representing a point cloud, filtered by a mask, to a CSV file.

    Parameters:
    - gdf (gpd.GeoDataFrame): The input GeoDataFrame containing the point cloud data.
    - filename (str): The base name for the output CSV file. The file will be saved in the "./output/filtered/" directory.

    Returns:
    - None

    Note:
    - The function checks if the GeoDataFrame contains a 'geometry' column. If present, the 'geometry' column is dropped
      before saving to the CSV file.
    - The CSV file is saved in the "./output/filtered/" directory with the specified filename followed by "_filtered.csv".
    - The function prints a message indicating the successful save operation.
    """
    if "geometry" in df.columns:
        df = df.drop(columns="geometry")
    filepath = "./data/output/" + filename + "_filtered.csv"
    df.to_csv(filepath, index=False)
    print(f"Saved filtered point cloud to '{filepath}'.")
