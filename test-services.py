from services import bitrix24_service

# print(bitrix24_service.Deal.get(57113))

# id = 5665
# while id < 5715:
#     data = bitrix24_service.Deal.get(id)
#     if data:
#         ha_id = data.get('UF_CRM_1623809034975',None)
#         if ha_id:
#             print(ha_id,id)

#     id +=2

list = [5683
, 5687
, 5689
, 5691
, 5693
, 5695
, 5697
, 5699
, 5701
, 5705
, 5707]

for id in list:
    bitrix24_service.Deal.delete(id)


