import os
import json
import argparse
from collections import OrderedDict
import pandas as pd

GLOBAL_EXCLUDE_IDS = [
    "Section",
    "ID",
]


def process_record_output(records_df):
    processed_data = []

    for _, row in records_df.iterrows():
        record = row.tolist()

        if len(record) < 3:
            continue

        selected_cols = []
        if len(record) == 3:
            selected_cols = [record[1], record[2]]
        elif len(record) >= 4:
            selected_cols = [record[2], record[3]]

        formatted_cols = pd.Series(selected_cols).fillna("(empty col)").tolist()
        processed_data.append(formatted_cols)

    return processed_data


def dialogue_ID_difference():
    # Setup command line arguments
    parser = argparse.ArgumentParser(
        description="Compare IDs between two CSV files and output differences."
    )

    parser.add_argument("old_csv", help="Path to the old CSV file. \033[32m(Required)\033[0m")
    parser.add_argument("new_csv", help="Path to the new CSV file. \033[32m(Required)\033[0m")

    parser.add_argument(
        "-o",
        "--output-file",
        default="differences.json",
        help="Output JSON file name \033[33m[Default: 'differences.json']\033[0m. \033[36m(Optional)\033[0m",
    )

    parser.add_argument(
        "-in",
        "--include-new-only",
        action="store_true",
        help="Include IDs with 0 count in OLD and >=1 in NEW \033[33m[Default: Exclude]\033[0m. \033[36m(Optional)\033[0m",
    )

    parser.add_argument(
        "-v",
        "--value-records",
        action="store_true",
        help="Output actual record (row) values instead of ID counts \033[33m[Default: ID counts]\033[0m. \033[36m(Optional)\033[0m",
    )

    args = parser.parse_args()

    old_CSV_file = args.old_csv
    new_CSV_file = args.new_csv
    output_file = args.output_file
    exclude_new_only_ids = not args.include_new_only
    output_as_records = args.value_records

    # Validate file paths
    if not os.path.exists(old_CSV_file):
        print(f"Error: '{old_CSV_file}' not found.")
        return
    if not os.path.exists(new_CSV_file):
        print(f"Error: '{new_CSV_file}' not found.")
        return

    try:
        # Read old CSV
        df_old = pd.read_csv(old_CSV_file, header=0, dtype={0: str})
        old_ids_series = df_old.iloc[:, 0].dropna()
        old_id_counts = old_ids_series.value_counts().to_dict()

        # Read new CSV
        df_new = pd.read_csv(new_CSV_file, header=0, dtype={0: str})
        new_ids_series = df_new.iloc[:, 0].dropna()
        new_id_counts = new_ids_series.value_counts().to_dict()

        # Prepare output
        all_unique_ids = list(
            OrderedDict.fromkeys(old_ids_series.tolist() + new_ids_series.tolist())
        )

        output_data = OrderedDict()
        for id_val in all_unique_ids:
            # Skip global excluded IDs
            if id_val in GLOBAL_EXCLUDE_IDS:
                continue

            old_count = old_id_counts.get(id_val, 0)
            new_count = new_id_counts.get(id_val, 0)

            # Skip newly added IDs
            if exclude_new_only_ids and old_count == 0 and new_count >= 1:
                continue

            # Skip unchanged IDs
            if old_count == new_count:
                continue

            # Output records style
            if output_as_records:
                filtered_df_old = df_old[df_old.iloc[:, 0].astype(str) == id_val]
                filtered_df_new = df_new[df_new.iloc[:, 0].astype(str) == id_val]

                old_records = process_record_output(filtered_df_old)
                new_records = process_record_output(filtered_df_new)

                if old_records or new_records:
                    output_data[id_val] = {
                        "OLD FILE": old_records,
                        "NEW FILE": new_records,
                    }
            else:
                filtered_new_count = new_count
                if new_count == 0:
                    filtered_new_count = "(deleted)"

                output_data[id_val] = {
                    "OLD FILE": old_count,
                    "NEW FILE": filtered_new_count,
                }

        # Write output JSON
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
