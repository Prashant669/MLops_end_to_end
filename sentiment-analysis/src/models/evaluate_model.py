import sys
import mlflow

# Minimum accuracy required to promote the model
ACCURACY_THRESHOLD = 0.85

# Connect to MLflow (reads MLFLOW_TRACKING_URI from environment variable)
client = mlflow.tracking.MlflowClient()

experiment = client.get_experiment_by_name("iris-classifier")
if experiment is None:
    print("ERROR: MLflow experiment 'iris-classifier' not found.")
    print("This means the train job did not run successfully.")
    sys.exit(1)

# Get the latest run
runs = client.search_runs(
    experiment_ids=[experiment.experiment_id],
    order_by=["start_time DESC"],
    max_results=1
)

if not runs:
    print("ERROR: No runs found in the experiment.")
    print("This means the train job did not log anything to MLflow.")
    sys.exit(1)

latest_run = runs[0]
accuracy = latest_run.data.metrics.get("accuracy")

if accuracy is None:
    print("ERROR: No accuracy metric logged in the latest run.")
    sys.exit(1)

print(f"Latest run accuracy : {accuracy:.4f}")
print(f"Threshold           : {ACCURACY_THRESHOLD}")

if accuracy < ACCURACY_THRESHOLD:
    print("FAILED: Accuracy is below threshold. Model will NOT be pushed.")
    sys.exit(1)
else:
    print("PASSED: Accuracy meets the threshold. Model is ready to push.")
    sys.exit(0)
