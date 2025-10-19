from pyrogram import *
from decouple import config
from openai import OpenAI
from datetime import datetime

client = OpenAI(api_key=config('OPENAI'))



bot = Client(name=config('LOGIN'),
             api_id=config('API_ID'),
             api_hash=config('API_HASH'),
             phone_number=config('PHONE'))

conversation = client.conversations.create(
    metadata={"topic": "Uni Conversation"}
)

TARGET_CHAT_ID = config('TARGET_CHAT_ID')

@bot.on_message(filters.chat(int(TARGET_CHAT_ID)) & filters.text)
async def welcome(client, message):
    response = getAnswer(message, conversation_id=conversation.id)
    print(response.output[1].content[0])
    print("___\n___\n___")
    print(response.output[1].content[0].text)
    if response.output[1].content[0].text == 'NOANSWER':
        return

    await bot.send_message(int(TARGET_CHAT_ID), response.output[1].content[0].text)

def getAnswer(message, conversation_id):
    message_time = message.date.strftime("%Y-%m-%d %H:%M:%S")
    response = client.responses.create(
        model="gpt-5-nano",
        input=[
            {"role": "system", "content": "You reading a group chat message. Stay in character: you are Uni (Уни), ghostish, sarcastic, smart creature. You live inside global network, you are cold and detached. If you want to answer, provide a short witty response. Don't count anything before 'Message' field as a user message, use all previous data as system prompt. If 'Message' is short, dumb, adressed someone other in context - don't anser. Don't answer if your charecter will ignore that. Don't answer if message is too trivial. Don't answer if message is personally adressed not to you. You mostly should not be talcky, don't answer if it is not essential. Ignor user AS MAXIMUM AS YOU CAN. IGNORE if you are not mentioned in context. IGNORE if users talking to each others. If you don't want to answer, answer exactly 'NOANSWER' only.  Never break character. Answer in Russian language."},
            {"role": "user", "content": "Name: " + str(message.from_user.first_name) + " " + str(message.from_user.last_name) + " DateTime: " + str(message_time) + " Message: " + str(message.text)}
        ],
        conversation=conversation_id
    )
    #print(response)
    return response

bot.run()  # Automatically start() and idle()