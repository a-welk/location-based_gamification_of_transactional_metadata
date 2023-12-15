import pandas as pd

# Load the CSV file
df = pd.read_csv('transactions_final.csv')

# Remove the "Merchant Name" column
df.drop('Merchant Name', axis=1, inplace=True)

# Save the modified DataFrame back to a CSV file
df.to_csv('transactions_final_modified.csv', index=False)
