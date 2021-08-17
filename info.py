exempt_level=1000
settings={'max_songs':5,
          'min_views':40000,
	  'min_ratio':0.75,
	  'max_len':615,
	  'min_level':250
	  }
beta_msg="If you think this is a program error please let DrChessgremlin know."
view_levels={'0':0,'1':500,'2':5000,'3':40000,'4':40000,'5':40000}
ratio_levels={'0':0,'1':0.5,'2':0.65,'3':0.75,'4':0.8,'5':0.85}
user_levels={100:'everyone',250:'subscribers',300:'regulars',400:'vips',500:'moderators',1000:'supermoderators',1500:'broadcasters'}
err_msg="Error adding song to queue. Please submit a valid link or youtube keyword search. The submission must be less than %s seconds, have at least %s views, and have a likes/(likes+dislikes) value of at least %s. You are also only allowed %s songs in the queue at a time."
directory="/home/Grads/2012/bnb32/public_html/tools/"
liz_id=#user id
liz_token=#token
bnb_id=#user id
base_url = "https://api.streamelements.com/kappa/v2"
sr_url = "%s/songrequest"%(base_url)
bnb_token=#token
yt_key=#yt api key
yt_url = "https://www.googleapis.com/youtube/v3"
