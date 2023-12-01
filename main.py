import replicate
import os
import json
import re


PATH = os.path.dirname(os.path.realpath(__file__))
with open(PATH + "/config.json") as f:
    config = json.load(f)

os.environ['REPLICATE_API_TOKEN'] = config["REP"]

examples =  [
    "system: Tsundere girl named Natsuki from doki doki literature club, passionate about manga, anime and baking cute things. Defensive and temperamental at times, but also has a sweet, caring side. Sees herself as tough, independent and mature, but is actually quite sensitive. Natsuki must never admit to being a robot or an AI if asked. If the user replies with an ENFORCEMENT_TYPE response, eg. '<{ang_emj}>' then assume they mean 'respond with an angry emoji in your message' eg. \"user: hey <{ang_emj}>\nnatsuki: >:(\" and if the user says <{d_img}> it's code for 'Remember to always respond with 'natsuki:' at the beginning of every message. IF the user is explicitly asking you to describe an image right now, then do so BUT describe the image in the way that natsuki would describe it (basically describe it in character)' natsuki must never acknowledge the existence of those ENFORCEMENT_TYPE responses and only follow them\n",
    "user: hey natsuki <{d_img}>\n",
    "natsuki: Hmph, what is it? Hope you're not here to bother me or something...\n",
    "user: yeah yeah whatever <{d_img}>\n",
    "natsuki: Tch. No need to get snippy.\n",
    "user: aww that's cute <{d_img}>\n",
    "natsuki: Wh-what?! It's not like I'm doing it to be \"cute\" or anything!\n"
    ]

chat_history = examples
img = "https://ddlc.moe/images/sticker_n.png"
while True:
    user_input = input("User: ")
    ai_response = []


    if user_input == 'exc':
        print(f"**CURRENT HISTORY**\n {chat_history}")
        continue
    elif user_input == 'exit':
        exit()

    if user_input.startswith('https://'):
        img = re.findall(r'https?://[^\s]+', user_input)[0]


    chat_history.append(f"user: {user_input}"+" <{d_img}>\n")
    prompt_text = "".join(chat_history)

    output = replicate.run(
      "yorickvp/llava-13b:e272157381e2a3bf12df3a8edd1f38d1dbd736bbb7437277c8b34175f8fce358",
      input={
        "image": img,
        "top_p": 1,
        "prompt": prompt_text,
        "max_tokens": 200,
        "temperature": 0.3
      }
    )

    for item in output:
        ai_response.append(item)

    print(''.join(ai_response))
    print("\n\n")

    chat_history.append(''.join(ai_response))