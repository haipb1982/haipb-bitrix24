
import services.bitrix24_service as bx24
from datetime import datetime, timedelta
def HaravanToBitrix24(ha):
    
    bx = {}    
    bx['ID'] = ha.get('id' , 0)
    bx['TITLE'] = 'Haravan Order ' + ha.get('name', 'not_found')
    bx['ADDITIONAL_INFO'] = ha.get('note', 'no information')
    bx['OPPORTUNITY'] = ha.get('total_price', 0)
    # bx['DATE_CREATE'] = datetime.strptime(ha['created_at'][0:10],'%Y-%m-%d')
    bx['DATE_CREATE'] = ha.get('created_at')[0:10]
    bx['BEGINDATE'] = ha.get('created_at')[0:10]

    contact_id =  bx24.getContactIDbyPhone(ha['customer']['phone'] or ha['billing_address']['phone'])[0] or [{'ID':'0'}]['ID']
    bx['CONTACT_ID'] = contact_id
    bx['STAGE_ID'] = "C18:NEW"
    bx['CURRENCY_ID'] = "VND"
    bx['IS_MANUAL_OPPORTUNITY'] = "N"
    bx['CATEGORY_ID'] = "18"
    bx['STAGE_SEMANTIC_ID'] = "P"

    print('HaravanToBitrix24',bx)

    return bx


def Bitrix24ToHaravan(bx):
    ha = {}
    
    ha['id'] = 999 #???
    ha['name'] = bx.TITLE

    return ha

def replaceString(str):
    return str