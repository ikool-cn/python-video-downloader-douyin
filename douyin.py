#!/usr/bin/python
# coding=utf-8
import sys
import requests
import re
import os
import logging

logging.basicConfig(format='%(asctime)s [%(levelname)s] %(message)s', level=logging.INFO, datefmt='%Y-%m-%d %H:%M:%S')


class DouYin():
    def __init__(self):
        self.headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3877.400 QQBrowser/10.8.4506.400',
        }

    def parse(self, share_txt):
        """
        解析分享链接
        :param share_txt:
        :return:
        """
        self.share_txt = share_txt
        self.__parse_share_link().__get_redirect_url().__get_item_id().__get_video_url()
        return self

    def get_video_url(self):
        """
        获取无水印视频链接
        :return:
        """
        return self.video_url

    def download_video(self, path):
        """
        下载视频
        :param path:
        :return:
        """
        resp = requests.get(url=self.video_url, headers=self.headers)
        if resp and resp.status_code == 200:
            save_path = os.path.join(os.getcwd(), path)
            if not os.path.exists(save_path):
                os.makedirs(save_path)

            remove_chars = r"[\/\\\:\*\?\"\<\>\|]"  # '/ \ : * ? " < > |'
            new_title = re.sub(remove_chars, "_", self.title)
            filename = '%s.mp4' % new_title
            with open(save_path + "/" + filename, 'wb') as f:
                f.write(resp.content)

    def __parse_share_link(self):
        match = re.findall('(https://v.douyin.com/.*?/)', self.share_txt, re.S)
        if match:
            logging.info("parse_share_link:%s" % match[0])
            self.share_link = match[0]
            return self
        raise Exception("parse_share_link failed")

    def __get_redirect_url(self):
        resp = requests.get(self.share_link, allow_redirects=False)
        if resp and resp.status_code == 302:
            logging.info("get_redirect_url:%s" % resp.headers['Location'])
            self.redirect_url = resp.headers['Location']
            return self
        raise Exception("get_redirect_url failed")

    def __get_item_id(self):
        item_ids = re.findall('video\/(.*?)\/\?region', self.redirect_url)
        if item_ids:
            logging.info("get_item_id:%s" % item_ids[0])
            self.item_id = item_ids[0]
            return self
        raise Exception("get_item_id failed")

    def __get_video_url(self):
        url = f'https://www.iesdouyin.com/web/api/v2/aweme/iteminfo/?item_ids={self.item_id}'
        resp = requests.get(url, headers=self.headers)
        if resp and resp.status_code == 200:
            data = resp.json()
            self.title = data['item_list'][0]['desc']
            self.video_id = data['item_list'][0]['video']['play_addr']['uri']
            self.video_url = f'https://aweme.snssdk.com/aweme/v1/play/?video_id={self.video_id}&ratio=720p&line=0'
            logging.info("title:%s, video_id:%s, video_url:%s", self.title, self.video_id, self.video_url)
            return self
        raise Exception("get_video_url failed")
