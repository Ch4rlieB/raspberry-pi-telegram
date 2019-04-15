import telepot

bot = telepot.Bot('API TOKEN')
print(bot.getMe())

response = bot.getUpdates()
print(response)
