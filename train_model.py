from pathlib import Path
import json,joblib,pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score,precision_score,recall_score,f1_score,confusion_matrix
from modules.data_processing import FEATURES,CATEGORICAL,NUMERIC,validate
root=Path(__file__).resolve().parent
df=validate(pd.read_csv(root/"data/student_data.csv"))
df=df[df.Status.astype(str).str.lower().eq("completed") & df.SLA_Breached.isin([0,1])].copy()
X,y=df[FEATURES],df.SLA_Breached.astype(int)
pre=ColumnTransformer([("cat",Pipeline([("imp",SimpleImputer(strategy="most_frequent")),("ohe",OneHotEncoder(handle_unknown="ignore"))]),CATEGORICAL),("num",SimpleImputer(strategy="median"),NUMERIC)])
model=Pipeline([("prep",pre),("tree",DecisionTreeClassifier(max_depth=5,min_samples_leaf=5,random_state=42))])
Xtr,Xte,ytr,yte=train_test_split(X,y,test_size=.2,stratify=y,random_state=42)
model.fit(Xtr,ytr); p=model.predict(Xte)
metrics={"accuracy":accuracy_score(yte,p),"precision":precision_score(yte,p,zero_division=0),"recall":recall_score(yte,p,zero_division=0),"f1":f1_score(yte,p,zero_division=0),"confusion_matrix":confusion_matrix(yte,p).tolist(),"training_rows":len(Xtr),"test_rows":len(Xte)}
joblib.dump(model,root/"models/student_model.pkl")
(root/"models/metrics.json").write_text(json.dumps(metrics,indent=2))
print(json.dumps(metrics,indent=2))
