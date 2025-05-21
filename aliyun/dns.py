import requests
import time
import hmac
import hashlib
import base64
import datetime
import urllib


class AliyunDNS:
    def __init__(self, BASE_URL, ACCESS_KEY_ID, ACCESS_KEY_SECRET):
        self.BASE_URL = BASE_URL
        self.ACCESS_KEY_ID = ACCESS_KEY_ID
        self.ACCESS_KEY_SECRET = ACCESS_KEY_SECRET

    def params(self, params): # 请求体公共加密
        params = {
            'Format': 'JSON', 
            'Version': '2015-01-09', 
            'AccessKeyId': self.ACCESS_KEY_ID, 
            'SignatureMethod': 'HMAC-SHA1', 
            'SignatureVersion': '1.0',
            'SignatureNonce': str(time.time()), 
            'Timestamp': datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'), 
            **params
        }
        # 加密验证签名部分
        sign = sorted(params.items(), key=lambda x: x[0])
        sign = '&'.join([urllib.parse.quote_plus(k) + '=' + urllib.parse.quote_plus(v) for k, v in sign])
        sign = 'GET&%2F&' + urllib.parse.quote_plus(sign)
        sign = base64.b64encode(
            hmac.new(
                self.ACCESS_KEY_SECRET.encode('utf-8') + b'&', 
                sign.encode('utf-8'), 
                hashlib.sha1
            ).digest()
        ).decode('utf-8')
        params['Signature'] = sign
        return params

    def DescribeDomainRecords(self, DomainName, PageSize=100): # 查看所有解析记录
        response = requests.get(
            url=self.BASE_URL, 
            params=self.params(params={
                'Action': 'DescribeDomainRecords',
                'DomainName': DomainName, 
                "PageSize": str(PageSize)
            })
        )
        assert response.status_code == 200
        return response.json()

    def AddDomainRecord(self, DomainName, RR, Type, Value, Line="default", TTL=600): # 新增解析记录
        response = requests.get(
            url=self.BASE_URL, 
            params=self.params(params={
                'Action': 'AddDomainRecord',
                'DomainName': DomainName,
                'RR': RR, 'Type': Type, 'Value': Value, 'Line': Line, 'TTL': str(TTL)
            })
        )
        assert response.status_code == 200
        return response.json()

    def DeleteDomainRecord(self, RecordId): # 删除解析记录
        response = requests.get(
            url=self.BASE_URL, 
            params=self.params(params={
                'Action': 'DeleteDomainRecord',
                'RecordId': RecordId, 
            })
        )
        assert response.status_code == 200
        return response.json()

