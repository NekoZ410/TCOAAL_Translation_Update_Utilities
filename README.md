# Purpose
Utilities things to check and merge after update The Coffin of Andy and Leyley translation file


# compare_dialogue_ID
Compare and find lost translation lines caused by dev's translator tool Update function

- Example:
  + Old translation: 
  ```
  NLt1n5BR,Andrew,"""Though he'll come in guns blazing...""","""Cơ mà như vậy thì chắc chắn ông ta sẽ" 
  NLt1n5BR,Andrew,"","cầm theo súng và lên đạn sẵn..."""
  ```

  + After update: 
  ```
  NLt1n5BR,Andrew,"""Though he'll come in guns blazing...""","""Cơ mà như vậy thì chắc chắn ông ta sẽ"
  ```

- Difference found:
  ```json
  ...
  "NLt1n5BR": {
        "OLD file": 2,
        "NEW file": 1
  },
  ...
  ```
## Usage

- Python:
```powershell
python dialogue_ID_difference.py [-h] [-o OUTPUT_FILE] [-in] [-v] old_csv new_csv
```

- Executable:
```powershell
dialogue_ID_difference.exe [-h] [-o OUTPUT_FILE] [-in] [-v] old_csv new_csv
```

- Params:

Shorthand | Full | Description
--- | --- | --- 
-h | --help | Show help
-o OUTPUT_FILE | --output-file OUTPUT_FILE | Output JSON file name [Default: 'differences.json']<br> (Optional) 
-in | --include-new-only | Include IDs with 0 count in OLD and >=1 in NEW [Default: Exclude]<br> (Optional)
-v | --value-records | Output actual record (row) values instead of ID counts [Default: ID counts]<br> (Optional)
❌ | old_csv | Path to the old CSV file<br> (Required)
❌ | new_csv | Path to the new CSV file<br> (Required)

# placeholder_new_text
Find newly added texts and replace with placeholder text\
(Some texts like name can be consider as duplicated and replace with placeholder)

- Example:
  + Original updated translation:
  ```csv
  t1mR4QYN,TV,TV,
  Cr6qQTg3,***,***,
  S78FX5bH,Dad,Bố,
  1Cx9N8s4,Dog,Dog,
  zrjGb3vm,Guy,Tên gác cửa 1,
  xyM2M8DP,Hag,Hag,
  SLbYdGlZ,Kid,Kid,
  4k44cyMW,Man,Man,
  S56hx4v9,Mom,Mẹ,
  kJ8dGf8G,Andy,Andy,
  5w14yHKd,Boss,Boss,
  sGxYg2dt,Dude,Tên gác cửa 2,
  ```

  + Replaced with placeholders:
  ```csv
  t1mR4QYN,TV,xxxxx,
  Cr6qQTg3,***,xxxxx,
  S78FX5bH,Dad,Bố,
  1Cx9N8s4,Dog,xxxxx,
  zrjGb3vm,Guy,Tên gác cửa 1,
  xyM2M8DP,Hag,xxxxx,
  SLbYdGlZ,Kid,xxxxx,
  4k44cyMW,Man,xxxxx,
  S56hx4v9,Mom,Mẹ,
  kJ8dGf8G,Andy,xxxxx,
  5w14yHKd,Boss,xxxxx,
  sGxYg2dt,Dude,Tên gác cửa 2,
  ```

## Usage

- Python:
```powershell
python placeholder_new_text.py [-h] [-o OUTPUT_FILE] [-plhd PLACEHOLDER_TEXT] input_file
```

- Executable:
```powershell
placeholder_new_text.exe [-h] [-o OUTPUT_FILE] [-plhd PLACEHOLDER_TEXT] input_file
```

- Params:

Shorthand | Full | Description
--- | --- | --- 
-h | --help | Show help
-o OUTPUT_FILE | --output_file OUTPUT_FILE | Path to the output CSV file [Defaults: <input_file_basename>.plhd.<extension>]<br> (Optional)
-plhd PLACEHOLDER_TEXT | --placeholder_text PLACEHOLDER_TEXT | The text to use as a placeholder [Defaults: 'xxxxx']<br> (Optional)
❌ | input_file | Path to the input CSV file<br> (Required)