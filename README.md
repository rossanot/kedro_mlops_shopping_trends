# **Prediction of a Customer Subscription Status**
## **Business Case**
Use case: Predict a customer subscription status. Predicting the subscription status of a customer would allow to provide customized offers/products that could eventually lead to the subscription of the customer.

Herein, I explore the use of Kedro, mlflow, and Kaggle in the creation of a streamlined ML framework. The pipeline consumes a Kaggle dataset via Kaggle's API service and serves a classification model. An overview of the Kedro pipeline is provided below.

![Kedro (intermediate) data layer pipeline](./docs/figures/kedro_intermediate_pipeline_clear_01.png)

## **Project Highlights**
- **Target**: `Subscription Status`
- Problem: Bimodal classification
- Training/Validation/Test dataset size:
    - training: 0.8
    - test: 0.15
    - validation: 0.05
- Implementation of an ML pipeline using Kedro
- Integration of Kaggle API into a Kedro pipeline
- The project includes the following pipeline items:
    - `eda`
    - `data_acquisition` using Kaggle API.
    - `data_processing`:
        - This steps explores the creatio of three different data layers called `intermediate`, `primary`, and `feature`.
    - `model_training`
        - baseline using Decision Tree
        - implemented algorithms: 
        ```
        'Decision Tree': DecisionTreeClassifier,
        'XGBoost': XGBClassifier,
        'Logistic Regression': LogisticRegression,
        'KNN': KNeighborsClassifier,
        'Naive Bayes': GaussianNB,
        'SVM': svm
        ```
    - `model_validation`

## **Running and Configuring the Pipeline**
### **Model Training Configuration**
```
model_training:
  classifier: Decision Tree
  dataset_stage: primary
  kfold: True
  hyperparams:
    criterion: ['gini', 'entropy', 'log_loss']
    splitter: ['best', 'random']
    max_depth: [2, 4, 8]
```

### **Running the Pipeline**
- The entire pipeline can be run using the following command

```
kedro run
```

- The artifacts, including metrics, per each run are tracked using mlflow. To specify the name of the run, for example, when a specific data layer is consumed:

```
kedro run --params mlflow_run_name="my-awesome-name"
```
    
- Alternativetely, each pipeline can be run separately as:

```
kedro run --pipeline pipeline_item
```

where `pipeline_item` can be `data_acquisition`, `data_processing`, `eda`, `model_training`, `model_validation`

- Finally, a Streamlit dashboard is implemented to explore the data interactivelly. The dashboard is invoked through:

```
streamlit run streamlit-entry.py
```

![Subscription Status Distribution](./docs/figures/streamlit_dashboard_01.png)

> [!NOTE]: `03_primary` and `04_feature` data sets do not necessarily add value to the data science pipeline, however, they are included in the pipeline with the objective of exploring the use of those data layers. Here, the ML pipelines only use the `02_intermediate` dataset.

- MLflow for `model tracking`
    ```
    mlflow ui --backend-store-uri ./mlflow_runs
    ```
    > [!NOTE]
    > The `./mlflow_runs` directory is created upon `kedro run` execution.

## **Notes about installation**
Should you have any problems installing `kedro[pandas]` through `pip install kedro[pandas]` try performing separate type level instalaltions, e.g., 

```
pip install kedro-datasets[pandas.ParquetDataset]
pip install kedro-datasets[matplotlib.MatplotlibWriter]
```

> [!IMPORTANT]  
> Partial migration from Kedro 0.18.14 to 0.19.8 was done, meaning that some capabilities might need further update.

## Kaggle API configuration
Add API Kaggle token to `./conf/local/credentials.yml` as follows:
```
kaggle:
      KAGGLE_USERNAME: my_kaggle_username
      KAGGLE_KEY: my_kaggle_key
```

The `KAGGLE_KEY` refers to your Kaggle token. How to create a Kaggle token is described [here](https://www.kaggle.com/docs/api#getting-started-installation-&-authentication).

## MLflow UI
```
mlflow ui --backend-store-uri ./mlflow_runs
```
> [!NOTE]
> The `./mlflow_runs` directory is created upon `kedro run` execution.

## 