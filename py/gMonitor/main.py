#!/usr/bin/env python
import http.client
import json
import os
from datetime import datetime, timedelta
import random

CLIENT_ID = "zFY4arMzQn5rf0hRbNbfDKQZff9175aF"
CLIENT_SECRET = "gMKbRit4PrKoJaOj"
REDIRECT_URI = ""
ACCESS_TOKEN = "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJzdWIiOiI0ZjRhNzAwYS04ZDU0LTQ5ZGYtYTg4OS0zOWVhOGQ1MWZmYjIiLCJhdWQiOiJodHRwczovL3NhbmRib3gtYXBpLmRleGNvbS5jb20iLCJzY29wZSI6WyJlZ3YiLCJjYWxpYnJhdGlvbiIsImRldmljZSIsImV2ZW50Iiwic3RhdGlzdGljcyIsIm9mZmxpbmVfYWNjZXNzIl0sImlzcyI6Imh0dHBzOi8vc2FuZGJveC1hcGkuZGV4Y29tLmNvbSIsImV4cCI6MTYzMzY1NjMwMCwiaWF0IjoxNjMzNjQ5MTAwLCJjbGllbnRfaWQiOiJ6Rlk0YXJNelFuNXJmMGhSYk5iZkRLUVpmZjkxNzVhRiJ9.YzqotqLPkVx39XGE9DMNabALXDeMn1gKxZ4QvtzxPxOC8LeJcTXG2a-Zq0owv3HpAYm-VYuDgL_4nBAxCrYfgxFrLl5taFnbevRoTg0tGeaF6fbnzjnSHc7CXVA2d4UT0DAnWaAIdAI1KbQlk2GR4x2Ys1wA4AYgFc5kzve77uwX0rZgi8cNJboF7Z740xST-I_EEXxknA_wzz1bdAL9e52dACx3XTOodrXTjJ5kvIi2TxJvS8tvHtZJUIkFstc-E9LzbgNr4F19GowRHN0JyV7cDJleH_RA6inqWJwTey6B4v4iXH-vGEyRf3iXdiP-BNkQ5ZbkO4eQn-xAGashTQ"
REFRESH_TOKEN = "d43d263d403995be3af5227801833e40"
USER_ID = 'User4'
TOPIC_ID = 'dexcom-topic' #TODO
API_MESSAGE = 'egvs'
LATEST_DATE = "2021-10-02" #Available in dexcom SandBox
numdays = 360
conn = http.client.HTTPSConnection("sandbox-api.dexcom.com")


def get_latest_data(access_token):
  """
     Gets random data from sandbox to emulate real time event pulling (since sandbox data is not updated in realtime).
 """
  result_data = []
  max_attempts = 10
  attempt = 0
  while len(result_data) == 0 and attempt < max_attempts:
    attempt += 1
    dt = get_random_date(LATEST_DATE)
    start_date = dt.strftime('%Y-%m-%dT%H:%M:%S')
    end_date = (dt + timedelta(minutes=15)).strftime('%Y-%m-%dT%H:%M:%S')
    result_data = get_data(access_token, start_date, end_date)

  if len(result_data) == 0:
    print("Error, could not retrieve Sandbox data")
    return

  #Extract Just One message
  message = result_data[-1]

  #Fix the data
  message['systemTime'] = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
  message['displayTime'] = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')

  return message


def monitor_http(request):
  request_json = request.get_json(silent=True)

  user_id = request_json.get("user")
  topic_id = request_json.get("topic")
  message = request_json.get("message")
  return monitor(topic_id, user_id, API_MESSAGE)


def monitor_pubsub(event, context):
  import base64
  if 'data' in event:
    data = base64.b64decode(event['data'])
    print(f'Received message:{data}')

  topic_id = TOPIC_ID
  user_id = USER_ID
  if 'attributes' in event:
    attributes = event['attributes']
    keys = ",".join([x for x in  attributes.keys])
    print(f"Received message attributes: {keys}")
    if 'topic' in attributes:
        topic_id = attributes['topic']
    if 'userId' in attributes:
      user_id = attributes['userId']
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

def get_random_date(end_date: str) -> datetime:
  date_list = [datetime.strptime(end_date, "%Y-%m-%d") - timedelta(days=x) for x in range(numdays)]
  selected_date = date_list[random.randint(0, len(date_list)-1)]
  dt = selected_date + random.random() * timedelta(days=1)

  return dt

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

# def obtain_access_token():
#
#   payload = "client_secret={your_client_secret}&client_id={CLIENT_ID}&code={your_authorization_code}&grant_type=authorization_code&redirect_uri={REDIRECT_URI}"
#   headers = {
#       'content-type': "application/x-www-form-urlencoded",
#       'cache-control': "no-cache"
#   }
#   conn.request("POST", "/v2/oauth2/token", payload, headers)
#   res = conn.getresponse()
#   data = res.read()
#   print(data.decode("utf-8"))

def token_refresh():
  payload = f"client_secret={CLIENT_SECRET}&client_id={CLIENT_ID}&refresh_token={REFRESH_TOKEN}&grant_type=refresh_token&redirect_uri={REDIRECT_URI}"
  headers = {
      'content-type': "application/x-www-form-urlencoded",
      'cache-control': "no-cache"
  }

  conn.request("POST", "/v2/oauth2/token", payload, headers)
  res = conn.getresponse()
  data = res.read()
  data_dict = json.loads(data)
  print(data.decode("utf-8"))
  return data_dict


def get_data_range(access_token):
  headers = {
      'authorization': f"Bearer {access_token}"
  }

  conn.request("GET", "/v2/users/self/dataRange", headers=headers)

  res = conn.getresponse()
  data_object = json.loads(res.read())
  print(json.dumps(data_object, indent=2))

monitor(USER_ID, TOPIC_ID, API_MESSAGE)