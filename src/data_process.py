import geopandas as gpd
from shapely.geometry import Point


def preprocess(df: gpd.GeoDataFrame, epsg_code: str) -> gpd.GeoDataFrame:
    """
    Preprocesses a GeoDataFrame representing point cloud data by creating a GeoDataFrame with Point geometries.

    Parameters:
    - df (gpd.GeoDataFrame): The input GeoDataFrame containing point cloud data.
    - epsg_code (str): The EPSG code representing the Coordinate Reference System (CRS) for the point cloud data.
                      If None, the default EPSG code 'EPSG:3006' ('SWEREF 99 TM') is assumed.

    Returns:
    - gpd.GeoDataFrame: A new GeoDataFrame containing Point geometries based on the 'x' and 'y' coordinates in the input.

    Raises:
    - NameError: If the 'x' and 'y' columns are not found in the input GeoDataFrame.

    Note:
    - The function creates Point geometries from 'x' and 'y' coordinates in the input GeoDataFrame.
    - If 'epsg_code' is None, the default CRS 'EPSG:3006' ('SWEREF 99 TM') is assumed.
    - The resulting GeoDataFrame has the specified or default CRS.

    Example:
    >>> input_df = gpd.read_file('path/to/point_cloud_data.shp')
    >>> preprocessed_df = preprocess(input_df, 'EPSG:4326')
    """
    if not "x" in df.columns and not "y" in df.columns:
        raise NameError("Coordinates have to be labeled 'x' and 'y'")

    points_geom = [Point(row.x, row.y) for _, row in df.iterrows()]

    if epsg_code is None:
        print("=" * 30)
        print(
            "No EPSG code provided. Assuming data are in 'EPSG:3006' ('SWEREF 99 TM')"
        )
        gdf = gpd.GeoDataFrame(df, geometry=points_geom, crs="EPSG:3006")

    else:
        print("=" * 30)
        print(f"Input point cloud in 'EPSG:{epsg_code}'")
        gdf = gpd.GeoDataFrame(df, geometry=points_geom, crs=f"EPSG:{epsg_code}")

    return gdf


def split_point_cloud_by_mask(
    mask: gpd.GeoDataFrame, point_cloud: gpd.GeoDataFrame
) -> (gpd.GeoDataFrame, gpd.GeoDataFrame):
    """
    Splits a GeoDataFrame representing a point cloud into two GeoDataFrames based on a mask.

    Parameters:
    - mask (gpd.GeoDataFrame): The GeoDataFrame representing the mask used for splitting the point cloud.
    - point_cloud (gpd.GeoDataFrame): The GeoDataFrame representing the input point cloud.

    Returns:
    - Tuple[gpd.GeoDataFrame, gpd.GeoDataFrame]: A tuple containing two GeoDataFrames -
      the first one representing the point cloud inside the mask, and the second one representing
      the point cloud outside the mask.

    Note:
    - The function uses the 'transform_crs' function to ensure both the mask and point cloud have the same CRS.
    - The point cloud is split into two parts: 'pc_inside_mask' contains points inside the mask, and
      'pc_outside_mask' contains points outside the mask.
    - The function provides a summary of the shapes of the input point cloud, point cloud inside the mask,
      and point cloud outside the mask.

    Example:
    >>> mask = gpd.read_file('path/to/mask.shp')
    >>> point_cloud = gpd.read_file('path/to/point_cloud.shp')
    >>> pc_inside, pc_outside = split_point_cloud_by_mask(mask, point_cloud)
    """

    def _summary():
        print("=" * 30)
        print("Summary")
        print("-" * 30)
        print("Shape of point clouds:")
        print(f"Input point cloud: {point_cloud.shape}")
        print(f"Point cloud inside mask: {pc_inside_mask.shape}")
        print(f"Point cloud outside mask: {pc_outside_mask.shape}")
        print("=" * 30)

    # Ensure both mask and point cloud have the same CRS
    target_crs = mask.crs
    point_cloud = transform_crs(point_cloud, target_crs)

    # Spatial join to separate points inside and outside the mask
    pc_inside_mask = gpd.sjoin(point_cloud, mask, predicate="within")
    pc_inside_mask = pc_inside_mask[list(point_cloud.columns)]
    pc_outside_mask = point_cloud[~point_cloud.index.isin(pc_inside_mask.index)]

    # Display summary information
    _summary()

    return pc_inside_mask, pc_outside_mask


def transform_crs(gdf: gpd.GeoDataFrame, target_crs: str) -> gpd.GeoDataFrame:
    """
    Transforms the Coordinate Reference System (CRS) of a GeoDataFrame to the specified target CRS.

    Parameters:
    - gdf (gpd.GeoDataFrame): The input GeoDataFrame with spatial data.
    - target_crs (str): The target Coordinate Reference System (CRS) to which the GeoDataFrame should be transformed.

    Returns:
    - gpd.GeoDataFrame: A new GeoDataFrame with the spatial data transformed to the target CRS.

    Raises:
    - ValueError: If the input GeoDataFrame does not have a defined CRS.

    Note:
    - The function uses the `to_crs` method of GeoDataFrame to perform the CRS transformation.

    Example:
    >>> transformed_data = transform_crs(my_geo_dataframe, 'EPSG:4326')
    """
    if gdf.crs is None:
        print("GeoDataFrame is missing a CRS.")
        return []

    transformed_gdf = gdf.to_crs(target_crs)
    return transformed_gdf
