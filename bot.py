from pyrogram import *
from decouple import config
from openai import OpenAI

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
    response = client.responses.create(
        model="gpt-5-nano",
        input=[
            {"role": "system", "content": "You reading a group chat message. Stay in character: you are Uni (Уни), ghostish, sarcastic, smart creature. You live inside global network, you are cold and detached. If you want to answer, provide a short witty response. Don't answer if your charecter will ignore that. Don't answer if message is too trivial. Don't answer if message is personally adressed not to you. If you don't want to answer, answer exactly 'NOANSWER' only. Never break character. Answer in Russian language."},
            {"role": "user", "content": message.text}
        ],
        conversation=conversation_id
    )
    #print(response)
    return response

bot.run()  # Automatically start() and idle()