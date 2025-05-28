import pandas as pd
import json
import os
from collections import OrderedDict


def dialogue_ID_difference():
    # Old CSV file
    old_CSV_file = input("\033[32mPath to old CSV: \033[0m").strip()
    while not old_CSV_file:
        print("Path cannot be empty.")
        old_CSV_file = input("\033[32mPath to old CSV: \033[0m").strip()
    if not os.path.exists(old_CSV_file):
        print(f"Error: '{old_CSV_file}' not found.")
        return

    # New CSV file
    new_CSV_file = input("\033[32mPath to new CSV: \033[0m").strip()
    while not new_CSV_file:
        print("Path cannot be empty.")
        new_CSV_file = input("\033[32mPath to new CSV: \033[0m").strip()
    if not os.path.exists(new_CSV_file):
        print(f"Error: '{new_CSV_file}' not found.")
        return

    # Output file
    output_file = input("\033[33mOutput JSON file name [Default: 'differences.json']: \033[0m")
    if not output_file:
        output_file = "differences.json"

    # Skip newly added IDs
    filter_option = (
        input("\033[36mSkip newly added IDs (0 in OLD)? (Y/N) [Default: Y]: \033[0m")
        .strip()
        .lower()
    )
    if not filter_option or filter_option == "y":
        exclude_new_only_ids = True
    else:
        exclude_new_only_ids = False

    try:
        # Read old CSV
        df_old = pd.read_csv(old_CSV_file, header=0, dtype={0: str})
        old_ids = df_old.iloc[:, 0].dropna()
        old_id_counts = old_ids.value_counts().to_dict()

        # Read new CSV
        df_new = pd.read_csv(new_CSV_file, header=0, dtype={0: str})
        new_ids = df_new.iloc[:, 0].dropna()
        new_id_counts = new_ids.value_counts().to_dict()

        # Prepare output data
        all_unique_ids = list(OrderedDict.fromkeys(old_ids.tolist() + new_ids.tolist()))
        output_data = OrderedDict()
        for id_val in all_unique_ids:
            old_count = old_id_counts.get(id_val, 0)
            new_count = new_id_counts.get(id_val, 0)

            if (exclude_new_only_ids and old_count == 0 and new_count >= 1) or (
                old_count == new_count
            ):
                continue

            output_data[id_val] = {"OLD FILE": old_count, "NEW FILE": new_count}

        # Write to JSON
        with open(output_file, "w", encoding="utf-8") as f_out:
            json.dump(output_data, f_out, indent=4, ensure_ascii=False)
        print(f"Output written to: {output_file}")

    except pd.errors.EmptyDataError:
        print("Error: One of the CSV files is empty or not a valid CSV format.")
        return
    except FileNotFoundError as e:
        print(f"Error: {e}.")
        return
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    dialogue_ID_difference()
    input("Press any key to exit...")
