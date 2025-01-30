# Databricks notebook source
# MAGIC %pip install -qq mlflow==2.16.1

# COMMAND ----------

import requests
import json
import mlflow

# COMMAND ----------

# Set your Databricks workspace URL and personal access token
workspace_url = mlflow.utils.databricks_utils.get_databricks_host_creds().host
print(workspace_url)
token = dbutils.notebook.entry_point.getDbutils().notebook().getContext().apiToken().get() # os.getenv("DATABRICKS_TOKEN")

# API endpoint for creating a warehouse
api_endpoint = f"{workspace_url}/api/2.0/sql/warehouses"

# Define the warehouse configuration
warehouse_config = {
    "name": "david_test_Warehouse",
    "cluster_size": "2X-Small",
    "min_num_clusters": 1,
    "max_num_clusters": 1,
    "auto_stop_mins": 20,
    "enable_photon": True,
    "warehouse_type": "PRO",
    "spot_instance_policy": "COST_OPTIMIZED",
    "channel": {
        "name": "CURRENT"
    }
}

# Set up the request headers
headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json"
}

# Send the POST request to create the warehouse
response = requests.post(api_endpoint, headers=headers, data=json.dumps(warehouse_config))

# Check the response
if response.status_code == 200:
    print("Warehouse created successfully!")
    print(json.dumps(response.json(), indent=2))
else:
    print(f"Failed to create warehouse. Status code: {response.status_code}")
    print(response.text)
