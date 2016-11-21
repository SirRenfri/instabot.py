#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys, os
sys.path.append(os.path.join(sys.path[0], 'src'))

from instabot import InstaBot
import json
from models import Model

class Mod6(InstaBot):
    '''
        Описание класса
    '''

    url_tag = 'https://www.instagram.com/explore/tags/'
    url_post = 'https://www.instagram.com/p/%s/?__a=1'

    def __init__(self, login, password,
                 like_per_day=1000,
                 media_max_like=50,
                 media_min_like=0,
                 follow_per_day=0,
                 follow_time=5 * 60 * 60,
                 unfollow_per_day=0,
                 comments_per_day=0,
                 tag_list=['cat', 'car', 'dog'],
                 max_like_for_one_tag=5,
                 unfollow_break_min=15,
                 unfollow_break_max=30,
                 log_mod=0,
                 proxy="",
                 user_blacklist={},
                 tag_blacklist=[],
                 unwanted_username_list=[]):
        InstaBot.__init__(self, login, password,
                 like_per_day,
                 media_max_like,
                 media_min_like,
                 follow_per_day,
                 follow_time,
                 unfollow_per_day,
                 comments_per_day,
                 tag_list,
                 max_like_for_one_tag,
                 unfollow_break_min,
                 unfollow_break_max,
                 log_mod,
                 proxy,
                 user_blacklist,
                 tag_blacklist,
                 unwanted_username_list)
        self.posts_info_by_tag = []
        self.username_by_code = ''

    def get_posts_info_by_tag(self, tag):
        if (self.login_status):
            log_string = "Get media id by tag: %s" % (tag)
            self.write_log(log_string)
            if self.login_status == 1:
                url_tag = '%s%s%s' % (self.url_tag, tag, '/?__a=1')
                try:
                    r = self.s.get(url_tag)
                    text = r.text
                    all_data = json.loads(text)
                    posts = all_data['tag']['media']['nodes']

                    codes_and_id = []
                    db = Model()
                    for post in posts:
                        code = post['code']
                        id = post['owner']['id']

                        if db.check_user(id) == False:
                            codes_and_id.append({'user_id': id, 'code': code})
                    db.close()

                    self.posts_info_by_tag = codes_and_id

                except:
                    self.code_by_tag = []
                    self.write_log("Except on get code!")
            else:
                return 0

    def get_username_by_code(self, code):
        log_string = "Get username by post code: %s" % (code)
        self.write_log(log_string)
        if self.login_status == 1:
            url_code = self.url_post % code
            try:
                r = self.s.get(url_code)
                text = r.text
                all_data = json.loads(text)
                username = all_data['media']['owner']['username']

                self.username_by_code += username

            except:
                self.username_by_code = ''
                self.write_log("Except on get username!")
        else:
            return 0

    def auto_mod6(self, tag):
        self.get_posts_info_by_tag(tag)
        posts_info = self.posts_info_by_tag
        print(posts_info)