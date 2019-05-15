import subprocess
import sys
import time
import telepot
import picamera
from telepot.loop import MessageLoop

# add --on-boot param if script is started during raspberry pi booting
# script is added to /etc/rc.local
onboot = False
for arg in sys.argv:
  if arg == '--on-boot':
    onboot = True

if onboot:
  # sleeping and waiting... everything must be ok
  time.sleep(60)

userId = 1234567890 # chat.id from message, only we can control our Raspberry Pi
exited = False
picturePath = '/path/to/photo.jpg'

bot = telepot.Bot('API TOKEN')

print(bot.getMe())

bot.sendMessage(userId, 'Hi... I\'m back...')

def handleMsg(msg):
  global userId
  global exited

  print(msg)

  chatId = msg['chat']['id']

  if (not userId) or (chatId == userId):
    output = ''
    if 'text' in msg:
      command = msg['text']
      if command == '/help':
        output = output + '/help - prints this help\n'
        output = output + '/photo - sends actual photo from camera\n'
        output = output + '/uptime - shows uptime from RPi\n'
        output = output + '/df - shows free disk space\n'
        output = output + '/die - stops bot\n'
        output = output + '/reboot - reboot RPi\n'
      elif command == '/photo':
        camera = None
        try:
          camera = picamera.PiCamera()
        except:
          output = 'Camera not connected!'
        if camera is not None:
          try:
            time.sleep(5)
            camera.resolution = '1080p'
            camera.hflip = True
            camera.vflip = True
            camera.capture(picturePath)
            bot.sendPhoto(chatId, open(picturePath, 'rb'))
          finally:
            camera.close()
      elif command == '/uptime':
        output = subprocess.check_output('uptime')
      elif command == '/df':
        output = subprocess.check_output(['df', '-h'])
      elif command == '/die':
        bot.sendMessage(chatId, 'Bye bye... :-(')
        exited = True
      elif command == '/reboot':
        bot.sendMessage(chatId, 'Bye bye... I\'ll be back soon...')
        subprocess.Popen(['sudo','/sbin/reboot'])
      else:
        bot.sendMessage(chatId, 'Received message: ' + msg['text'])
    else:
      bot.sendMessage(chatId, 'Unknown message :-(')

    if output != '':
      bot.sendMessage(chatId, output)
  else :
    bot.sendMessage(chatId, 'I can\'t talk to you... Sorry')
  
bot.message_loop(handleMsg)


# Keep program running
try:
  while 1:
    if exited:
      sys.exit(0)
    time.sleep(10)
except KeyboardInterrupt:
  bot.sendMessage(userId, 'I\'m going offline')
  sys.exit(0)
