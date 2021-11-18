from services import haravan_to_bitrix, bitrix_to_haravan

from mysqldb.dao.DealDAO import DealDAO 

from mysqldb.dao.ProductDAO import ProductDAO 

haravan_id = 1016557495

body_update = {"body_html":'test HTML here',"body_plain":None,"created_at":"2021-11-15T23:42:02.285Z","handle":"test-product","id":1037021632,"images":[],"product_type":"Khác","published_at":"2021-11-15T23:41:55.742Z","published_scope":"global","tags":None,"template_suffix":"product","title":"test product","updated_at":"2021-11-15T23:42:02.289Z","variants":[{"barcode":None,"compare_at_price":0,"created_at":"2021-11-15T23:42:02.285Z","fulfillment_service":None,"grams":0,"id":1080634682,"inventory_management":"haravan","inventory_policy":"deny","inventory_quantity":0,"position":1,"price":0,"product_id":1037021632,"requires_shipping":True,"sku":None,"taxable":True,"title":"Default Title","updated_at":"2021-11-15T23:42:02.289Z","image_id":None,"option1":"Default Title","option2":None,"option3":None,"inventory_advance":{"qty_available":0,"qty_onhand":0,"qty_commited":0,"qty_incoming":0}}],"vendor":"Khác","options":[{"name":"Title","id":2508368083,"position":1,"product_id":1037021632}],"only_hide_from_list":False,"metafields_global_title_tag":"test product","metafields_global_description_tag":None,"not_allow_promotion":False}

# haravan_to_bitrix.create_product_bitrix(body_update)

haravan_to_bitrix.update_product_bitrix(body_update)
