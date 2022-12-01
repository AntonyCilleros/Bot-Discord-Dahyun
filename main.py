import bot
import threading

def thread_message(name):
    bot.run_discord_bot_message()

def thread_command(name):
    bot.run_discord_bot_command()

if __name__ == '__main__' :
    message = threading.Thread(target=thread_message, args=(1,))
    command = threading.Thread(target=thread_command, args=(1,))
    message.start()
    command.start()
    message.join()
    command.join()