import pandas as pd
import seaborn as sns
import matplotlib as mpl
import matplotlib.pyplot as plt
from sklearn import decomposition
from random import shuffle
from mpl_toolkits.mplot3d import Axes3D

seperator = '\n-------------------------\n'

ratios_df = pd.read_csv('ratiostest.csv')
train_df = pd.read_csv('Data/train.csv')
# train_df = train_df.loc[:, ['id', 'species']]

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

# Plot species on x-axis and ratios on y-axis. Categories appear in the order we specified above.
# Therefore, they appear in order of increasing mean ratio.

print(seperator, 'Training Data set after attaching ordering\n', train_df[:10])
ax = sns.stripplot(x = 'species', y = 'isopratio', data = train_df)
plt.show()

# Now do PCA on texturedata

print(seperator, 'Look at some texture columns')
print(train_df.loc[:10, ['texture1', 'texture2']] )
texturecollist = ['texture' + str(i+1) for i in range(64)]

# Combine texture columns into a column of lists 

train_df['texturevect'] = train_df[texturecollist].values.tolist()
print(train_df.loc[:10, 'texturevect'])

# Now do PCA decomposition on textures
pca = decomposition.PCA(n_components = 2)
texture_matrix = train_df[texturecollist].values
pca.fit( texture_matrix )
texture_matrix = pca.transform( texture_matrix )
print(texture_matrix[:3] )
for i in range(len(texture_matrix[0,:])):
    colname = 'texture_pca' + str(i+1)
    train_df[colname] = texture_matrix[:, i]

print(seperator, 'Result of pca analysis of textures = \n', train_df.loc[:10, ['texture_pca1', 'texture_pca2']] )

# Randomly shuffle order of species
shuffle(speciesorder)
print('New random order of species is\n', speciesorder[:10] )
train_df['species'] = train_df['species'].cat.reorder_categories(speciesorder, ordered = True)
train_df.sort_values(by = 'species')

colordict = {}
for i in range(len(speciesorder)):
    colordict[speciesorder[i]] = i

plotcolors = train_df['species'].apply(lambda x: colordict[x]) 
fig2 = plt.figure()
ax2 = fig2.add_subplot(111, projection = '3d' )
ax2.scatter(train_df['isopratio'], train_df['texture_pca1'], train_df['texture_pca2'], c = plotcolors)
plt.show()

# sns.set()
plt.close()
plot_df = train_df[['species', 'isopratio', 'texture_pca1', 'texture_pca2']]
plot_df.sort_values(by = 'species')
ax = sns.pairplot(plot_df, hue = 'species')
plt.show()
