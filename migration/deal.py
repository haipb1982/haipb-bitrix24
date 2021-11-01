
import services.bitrix24_service as bx24
from datetime import datetime, timedelta
def HaravanToBitrix24(ha):

    bx = {}    
    bx['ID'] = ha['id'] or 0
    bx['TITLE'] = 'Haravan Order ' + (ha['name'] or 'not_found')
    bx['ADDITIONAL_INFO'] = ha['note'] or 'no information'
    bx['OPPORTUNITY'] = ha['total_price']
    # bx['DATE_CREATE'] = datetime.strptime(ha['created_at'][0:10],'%Y-%m-%d')
    bx['DATE_CREATE'] = ha['created_at'][0:10]
    bx['BEGINDATE'] = ha['created_at'][0:10]

    contact_id =  bx24.getContactIDbyPhone(ha['customer']['phone'] or ha['billing_address']['phone'])[0]['ID'] or 0
    bx['CONTACT_ID'] = contact_id
    bx['STAGE_ID'] = "C18:NEW"
    bx['CURRENCY_ID'] = "VND"
    bx['IS_MANUAL_OPPORTUNITY'] = "N"
    bx['CATEGORY_ID'] = "18"
    bx['STAGE_SEMANTIC_ID'] = "P"

    return bx


def Bitrix24ToHaravan(bx):
    ha = {}
    
    ha['id'] = 999 #???
    ha['name'] = bx.TITLE

    return ha
