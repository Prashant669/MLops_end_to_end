import mlflow
import mlflow.sklearn
import sys
import joblib
import os
import pandas as pd
from pathlib import Path
from sklearn.datasets import load_iris
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from helper import clean_text, tfidf

# Load data

data_path = sys.argv[1]
model_path = sys.argv[2]
tfidf_path = sys.argv[3]

df = pd.read_csv(data_path)  ### load data

df["sentiment"]=df['sentiment'].map({
    'positive':1,
    'negative':0
})

x=df['review']
y=df['sentiment']

x_train,x_test,y_train,y_test=train_test_split(
    x,y,
    test_size=0.2,
    random_state=42
)

x_train=x_train.apply(clean_text)
x_test=x_test.apply(clean_text)

x_train_tfidf=tfidf.fit_transform(x_train)
x_test_tfidf=tfidf.transform(x_test)


# Set experiment name
mlflow.set_experiment("iris-classifier")


# Read and increment version
version_file = Path.cwd().as_posix() + '/docs/version.txt'
# version_file = "version.txt"
if os.path.exists(version_file):
    with open(version_file, "r") as f:
        version = int(f.read().strip()) + 1
else:
    version = 1

# Save updated version
with open(version_file, "w") as f:
    f.write(str(version))

model_name = f"random_forest_v{version}"

# Start tracking
with mlflow.start_run():

    # 1. Log your hyperparameters
    n_estimators = 300
    max_depth = 5
    mlflow.log_param("n_estimators", n_estimators)
    mlflow.log_param("max_depth", max_depth)

    # 2. Train your model
    model = RandomForestClassifier(n_estimators=n_estimators, max_depth=max_depth)
    model.fit(x_train_tfidf, y_train)

    # 3. Evaluate
    predictions = model.predict(x_test_tfidf)
    accuracy = accuracy_score(y_test, predictions)

    # 4. Log the result
    mlflow.log_metric("accuracy", accuracy)

    # 5. Save the model
    mlflow.sklearn.log_model(model, model_name)

    joblib.dump(model,model_path)
    joblib.dump(tfidf,tfidf_path)



    print(f"Accuracy: {accuracy:.2f}")