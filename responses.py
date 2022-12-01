import random

def handle_response(message) -> str:
    p_message = message.lower()
    if p_message == "hello" :
        return "Hey there!"
    if p_message == 'dice' :
        return str(random.randint(1,6))
    if 'happy birthday' in p_message or 'joyeux an' in p_message or 'bon an' in p_message:
        return 'Joyeux anniversaire ! 🎈🎉'