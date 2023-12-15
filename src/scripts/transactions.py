
import cudf
import cupy as cp

# Read the CSV files using cuDF
df = cudf.read_csv('credit_card_transactions-ibm_v2.csv')
cards = cudf.read_csv('sd254_cards.csv')

# Find the highest index for each user where Card_Number is not NaN
max_index_per_user = cards.groupby('User')['CARD INDEX'].idxmax()

# Creating a new column 'Merchant_ID' based on 'Merchant Name'
merchant_id_map = {merchant: index for index, merchant in enumerate(df['Merchant Name'].unique().to_arrow().to_pylist())}
df['Merchant_ID'] = df['Merchant Name'].map(merchant_id_map)

# Creating a new column 'transaction_id' with incremental values
df['transaction_id'] = cp.arange(len(df))

# Save the modified DataFrame to a new CSV file
df.to_csv("transactions_table_updated.csv", index=False, chunksize=100)

print("Done")
