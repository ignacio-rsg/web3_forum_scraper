from telegram.ext import *
import time , requests
from datetime import date, datetime 
from zoneinfo import ZoneInfo
from scraper import check_for_posts, new_unchecked_posts
from apscheduler.schedulers.background import BackgroundScheduler, BlockingScheduler
from pytz import utc
from dotenv import load_dotenv
import os

load_dotenv()

Apikey= os.getenv('API_KEY')
telegram_id= os.getenv('TELEGRAM_ID')


def send_msg(message):
    url=f'https://api.telegram.org/bot{Apikey}/sendMessage?chat_id={telegram_id}&text={str(message)}'
    response = requests.post(url)
    
    print(response)


def sample_responses(input_text):
    user_message = str(input_text).lower()
    
    if user_message in ("hello", "hi", "sup"):
        return "Hey! How are you doing?"
    
    # if "log in notion" in user_message:
    #     url=(user_message[14:])
    #     if url:
    #         if 'http' not in url:
    #             return "Maybe the website is wrong.. but is missing the 'http'\n Tip: try the '\help' command"
    #         else:
    #             response = createNotionPage(url)
    #             return response
    # return "Maybe the website is wrong.. but is missing the 'http'\n Tip: try the '\help' command"



print("bot started")


def log_command(update,context):
    text_message = update['message']['text']
    url = text_message[8:]
    print(url)
    if url:
        if 'http' not in url:
            txt= "Maybe the website is wrong.. but is missing the 'http'\n Tip: try the '/help' command"
            
            update.message.reply_text(txt)
        else:
            response = createNotionPage(url)
            txt = "Page created"
            update.message.reply_text(txt)
            
    txt = "Maybe the website is wrong.. but is missing the 'http'\n Tip: try the '/help' command"
    update.message.reply_text(txt)
    




def start_command(update,context):
    update.message.reply_text("Bot started")
    

def help_command(update,context):
    update.message.reply_text("If you need some help, maybe search in google!")
    time.sleep(10)
    update.message.reply_text("I was kidding!! :)")
    time.sleep(2)
    update.message.reply_text("I will fetch new posts every 10 - 12 hours.. if you would like to log some of them in notion just send me a command:\n \"/notion <uSrl>\"")
    
    
def handle_message(update, context):
    text = str(update.message.text).lower()
    response = sample_responses(text)
    
    update.message.reply_text(response)
    
def push_command(update, context):
    update.message.reply_text("Searching for updates, this may take a while..")

    #scraping defi for new posts
    data=new_unchecked_posts()

    #if data is a str means there are no new posts
    if type(data) == str:
        update.message.reply_text(data)
        
    #this else will return the new available posts
    else:
        #sending messages
        for item in data: 
            text_message = f"Title: {item[0]} \n URL: {item[1]} \n Comments: {item[2]} \n Views: {item[3]}"
            update.message.reply_text(text_message)
            print("Message sent to group")

    
def error(update, context):
    update.message.reply_text(f"Update {update} caused error {context.error}")
    print( f"Update {update} caused error {context.error}")
    
    
def main():
    
     # Create the Application and pass it your bot's token.
    application = Application.builder().token(Apikey).build()

    # Add handlers
    application.add_handler(CommandHandler("push", push_command))
    application.add_handler(CommandHandler("notion", log_command))
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(MessageHandler(filters.Text, handle_message))

    # Run the bot until the user presses Ctrl-C
    application.run_polling()


#### CARLOS ACA PONES LAS SPECIAL KEYWORDS #### 
    
specialKeywords=('nomination','job','hiring','project manager','project lead','position','role','open','vacancies','vacancy','applicants','application','looking for')

def daily():
    #scraping defi for new posts
    data=new_unchecked_posts()
    #if data is a str means there are no new posts
    if type(data) == str:
        
        send_msg(data)
        #print(data)
        #update.message.reply_text(data)
    #this else will return the new available posts
    else:
        #sending messages
        for item in data: 
            for word in specialKeywords:
                if word in item[0].lower():
                    if '#' in item[0]:
                        title = item[0].replace("#", "")
                        text_message = f"Title: {title} \n URL: {item[1]} \n Comments: {item[2]} \n Views: {item[3]}"
                    elif '&' in item[0]:
                        title = item[0].replace("&", "")
                        text_message = f"Title: {title} \n URL: {item[1]} \n Comments: {item[2]} \n Views: {item[3]}"
                    else:
                        text_message = f"Title: {item[0]} \n URL: {item[1]} \n Comments: {item[2]} \n Views: {item[3]}"
                    #update.message.reply_text(text_message)
                    send_msg(text_message)    
                    #print(text_message)
                    print("Message sent to group")

###################################################################################################################################
daily()
####################### APP SCHEDULER > 
sched = BlockingScheduler(timezone=utc)
sched = BackgroundScheduler(daemon=True)
#sched.add_job(daily,'interval',minutes=720)# 120hs
sched.add_job(daily,'interval',minutes=120)
sched.start()
#################

main()


    


