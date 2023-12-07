import pandas as pd


df = pd.read_csv('transactions_table_1.csv')
cards = pd.read_csv('sd254_cards.csv')


# Find the highest index for each user where Card_Number is not NaN
max_index_per_user = cards.groupby('User')['CARD INDEX'].idxmax()

# Update NaN values in 'Card_Number' based on the highest index for each user
'''df['Card Number'] = df.apply(lambda row: cards.loc[max_index_per_user.loc[row['User']], 'Card Number']
                             if pd.isna(row['Card Number']) else row['Card Number'], axis=1)'''

# Creating a new column 'Merchant_ID' based on 'Merchant Name'
df['Merchant_ID'] = df['Merchant Name'].apply(lambda x: df[df['Merchant Name'] == x].index[0])

# Creating a new column 'transaction_id' with incremental values
df['transaction_id'] = range(len(df))

# Save the modified DataFrame to a new CSV file
df.to_csv("transactions_table_updated.csv", index=False)

print("Done")
