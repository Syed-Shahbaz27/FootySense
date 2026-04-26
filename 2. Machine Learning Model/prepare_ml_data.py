# Use pandas for data analysis
import pandas as pd
from sklearn.model_selection import train_test_split
# Import or read the csv file 
df = pd.read_csv("2. Machine Learning Model/epl_final.csv")
# Prints first five rows 
print(df.head())
print(df.columns.tolist())
print(df.shape)
print(df['FullTimeResult'].value_counts())

# Adding features
features = ['HomeShots','AwayShots','HomeShotsOnTarget','AwayShotsOnTarget','HomeCorners','AwayCorners']
target = 'FullTimeResult'

X = df[features]
y = df[target]
print(X.shape)
print(y.shape)

X_train,X_test, y_train, y_test = train_test_split(X,y, test_size = 0.20, random_state= 42)
print(X_test.shape)
print(X_train.shape)
X_train.to_csv("X_train.csv", index =False)
X_test.to_csv("X_test.csv", index =False)
y_train.to_csv("y_train.csv", index =False)
y_test.to_csv("y_test.csv", index =False)
print("The Data and progress has beens saved successfully")

