import os
import openai
from aiogram import Bot, Dispatcher, executor, types
from keep_alive import keep_alive

bot = Bot(token=os.getenv("tg_token"))
dp = Dispatcher(bot)

openai.api_key = os.getenv("ai_token")

keep_alive()


@dp.message_handler(commands=['start', 'help'])
async def welcome(message: types.Message):
  await message.reply('Hello! Im GPT chat bot. Ask me something')


@dp.message_handler()
async def gpt(message: types.Message):

  ######### option: using Chat API - chat completions
  # https://platform.openai.com/docs/api-reference/chat

  # response = openai.ChatCompletion.create(
  # model="gpt-3.5-turbo",
  # messages=[
  # {"role": "user", "content": "How does a computer work?"},
  # {"role": "system", "content": "A computer works by processing data through its various components."},
  # {"role": "user", "content": "Can you explain more about these components?"},
  # ],

  # generated_text = response.choices[0].message.content


  ######### option: using Completions API - create completions
  # https://platform.openai.com/docs/api-reference/completions
  
  response = openai.Completion.create(
    model="gpt-3.5-turbo-instruct",
    prompt=message.text,
    temperature=0.5,
    max_tokens=1024,
    top_p=1,
    frequency_penalty=0.0,
    presence_penalty=0.0)

  generated_text = response.choices[0].text

  await message.reply(generated_text)

if __name__ == "__main__":
  executor.start_polling(dp)
