# import the necessary libraries
from twilio.rest import Client

# set up the Twilio client
account_sid = 'AC7dc1bd049cdfff0671a8c5b2a91d925f'
auth_token = 'bdc1f88c8f71ddc1ca45b1c3f8a6fc2a'
client = Client(account_sid, auth_token)

# send the message
message = client.messages.create(
    body='Check out this image!',
    from_='whatsapp:+14155238886',
    media_url='https://www.istockphoto.com/photo/rush-in-the-city-gm1190475811-337501205',
    to='whatsapp:+7980136952'
)

print(message.sid)
print("Hello")
