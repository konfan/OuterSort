# coding=utf-8
import json

def _decode_list(data):
    rv = []
    for item in data:
        if isinstance(item, unicode):
            item = item.encode('utf-8')
        elif isinstance(item, list):
            item = _decode_list(item)
        elif isinstance(item, dict):
            item = _decode_dict(item)
        rv.append(item)
    return rv

def _decode_dict(data):
    rv = {}
    for key, value in data.iteritems():
        if isinstance(key, unicode):
           key = key.encode('utf-8')
        if isinstance(value, unicode):
           value = value.encode('utf-8')
        elif isinstance(value, list):
           value = _decode_list(value)
        elif isinstance(value, dict):
           value = _decode_dict(value)
        rv[key] = value
    return rv

def checktype(obj):
    assert type(obj) == dict
    assert obj.has_key('src')
    assert obj.has_key('dst')
    assert obj.has_key('opt')
    assert obj.has_key('type')

def decode(jsonstr):
    obj = json.loads(jsonstr, object_hook = _decode_dict)
    return obj

def encode(obj):
    return json.dumps(obj)
