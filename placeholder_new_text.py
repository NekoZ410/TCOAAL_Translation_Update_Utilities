import pandas as pd

new_csv_file = ''
output_file_path = ''
placeholder_text = 'xxxxx'

# Read CSV
df = pd.read_csv(new_csv_file)

# Check col 2 and 3, if be the same replace values in col 3 with placholder
df.iloc[:, 2] = df.apply(lambda row: placeholder_text if row.iloc[1] == row.iloc[2] else row.iloc[2], axis=1)

# Check col 3 and 4, if be the same replace values in col 4 with placholder
df.iloc[:, 3] = df.apply(lambda row: placeholder_text if row.iloc[2] == row.iloc[3] else row.iloc[3], axis=1)

# Write new CSV
df.to_csv(output_file_path, index=False)

print(f'Replaced new text with placeholder into new CSV: {output_file_path}')
