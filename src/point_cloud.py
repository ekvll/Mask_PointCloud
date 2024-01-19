import random
import geopandas as gpd
import pandas as pd
from shapely.geometry import Point


def gen_point_cloud(polygon_mask: gpd.GeoDataFrame, settings: dict) -> gpd.GeoDataFrame:
    """
    Generates a GeoDataFrame representing a point cloud within the largest area of a specified polygon mask.

    Parameters:
    - polygon_mask (gpd.GeoDataFrame): The GeoDataFrame containing the polygon mask.
    - settings (dict): A dictionary containing generation settings:
        - 'base_point' (tuple): The base point (x, y) around which the point cloud is generated.
        - 'num_points' (int): The number of points to generate in the point cloud.
        - 'radius' (float): The radius around the base point within which points are generated.

    Returns:
    - gpd.GeoDataFrame: A new GeoDataFrame containing the generated point cloud.

    Note:
    - The function first extracts the largest area polygon from the input polygon mask.
    - It then generates random points within a specified radius around a base point.
    - The resulting GeoDataFrame is saved to a CSV file using the 'save_to_csv' function.

    Example:
    >>> mask_gdf = gpd.read_file('path/to/mask.shp')
    >>> generation_settings = {'base_point': (10, 20), 'num_points': 100, 'radius': 5.0}
    >>> generated_point_cloud = gen_point_cloud(mask_gdf, generation_settings)
    """
    polygon_mask = keep_largest_area_polygon(polygon_mask)

    base_point = settings["base_point"]
    num_points = settings["num_points"]
    radius = settings["radius"]

    # Generate random points within the specified radius around the base point
    point_cloud = [
        Point(
            base_point[0] + random.uniform(-radius, radius),
            base_point[1] + random.uniform(-radius, radius),
        )
        for _ in range(num_points)
    ]

    # Create a GeoDataFrame from the generated points with the specified CRS
    point_cloud = gpd.GeoDataFrame(geometry=point_cloud, crs="EPSG:3006")

    # Save the generated point cloud to a CSV file
    save_to_csv(point_cloud)

    return point_cloud


def keep_largest_area_polygon(gdf: gpd.GeoDataFrame) -> gpd.GeoDataFrame:
    """
    Filters a GeoDataFrame to keep only the polygon with the largest area.

    Parameters:
    - gdf (gpd.GeoDataFrame): The input GeoDataFrame containing polygon geometries.

    Returns:
    - gpd.GeoDataFrame: A new GeoDataFrame containing only the polygon with the largest area.

    Raises:
    - ValueError: If the input GeoDataFrame is empty.

    Note:
    - The function calculates the area of each polygon in the GeoDataFrame and adds an 'area' column.
    - The polygon with the largest area is selected, and a new GeoDataFrame containing only that polygon is returned.
    """
    if len(gdf) == 0:
        raise ValueError("Input GeoDataFrame is empty.")

    # Calculate area for each polygon
    gdf = gdf.assign(area=gdf.geometry.area)

    # Find the index of the polygon with the largest area
    largest_area_index = gdf.area.idxmax()

    # Extract the polygon with the largest area and remove the 'area' column
    largest_area_polygon = gdf.loc[largest_area_index:largest_area_index].copy()
    largest_area_polygon = largest_area_polygon.drop(columns="area")

    return largest_area_polygon


def save_to_csv(point_cloud: gpd.GeoDataFrame) -> None:
    """
    Saves a GeoDataFrame representing a point cloud to a CSV file containing 'x' and 'y' columns.

    Parameters:
    - point_cloud (gpd.GeoDataFrame): The GeoDataFrame containing point cloud data.

    Returns:
    - None

    Note:
    - The function extracts 'x' and 'y' coordinates from the 'geometry' column of the input GeoDataFrame.
    - It creates a DataFrame with 'x' and 'y' columns and saves it to a CSV file in the "./input/point_cloud/" directory.
    - The CSV file is named "test_point_cloud.csv" and does not include an index column.
    """
    data = {
        "x": point_cloud.geometry.x.values,
        "y": point_cloud.geometry.y.values,
    }

    to_csv = pd.DataFrame(data)
    to_csv.to_csv("./data/input/point_cloud/test_point_cloud.csv", index=False)
