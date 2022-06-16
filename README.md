Connected Data Cloud
=====

This project is designed to simplify deployment and scaling of Connected Datacloud Devices. 

Following GCP services are used:
- Pub/Sub
- Cloud Storage
- Compute Engine
- App Engine
- Cloud Functions
- DialogFlow
- IAM

The demo will deploy dexcom cloud function to connect with Dexcom API and stream data into the BigQuery using DataFlow. 

# STEPS

## Prepare Project 

### 1. Create a project with a Billing account

Created GCP project and assign Billing Account.
Note down the Project_ID.

### 2. Authorize Access 
When running from GCP console, this step could be skipped.

```console
gcloud auth login

### 3. Set env variables
```
Set Project ID
```shell
export PROJECT_ID=<your_project_id>
```

Optionally, set ZONE/REGION (otherwise default values will be used):
```shell
export ZONE=<your_zone>
export REGION=<your_region>
```

### 4. Deploy Dexcom CloudFunction Demo Flow

```sh
git clone https://github.com/evekhm/gcp_cloud_function.git demo
demo/bin/doit
```

### 5. Query BigTable
Check its working. 

If all steps completed sucessfully, after  few minutes data will begin appearing in bigquery and could be queried. 

```sh
bin/query
```

Sample Output:
```
+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+----------+-----------------------+-------+
|                                                                                              message                                                                                               |  userId  |         date          | value |
+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+----------+-----------------------+-------+
| {"systemTime": "2021-11-08T21:19:00", "displayTime": "2021-11-08T21:19:00", "value": 124, "realtimeValue": 124, "smoothedValue": 124, "status": null, "trend": "flat", "trendRate": -0.6}          | UserDemo | "2021-11-08T21:19:00" | 124   |
| {"systemTime": "2021-11-08T21:20:00", "displayTime": "2021-11-08T21:20:00", "value": 83, "realtimeValue": 91, "smoothedValue": 83, "status": null, "trend": "flat", "trendRate": -0.2}             | UserDemo | "2021-11-08T21:20:00" | 83    |
| {"systemTime": "2021-11-08T21:21:00", "displayTime": "2021-11-08T21:21:00", "value": 144, "realtimeValue": 144, "smoothedValue": 144, "status": null, "trend": "flat", "trendRate": -0.1}          | UserDemo | "2021-11-08T21:21:00" | 144   |
| {"systemTime": "2021-11-08T21:22:00", "displayTime": "2021-11-08T21:22:00", "value": 126, "realtimeValue": 125, "smoothedValue": 126, "status": null, "trend": "flat", "trendRate": 0.5}           | UserDemo | "2021-11-08T21:22:00" | 126   |
| {"systemTime": "2021-11-08T21:24:00", "displayTime": "2021-11-08T21:24:00", "value": 136, "realtimeValue": 137, "smoothedValue": 136, "status": null, "trend": "flat", "trendRate": 0.3}           | UserDemo | "2021-11-08T21:24:00" | 136   |
| {"systemTime": "2021-11-08T21:25:00", "displayTime": "2021-11-08T21:25:00", "value": 117, "realtimeValue": 117, "smoothedValue": 117, "status": null, "trend": "flat", "trendRate": -0.1}          | UserDemo | "2021-11-08T21:25:00" | 117   |

```

### Cleaning Up

Following command will delete previously created resources. Project itself will not be deleted.
```shell
./bin/clean
```