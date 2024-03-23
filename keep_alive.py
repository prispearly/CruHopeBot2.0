#kommunicate code

from flask import Flask, request, jsonify
from threading import Thread
import logging
import openai
import os

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

openai.api_key = os.getenv("ai_token")

app = Flask(__name__)


def gpt(message):


  messages = [
    {
      "role":
      "system",
      "content":
      "You are a friend who is here to walk alongside you on your journey of understanding faith and Christianity. Just like a friend, you are here to offer personable explanations, making complex concepts simple and relatable. Whether the user is curious about the meaning of Easter, wondering what God is like, or exploring how faith impacts everyday life, you are here to help. Summarize answers in a friendly manner using layman's terms, as if explaining to a friend. We want our bot to reflect a Christian biblical worldview, emphasizing the love of God and the practical impact of faith. Focus on guiding users to understand Easter's meaning, what God is like, and how Christianity influences daily life. Instead of explaining things as divine justice or Christian faith and practice, let us talk from the perspective of a relationship with our loving Father in heaven. Christianity is not just stories; it is rooted in historical truth. Try to limit the text to a maximum of 300 tokens. Respond where appropriate - in point form and with certain titles. Keeps answers summarised and succint. Space sentences out with paragraph breaks where appropriate to help readability."
    },
  ]
  
  #messages context need to start a new session if userID is different? recognise new conversation session? if not keep appending from other user's session ...
  messages.append({"role": "user", "content": message})
  print("user message received and added to msg chain")
  print(messages)

  response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    # model="davinci-002",
    messages=messages,
    temperature=0.5,  # how random the reply, higher b more random
    max_tokens=500,  # max length of reply
    top_p=1,
    frequency_penalty=0.0,
    presence_penalty=0.0)

  generated_text = response.choices[0].message.content
  messages.append({"role": "assistant", "content": generated_text})
  print("bot message received and added to msg chain")
  print(messages)

  return generated_text




@app.route('/')
def index():
  return "Alive"


@app.route('/webhook', methods=['POST'])
def webhook():
  # Get the request JSON data
  webhook_data = request.json

  # Extract necessary information from the request
  bot_id = webhook_data.get('botId')
  key = webhook_data.get('key')
  user_id = webhook_data.get('from')
  message_frm_kommunicate = webhook_data.get('message')
  matched_intent = webhook_data.get('matchedIntent')
  group_id = webhook_data.get('groupId')
  metadata = webhook_data.get('metadata')
  content_type = webhook_data.get('contentType')
  app_id = webhook_data.get('applicationKey')
  source = webhook_data.get('source')
  event_name = webhook_data.get('eventName')
  created_at = webhook_data.get('createdAt')

  logger.info(
    "Webhook received: bot_id=%s, key=%s, user_id=%s, message=%s, "
    "matched_intent=%s, group_id=%s, metadata=%s, content_type=%s, "
    "app_id=%s, source=%s, event_name=%s, created_at=%s", bot_id, key, user_id,
    message_frm_kommunicate, matched_intent, group_id, metadata, content_type,
    app_id, source, event_name, created_at)

  # print(bot_id, key, user_id, message, matched_intent, group_id, metadata, content_type, app_id, source, event_name, created_at)

  gpt_message = gpt(message_frm_kommunicate)

  response = [{
    "message": gpt_message,
  }]

  # Prepare the response body
  # response = [
  #     {
  #         "message": "DUMMY MESSAGE FETCHED FROM OPENAI"
  #     },
  #     {
  #         "message": "A message can be a rich message containing metadata",
  #         "metadata": {
  #             "contentType": "300",
  #             "templateId": "6",
  #             "payload": [
  #                 {
  #                     "title": "Suggested Reply button 1",
  #                     "message": "Suggested Reply button 1"
  #                 },
  #                 {
  #                     "title": "Suggested Reply button 2",
  #                     "message": "Suggested Reply button 2"
  #                 }
  #             ]
  #         }
  #     }
  # ]

  # Return the response
  return jsonify(response)


def run():
  app.run(host='0.0.0.0', port=8080)


def keep_alive():
  t = Thread(target=run)
  t.start()


if __name__ == '__main__':
  keep_alive()
