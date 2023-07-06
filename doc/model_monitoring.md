# Metrics to monitor in production

## Applicable to almost any ML task

- Service health
- Model performance
- Data quality and integrity
- Data/concept drift

## Applicable to certain ML tasks

- Performance by segment 
- Model bias/fairness
- Outliers (to send to manual review)
- Explainability (eg for recommeder systems)

### Problem: some metrics require batch mode deployment

- Drift detection (to compare "before" and "after" disctibutions)

- Quality metrics (presicion, recall etc)

### Solution: for non-batch deployments use a window function

- Quality metrics: calculate continuously/incrementally

- Statistical tests: use window function (without moving a reference window)

# Monitoring implementation scheme

The idea is to create the monitoring system on top of the logs. 

This way it doesn't matter the mode the underlying model is deployed cause we can always work on the logs in batch mode.

---

# Practice

1. Install additional libs `evidently` and `psycopg` (that are added to [requirements.txt](../requirements.txt)) in the existing environment 

1. First we run [baseline_model_nyc_taxi_data.ipynb](../monitoring/baseline_model_nyc_taxi_data.ipynb) to download the data and train and save the model

1. Spin up grafana and co by running
    ```bash
    docker compose up
    ```
1. Run [dummy_metrics_calculation.py](../monitoring/dummy_metrics_calculation.py) to see how dummy metrics to check out grafana interface

1. Run [evidently_metrics_calculation.py](../monitoring/evidently_metrics_calculation.py) to fill the dashboard with real metrics


To save model's json between docker runs do the following:

1. Create a dashboard 
2. Go to Dashboard settings
3. Go to JSON model tab
4. Copy json and save it in a file in the /dashboards directory eg in [../monitoring/dashboards/)](../monitoring/dashboards/) that will then be picked up be the grafana configuration described in [grafana_dashboards.yaml](../monitoring/config/grafana_dashboards.yaml)