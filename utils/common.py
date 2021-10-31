import base64
import decimal
import json
import re

from .model import Payload

from . import log
LOGGER = log.get_logger(__name__)

RESPONSE_HEADERS = {
    # 'Access-Control-Allow-Headers': 'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token,x-requested-with',
    # 'Access-Control-Allow-Methods': 'GET, POST, PUT, PATCH, DELETE, OPTIONS',
    # 'Access-Control-Allow-Origin': '*',
    # 'Allow': 'GET, POST, PUT, PATCH, DELETE, OPTIONS',
    'Content-Type': 'application/json'
}

class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            if o % 1 > 0:
                return float(o)
            else:
                return int(o)
        return super(DecimalEncoder, self).default(o)

def decimal_default(obj):
    if isinstance(obj, decimal.Decimal):
        return int(obj)

def build_response(status_code, payload):
    # LOGGER.info("Common::build_response : ", extra={"payload": payload})
    # body = {}
    # if payload is not None:
    #     # response["body"] = json.dumps(payload, default=decimal_default, indent=4, ensure_ascii=False)
    #     body = json.dumps(payload, cls=DecimalEncoder, indent=4, ensure_ascii=False)
    # LOGGER.info("Common::response : ", extra={"status" :status_code, "body": body})
    return payload, status_code, RESPONSE_HEADERS

def build_response_200(message=None, data=None):
    payload = Payload(message, data).toJSON()
    return build_response(200, payload)


def build_response_400(message, data=None):
    payload = Payload(message, data, 1).toJSON()
    return build_response(400, payload)

def build_response_500(message, data=None):
    payload = Payload(message, data, 1).toJSON()
    return build_response(500, payload)

def dict_get_lower_key(data, key):
    d_lower = dict((k.lower(), v) for k, v in data.items())
    return d_lower.get(key)


def is_email(email):
    REGEX_EMAIL = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
    return True if re.search(REGEX_EMAIL,email) else False

def encrypt_data(data):
    encoded = base64.b64encode(data.encode("utf-8"))
    return encoded.decode("utf-8")

def decrypt_data(data):
    try:
        return base64.b64decode(data.encode("utf-8")).decode("utf-8")
    except Exception as e:
        LOGGER.debug(f"utils.decrypt_data:: Exception when decrypt data: {str(e)}")
        return None