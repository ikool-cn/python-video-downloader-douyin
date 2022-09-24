# A Python Video Downloader For Douyin

### Usage
```python
import os

from douyin import DouYin

if __name__ == "__main__":
    share_txt = "4.87 OkP:/ 马斯克被问SpaceX为什么不招外国人？这不是我们能决定的...# 科技 # 火箭 https://v.douyin.com/64QoUQn/ 复制此链接，打开Dou音搜索，直接观看视频！"
    path = os.getcwd() + "/download"

    # 获取无水印视频链接
    try:
        url = DouYin().parse(share_txt).get_video_url()
        print(url)
    except Exception as e:
        print(str(e))

    # 下载视频
    try:
        DouYin().parse(share_txt).download_video(path)
    except Exception as e:
        print(str(e))

```