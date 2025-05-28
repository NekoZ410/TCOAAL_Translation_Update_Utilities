import pandas as pd
import os


def process_csv_with_placeholders():
    # Updated translation CSV file path
    input_file = input("Path to updated CSV: ").strip()
    while not input_file:
        print("Path cannot be empty.")
        input_file = input("Path to updated CSV: ").strip()
    if not os.path.exists(input_file):
        print(f"Error: '{input_file}' not found.")
        return

    # Output CSV file path
    base_name, ext = os.path.splitext(input_file)
    default_output_file = f"{base_name}.plhd{ext}"
    custom_output_file = input(
        f"Output CSV file (Default: {default_output_file}): "
    ).strip()
    output_file = custom_output_file if custom_output_file else default_output_file

    # Placeholder text, default is 'xxxxx'
    placeholder_input = input("Placeholder text (Default: 'xxxxx'): ").strip()
    placeholder_text = placeholder_input if placeholder_input else "xxxxx"

    try:
        # Read input CSV file
        df = pd.read_csv(input_file)
        print(f"Read '{input_file}', {len(df)} rows, {len(df.columns)} cols.")

        # Ensure the CSV has true format
        if df.shape[1] < 4:
            print(
                "Error: CSV file must be in true format (4 columns).\n(Try open CSV with Excel and save to automatically formatted.)"
            )
            return

        # Compare col 2 and 3 (Speakers, Items, )
        df.iloc[:, 2] = df.apply(
            lambda row: placeholder_text if row.iloc[1] == row.iloc[2] else row.iloc[2],
            axis=1,
        )
        print("Replaced with placeholders at Speakers and Items.")

        # Compare col 3 and 4 (Item desc, Dialogues)
        df.iloc[:, 3] = df.apply(
            lambda row: placeholder_text if row.iloc[2] == row.iloc[3] else row.iloc[3],
            axis=1,
        )
        print("Replaced with placeholders at Item desc and Dialogues.")

        # Write ouput CSV file
        df.to_csv(output_file, index=False)
        print(f"\nOutput written to: {output_file}")

    except FileNotFoundError:
        print(f"Error: File '{input_file}' not found.")
    except pd.errors.EmptyDataError:
        print(f"Error: File '{input_file}' is empty.")
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    process_csv_with_placeholders()
    input("Press any key to exit...")
