import pandas as pb
from sklearn.tree import DecisionTreeClassifier
import joblib
from sklearn import tree
df = pb.read_csv("music.csv")
X=df.drop(columns=["genre"])
y=df["genre"]
model=DecisionTreeClassifier()
model.fit(X, y)
model.predict()
