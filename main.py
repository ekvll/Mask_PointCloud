import argparse
from src.args import gen_args
from src.plot import plot_data
from src.data_process import (
    split_point_cloud_by_mask,
)
from src.helpers import (
    read_mask,
    generate_test_point_cloud,
    read_point_cloud,
    preprocess_point_cloud,
    save_pc_inside_mask,
)


def main(args: argparse.Namespace):
    """
    Main function for processing environmental data.

    Parameters:
    - args (argparse.Namespace): Parsed command-line arguments.

    Returns:
    - None
    """
    mask_path = f"./data/input/mask/{args.mask}.gpkg"
    mask = read_mask(mask_path)

    if args.test and not args.input:
        args.input = "test_point_cloud"
        settings = {
            "base_point": (303559.734, 6401018.756),
            "num_points": 70,
            "radius": 35,
        }
        point_cloud = generate_test_point_cloud(mask, settings)

    elif args.input and not args.test:
        point_cloud_path = "./data/input/point_cloud/"
        point_cloud = read_point_cloud(point_cloud_path + args.input + ".csv")

    elif args.input and args.test:
        raise KeyError(
            "call main.py with either '-t' or '-i <input_point_cloud>', not both simultaneously"
        )

    point_cloud = preprocess_point_cloud(point_cloud, args.epsg)

    pc_inside_mask, pc_outside_mask = split_point_cloud_by_mask(mask, point_cloud)
    save_pc_inside_mask(pc_inside_mask, args.input)

    data = {
        "Plot": args.Plot,
        "mask": mask,
        "pc": point_cloud,
        "in": pc_inside_mask,
        "out": pc_outside_mask,
    }

    if args.plot or args.Plot:
        plot_data(data)


if __name__ == "__main__":
    args = gen_args()
    main(args)
