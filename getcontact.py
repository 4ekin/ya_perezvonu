#!/usr/bin/env python
# Dmitry Chastuhin
# Twitter: https://twitter.com/_chipik

from Crypto.Cipher import AES
from random import randint
import argparse
import requests
import logging
import hashlib
import base64
import time
import json
import hmac
import sys

help_desc = '''
This script allows to get information about phone number from GetContact servers.
Information about API was received by reverse engineering "app.source.getcontact" Android application 
--- chipik
'''

parser = argparse.ArgumentParser(description=help_desc, formatter_class=argparse.RawTextHelpFormatter)
parser.add_argument('-p', '--phoneNumber', help='Phone number (example: +79217XXX514)')
parser.add_argument('-t', '--token', required=True, help='Token for request (Ex:: AxPA568b72d9c908520b95407e6e95b5482c7995fd98b1e794a2e516a3d1)')
parser.add_argument('-d', '--deviceID', default='27b6dc0c3cb{}'.format(randint(10000, 90000)), help='DeviceID (default: 27b6dc0c3cb{})'.format(randint(10000, 90000)))
parser.add_argument('-c', '--countryCode', default='US', help='Country code (default: US)')
parser.add_argument('-a', '--all', action='store_true', help='Print all possible info')
parser.add_argument('-D', '--decrypt', help='Decrypt data')
parser.add_argument('-E', '--encrypt', help='Encrypt data')
parser.add_argument('-P', '--proxy', help='Use proxy (ex: 127.0.0.1:8080)')
parser.add_argument('-v', '--debug', action='store_true', help='Show debug info')
args = parser.parse_args()


# Global vars
HMAC_key= "2Wq7)qkX~cp7)H|n_tc&o+:G_USN3/-uIi~>M+c ;Oq]E{t9)RC_5|lhAA_Qq%_4"
AES_key = "0705a53f0b0c1fbe14d68313939c6683f2baa687aff535dd2469291834bff606".decode("hex")
base_url = "https://pbssrv-centralevents.com"
base_uri = "/v2.1/"
methods = {"number-detail":"details", "search":"search", "verify-code":""}
timestamp = str(time.time()).split('.')[0]


headers = {
    "X-App-Version": "4.2.0",
    "X-Req-Timestamp": timestamp,
    "X-Os": "android 7.1.1",
    "X-Token": args.token,
    "X-Encrypted": "1",
    "X-Client-Device-Id": args.deviceID,
    "X-Req-Signature": "",
    "Content-Type": "application/json; charset=utf-8",
    "Connection": "close",
    "Accept-Encoding": "gzip, deflate"}


data = {"countryCode":args.countryCode,
        "phoneNumber":args.phoneNumber,
        "source":"",
        "token":args.token,
        }

captcha_data={"token":args.token,
              "validationCode":"",
              }

proxies={}
verify = True
if args.proxy:
    verify = False
    proxies = {
      'http': args.proxy,
      'https': args.proxy,
    }

def init_logger(logname, level):
    # generic log conf
    logger = logging.getLogger(logname)
    logger.setLevel(level)
    console_format = logging.Formatter("[%(levelname)-5s] %(message)s")
    # console handler
    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(level)
    ch.setFormatter(console_format)
    logger.addHandler(ch)
    return logger

def prepare_payload(payload):
    return json.dumps(payload).replace(" ","")

def create_sign(timestamp, payload):
    logger.debug("Signing...\n{}-{}".format(timestamp, payload))
    message = bytes("{}-{}".format(timestamp, payload))
    secret = bytes(HMAC_key)
    signature = base64.b64encode(hmac.new(secret, message, digestmod=hashlib.sha256).digest())
    logger.debug("Result: {}".format(signature))
    return signature

def send_post(url, data):
    logger.debug("Sending request: {}\nDATA: {}".format(url, data))
    data = json.dumps({"data":data})
    r = requests.post(url, data=data, headers=headers, proxies = proxies, verify=verify)
    if r.status_code == 200:
        logger.debug("Response: {}".format(r.json()["data"]))
        return r.json()["data"]
    elif r.status_code == 404:
        print "Nothing found for {} :(".format(args.phoneNumber)
    elif r.status_code == 403:
        logger.debug("Captcha? Status:{}".format(r.status_code))
        return r.json()["data"]
    elif r.status_code == 400:
        print "Wrong Number? Status: {}".format(r.status_code)
        return r.json()["data"]
    else:
        print "Something wrong! Status: {}".format(r.status_code)
    return r.status_code

BS = 16
pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS)
unpad = lambda s: s[0:-ord(s[-1])]
logger = init_logger("GetContact", logging.INFO)

def decrypt_aes(payload):
    logger.debug("Decrypting...\nDATA:{}".format(payload.encode("hex")))
    cipher = AES.new(AES_key, AES.MODE_ECB)
    rez =  unpad(cipher.decrypt(payload))
    logger.debug("Decrypted result:{}".format(rez))
    return rez

def encrypt_aes(str):
    logger.debug("Encrypting...\nDATA:{}".format(str))
    raw = pad(str)
    cipher = AES.new(AES_key, AES.MODE_ECB)
    return base64.b64encode(cipher.encrypt(raw))

def send_req_to_the_server(url, payload):
    headers["X-Req-Signature"] = create_sign(timestamp, prepare_payload(payload))
    result_enc = send_post(url, encrypt_aes(prepare_payload(payload)))
    if isinstance(result_enc,int):
        result = {'meta':{}}
        result['meta']['httpStatusCode'] = result_enc
        result['meta']['errorCode'] = result_enc
        result['meta']['errorMessage'] = str(result_enc)
        return result
    else:
        return json.loads(decrypt_aes(base64.b64decode(result_enc)))


