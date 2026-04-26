import pandas as pd 
import pickle
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
X_test =pd.read_csv("2. Machine Learning Model/X_test.csv")
X_train=pd.read_csv("2. Machine Learning Model/X_train.csv")
y_test=pd.read_csv("2. Machine Learning Model/y_test.csv").squeeze()
y_train= pd.read_csv("2. Machine Learning Model/y_train.csv").squeeze()
classifier = RandomForestClassifier(n_estimators=100, random_state=42)
classifier.fit(X_train, y_train)
y_pred = classifier.predict(X_test)
print("Accuracy:", accuracy_score(y_test,y_pred))
filename= '2. Machine Learning Model/model.pkl'
with open (filename,'wb') as file:
  pickle.dump(classifier,file)