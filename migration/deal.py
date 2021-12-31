
import json
import services.bitrix24_service as bx24
from datetime import datetime, timedelta
def HaravanToBitrix24(ha):
    
    bx = {}
        
    # bx['ID'] = ha.get('id' , 0) # set value ở haravab_to_bitrix24
    # tên Deal
    bx['TITLE'] = 'Haravan Order ' + ha.get('name', 'not_found').replace("#", "")
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

    order_status = ha["order_processing_status"]

    fulfillment_status = ha["fulfillment_status"] # Trạng thái của đơn hàng

    financial_status = ha["financial_status"] # Trạng thái thanh toán của đơn hàng

    if order_status == "complete":
        bx['STAGE_ID'] = "WIN"
    elif order_status == "cancel":
        bx['STAGE_ID'] = "C18:LOSE"
    elif order_status == "confirmed" and fulfillment_status == "notfulfilled":
        bx['STAGE_ID'] = "C18:NEW"
    elif order_status == "confirmed" and fulfillment_status == "notfulfilled" and financial_status == "pending":
        bx['STAGE_ID'] = "C18:NEW"
    elif order_status == "confirmed" and fulfillment_status == "notfulfilled" and financial_status == "paid":
        bx['STAGE_ID'] = "P"


    # Đơn hàng Haravan
    bx['UF_CRM_1637252157269'] = ha.get('name','New Order') # mã đơn
    bx['UF_CRM_1623725469652'] = 'https://blusaigon.myharavan.com/admin/orders/' + str(ha.get('id',0)) # đơn hàng haravan
    bx['UF_CRM_1623809034975'] = str(ha.get('id',0)) # haravan ID
    bx['UF_CRM_1627457986'] = ha.get('note','Không tìm thấy ghi chú') # ghi chú đơn hàng
    bx['UF_CRM_1628149922667'] = ha.get('fulfillment_status','Chưa rõ trạng thái') # trạng thái đơn hàng
    bx['UF_CRM_1628149984252'] = ha.get('order_processing_status','confirmed') # trạng thái giao hàng
    
    # More
    #
    # bx['UF_CRM_1630417157521'] = 'HARAVAN-BITRIX APP' # người tạo đơn
    bx['UF_CRM_1630417292478'] = ha.get('source_name','New Order') # Kênh bán hàng 

    # print('HaravanToBitrix24',bx)
    return bx


def Bitrix24ToHaravan(bx):
    ha = {}
    
    ha['id'] = 999 #???
    ha['name'] = bx.TITLE

    return ha

def CompareHaravanNewData(deal_order, payload):
    
    old = json.loads(deal_order.get('haravan_data'))
    new = payload

    if old.get('billing_address') != new.get('billing_address'):
        return  False

    if old.get('financial_status') != new.get('financial_status'):
        return  False

    if old.get('fulfillment_status') != new.get('fulfillment_status'):
        return  False

    if old.get('line_items') != new.get('line_items'):
        return  False

    if old.get('name') != new.get('name'):
        return  False

    if old.get('note') != new.get('note'):
        return  False
    
    if old.get('shipping_address') != new.get('shipping_address'):
        return  False
    
    if old.get('cancelled_status') != new.get('cancelled_status'):
        return  False
    
    if old.get('confirmed_status') != new.get('confirmed_status'):
        return  False
    
    if old.get('order_processing_status') != new.get('order_processing_status'):
        return  False
    
    return True

def CompareBitrixNewData(deal_order, payload):
    old = json.loads(deal_order.get('bitrix_data'))
    new = payload
    
    if old.get('TITLE') != new.get('TITLE'):
        return  False

    if old.get('ADDITIONAL_INFO') != new.get('ADDITIONAL_INFO'):
        return  False
    
    if old.get('OPPORTUNITY') != new.get('OPPORTUNITY'):
        return  False
    
    if old.get('STAGE_SEMANTIC_ID') != new.get('STAGE_SEMANTIC_ID'):
        return  False

    return True

def replaceString(str):
    return str