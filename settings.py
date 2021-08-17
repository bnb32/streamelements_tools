import info
import processing as proc

channel_id=info.liz_id
token=info.liz_token

headers = {'accept': 'application/json','authorization': 'Bearer {token}'.format(token=token)}

s=proc.getSettings(channel_id,headers)

print("Queued songs per user limit: %s"%(s['max_songs']))
print("Filter level for submissions: %s"%(s['sec_level']))
print("Maximum length for submissions: %s seconds"%(s['max_len']))

