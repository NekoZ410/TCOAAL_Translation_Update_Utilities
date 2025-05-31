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
    data = OrderedDict()

    if records_df.empty or records_df.shape[1] < 3:
        return data

    for id_val in records_df.iloc[:, 0].dropna().unique():
        filtered_rows = records_df[records_df.iloc[:, 0].astype(str) == id_val]

        texts = filtered_rows.iloc[:, 2].fillna('').astype(str).tolist()
        combined_text = "|".join(texts).strip()
        data[id_val] = combined_text
    return data


def new_text_change():
    # Setup command line arguments
    parser = argparse.ArgumentParser(
        description="Compare text content associated with IDs between two CSV files and output differences."
    )

    parser.add_argument("old_csv", help="Path to the old CSV file. \033[32m(Required)\033[0m")
    parser.add_argument("new_csv", help="Path to the new CSV file. \033[32m(Required)\033[0m")

    parser.add_argument(
        "-o",
        "--output-file",
        default="text_differences.json",
        help="Output JSON file name \033[33m[Default: 'text_differences.json']\033[0m. \033[36m(Optional)\033[0m",
    )
    
    parser.add_argument(
        "-in",
        "--include-new-only",
        action="store_true",
        help="Include IDs that only appear in the NEW file (0 count in OLD, >=1 in NEW) \033[33m[Default: Exclude]\033[0m. \033[36m(Optional)\033[0m",
    )

    args = parser.parse_args()

    old_CSV_file = args.old_csv
    new_CSV_file = args.new_csv
    output_file = args.output_file
    include_new_only_ids = args.include_new_only 

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
        old_id_texts = process_record_output(df_old)
        
        # Read new CSV
        df_new = pd.read_csv(new_CSV_file, header=0, dtype={0: str})
        new_id_texts = process_record_output(df_new)

        # Prepare output
        all_unique_ids = list(
            OrderedDict.fromkeys(list(old_id_texts.keys()) + list(new_id_texts.keys()))
        )

        output_data = OrderedDict()
        for id_val in all_unique_ids:
            # Skip global excluded IDs
            if id_val in GLOBAL_EXCLUDE_IDS:
                continue

            old_text = old_id_texts.get(id_val, "")
            new_text = new_id_texts.get(id_val, "")

            # Skip newly added IDs
            if not include_new_only_ids and not old_text and new_text:
                continue

            # Output differences
            if old_text != new_text:
                output_data[id_val] = {
                    "OLD FILE": old_text if old_text else "(empty text)",
                    "NEW FILE": new_text if new_text else "(empty text)",
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
        print(f"Error: An unexpected error occurred: {e}")


if __name__ == "__main__":
    new_text_change()