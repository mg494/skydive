import pandas as pd

df = pd.DataFrame({'A': ['a', 'b', 'c', 'd', 'e'],

                   'B': ['f', 'g', 'h', 'i', 'j'],

                   'C': ['k', 'l', 'm', 'n', 'o']},

                  index=[1, 2, 3, 4, 5])
print(df.tail())

df = df.truncate(before=2, after=4)
print(df.tail())
