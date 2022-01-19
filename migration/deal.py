
import json
import services.bitrix24_service as bx24
from datetime import datetime, timedelta


def HaravanToBitrix24(ha):

    bx = {}

    # bx['ID'] = ha.get('id' , 0) # set value ở haravab_to_bitrix24
    # tên Deal
    bx['TITLE'] = 'Haravan Order ' + \
        ha.get('name', 'not_found').replace("#", "")
    #
    bx['ADDITIONAL_INFO'] = ha.get('note', 'no information')
    bx['OPPORTUNITY'] = ha.get('total_price', 0)
    # bx['DATE_CREATE'] = datetime.strptime(ha['created_at'][0:10],'%Y-%m-%d')
    # bx['DATE_CREATE'] = ha.get('created_at',datetime.now())[0:10]
    # bx['BEGINDATE'] = ha.get('created_at',datetime.now())[0:10]

    # contact_id =  bx24.getContactIDbyPhone(ha['customer']['phone'] or ha['billing_address']['phone'])[0] or [{'ID':'0'}]['ID']
    # bx['CONTACT_ID'] = contact_id

    bx['CURRENCY_ID'] = "VND"
    bx['IS_MANUAL_OPPORTUNITY'] = "N"
    bx['CATEGORY_ID'] = "18"
    bx['STAGE_SEMANTIC_ID'] = "P"

    # Bitrix
    #
    # Đặt hàng thành công = C18:NEW
    # Chuyển đơn cho sản xuất = C18:4
    # Đang chuyển về showroom = C18:6
    # Đã nhận và đang đóng gói = C18:5
    # Đã giao cho nhà vận chuyển = C18:PREPARATION
    #
    # ĐƠN HÀNG TREO = C18:LOSE
    #
    # Haravan
    # financial_status - Trạng thái của các khoản thanh toán
    # pending: Các khoản thanh toán đang chờ xử lý. Thanh toán có thể không thành công ở trạng thái này. Kiểm tra lại để xác nhận xem các khoản thanh toán đã được thanh toán thành công hay chưa.
    # authorized: Các khoản thanh toán đã được ủy quyền.
    # partially_paid: Đơn hàng đã được thanh toán một phần.
    # paid: Các khoản thanh toán đã được thanh toán.
    # partially_refunded: Các khoản thanh toán đã được hoàn trả một phần.
    # refunded: Các khoản thanh toán đã được hoàn trả.
    # voided: Các khoản thanh toán đã bị vô hiệu.

    # fulfillment_status - Trạng thái của đơn hàng về các mục hàng đã đáp ứng
    # notfulfilled
    # fulfilled: Mọi chi tiết đơn hàng trong đơn đặt hàng đã được hoàn thành.
    # null: Không có chi tiết đơn hàng nào trong đơn đặt hàng đã được đáp ứng.
    # partial: Ít nhất một mục hàng trong đơn hàng đã được đáp ứng.
    # restocked: Mọi chi tiết đơn hàng trong đơn đặt hàng đã được bổ sung và đơn đặt hàng đã bị hủy.

    # Kiểm tra trạng thái của đơn hàng

    # 12-01-2022: Huỷ không cập nhật Trạng thái từ Haravan --> Bx24
    # order_status = ha["order_processing_status"]

    # fulfillment_status = ha["fulfillment_status"] # Trạng thái của đơn hàng

    # financial_status = ha["financial_status"] # Trạng thái thanh toán của đơn hàng

    # if order_status == "complete":
    #     bx['STAGE_ID'] = "C18:WON"
    # elif order_status == "cancel":
    #     bx['STAGE_ID'] = "C18:LOSE"
    # elif order_status == "confirmed" and fulfillment_status == "notfulfilled":
    #     bx['STAGE_ID'] = "C18:NEW"
    # elif order_status == "confirmed" and fulfillment_status == "notfulfilled" and financial_status == "pending":
    #     bx['STAGE_ID'] = "C18:NEW"
    # elif order_status == "confirmed" and fulfillment_status == "notfulfilled" and financial_status == "paid":
    #     bx['STAGE_ID'] = "C18:P"

    # Đơn hàng Haravan
    bx['UF_CRM_1630416306053'] = ha.get('name', 'not found name')  # mã đơn
    bx['UF_CRM_1623725469652'] = 'https://blusaigon.myharavan.com/admin/orders/' + \
        str(ha.get('id', 0))  # đơn hàng haravan
    bx['UF_CRM_1623809034975'] = str(ha.get('id', 0))  # haravan ID
    bx['UF_CRM_1627457986'] = ha.get(
        'note', 'Không tìm thấy ghi chú')  # ghi chú đơn hàng
    # bx['UF_CRM_1628149922667'] = ha.get('fulfillment_status','Chưa rõ trạng thái') # trạng thái đơn hàng
    # bx['UF_CRM_1628149948721'] = ha.get('financial_status','pending') # trạng thái thanh toán
    # bx['UF_CRM_1628149984252'] = ha.get('order_processing_status','confirmed') # trạng thái giao hàng

    changed = ""
    order_status = ha.get("order_processing_status", "")

    # Trạng thái đơn hàng: 'UF_CRM_1641976282':
    changed = ""
    # Verified 419
    if order_status.upper() in ["VERIFIED", "CONFIRMED"]:
        changed = "419"
    # Change location 421
    if order_status.upper() in ["CHANGE LOCATION","CHANGE_LOCATION","CHANGELOCATION"]:
        changed = "421"
    # Available confirmed 423
    if order_status.upper() in ["AVAILABLE CONFIRMED","AVAILABLE_CONFIRMED","AVAILABLECONFIRMED"]:
        changed = "423"
    # Out of stock 425
    if order_status.upper() in ["OUT OF STOCK","OUT_OF_STOCK","OUTOFSTOCK"]:
        changed = "425"
    # Exported 427
    if order_status.upper() in ["EXPORTED", "EXPORT_CONFIRM"]:
        changed = "427"
    # On transported 429
    if order_status.upper() in ["ON TRANSPORTED","ON_TRANSPORTED","ONTRANSPORTED"]:
        changed = "429"
    # Self delivery 431
    if order_status.upper() in ["SELF DELIVERY","SELF_DELIVERY","SELFDELIVERY"]:
        changed = "431"
    # Completed 433
    if order_status.upper() in ["COMPLETED","COMPLETE"]:
        changed = "433"

    bx['UF_CRM_1641976282'] = changed

    financial_status = ha.get("financial_status", "")

    # Trạng thái thanh toán 'UF_CRM_1641976342':
    changed = ""
    # Paid 337
    if financial_status.upper() in ["PAID"]:
        changed = "337"
    # Partially refund 339
    if financial_status.upper() in ["PARTIALLY REFUND","PARTIALLY_REFUND","PARTIALLYREFUND"]:
        changed = "339"
    # Partially paid 341
    if financial_status.upper() in ["PARTIALLY PAID","PARTIALLY_PAID","PARTIALLYPAID"]:
        changed = "341"
    # Pending 343
    if financial_status.upper() in ["PENDING"]:
        changed = "343"
    # Refunded 345
    if financial_status.upper() in ["REFUNDED"]:
        changed = "345"
    # Unpaid 347
    if financial_status.upper() in ["UNPAID"]:
        changed = "347"
    # Canceled 349
    if financial_status.upper() in ["CANCELED"]:
        changed = "349"

    bx['UF_CRM_1641976342'] = changed

    # Trạng thái của đơn hàng
    
    fulfillment_status = ha.get("fulfillment_status", "")
    if len(ha.get('fulfillments')) > 0:        
        fulfillment_status = ha['fulfillments'][0].get("carrier_status_code","NOTFULFILLED")    

    # Trạng thái giao hàng 'UF_CRM_1641976377': '',
    changed = ""
    # Ready 359
    if fulfillment_status.upper() in ["READY","READYTOPICK"]:
        changed = "359"
    # Picking up 361
    if fulfillment_status.upper() in ["PICKING"]:
        changed = "361"
    # On the way 363
    if fulfillment_status.upper() in ["ON THE WAY","ON_THE_WAY","ONTHEWAY","DELIVERING"]:
        changed = "363"
    # Delivered 365
    if fulfillment_status.upper() in ["DELIVERED","FULFILLED"]:
        changed = "365"
    # Delivery canceled 367
    if fulfillment_status.upper() in ["DELIVERY CANCELED","DELIVERY_CANCELED","DELIVERYCANCELED"]:
        changed = "367"
    # Return 369
    if fulfillment_status.upper() in ["RETURN"]:
        changed = "369"
    # Waiting to deliver 371
    if fulfillment_status.upper() in ["WAITING TO DELIVER","WAITING_TO_DELIVER","WAITINGTODELIVER"]:
        changed = "371"
    # Customer absent 373
    if fulfillment_status.upper() in ["CUSTOMER ABSENT","CUSTOMER_ABSENT","CUSTOMERABSENT"]:
        changed = "373"
    # Waiting for return 375
    if fulfillment_status.upper() in ["WAITING FOR RETURN","WAITINGFORRETURN"]:
        changed = "375"
    # Not finished 377
    if fulfillment_status.upper() in ["NOT FINISHED", 'NOTFULFILLED',"NOTFINISHED"]:
        changed = "377"
    # Processing failed 379
    if fulfillment_status.upper() in ["PROCESSING FAILED"]:
        changed = "379"

    bx['UF_CRM_1641976377'] = changed

    # More
    #
    # bx['UF_CRM_1630417157521'] = 'HARAVAN-BITRIX APP' # người tạo đơn
    bx['UF_CRM_1630417292478'] = ha.get(
        'source_name', 'not found source_name')  # Kênh bán hàng

    # print('HaravanToBitrix24',bx)
    return bx


