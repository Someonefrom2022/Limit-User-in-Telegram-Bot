from telegram import Bot, Update
from telegram.ext import MessageHandler, CommandHandler, CallbackContext, ApplicationBuilder
import logging, time

import requests # This is optional for you. You don't need it if you have no use of it


# You can add multiple chatids in the admins list to escape from getting the message limit

admins = ["Your Chat ID"] # Add the chatids as int. Not str


# Your bot's token
key = "Token"


# Logging what's happening
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO)


async def start_commmand(update:Update, context: CallbackContext.DEFAULT_TYPE) -> None:
	msg = "Hello there!\nThis is the start command."
	await update.effective_message.reply_text(msg)



class Hello:
	# I'm skipping the __init__ functions for now. We don't need that here
	time_dict = {} # The dict where we'll keep track of user's limit


# The function for limiting the user.
def can_message(chatid) -> bool:
	# No limit for admins :P
	if chatid in admins:
		return True
	
	the_dict = Hello.time_dict
	current_time = time.time()
	
	# If the chatid is not in the dict, it will through KeyError
	# So, using try except to escape that
	try:
		the_dict[chatid] # If this passes, the chatid is in the dict
	except:
		the_dict[chatid] = None # As the chatid is not in the list, putting the value as None
	
	if the_dict[chatid] == None:
		the_dict[chatid] = current_time
		return True
		
	else:
		if current_time - the_dict[chatid] >= 3: # If the difference between the last message is >= 3 seconds
			the_dict[chatid] = current_time
			return True
		else:
			return False






# Your function that you want to limit for normal users
async def cute_cats(update:Update, context:CallbackContext.DEFAULT_TYPE) -> None:
	chatid = update.effective_user.id
	
	if can_message(chatid):
		# I'm just taking some data from an API
		req = requests.get("https://api.thecatapi.com/v1/images/search").json()[0]["url"]
		await context.bot.send_photo(chatid, req)
	else:
		await update.effective_message.reply_text("Calm down man... :')")




def main():
    app = ApplicationBuilder().token(key).build()
    
    # Command Handlers...
    start_h = CommandHandler("start", start_commmand)
    
    cat_h = CommandHandler("cat", cute_cats)
    app.add_handler(start_h)
    app.add_handler(cat_h)
    app.run_polling()

if __name__ == "__main__":
	main()
