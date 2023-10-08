import os
import pandas as pd

!tar -xzvf '/content/drive/MyDrive/data/aclImdb_v1.tar.gz'

train_neg = '/content/aclImdb/train/neg'
train_pos = '/content/aclImdb/train/pos'
test_neg = '/content/aclImdb/test/neg'
test_pos = '/content/aclImdb/test/pos'

def get_csv(folder_path):
  data = []

  # Iterate over all files in the folder
  for filename in os.listdir(folder_path):
    if filename.endswith('.txt'):
      with open(os.path.join(folder_path, filename), 'r') as file:
        content = file.read()

        # Extract rating from the filename
        rating = filename.split('_')[1].replace('.txt', '')

        data.append({'filename': filename, 'content': content, 'rating': rating})
  df2 = pd.DataFrame(data)

  return df2

df_train = get_csv(train_pos)
df_train2 = get_csv(train_neg)

df_test = get_csv(test_pos)
df_test2 = get_csv(test_neg)

train = pd.concat([df_train,df_train2])
test= pd.concat([df_test,df_test2])
