#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys, os
sys.path.append(os.path.join(sys.path[0], 'src'))

from mod_6 import Mod6


bot = Mod6(login="davydovdmitrii7865", password="4815162342",
               like_per_day=1000,
               comments_per_day=0,
               tag_list=['follow4follow', 'f4f', 'cute'],
               tag_blacklist=['rain', 'thunderstorm'],
               user_blacklist={},
               max_like_for_one_tag=50,
               follow_per_day=300,
               follow_time=1*60,
               unfollow_per_day=300,
               unfollow_break_min=15,
               unfollow_break_max=30,
               log_mod=0,
               proxy='',
               # Use unwanted username list to block users which have username contains one of this string
               ## Doesn't have to match entirely example: mozart will be blocked because it contains *art
               ### freefollowers will be blocked because it contains free
               unwanted_username_list=['second','stuff','art','project','love','life','food','blog','free','keren','photo','graphy','indo',
                                       'travel','art','shop','store','sex','toko','jual','online','murah','jam','kaos','case','baju','fashion',
                                        'corp','tas','butik','grosir','karpet','sosis','salon','skin','care','cloth','tech','rental',
                                        'kamera','beauty','express','kredit','collection','impor','preloved','follow','follower','gain',
                                        '.id','_id','bags'])

'''
MOD 0 - collect user by teg in db
MOD 1 - collect user from file in db
MOD 2 - like users from db
'''
mod = 1


if mod == 0:
    while True:
        bot.сollect_users_by_tags()
elif mod == 1:
    bot.сollect_users_from_file()
elif mod == 2:
    bot.like_and_follow_user_from_db()
else:
    print("Wrong mode!")


