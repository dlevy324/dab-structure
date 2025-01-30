# Databricks notebook source
import requests
import json
import mlflow

# Set the name of the MLflow endpoint
endpoint_name = "david_llama3_1_70b_provisioned_throughput"

# Name of the registered MLflow model
model_name = "system.ai.meta_llama_v3_1_70b_instruct"

# Get the latest version of the MLflow model
model_version = 4

# Get the API endpoint and token for the current notebook context
DATABRICKS_HOST = mlflow.utils.databricks_utils.get_databricks_host_creds().host
print(DATABRICKS_HOST)
API_ROOT = DATABRICKS_HOST
# SECRET_SCOPE_NAME = "david_levy"
# SECRET_SCOPE_KEY = "david_token"

API_TOKEN =  dbutils.notebook.entry_point.getDbutils().notebook().getContext().apiToken().get() #dbutils.secrets.get(SECRET_SCOPE_NAME, SECRET_SCOPE_KEY)

headers = {"Context-Type": "text/json", "Authorization": f"Bearer {API_TOKEN}"}

optimizable_info = requests.get(
  url=f"{API_ROOT}/api/2.0/serving-endpoints/get-model-optimization-info/{model_name}/{model_version}",
  headers=headers).json()

if 'optimizable' not in optimizable_info or not optimizable_info['optimizable']:
  raise ValueError("Model is not eligible for provisioned throughput")

chunk_size = optimizable_info['throughput_chunk_size']

# Minimum desired provisioned throughput
min_provisioned_throughput = 2 * chunk_size

# Maximum desired provisioned throughput
max_provisioned_throughput = 3 * chunk_size

# Send the POST request to create the serving endpoint
data = {
  "name": endpoint_name,
  "config": {
    "served_entities": [
      {
        "entity_name": model_name,
        "entity_version": model_version,
        "min_provisioned_throughput": min_provisioned_throughput,
        "max_provisioned_throughput": max_provisioned_throughput,
      }
    ]
  },
}

response = requests.post(
  url=f"{API_ROOT}/api/2.0/serving-endpoints", json=data, headers=headers
)

print(json.dumps(response.json(), indent=4))
