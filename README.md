# dab-structure




### **Setup**
1. Clone the repository and navigate to the backend:
    
2. navigate to the root of the repo and run:
    ```
    databricks bundle validate
    ```

3. deploy the bundle to the target environment:
    ```
    databricks bundle deploy
    ```

Currently i grab credentials from the notebook context, but we could also use parameters to pass in the credentials, i have an example of that in the DAB.