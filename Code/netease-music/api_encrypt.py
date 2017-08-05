"""
This is api encrypt
"""
#coding = utf-8

import base64
import json
import requests

from Crypto.Cipher import AES

from music import SongComment

headers = {
    'Cookie': 'appver=1.5.0.75771;',
    'Referer': 'http://music.163.com/'
}

first_param = "{rid:\"\", offset:\"0\", total:\"true\", limit:\"20\", csrf_token:\"\"}"
second_param = "010001"
third_param = "00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7"
forth_param = "0CoJUm6Qyw8W8jud"


def get_params():
    iv = "0102030405060708"
    first_key = forth_param
    second_key = 16 * 'F'
    h_encText = AES_encrypt(first_param, first_key, iv)
    h_encText = AES_encrypt(h_encText, second_key, iv)
    return h_encText


def get_encSecKey():
    encSecKey = "257348aecb5e556c066de214e531faadd1c55d814f9be95fd06d6bff9f4c7a41f831f6394d5a3fd2e3881736d94a02ca919d952872e7d0a50ebfa1769a7a62d512f5f1ca21aec60bc3819a9c3ffca5eca9a0dba6d6f7249b06f5965ecfff3695b54e1c28f3f624750ed39e7de08fc8493242e26dbc4484a01c76f739e135637c"
    return encSecKey


def AES_encrypt(text, key, iv):
    pad = 16 - len(text) % 16
    text = text + pad * chr(pad)
    encryptor = AES.new(key, AES.MODE_CBC, iv)
    encrypt_text = encryptor.encrypt(text)
    encrypt_text = base64.b64encode(encrypt_text)
    return encrypt_text

def get_json(url, params, encSecKey):
    print(params)
    print(encSecKey)
    # params = 'v163/FTKJIkDkIfOnrcHiMNYPSJkJwJaoPHyhA3wPSGoOLsQqaYIQ/BAOyOypuseFDIifCsjY8j1ip4knS4VTEcA/8ljXREmwBxGl9m3Pfei2sqItWPsMIy/jvjFF8sQKxc73boUk9pV72nRYz6WcbJjUvSr+xkiNj5hx0riXBR3YkCAJqn/zk5qzwQ6C/Ss'
    # encSecKey = '1ca4a82046a2a494252938a7ab2f55a643adeae94a3d7af04545eaa642b450a8072c27946f58d97b632f175defb15b8f176e2956e9b328b9f3de0dc4c51066945980baf796d17f5bcd8f031d016d433168dec1f5a2899e6534f416685a1cb13042de75aac3d10cf06c25654aa2de5f9da472356567f97dd51208c6055b02863f'
    data = {
        "params": params,
        "encSecKey": encSecKey
    }
    response = requests.post(url, headers=headers, data=data)
    return response.content

if __name__ == "__main__":
    url = "http://music.163.com/weapi/v1/resource/comments/R_SO_4_26584163/?csrf_token="
    params = get_params()
    encSecKey = get_encSecKey()
    json_text = get_json(url, params, encSecKey)
    json_dict = json.loads(json_text)
    
    # comment = SongComment()
    # comment.set_comment_total(json_dict['total'])
    print(json_dict['total'])

    # print(comment.get_comment_total())

    for item in json_dict['comments']:
        print(item['content'])
