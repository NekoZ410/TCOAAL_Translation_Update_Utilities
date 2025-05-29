import os
import argparse
import pandas as pd


def placeholder_new_text():
    # Setup command line arguments
    parser = argparse.ArgumentParser(
        description="Process a CSV file to replace specific column values with placeholder text."
    )

    parser.add_argument(
        "input_file",
        type=str,
        help="Path to the input CSV file. \033[32m(Required)\033[0m",
    )

    parser.add_argument(
        "-o",
        "--output_file",
        type=str,
        default=None,
        help="Path to the output CSV file \033[33m[Defaults: <input_file_basename>.plhd.<extension>]\033[0m. \033[36m(Optional)\033[0m",
    )

    parser.add_argument(
        "-plhd",
        "--placeholder_text",
        type=str,
        default="xxxxx",
        help="The text to use as a placeholder \033[33m[Defaults: 'xxxxx']\033[0m. \033[36m(Optional)\033[0m",
    )

    args = parser.parse_args()

    input_file = args.input_file
    output_file = args.output_file
    placeholder_text = args.placeholder_text

    # Validate file path
    if not input_file:
        print("Error: Input file path cannot be empty.")
        return

    input_file_abs = os.path.abspath(input_file)
    if not os.path.exists(input_file_abs):
        print(f"Error: '{input_file_abs}' not found.")
        return

    # Default output file path
    if output_file is None:
        base_name, ext = os.path.splitext(input_file_abs)
        output_file_abs = f"{base_name}.plhd{ext}"
    else:
        output_file_abs = os.path.abspath(output_file)

    try:
        # Read input CSV
        df = pd.read_csv(input_file_abs)

        if df.shape[1] < 4:
            print(
                "Error: CSV file must be in true format (4 columns).\n"
                "(Try opening CSV with Excel and saving to automatically format.)"
            )
            return

        df.iloc[:, 2] = df.apply(
            lambda row: placeholder_text if row.iloc[1] == row.iloc[2] else row.iloc[2],
            axis=1,
        )

        df.iloc[:, 3] = df.apply(
            lambda row: placeholder_text if row.iloc[2] == row.iloc[3] else row.iloc[3],
            axis=1,
        )

        # Write output CSV
        df.to_csv(output_file_abs, index=False)
        print(f"\nOutput written to: {output_file_abs}")

    except FileNotFoundError:
        print(f"Error: '{input_file_abs}' not found.")
    except pd.errors.EmptyDataError:
        print(f"Error: '{input_file_abs}' is empty.")
    except Exception as e:
        print(f"Error: An unexpected error occurred: {e}")


if __name__ == "__main__":
    placeholder_new_text()
