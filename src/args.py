import argparse


def gen_args() -> argparse.Namespace:
    """
    Generates command-line arguments for an EPA (Environmental Protection Agency) application.

    Returns:
    - argparse.Namespace: An object containing the parsed command-line arguments.

    Note:
    - The function uses argparse to define and parse command-line arguments for the EPA application.
    - The available arguments include 'mask', 'input', 'test', 'plot', 'Plot', and 'epsg'.
    - 'mask' is the name of the mask file (without the '.gpkg' file extension). To use a small example mask, use 'small_mask'.
    - 'input' is the input point cloud to be filtered. Requires 'x' and 'y' to be column names of coordinate data.
    - 'test' activates test mode. This will generate and thereafter load and process a test point cloud.
    - 'plot' and 'Plot' activate data plotting (excluding and including the mask, respectively).
    - 'epsg' specifies the EPSG code (e.g., 3006 for SWEREF 99 TM (EPSG:3006)).
    """
    parser = argparse.ArgumentParser(description="EPA")
    parser.add_argument(
        "-m",
        "--mask",
        help="Name of mask file, without the '.gpkg' file extension. To use a small example mask use 'small_mask'.",
    )
    parser.add_argument(
        "-i",
        "--input",
        help="Input point cloud to be filtered. Requires 'x' and 'y' to be column names of coordinate data.",
    )
    parser.add_argument(
        "-t",
        "--test",
        action="store_true",
        help="Activate test mode. This will generate and thereafter load and process a test point cloud.",
    )
    parser.add_argument(
        "-p",
        "--plot",
        action="store_true",
        help="Plot processed data, excluding the mask.",
    )
    parser.add_argument(
        "-P",
        "--Plot",
        action="store_true",
        help="Plot processed data, including the mask. Note, if the mask is large the script run time is likely to be very long. If you are using the example mask 'small_mask' it is completely fine to plot with '-P'.",
    )
    parser.add_argument(
        "--epsg",
        help="EPSG digits (e.g. 3006 for SWEREF 99 TM (EPSG:3006)).",
        required=False,
    )
    args = parser.parse_args()
    return args
