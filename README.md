# TCOAAL_Translation_Update_Utilities
Utilities things to check and merge after update The Coffin of Andy and Leyley translation file

## compare_dialogue_ID
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

## placeholder_new_text
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