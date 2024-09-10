#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@author: 
@create: 2024/9/11
@brief:
"""

import requests
import base64

# 替换为您的 V2Ray 订阅链接
subscription_url = ""

# 发起 HTTP 请求获取订阅内容
response = requests.get(subscription_url)
subscription_data = base64.b64decode(response.text).decode("utf-8")

# 解析订阅内容
nodes = []
for line in subscription_data.splitlines():
    print(line)


if __name__ == '__main__':
    pass