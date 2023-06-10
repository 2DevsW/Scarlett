import requests
import json


def SendToCarter(sentence, User, APIkey):
  response = requests.post("https://api.carterlabs.ai/chat",
                           headers={"Content-Type": "application/json"},
                           data=json.dumps({
                             "text": f"{sentence}",
                             "key": f"{APIkey}",
                             "playerId": f"{User}"
                           }))

  RawResponse = response.json()
  Response = RawResponse["output"]
  FullResponse = Response["text"]
  ResponseOutput = FullResponse

  ResponseOutput = ResponseOutput.replace("Unknown person", User)
  ResponseOutput = ResponseOutput.replace("Unknown Person", User)
  ResponseOutput = ResponseOutput.replace("unknown person", User)

  f = open("ResponseOutput.txt", "w+")
  f.write(f"{ResponseOutput}")
  f.close()
