# aliyun-sdk
阿里云SDK简化版的python实现

## 目前已实现功能

- [x] 云解析
- [ ] 轻量应用服务器

## 原始项目及SDK文档

`https://next.api.aliyun.com/document`  
`https://github.com/aliyun/alibabacloud-python-sdk`

## AccessKey获取方法

`https://ram.console.aliyun.com/profile/access-keys`

## dns使用方法

```
from aliyun import AliyunDNS

dns = AliyunDNS(
    BASE_URL="http://alidns.aliyuncs.com", 
    ACCESS_KEY_ID="<AccessKey>", 
    ACCESS_KEY_SECRET="<AccessKey Secret>"
)

print(dns.DescribeDomainRecords(
    DomainName="<你的主域名>", 
    PageSize=100
))
print(dns.AddDomainRecord(
    DomainName="<你的主域名>", 
    RR="<你的子域名>", 
    Type="<解析地址类型>", 
    Value="<解析地址>", 
    Line="default", 
    TTL=600
))
print(dns.DeleteDomainRecord(
    RecordId="<解析记录编号>"
))
```

