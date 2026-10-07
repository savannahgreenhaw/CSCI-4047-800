import discord
import os 
from dotenv import load_dotenv

load_dotenv()

token = os.getenv("TOKEN")

if token is None:
    raise Exception("Discord Token doesn't exist.")

# Intents
intents = discord.Intents.default()
intents.message_content = True # bot can read what people type in chat
intents.members = True # bot can see members and role info

bot = discord.Client(intents=intents) # creats the bots and tells it to use the intents we set up

player_points = {}

##### EVENTS #####
@bot.event
async def on_ready(): # When bot connects to server
    print(f"The bot is online as {bot.user}")

@bot.event
async def on_message(message): # When a message is sent that the bot can read it will send:
    print("---------------------------------------")
    print("Message Received") # Incase it fails
    print("Author:", message.author) # Who sent the message
    print("Author ID:", message.author.id) # This is important for later when we tell the bot to only read messages from the wordle game id
    print("Content:", message.content) # What did it say
    print("---------------------------------------")
# this next stuff is because the number of the wordle being played is in an image so the bot wouldnt be able to read it normally
# so all this is basically to check what the image is so no matter what kind it is the bot should be able to read it even tho its not text.
    print(" Attachments:")
    for attachments in message.attachments:
        print(" File:", attachments.filename)
        print(" URL:",  attachments.url)

    print(" Embeds:")
    for embed in message.embeds:
        print(" Title:",         embed.title)
        print(" Description:",   embed.description)
        print(" Type:",          embed.type)
        print(" URL:",           embed.image.url if embed.image else None) # helps it not crash if theres no image

    print(" Replying to:" , message.reference.message_id if message.reference else None)

    print(" Mentions:")
    for user in message.mentions:
        print(" Mentioned:", user, "| ID:", user.id)

    print("---------------------------------------")
    print("---------------------------------------")

# We cant make wordle send a message whenever we want so this will be fake wordle messages for testing
    if message.content.startswith("!wordletest"):
        result = message.content.split()[1] 
# bassically with this if a message is sent with !wordletest at the front then followed by whatever 
# it will take that second part and store it as the result
# so "!wordletest 5/6" becomes result = 5/6
        if result == "X/6":  # failure
            attempts = 0
        else:
            attempts = int(result[0])

        print("TEST WORDLE DETECTED")
        print("Result:", result)
        print("Attepmts taken:", attempts)

        # Points system
        points = {
            1: +40,
            2: +35,
            3: +30,
            4: +25,
            5: +20,
            6: +15,
            0: -10,
        }

        earned_points = points[attempts]
        print("Points earned:", earned_points)



# adding points to the players total
# ok so this is fine for the practice but once the bot shuts down and starts again all the points saved will be earased
# So we will need to transfer this to SQLite to have a permanent database
        user_id = message.author.id

        if user_id not in player_points:
            player_points[user_id] = 0

        player_points[user_id] += earned_points

        print("Total points:", player_points[user_id])




bot.run(token)