import sys
import pandas as pd

print('Arguments:', sys.argv)

df = pd.DataFrame({"A": [1, 2], "B": [3, 4]})
print(df.head())

month = 2

df.to_parquet(f"output_{month}.parquet")


print('hello pipeline')