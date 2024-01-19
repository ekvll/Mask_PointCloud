```markdown
# Mask PointCloud

## Overview

This Python application is designed for processing data, including filtering point clouds based on a specified mask and visualizing the results. The application uses GeoPandas, Matplotlib, and other libraries to perform various tasks related to data analysis.

## Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/ekvll/your-repo.git
   cd your-repo
   ```

2. **Install the required dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Command-Line Interface

The application can be run from the command line using the following syntax:

```bash
python main_script.py -m <mask_name> -i <input_point_cloud> -t -p -P --epsg <epsg_code>
```

- `-m` or `--mask`: Specify the name of the mask file (without the '.gpkg' file extension). To use a small example mask, use 'small_mask'.
- `-i` or `--input`: Specify the input point cloud to be filtered. Requires 'x' and 'y' to be column names of coordinate data.
- `-t` or `--test`: Activate test mode. This will generate and thereafter load and process a test point cloud.
- `-p` or `--plot`: Plot processed data, excluding the mask.
- `-P` or `--Plot`: Plot processed data, including the mask. Note, if the mask is large, the script run time is likely to be very long. If you are using the example mask 'small_mask' it is completely fine to plot with '-P'.
- `--epsg`: Specify the EPSG code (e.g., 3006 for SWEREF 99 TM).

### Functions

#### `gen_args()`

Generates command-line arguments for the application using argparse.

#### `read_mask(mask_path, target_crs="EPSG:3006")`

Reads the mask GeoDataFrame from a file and ensures it has the correct CRS.

#### `generate_test_point_cloud(mask, settings)`

Generates a test point cloud based on the provided mask and settings.

#### `read_point_cloud(file_path)`

Reads a point cloud from a CSV file.

#### `preprocess_point_cloud(point_cloud, epsg_code)`

Preprocesses the point cloud by creating a GeoDataFrame with Point geometries.

#### `main(args)`

Main function for processing environmental data. Handles reading mask and point cloud data, preprocessing, filtering, and visualization.

### Directory Structure

```plaintext
|-- LICENSE
|-- README.md
|-- input
|   |-- mask
|   |   |-- coastline.gpkg
|   |   `-- small_mask.gpkg
|   `-- point_cloud
|       |-- test1.csv
|       `-- test_point_cloud.csv
|-- main.py
|-- output
|-- requirements.txt
`-- src
    |-- __init__.py
    |-- args.py
    |-- data_process.py
    |-- helpers.py
    |-- plot.py
    `-- point_cloud.py
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
```