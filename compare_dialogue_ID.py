import csv
import json
from collections import Counter


def compare_dialogue_ids(old_file, new_file, output_file):

    old_ids = []
    new_ids = []

    # Read ID from old file
    with open(old_file, "r", encoding="utf-8") as f_old:
        reader_old = csv.reader(f_old)
        for row in reader_old:
            if row:
                old_ids.append(row[0])

    # Read ID from new file
    with open(new_file, "r", encoding="utf-8") as f_new:
        reader_new = csv.reader(f_new)
        for row in reader_new:
            if row:
                new_ids.append(row[0])

    # Count adn compare the number of times each ID appears
    old_id_counts = Counter(old_ids)
    new_id_counts = Counter(new_ids)

    differences = {}
    for id_val in old_id_counts:
        if id_val in new_id_counts:
            if old_id_counts[id_val] != new_id_counts[id_val]:
                differences[id_val] = {
                    "OLD file": old_id_counts[id_val],
                    "NEW file": new_id_counts[id_val],
                }

    # Write the differences
    with open(output_file, "w", encoding="utf-8") as f_out:
        json.dump(differences, f_out, indent=4, ensure_ascii=False)

    print(f"Comparison results have been written to: {output_file}")
    if not differences:
        print("No differences found.")

old_csv_file = ""
new_csv_file = ""
output_file_path = "differences.json"
compare_dialogue_ids(old_csv_file, new_csv_file, output_file_path)
