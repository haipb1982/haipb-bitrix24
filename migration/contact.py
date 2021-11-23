

def HaravanToBitrix24(ha):

    bx = {}

    default_address = ha.get("default_address")

    # Set giá trị address cho bitrix từ haravan
    if default_address:
        bx["ADDRESS"] = default_address.get("address1")
        bx["ADDRESS_2"] = default_address.get("address2")
        bx["ADDRESS_CITY"] = default_address.get("city")
        bx["ADDRESS_COUNTRY"] = default_address.get("country")
        bx["ADDRESS_COUNTRY_CODE"] = default_address.get("country_code")
        bx["ADDRESS_POSTAL_CODE"] = default_address.get("zip")
        bx["ADDRESS_PROVINCE"] = default_address.get("province")
        # bx["ADDRESS_REGION"] = default_addres.get("")

    # Set giá trị company
    # bx["COMPANY_ID"] = ""

    # bx["DATA_CREATE"] = ha.get("created_at")
    # bx["DATA_MODIFY"] = ha.get("updated_at")

    bx["EMAIL"] = ha.get("email")
    bx["PHONE"] = ha.get("phone")

    bx["NAME"] = ha.get("last_name")
    bx["LAST_NAME"] = ha.get("last_name")
    bx["SECOND_NAME"] = ha.get("email")
    bx["BIRTHDAY"] = ha.get("birthday")

    # TODO: Sẽ cần mapping dữ liệu custom field ở đây