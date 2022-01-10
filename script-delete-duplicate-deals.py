from mysqldb.dao.DealDAO import DealDAO
from mysqldb.dao.RetryJobDAO import RetryJobDAO
from services import bitrix24_service, haravan_service, webapp_service

# print(bitrix24_service.Deal.get(57113))

deal_dao = DealDAO()

retry_dao = RetryJobDAO()

# id = 2133

id = 7363
last_id = 7613 

print('GO GO GO')

while id < last_id + 2:
    # print(id)
    try:
        data = bitrix24_service.Deal.get(id)
        if data:
            ha_id = data.get('UF_CRM_1623809034975', None)
            if ha_id:
                # Nếu có ha_id tìm record tbl_deal_order
                dao = deal_dao.getDealOrderByHaID(ha_id)
                # print(dao)

                if dao['data']:
                    bx_id = dao['data'][0].get('bitrix24_id', None)

                    if bx_id:
                        # Nếu có bx_id so sánh với id
                        if not id == bx_id:
                            # Nếu id khác bx_id xoá Deal=id
                            bitrix24_service.Deal.delete(id)
                else:
                    # Nếu không có ha_id thêm mới record tbl_deal_order
                    print(deal_dao.addNewDeal(ha_id, id, None, None))
    except Exception as err:
        retry_dao.insertRetryJobRecord(bitrix24_id=id)
        print(f'ERROR {id}: ', err)

    id += 2

print('FINISH!!!')