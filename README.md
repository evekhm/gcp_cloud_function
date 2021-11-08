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
- ...


## STEPS

Checkput GitHub Code:
```console
git clone git@github.com:evekhm/gcp.git
```

```console
cd gcp bin
```

### Prepare Project


```console
gcloud auth login
```

#### 1. Setup Enviroment Variables for GCP Project creation and deployment:
```console
export ACCOUNT='<account>'
export BILLING='<billing_id>'
export REGION='us-west1'
export ZONE='us-west1-a'
```
Argolis BILLING='016EA1-F95FE4-01826A'

<p>Example:

```console
export ACCOUNT='admin@myaccount.altostrat.com'
export BILLING='016EA1-F95FE4-01826A'
export REGION='us-west1'
export ZONE='us-west1-a'
```


#### 2. Create and activate dedicated config

Following step creates and activates dedicated config called **dexcom-demo**.<br>
Enter *PROJECT_ID* - a unique new Project ID to be created.

```console
./init <PROJECT_ID>
```

### Run Deployment
```console
./run
```

### Query BigTable
After few minutes, data been collected and streamlined into BigQuery:
```console
./query
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
Following command will unset previously set Enviroment Variables (including BILLING, REGION, ZONE):

```console
./UNSET
```

Following command will delete previously created resources. Project itself will not be deleted.
```console
./clean
```