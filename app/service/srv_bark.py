# coding=utf8
import base64,json,requests,random

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import algorithms, modes, Cipher
from cryptography.hazmat.primitives.ciphers.algorithms import AES

# bark专属加密方法
def bark_encrypt_payload(
        payload:bytes,aes_key:bytes,aes_iv:bytes):
    
    '''
    通过AES-256-CBC with PKCS7 padding进行加密
    '''

    # Add padding to the payload
    padder = padding.PKCS7(AES.block_size).padder()
    padded_data = padder.update(payload) + padder.finalize()

    # Create the cipher
    cipher = Cipher(algorithms.AES(aes_key), modes.CBC(aes_iv), backend=default_backend())

    # Encrypt the padded data
    encryptor = cipher.encryptor()
    encrypted = encryptor.update(padded_data) + encryptor.finalize()

    # Return the Base64 encoded ciphertext
    return base64.b64encode(encrypted).decode()

def send_bark_nfy(**kwargs):

    defaults = {
        'title': None,
        'body': None,
        'level': None,
        'autoCopy': None,
        'copy': None,
        'sound': None,
        'icon': None,
        'group': None,
        'isArchive': 1,
        'url': None
    }

    for k,v in defaults.items():
        defaults[k] = kwargs.get(k,v)

    cleaned_data = {k: v for k, v in defaults.items() if v}

    try:
        url = kwargs.get('chnl_host',None) + '/' + kwargs.get('device_key',None)
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}

        json_data = json.dumps(cleaned_data,ensure_ascii=False)
        encryption_iv = bytes(random.randint(32, 126) for _ in range(16))
        encryption_key = kwargs.get('usr_key',None)
        encrypted_payload = bark_encrypt_payload(json_data.encode(), encryption_key.encode(), encryption_iv)

        payload = {
            'ciphertext': encrypted_payload,
            'iv': encryption_iv.decode()
        }

        auth_usr = kwargs.get('chnl_auth_usr',None)
        auth_pwd = kwargs.get('chnl_auth_pwd',None)

        response = requests.request('GET',url,headers=headers,data=payload,timeout=30,auth=(auth_usr,auth_pwd))

    except requests.RequestException as e:
        return 'request exception:' + str(e)
    except Exception as e:
        return 'fail to request:' + str(e)