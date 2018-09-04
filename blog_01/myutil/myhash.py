"""
密码加密
"""
import hashlib

def mysha256(password):

    h = hashlib.sha256()
    h.update(password.encode('utf-8'))
    return h.hexdigest()