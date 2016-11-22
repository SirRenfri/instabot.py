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
    url_user_media = 'https://www.instagram.com/%s/media/'

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
        self.users_info_by_tag = []
        self.username_by_code = ''
        self.usernames = []

    def get_users_by_tag(self, tag):
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

                    users_info = []
                    db = Model()
                    for post in posts:
                        code = post['code']
                        self.get_username_by_code(code)
                        id = post['owner']['id']

                        if db.check_user(id) == False:
                            users_info.append({'user_id': id, 'username': self.username_by_code})

                            log_string = "Get new user: %s" % (self.username_by_code)
                            self.write_log(log_string)
                        else:
                            log_string = "User already added in db: %s" % (self.username_by_code)
                            self.write_log(log_string)
                    db.close()

                    self.users_info_by_tag = users_info

                except:
                    self.users_info_by_tag = []
                    self.write_log("Except on get code!")
            else:
                return 0

    def get_username_by_code(self, code):
        if self.login_status == 1:
            url_code = self.url_post % code
            try:
                r = self.s.get(url_code)
                text = r.text
                all_data = json.loads(text)
                username = all_data['media']['owner']['username']

                self.username_by_code = username

            except:
                self.username_by_code = ''
                self.write_log("Except on get username!")
        else:
            return 0

    def check_posts_and_like(self, username, min_like=0):
        url_user_media = self.url_user_media % username
        try:
            r = self.s.get(url_user_media)
            text = r.text
            all_data = json.loads(text)
            posts_info = all_data['items']

            for post_info in posts_info:
                likes = post_info['likes']['count']
                if likes >= min_like:
                    InstaBot.like(self, post_info['id'])
                    log_string = "Like post: %s" % (post_info['id'])
                    self.write_log(log_string)
                else:
                    log_string = "Post %s have too litle like" % (post_info['id'])
                    self.write_log(log_string)

        except:
            self.write_log("This user is disappear!")

        else:
            return 0

    def сollect_users_by_tag(self, tag):
        self.get_users_by_tag(tag)
        users_info = self.users_info_by_tag

        db = Model()
        operation = 'COLLECT'
        for user_info in users_info:
            user_id = user_info['user_id']
            username = user_info['username']

            db.save_user(username, user_id, tag, operation)

            log_string = "User %s is added in db" % (username)
            self.write_log(log_string)
        db.close()

    def like_and_follow_user_from_db(self, min_like=0):
        db = Model()
        users_info = db.get_users_with_operation('COLLECT')

        for user_info in users_info:
            user_id = user_info['user_id']
            username = user_info['username']

            self.check_posts_and_like(username, min_like) # TODO: Тайм-паузы между лайками
            InstaBot.follow(self, user_id)

            db.change_operation_status(user_id, 'LIKED_AND_FOLLOWED')
            db.change_date(user_id)
        db.close()




