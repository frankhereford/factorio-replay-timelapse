import os
import sys
import pprint
import math
import shutil

def get_file_listing():
    source_dir = os.getenv('SOURCE', '/app/static')
    try:
        files = os.listdir(source_dir)
        return files
    except FileNotFoundError:
        return f"Directory {source_dir} does not exist."
    except PermissionError:
        return f"Permission denied to access {source_dir}."

def filter_and_sort_files(files):
    integer_files = [int(f) for f in files if f.lstrip('-').isdigit()]
    integer_files.sort()
    return integer_files

def get_directory_contents(directory):
    try:
        contents = os.listdir(directory)
        return contents
    except FileNotFoundError:
        return f"Directory {directory} does not exist."
    except PermissionError:
        return f"Permission denied to access {directory}."

def filter_and_sort_png_files(files):
    integer_files = [int(f[:-4]) for f in files if f.endswith('.png') and f[:-4].lstrip('-').isdigit()]
    integer_files.sort()
    return integer_files

def compute_grid_dimensions(nested_dict):
    all_coordinates = [(x, y) for x in nested_dict for y in nested_dict[x]]
    min_x = min(x for x, y in all_coordinates)
    max_x = max(x for x, y in all_coordinates)
    min_y = min(y for x, y in all_coordinates)
    max_y = max(y for x, y in all_coordinates)
    width = max_x - min_x + 1
    height = max_y - min_y + 1
    return width, height

def smallest_power_of_two_greater_than_or_equal_to(x):
    return 2 ** math.ceil(math.log2(x))

def transform_coordinates(n, nested_dict):
    all_coordinates = [(x, y) for x in nested_dict for y in nested_dict[x]]
    min_x = min(x for x, y in all_coordinates)
    max_x = max(x for x, y in all_coordinates)
    min_y = min(y for x, y in all_coordinates)
    max_y = max(y for x, y in all_coordinates)

    offset_x = (2**n - (max_x - min_x + 1)) // 2 - min_x
    offset_y = (2**n - (max_y - min_y + 1)) // 2 - min_y

    transformed_dict = {}
    for x in nested_dict:
        for y in nested_dict[x]:
            new_x = x + offset_x
            new_y = y + offset_y
            if new_x not in transformed_dict:
                transformed_dict[new_x] = {}
            transformed_dict[new_x][new_y] = nested_dict[x][y]

    return transformed_dict

def copy_files_to_target(transformed_dict, n):
    target_dir = os.getenv('TARGET', '/app/web-tiles/')
    for x in transformed_dict:
        for y in transformed_dict[x]:
            source_file = transformed_dict[x][y]
            target_path = os.path.join(target_dir, str(n), str(x), f"{y}.png")
            os.makedirs(os.path.dirname(target_path), exist_ok=True)
            shutil.copy2(source_file, target_path)

if __name__ == "__main__":
    file_listing = get_file_listing()
    if isinstance(file_listing, list):
        filtered_sorted_files = filter_and_sort_files(file_listing)
        if not filtered_sorted_files:
            print("No valid integer directories found.")
            sys.exit(1)

        if len(sys.argv) > 1:
            try:
                target_dir = int(sys.argv[1])
            except ValueError:
                print("The provided argument is not a valid integer.")
                sys.exit(1)
        else:
            target_dir = os.getenv('TICK')
            if target_dir is not None:
                try:
                    target_dir = int(target_dir)
                except ValueError:
                    print("The TICK environment variable is not a valid integer.")
                    sys.exit(1)
            else:
                target_dir = filtered_sorted_files[-1]

        if target_dir in filtered_sorted_files:
            directory_path = os.path.join(os.getenv('SOURCE', '/app/static'), str(target_dir))
            directory_contents = get_directory_contents(directory_path)
            # print(f"Contents of directory {directory_path}: {directory_contents}")

            subdirectory_path = os.path.join(directory_path, "10")
            subdirectory_contents = get_directory_contents(subdirectory_path)
            if isinstance(subdirectory_contents, list):
                filtered_sorted_subdirectories = filter_and_sort_files(subdirectory_contents)
                # print(f"Ordered integer directories inside '10': {filtered_sorted_subdirectories}")

                nested_dict = {}
                for subdirectory in filtered_sorted_subdirectories:
                    deepest_directory_path = os.path.join(subdirectory_path, str(subdirectory))
                    deepest_directory_contents = get_directory_contents(deepest_directory_path)
                    if isinstance(deepest_directory_contents, list):
                        filtered_sorted_png_files = filter_and_sort_png_files(deepest_directory_contents)
                        for file in filtered_sorted_png_files:
                            if subdirectory not in nested_dict:
                                nested_dict[subdirectory] = {}
                            nested_dict[subdirectory][file] = os.path.join(deepest_directory_path, f"{file}.png")
                    else:
                        print(deepest_directory_contents)

                # pprint.pprint(nested_dict)

                width, height = compute_grid_dimensions(nested_dict)
                grid_size = max(width, height)
                n = math.ceil(math.log2(grid_size))
                print(f"The smallest value of n such that the grid can fit into a 2^n by 2^n grid is: {n}")

                transformed_file_listing = transform_coordinates(n, nested_dict)
                pprint.pprint(transformed_file_listing)

                copy_files_to_target(transformed_file_listing, n)
            else:
                print(subdirectory_contents)
        else:
            print(f"Directory {target_dir} does not exist in the list of valid directories.")
    else:
        print(file_listing)