def print_results(profile, remainingCount):
    if args.all:
        print "We found:"
        for item in profile:
            if profile[item]:
                if item == 'tags':
                    print item
                    for tag in profile[item]:
                        print "\t",
                        print tag
                else:
                    print "{}:".format(item),
                    print profile[item]
        print "Left {} requests".format(remainingCount)
        return 0
    else:
        print profile['displayName'].encode('utf-8').strip()
        if profile['tags']:
            for tag in profile['tags']:
                print tag.encode('utf-8').strip()
    return 0

def handle_captcha(imgstring):
    logger.debug("Handling captcha...")
    imgdata = base64.b64decode(imgstring)
    filename = "captcha_{}.jpg".format(randint(0, 1000))
    with open(filename, 'wb') as f:
        f.write(imgdata)
    print "Captcha saved in file: {}".format(filename)
    print "[!] Check it and type it below. "
    captcha_value = raw_input("Enter captcha:")
    logger.debug("Got capthca value:{}".format(captcha_value))
    method = "verify-code"
    captcha_data['validationCode'] = captcha_value
    result = send_req_to_the_server(base_url + base_uri + method, captcha_data)
    if result['meta']['httpStatusCode'] == 200:
        print "Captcha passed. Now you can try search again!"
        return 0
    elif result['meta']['httpStatusCode'] == 403:
        code = result['meta']['errorCode']
        print "Error ({}):".format(code),
        print result['meta']['errorMessage']
        if code is "403004":
            print "Wrong Captcha!"
    return 1

def save_captcha_bot(imgstring):
    logger.debug("Handling captcha...")
    imgdata = base64.b64decode(imgstring)
    filename = "captcha/captcha_{}.jpg".format(randint(0, 1000))
    with open(filename, 'wb') as f:
        f.write(imgdata)
    print "Captcha saved in file: {}".format(filename)
    return filename

def send_captcha_bot(captcha_value):
    logger.debug("Got capthca value:{}".format(captcha_value))
    method = "verify-code"
    captcha_data['validationCode'] = captcha_value
    result = send_req_to_the_server(base_url + base_uri + method, captcha_data)
    if result['meta']['httpStatusCode'] == 200:
        logger.debug("Captcha passed")
        print "Captcha passed. Now you can try search again!"
        return 0
    elif result['meta']['httpStatusCode'] == 403:
        code = result['meta']['errorCode']
        print "Error ({}):".format(code),
        print result['meta']['errorMessage']
        if code is "403004":
            logger.debug("Wrong Captcha!")
            print "Wrong Captcha!"
    return 1

def get_number_info(phoneNumber):
    # return [code, data]
    method = "search"
    data["source"] = methods[method]
    data["phoneNumber"] = phoneNumber
    result = send_req_to_the_server(base_url + base_uri + method, data)
    if result['meta']['httpStatusCode'] == 200:
        profile = result['result']['profile']
        profile['tags'] = []
        remainingCount = result['result']['subscriptionInfo']['usage']['search']['remainingCount']
    elif result['meta']['httpStatusCode'] == 403:
        code = result['meta']['errorCode']
        print "Error ({}):".format(code),
        print result['meta']['errorMessage']
        img_file = ""
        if code == "403004":
            logger.debug("Captcha handler here")
            img_file = save_captcha_bot(result['result']['image'])
            # handle_captcha(result['result']['image'])
        # return code
        return [result['meta']['httpStatusCode'],[code,img_file]]
    elif result['meta']['httpStatusCode'] == 400:
        code = result['meta']['errorCode']
        print "Error ({}):".format(code),
        print result['meta']['errorMessage']
        return [result['meta']['httpStatusCode'], ""]
    elif result['meta']['httpStatusCode'] == 404:
        code = result['meta']['errorCode']
        print "Error ({}):".format(code),
        print result['meta']['errorMessage']
        return [result['meta']['httpStatusCode'], ""]
    else:
        print "Something wrong!"
        return [777, ""]
    if profile['tagCount'] > 0:
        # 1 - /v2.1/number-detail
        method = "number-detail"
        data["source"] = methods[method]
        headers["X-Req-Signature"] = create_sign(timestamp, prepare_payload(data))
        result_enc = send_post(base_url + base_uri + method, encrypt_aes(prepare_payload(data)))
        result_dec = json.loads(decrypt_aes(base64.b64decode(result_enc)))
        if result_dec['meta']['httpStatusCode'] == 200:
            tags_nbr = len(result_dec['result']['tags'])
            logger.debug("Got {} response. Found {} tags".format(result_dec['meta']['httpStatusCode'], tags_nbr))
            remainingCount = result['result']['subscriptionInfo']['usage']['search']['remainingCount']
            for tag in result_dec['result']['tags']:
                profile['tags'].append(tag['tag'])
    print_results(profile, remainingCount)
    return [200, [profile, remainingCount]]


if __name__ == '__main__':
    if args.debug:
        logger = init_logger("GetContact", logging.DEBUG)

    if args.phoneNumber:
        #0 - /v2.1/search
        get_number_info(args.phoneNumber)

    if args.decrypt:
        decrypted_payload =  decrypt_aes(base64.b64decode(args.decrypt))
        print "Decrypted: {}".format(decrypted_payload)

    if args.encrypt:
        encrypted_payload = encrypt_aes(args.encrypt)
        print "Encrypted: {}".format(encrypted_payload)
