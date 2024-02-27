import pandas as pd
import uuid


df = pd.read_csv('credit_card_transactions-ibm_v2.csv')
cards = pd.read_csv('sd254_cards.csv')


# Find the highest index for each user where Card_Number is not NaN
max_index_per_user = cards.groupby('User')['CARD INDEX'].idxmax()

# Creating a new column 'Merchant_ID' based on 'Merchant Name'
df['Merchant_ID'] = df['Merchant Name'].apply(lambda x: df[df['Merchant Name'] == x].index[0])

# Creating a new column 'transaction_id' with incremental values
df['UUID'] = [str(uuid.uuid4()) for x in range(len(df))]

# Save the modified DataFrame to a new CSV file
df.to_csv("transactions_table_updated.csv", index=False)

print("Done")