import json

product_mapping = [
    {
        "h_key": "title",
        "b_key": "NAME",
        "h_default_value": "123",
        "b_default_value": "123",
    },
    # {
    #     "h_key": "",
    #     "b_key": "PREVIEW_PICTURE"
    # },
    # {
    #     "h_key": "",
    #     "b_key": "DETAIL_PICTURE"
    # },
    # {
    #     "h_key": "body_html",
    #     "b_key": "DESCRIPTION" # Hien tai ko su dung dc vi bitrix k cho phep do dai qua lon
    # },
    {
        "h_key": "created_at",
        "b_key": "DATE_CREATE"
    },
    {
        "h_key": "",
        "b_key": "CURRENCY_ID",
        "b_default_value": "VND",
    },
    {
        "h_key": "",
        "b_key": "CREATED_BY"
    },
    {
        "h_key": "vendor",
        "b_key": "CATALOG_ID"
    },
    {
        "h_key": "",
        "b_key": "ACTIVE"
    },
    {
        "h_key": "handle",
        "b_key": "CODE"
    }
]

deal_mapping = [
    {
        "h_key": "name",
        "b_key": "TITLE",
    },
    {
        "h_key": "note",
        "b_key": "ADDITIONAL_INFO",
    },
    {
        "h_key": "total_price",
        "b_key": "OPPORTUNITY",
    },
]

contact_mapping = [
    {
        "h_key": "default_address.name",
        "b_key": "NAME",
    },
    {
        "h_key": "default_address.first_name",
        "b_key": "SECOND_NAME",
    },
    {
        "h_key": "default_address.last_name",
        "b_key": "LAST_NAME",
    },
    {
        "h_key": "default_address.address1",
        "b_key": "ADDRESS",
    },
    {
        "h_key": "default_address.city",
        "b_key": "ADDRESS_CITY",
    },
    {
        "h_key": "default_address.zip",
        "b_key": "ADDRESS_POSTAL_CODE",
    },
    {
        "h_key": "default_address.country",
        "b_key": "ADDRESS_COUNTRY",
    },
    {
        "h_key": "default_address.zip",
        "b_key": "ADDRESS_POSTAL_CODE",
    },
    {
        "h_key": "default_address.province",
        "b_key": "ADDRESS_PROVINCE",
    },
    {
        "h_key": "first_name",
        "b_key": "SECOND_NAME",
    },
    {
        "h_key": "last_name",
        "b_key": "LAST_NAME",
    },
    {
        "h_key": "default_address.address1",
        "b_key": "ADDRESS",
    },
    {
        "h_key": "",
        "b_key": "TYPE_ID",
        "b_default_value": "CLIENT",
    },
    {
        "h_key": "",
        "b_key": "OPENED",
        "b_default_value": "Y",
    },
]

# Hàm chỉ map những thuộc tính cơ bản giữa haravan và bitrix 24 theo field mapping định nghĩa trước
# Đối với việc mapping phức tạp sẽ phải mapping bằng tay
def convert_object(object: dict, mapping, type):
    if not type:
        return None
    if type == "HARAVAN":
        return bitrix_to_haravan(object, mapping)
    elif type == "BITRIX":
        return haravan_to_bitrix(object, mapping)
    return None

def bitrix_to_haravan(object, mapping):
    haravan = {}
    for item in mapping:
        if not item.get("h_key"):
            continue
        value = get_value(object, item["b_key"], item.get("h_default_value"))

        if not value:
            continue
        d = get_dict(item["h_key"], value)
        haravan = merge(haravan, d)
    return haravan

# Merge 2 dict thành 1 dict
def merge(source, destination):
    for key, value in source.items():
        if isinstance(value, dict):
            # get node or create one
            node = destination.setdefault(key, {})
            merge(value, node)
        else:
            destination[key] = value

    return destination

# Data của bitrix là 1 mặt phẳng ko phân chia cấp nên ko cần thiết phải set vào từng thành con
def haravan_to_bitrix(object, mapping):
    bitrix = {}
    for item in mapping:
        if not item.get("b_key"):
            continue
        value = get_value(object, item["h_key"], item.get("b_default_value"))
        if not value:
            continue

        bitrix[item["b_key"]] = value
    return bitrix


def get_value(object, key_item, default_value=""):
    bitrix_keys = key_item.split(".")
    value = object
    for b_k in bitrix_keys:
        if value.get(b_k) and isinstance(value.get(b_k), dict):
            value = value[b_k]
        # elif value.get(b_k) and any(x in ["[", "]"] for x in value[b_k]):
        #     value = value.get(b_k)[1:-1]
        else:
            value = value[b_k] if value.get(b_k) else default_value
            break
    return value if isinstance(value, str) else default_value


# Set giá trị cho haravan với data dạng kiểu default_address.name thành {"default_address": {"name": "Name"}}
def get_dict(key_item, value) -> dict:
    keys = key_item.split(".")
    data = {}
    i = 0
    for k in reversed(keys):
        if i == len(keys):
            break
        if i == 0:
            data[k] = value
        else:
            data1 = {}
            data1[k] = data
            data = data1
        i = i + 1
    return data

def set_data(d1: dict, d2: dict):
    d_temp1 = {}
    d_temp2 = {}
    for k in d1.keys():
        pass