def Bitrix24ToHaravan(bx):
    ha = {}

    ha['id'] = 999  # ???
    ha['name'] = bx.TITLE

    return ha


def CompareHaravanNewData(deal_order, payload):
    try:
        old = json.loads(deal_order.get('haravan_data'))
        new = payload

        if old.get('billing_address') != new.get('billing_address'):
            return False

        if old.get('financial_status') != new.get('financial_status'):
            return False

        if old.get('fulfillment_status') != new.get('fulfillment_status'):
            return False

        if old.get('line_items') != new.get('line_items'):
            return False

        if old.get('name') != new.get('name'):
            return False

        if old.get('note') != new.get('note'):
            return False

        if old.get('shipping_address') != new.get('shipping_address'):
            return False

        if old.get('cancelled_status') != new.get('cancelled_status'):
            return False

        if old.get('confirmed_status') != new.get('confirmed_status'):
            return False

        if old.get('order_processing_status') != new.get('order_processing_status'):
            return False
    except:
        return False

    return True


def CompareBitrixNewData(deal_order, payload):
    old = json.loads(deal_order.get('bitrix_data'))
    new = payload

    if old.get('TITLE') != new.get('TITLE'):
        return False

    if old.get('ADDITIONAL_INFO') != new.get('ADDITIONAL_INFO'):
        return False

    if old.get('OPPORTUNITY') != new.get('OPPORTUNITY'):
        return False

    if old.get('STAGE_SEMANTIC_ID') != new.get('STAGE_SEMANTIC_ID'):
        return False

    return True


def replaceString(str):
    return str
