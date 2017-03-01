import pandas as pd
import seaborn as sns
import matplotlib as mpl
import matplotlib.pyplot as plt

seperator = '\n-------------------------\n'

ratios_df = pd.read_csv('ratios.csv')
train_df = pd.read_csv('Data/train.csv')
train_df = train_df.loc[:, ['id', 'species']]

train_df = train_df.set_index('id')
print(seperator, 'Training Data Set Info')
print(train_df.info())
print(train_df[:10])

ratios_df = ratios_df.set_index('id')
print(seperator, 'Ratios Data Set Info')
print(ratios_df.info())
print(ratios_df[:10])

train_df = pd.concat([train_df, ratios_df], axis = 1, join_axes = [train_df.index])
print(seperator, 'After adding ratios column, training data is\n', train_df[:10])

traingroups = train_df.groupby('species').mean()
traingroups = traingroups.sort_values(by = 'isopratio', ascending = 1)
print(seperator, 'After grouping by species and reordering, traingroups = \n', traingroups[:10])
speciesorder = traingroups.index.values
print('Order of species is\n', speciesorder[:10])

train_df['species'] = train_df['species'].astype('category')
train_df['species'] = train_df['species'].cat.set_categories(speciesorder, ordered = True)

print(seperator, 'Training Data set after attaching ordering\n', train_df[:10])
ax = sns.stripplot(x = 'species', y = 'isopratio', data = train_df)
plt.show()

