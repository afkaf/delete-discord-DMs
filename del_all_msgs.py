import discum
import time
from tqdm import tqdm

bot = discum.Client(email="email",
					password="password",
					token=None,
					user_agent="chrome",
					log=False)

excluded_channels = []
rate_limit = 0.5

@bot.gateway.command
def get_user_data(resp):
	global channelIDs
	global user_id
	if resp.raw['t'] == 'READY_SUPPLEMENTAL':
		channelIDs = (bot.gateway.session.DMIDs)
		user_id = bot.gateway.session.user['id']
		bot.gateway.close()

def get_user_data():
	try:	
		bot.gateway.run()
	except:
		pass

def get_channel_messages(chanID):
	channel_messages = []
	last = ''
	messages = bot.getMessages(chanID,num=100).json()
	if messages == []:
		return channel_messages
	while last != messages[-1]['id']:
		time.sleep(rate_limit)
		for message in messages:
			if message['author']['id'] == user_id:
				channel_messages.append(message)
		last = messages[-1]['id']
		messages = bot.getMessages(chanID,num=100,aroundMessage=messages[-1]['id']).json()
	return channel_messages

def get_all_messages():
	msg_dict = {}
	for chanID in tqdm(sorted(channelIDs)):
		if chanID not in excluded_channels:
			messages = get_channel_messages(chanID)
			if len(messages) > 0:
				print(f'Channel ID: {chanID}, Messages to delete: {len(messages)}'),
				msg_dict[chanID] = messages
	return msg_dict

def delete_messages(msg_dict):
	for chanID in msg_dict.keys():
		print(f'Deleting messages in: {chanID}')
		for msg in tqdm(msg_dict[chanID]):
			bot.deleteMessage(chanID,msg['id'])
			time.sleep(rate_limit)

def delete_channel_messages(chanID):
	delete_messages({chanID : get_channel_messages()})



get_user_data()
print('Starting')

delete_messages(get_all_messages())