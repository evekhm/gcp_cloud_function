#!/usr/bin/env python
import http.client
import json
import os
import datetime
import requests

CLIENT_ID = "zFY4arMzQn5rf0hRbNbfDKQZff9175aF"
CLIENT_SECRET = "gMKbRit4PrKoJaOj"
REDIRECT_URI = ""
ACCESS_TOKEN = "eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIyM0I5RkwiLCJzdWIiOiI5R0hHTlMiLCJpc3MiOiJGaXRiaXQiLCJ0eXAiOiJhY2Nlc3NfdG9rZW4iLCJzY29wZXMiOiJyc29jIHJhY3QgcnNldCBybG9jIHJ3ZWkgcmhyIHJudXQgcnBybyByc2xlIiwiZXhwIjoxNjMzNDY0MzU3LCJpYXQiOjE2MzI4NTk2ODl9.KZQP1F5xr4TZoQhYAtETnqWKqF-Yg0FE3An806vmwkM"
REFRESH_TOKEN = "d43d263d403995be3af5227801833e40"
API_MESSAGE = 'egvs'
conn = http.client.HTTPSConnection("sandbox-api.dexcom.com")


def fitbit_pubsub(event, context):
  import base64
  if 'data' in event:
    data = base64.b64decode(event['data'])
    print(f'Received message:{data}')

  user_id = None
  topic_id = None
  if 'attributes' in event:
    attributes = event['attributes']
    print(f"Received message with attributes: {attributes}")
    if 'topic' in attributes:
        topic_id = attributes['topic']
    if 'userId' in attributes:
      user_id = attributes['userId']
    if not topic_id:
      return f"Aborted: userId is unspecified"
    if not user_id:
      return f"Aborted: topc is unspecified"

    return monitor(user_id, topic_id, API_MESSAGE)


def monitor(user_id, topic_id, api_message):
  project_id = os.getenv('GCP_PROJECT')
  info = token_refresh()
  access_token = info['access_token']
  return send_data(project_id, topic_id, access_token, user_id, api_message)


def send_data(project_id, topic_id, access_token, user_id, api_name):
  data = get_latest_data(access_token)
  message = json.dumps(data)
  message_json = json.dumps({'message': message,
                             'userId': user_id,
                             'type': api_name
                             })

  return publish_message(project_id, topic_id, message_json.encode('utf-8'))


def publish_message(project_id: str, topic_id: str, data: bytes):
  """Publishes multiple messages to a Pub/Sub topic."""
  # [START pubsub_quickstart_publisher]
  # [START pubsub_publish]
  from google.cloud import pubsub_v1


  publisher = pubsub_v1.PublisherClient()
  # The `topic_path` method creates a fully qualified identifier
  # in the form `projects/{project_id}/topics/{topic_id}`
  topic_path = publisher.topic_path(project_id, topic_id)

  try:
    print(f'Publishing {data} to {topic_path}')
    future = publisher.publish(topic_path, data=data)
    result = f"Published messages to {topic_path}. Result: " + future.result()
    print(result)
    return result

  except Exception as e:
    print("Could not publish a message: ", e)
    return e, 500


  # [END pubsub_quickstart_publisher]
  # [END pubsub_publish]

def get_data(access_token: str, start_date: str, end_date: str) -> []:
  headers = {
      'authorization': f"Bearer {access_token}"
  }

  try:
    conn.request("GET", f"/v2/users/self/egvs?startDate={start_date}&endDate={end_date}", headers=headers)
    res = conn.getresponse()
    if res.status == 401:
      print("Token needs refreshment")
    elif res.status == 200:
      data_object = json.loads(res.read())
      if API_MESSAGE in data_object:
        return data_object[API_MESSAGE]
      print(f"Error, {API_MESSAGE} field was missing")
    else:
      print("Error, returned status:", res.status)
  except http.client.HTTPException as err:
    print('Exception', err)

  return []

def fitbit_call_pubsub():
    day_range_length = 5
    start_date = "2021-06-25"
    end_date = "2021-06-27"

    now = datetime.datetime.now()
    current_time = now.strftime("%Y-%m-%d")
    print("Current Time =", current_time)
    #yesterday = datetime.today() - timedelta(days = 1 )
    date_N_days_ago = datetime.datetime.now() - datetime.timedelta(days=5)
    n_days_ago_time = date_N_days_ago.strftime("%Y-%m-%d")
    print("5 days ago Time =", n_days_ago_time)

    #Update your start and end dates here in yyyy-mm-dd format
    #start_date = "2021-09-24"
    start_date = n_days_ago_time
    start = datetime.datetime.strptime(start_date, "%Y-%m-%d")
    end = datetime.datetime.strptime(end_date, "%Y-%m-%d")
    current = datetime.datetime.strptime(current_time, "%Y-%m-%d")
    end = current

    date_array = (start + datetime.timedelta(days=x) for x in range(0, (end-start).days+1))

    day_list = []
    for date_object in date_array:
      day_list.append(date_object.strftime("%Y-%m-%d"))

    print("day range : ",day_list)

    header = {'Authorization': 'Bearer {}'.format(ACCESS_TOKEN)}

    for single_day in day_list:
      response = requests.get("https://api.fitbit.com/1/user/-/activities/heart/date/"+ single_day +"/1d/1min/time/00:00/23:59.json", headers=header).json()
    try:
      print(response)
      print(response['activities-heart-intraday']['dataset'])
      # df = pd.DataFrame(response['activities-heart-intraday']['dataset'])
      # date = pd.Timestamp(single_day).strftime('%Y-%m-%d')
      # df = df.set_index(pd.to_datetime(date + ' ' + df['time'].astype(str)))
      # #print(df)
      # df_all = df_all.append(df, sort=True)
    except KeyError as e:
      print("No data for the given date")

fitbit_call_pubsub()