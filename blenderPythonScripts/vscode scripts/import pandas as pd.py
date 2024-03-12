import pandas as pd

# Sample data frame
data = {
    'RowLabel': ['Row1', 'Row1', 'Row2', 'Row2'],
    'ColumnLabel': ['Col1', 'Col2', 'Col1', 'Col2'],
    'Value': [1, 2, 3, 4]
}
df = pd.DataFrame(data)

# Create a pivot table to reshape the data frame into a matrix
matrix_df = df.pivot(index='RowLabel', columns='ColumnLabel', values='Value')

# Reset index to get 'RowLabel' back as a column (optional, depending on your needs)
matrix_df.reset_index(inplace=True)

# Show the resulting matrix
print(matrix_df)
