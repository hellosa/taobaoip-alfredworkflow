#!/usr/bin/env python
# coding=utf8

import urllib2
import json
from xml.etree.ElementTree import Element, SubElement
from xml.etree import ElementTree
from xml.dom import minidom
import hashlib
import sys

"""
a response example:

{
    "code": 0,
    "data": {
        "area": "\u534e\u5317",
        "area_id": "100000",
        "city": "\u5317\u4eac\u5e02",
        "city_id": "110000",
        "country": "\u4e2d\u56fd",
        "country_id": "CN",
        "county": "",
        "county_id": "-1",
        "ip": "61.135.255.144",
        "isp": "\u8054\u901a",
        "isp_id": "100026",
        "region": "\u5317\u4eac\u5e02",
        "region_id": "110000"
    }
}

a feedback example:

<?xml version="1.0"?>
<items>
<item uid="8c476bd3b3a74629f393afcd6e724316" arg="北京市 联通">
<title>北京市 联通</title>
<subtitle>本站主数据</subtitle>
<icon>icon.png</icon>
</item>
<item uid="8c476bd3b3a74629f393afcd6e724316" arg="北京市 联通">
<title>北京市 联通</title>
<subtitle>参考数据一</subtitle>
<icon>icon.png</icon>
</item>
</items>

"""


def generate_feedback(ip, title, subtitle):
    items = Element('items')
    uid = hashlib.md5(ip).hexdigest()
    arg = title
    item = SubElement(items, 'item', {'uid': uid, 'arg': arg})
    element_item_title = SubElement(item, 'title')
    element_item_title.text = title
    element_item_subtitle = SubElement(item, 'subtitle')
    element_item_subtitle.text = subtitle
    element_item_icon = SubElement(item, 'icon')
    element_item_icon.text = "icon.png"

    rough_string = ElementTree.tostring(items, 'utf-8')
    #print rough_string
    print minidom.parseString(rough_string).toprettyxml(indent="    ")

ip = sys.argv[1]
ip_taobao_api_url = "http://ip.taobao.com/service/getIpInfo.php?ip="

f = urllib2.urlopen(ip_taobao_api_url + ip)
#print f.read()

result = json.loads(f.read())
# return code: 0: success, 1: failed
#code result["code"]
area = result["data"]["area"]
city = result["data"]["city"]
country = result["data"]["country"]
isp = result["data"]["isp"]
region = result["data"]["region"]

title = "%s %s %s" % (country, region, city)
subtitle = "%s %s" % (area, isp)

generate_feedback(ip, title, subtitle)
