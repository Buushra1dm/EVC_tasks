from pyrogram import Client

api_id = '######################3'  # API id
api_hash = '##################' # API hash
phone_number = '96654#######'  # Telegram phone number

# Create a new Client
app = Client("my_account", api_id=api_id, api_hash=api_hash, phone_number=phone_number)

# Function to send a message
def send_message(user_id, message):
    with app:
        app.send_message(user_id, message)


user_id = '@al11_0077'
message = 'Hello I am  Bushra. This is my account!'

# Send the message
send_message(user_id, message)