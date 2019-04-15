import telepot

bot = telepot.Bot('API TOKEN')
bot.getMe()
response = bot.getUpdates()
print(response)
