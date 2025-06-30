import pandas as pd

data_path = 'data/pgs_table_info.csv'
output_path = 'data/filtered_tab.csv'

df = pd.read_csv(data_path)

group_counts = df['Trait_group'].value_counts().reset_index()
group_counts.columns = ['Trait_group', 'Count']

print("Available groups:")
for i, row in group_counts.iterrows():
    print(f'{i+1}. {row.Trait_group} ({row.Count} rekordów)')

selected_indices = input("Enter group numbers separated by spaces: ").split()
selected_indices = [int(i) - 1 for i in selected_indices]

selected_groups = group_counts.loc[selected_indices, 'Trait_group'].tolist()

filtered_parts = []

for group in selected_groups:
    group_df = df[df['Trait_group'] == group]
    trait_names = group_df['Trait_name'].unique()

    num_traits = int(input(f"Enter the number of traits to download {group}? "))

    selected_traits = trait_names[:num_traits]

    for trait in selected_traits:
        trait_df = group_df[group_df['Trait_name'] == trait]
        filtered_parts.append(trait_df)

filtered_tab = pd.concat(filtered_parts, ignore_index=True)
filtered_tab.to_csv(output_path, index=False)

print(f'Saved {len(filtered_tab)} records.')
