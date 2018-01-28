#!/usr/bin/env python
# -*- coding:utf-8 -*-


import json
import re
import twitter

# replace 'default' with twitter user
user = 'mahavivo'
# path to json file with your twitter credentials (see https://python-twitter.readthedocs.io/en/latest/)
creds = 'creds.json'
file_name = 'mahavivo.txt'


def init_twitter():
    # load twitter API tokens；在creds.json文件中分别填入从网页获得的授权凭证。
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
    #
    # # 打印关注名单
    # friends = api.GetFriends()
    # print([u.name for u in friends])

    # # 打印Timeline
    # timeline = api.GetHomeTimeline(count=150)
    # print([tl.text for tl in timeline])

    # # 删除Twitter
    # statuses = api.GetUserTimeline(count=200)
    # for status in statuses:
    #     api.DestroyStatus(status._id)


    # get up to 4000 latest tweets
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