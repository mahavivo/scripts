#!/usr/bin/env python
# -*- coding:utf-8 -*-

import json
import re
import os

import twitter


# 替换此处的'default'为自己想使用的用户名
user = 'default'

# 在json文件中填入从twitter获得的授权账号和钥匙（credentials）。 (see https://python-twitter.readthedocs.io/en/latest/)
creds = 'twitter_creds.json'

file_name = '%s_tweets.txt' % user


def init_twitter():
    # load twitter API tokens
    with open(creds) as data_file:
        data = json.load(data_file)

    api = twitter.Api(consumer_key=data["consumer_key"],
                  consumer_secret=data["consumer_secret"],
                  access_token_key=data["access_token_key"],
                  access_token_secret=data["access_token_secret"])

    return api


def main():
    if user == 'default':
        print("Please define the twitter user's screenname to download content from in source code.")
        return

    api = init_twitter()

    # # 更新Twitter
    # status = api.PostUpdate('更新测试!')
    # print(status.text)

    # # 打印关注名单
    # friends = api.GetFriends()
    # print([u.name for u in friends])

    # # 打印Follower名单
    # followers = api.GetFollowers()
    # print([u.name for u in followers])

    # # 打印Timeline
    # timeline = api.GetHomeTimeline(count=150)
    # print([tl.text for tl in timeline])

    # # 删除200条推文，慎用！
    # statuses = api.GetUserTimeline(count=200)
    # for status in statuses:
    #     api.DestroyStatus(status._id)

    # # 批量关注。名单来自name_list文件，每一行前为网名（昵称），后为注册用名，即screen_name，空格分隔
    # with open('name_list.txt','r', encoding='gbk', errors='ignore') as f:
    #     for line in f.readlines():
    #         line = line.strip()
    #         if not len(line):   # 跳过空行
    #             continue
    #         follow_id = line.split()[-1]
    #         friend = api.CreateFriendship(screen_name=follow_id)
    #         if friend:
    #             print(friend.name)

    # # 批量取消关注。使用名单同上，也可另建。
    # with open('name_list.txt', 'r', encoding='gbk', errors='ignore') as f:
    #     for line in f.readlines():
    #         line = line.strip()
    #         if not len(line):  # 跳过空行
    #             continue
    #         follow_id = line.split()[-1]
    #         friend = api.DestroyFriendship(screen_name=follow_id)
    #         if friend:
    #             print(friend.name)

    # 下载 4000 条推文（Twitter系统有限制，最多只能获取3200条）
    tweets = api.GetUserTimeline(screen_name=user, count=200)
    curr_id = tweets[-1].id
    for i in range(19):
        tweets = tweets + api.GetUserTimeline(screen_name=user, count=200, max_id=curr_id)
        curr_id = tweets[-1].id

    print("Tweets: " + str(len(tweets)))

    # write tweets to file
    with open(file_name, 'w') as file_o:
        for tweet in tweets:
            create_time = tweet.created_at
            create_time = create_time[-4:] + ' ' + create_time[4:19]
            # tweet_cont = tweet.text
            tweet_cont = tweet.text.encode('gbk','ignore').decode('gbk')
            # # strip links
            # tweet_cont = re.sub(r'http\S+', '', tweet_cont)
            # # strip mentions
            # tweet_cont = re.sub(r'@\S+', '', tweet_cont)
            # # strip hashtags
            # tweet_cont = re.sub(r'#\S+', '', tweet_cont)
            # tweet_cont = tweet_cont.replace('RT: ', '')
            # tweet_cont = tweet_cont.replace('RT', '')
            tweet_cont = create_time + '  ' + tweet_cont.strip()
            file_o.write(tweet_cont + '\n')


if __name__ == "__main__":
    main()