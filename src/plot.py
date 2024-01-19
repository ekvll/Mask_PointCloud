import matplotlib.pyplot as plt
import contextily as ctx
import matplotlib.lines as mlines
from matplotlib.patches import Patch
from src.data_process import transform_crs


def plot_mask(ax, mask):
    """
    Plots a polygon mask on a given axis.

    Parameters:
    - ax (matplotlib.axes._subplots.AxesSubplot): The axis on which the polygon mask is plotted.
    - mask (gpd.GeoDataFrame): GeoDataFrame representing the polygon mask.

    Returns:
    - None

    Note:
    - The function uses the 'plot' method to display the polygon mask on the specified axis.
    - The polygon is filled with a transparency of 0.7, has a black edge, and is labeled as "Mask" in the legend.
    """
    mask.plot(ax=ax, alpha=0.7, edgecolor="k", linewidth=2, label="Mask")


def plot_point_inside(ax, pc_inside_polygon):
    """
    Plots points inside a specified polygon on a given axis.

    Parameters:
    - ax (matplotlib.axes._subplots.AxesSubplot): The axis on which the points are plotted.
    - pc_inside_polygon (gpd.GeoDataFrame): GeoDataFrame representing points inside the polygon.

    Returns:
    - None

    Note:
    - The function uses the 'plot' method to display points inside the polygon on the specified axis.
    - Points are plotted in blue, marked with 'o', and labeled as "Point Inside" in the legend.
    - The legend is updated with the new plot.
    """
    pc_inside_polygon.plot(
        ax=ax, color="blue", marker="o", markersize=50, label="Point Inside"
    )


def plot_point_outside(ax, pc_outside_polygon):
    """
    Plots points outside a specified polygon on a given axis.

    Parameters:
    - ax (matplotlib.axes._subplots.AxesSubplot): The axis on which the points are plotted.
    - pc_outside_polygon (gpd.GeoDataFrame): GeoDataFrame representing points outside the polygon.

    Returns:
    - None

    Note:
    - The function uses the 'plot' method to display points outside the polygon on the specified axis.
    - Points are plotted in red, marked with 'x', and labeled as "Point Outside" in the legend.
    - The legend is updated with the new plot.
    """
    pc_outside_polygon.plot(
        ax=ax, color="red", marker="x", markersize=50, label="Point Outside"
    )


def add_legend(data: dict):
    """
    Creates legend handles for a spatial data plot.

    Parameters:
    - data (dict): A dictionary containing spatial data:
        - 'out' (gpd.GeoDataFrame): GeoDataFrame representing points outside the polygon.
        - 'Plot' (bool): If True, the mask is plotted; otherwise, it is not.

    Returns:
    - list: A list of legend handles for the spatial data plot.

    Note:
    - The function defines legend handles for points inside the mask, points outside the mask, and the mask itself.
    - The legend handles are used to create a legend in the plot.
    """
    pc_inside_legend = mlines.Line2D(
        [],
        [],
        color="blue",
        marker="o",
        linestyle="None",
        markersize=10,
        label="Point Inside Mask",
    )

    legend_handles = [pc_inside_legend]

    if not data["out"].empty:
        pc_outside_legend = mlines.Line2D(
            [],
            [],
            color="red",
            marker="x",
            linestyle="None",
            markersize=10,
            label="Point Outside Mask",
        )
        legend_handles.append(pc_outside_legend)

    if not data["Plot"]:
        return legend_handles

    mask_legend = Patch(facecolor="blue", edgecolor="black", alpha=0.7, label="Mask")
    legend_handles.append(mask_legend)

    return legend_handles


def plot_data(data: dict):
    """
    Plots spatial data, including a mask, points inside a polygon, and optionally points outside the polygon.

    Parameters:
    - data (dict): A dictionary containing spatial data:
        - 'mask' (gpd.GeoDataFrame): GeoDataFrame representing the mask polygon.
        - 'in' (gpd.GeoDataFrame): GeoDataFrame representing points inside the polygon.
        - 'out' (gpd.GeoDataFrame): GeoDataFrame representing points outside the polygon.
        - 'Plot' (bool): If True, the mask is plotted; if False, the mask is not plotted.

    Returns:
    - None

    Note:
    - The function transforms input GeoDataFrames to a common target CRS ('EPSG:3857') for consistent plotting.
    - The function uses various plot functions (e.g., 'plot_mask', 'plot_point_inside', 'plot_point_outside').
    - If 'data["Plot"]' is True, the mask is plotted; otherwise, it is not.
    - The resulting plot includes OpenStreetMap basemap, legend, and is displayed using plt.show().
    """
    target_crs = "EPSG:3857"

    mask = transform_crs(data["mask"], target_crs)
    pc_inside_polygon = transform_crs(data["in"], target_crs)

    # Buffer the single-point GeoDataFrame if 'Plot' is not True
    if pc_inside_polygon.shape[0] == 1 and data["Plot"] is not True:
        pc_inside_polygon["geometry"] = pc_inside_polygon.buffer(0.0001)

    pc_outside_polygon = transform_crs(data["out"], target_crs)

    ax = plt.figure(figsize=(10, 10)).add_subplot(1, 1, 1)

    if data["Plot"]:
        plot_mask(ax, mask)

    plot_point_inside(ax, pc_inside_polygon)

    if not pc_outside_polygon.empty:
        plot_point_outside(ax, pc_outside_polygon)

    # Add OpenStreetMap basemap
    ctx.add_basemap(ax, source=ctx.providers.OpenStreetMap.Mapnik, zoom=19)

    legend_handles = add_legend(data)

    # Add legend
    ax.legend(
        loc="upper right",
        handles=legend_handles,
    )

    plt.show()
