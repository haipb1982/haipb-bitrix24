from datetime import datetime
from mysqldb.dao.DealDAO import DealDAO
from mysqldb.dao.RetryJobDAO import RetryJobDAO
from services import bitrix24_service, haravan_service, webapp_service, retryjob_service

# print(bitrix24_service.Deal.get(7713))

deal_dao = DealDAO()

retry_dao = RetryJobDAO()

# product = haravan_service.Product.getVariant(1036083436)
# product = haravan_service.Product.get(1028879920)

# print(product)

# order = haravan_service.Order.get(1261613090)
# print(order)

# product = {'NAME': 'Mạ Gold Titanium / M(0.7 mm) / Xanh', 'DATE_CREATE': '2019-01-01T02:37:46.219Z', 'CURRENCY_ID': 'VND', 'PRICE': 1499000.0, 'DISCOUNT_TYPE_ID': 1, 'DISCOUNT_SUM': None, 'PREVIEW_PICTURE': 'https://vnztech.com/no-image.png', 'DETAIL_PICTURE':  'https://vnztech.com/no-image.png'}

# bitrix24_data = bitrix24_service.Product.insert(fields=product)

# print(bitrix24_service.Product.get(6863))

# data_fields = {"TITLE": "Haravan Order WEB103339", "ADDITIONAL_INFO": "Kh\u1eafc: Danh s\u00e1ch \u0111\u01b0a sau:   \n\n+ 31 x\u1ea5p phong l\u00ec x\u00ec c\u1ee1 \u0111\u1ea1i, 5 phong/ x\u1ea5p.\n+ 8 set h\u1ed9p kh\u1ea9u trang kh\u00e1ng khu\u1ea9n cao c\u1ea5p.\n\nTh\u1eddi gian giao h\u00e0ng: Tr\u01b0\u1edbc 15h, 07.01.2022.\n\nB\u00caN A : C\u00d4NG TY TNHH TRUY\u1ec0N TH\u00d4NG LI\u00caN K\u1ebeT\n\u0110\u1ecba ch\u1ec9 : 27 Nguy\u1ec5n Th\u1ecb \u0110\u1ecbnh, Ph\u01b0\u1eddng An Ph\u00fa, TP. Th\u1ee7 \u0110\u1ee9c, TP. H\u1ed3 Ch\u00ed Minh\nM\u00e3 s\u1ed1 thu\u1ebf : 0314009892\n\nThanh to\u00e1n: chuy\u1ec3n kho\u1ea3n.\nKH c\u1ecdc 30% tr\u01b0\u1edbc khi s\u1ea3n xu\u1ea5t B\u00fat.\nKH thanh to\u00e1n 70% sau khi nh\u1eadn \u0111\u1ee7 h\u00e0ng h\u00f3a t\u1eeb 1 - 3 ng\u00e0y, theo th\u1ecfa thu\u1eadn h\u1ee3p \u0111\u1ed3ng mua b\u00e1n.\n\n\u0110en caro:\nNguy\u1ec5n Tr\u1ecdng H\u00e0o\nCh\u00e2u V\u0103n Tr\u1edf\t\nL\u00ea Tu\u1ea5n Anh\t\nPh\u1ea1m Xu\u00e2n D\u0169ng\t\n\nTr\u1eafng:\nTr\u1ea7n Kim Ph\u01b0\u1ee3ng\t\nNguy\u1ec5n Th\u1ecb Phan Th\u00fay\t\nPhan Th\u1ecb H\u1ed3ng \u0110\u1ee9c \t\n\nTr\u1eafng \u0110en aw\nPh\u1ea1m \u0110\u0103ng Tr\u1ecdng T\u01b0\u1eddng\t\nNguy\u1ec5n Thanh H\u00f9ng\t\nNguy\u1ec5n V\u0169 Ho\u00e0ng \nTr\u1ea7n Nguy\u00ean H\u00e0 \t\nPhan T\u1ea5n Thu\u1eadn  bsung \n\nCamPP:\nV\u0169 Th\u1ecb Ph\u01b0\u01a1ng Th\u1ea3o\t\nV\u00f5 Th\u1ecb \u0110oan Ph\u01b0\u1ee3ng\t\n\nH\u1ed3ng:\nTr\u1ea7n Nguy\u00ean \u00c1nh T\u00fa\t\nCh\u00e2u \u0110\u1ed7 T\u01b0\u1eddng Vi\t\n\n\u0110en caro:\nV\u0103n Th\u1ebf Trung\nPh\u00f9ng Nguy\u1ec5n Th\u1ebf Nguy\u00ean\n\nTr\u1eafng \u0111en WB:\nV\u00f5 Quang \u0110\u1ec9nh\t \nNguy\u1ec5n Tr\u1ea7n Nam  \nNguy\u1ec5n Huy Lu\u00e2n\t\n\nTr\u1eafng WW 0031:\nL\u00ea Th\u00e1i V\u00e2n Thanh\t\nL\u00ea Th\u1ecb Minh H\u1ed3ng\t\nL\u00ea Ng\u1ecdc Di\u1ec7p \nNguy\u1ec5n Th\u1ecb Kim Nhi \nV\u01b0\u01a1ng Th\u1ecb Ng\u1ecdc Lan \tB\u1ed5 sung  \n\nV\u00e0ng \nNguy\u1ec5n Th\u1ecb H\u1ed3ng Chuy\u00ean\t\nPh\u1ea1m Di\u1ec7p Thu\u1ef3 D\u01b0\u01a1ng\t\nT\u00f4n N\u1eef Minh Ph\u01b0\u01a1ng\t\nTr\u1ea7n Nguy\u1ec5n Nh\u01b0 Uy\u00ean\t\n\nCam \nL\u00fd Th\u1ecb M\u1ef9 Nhung\nTr\u1ea7n Ng\u1ecdc Kh\u00e1nh Nam", "OPPORTUNITY": 40775200, "CURRENCY_ID": "VND", "IS_MANUAL_OPPORTUNITY": "N", "CATEGORY_ID": "18", "STAGE_SEMANTIC_ID": "P", "STAGE_ID": "C18:NEW", "UF_CRM_1637252157269": "WEB103339", "UF_CRM_1623725469652": "https://blusaigon.myharavan.com/admin/orders/1258411229", "UF_CRM_1623809034975": "1258411229", "UF_CRM_1627457986": "Kh\u1eafc: Danh s\u00e1ch \u0111\u01b0a sau:   \n\n+ 31 x\u1ea5p phong l\u00ec x\u00ec c\u1ee1 \u0111\u1ea1i, 5 phong/ x\u1ea5p.\n+ 8 set h\u1ed9p kh\u1ea9u trang kh\u00e1ng khu\u1ea9n cao c\u1ea5p.\n\nTh\u1eddi gian giao h\u00e0ng: Tr\u01b0\u1edbc 15h, 07.01.2022.\n\nB\u00caN A : C\u00d4NG TY TNHH TRUY\u1ec0N TH\u00d4NG LI\u00caN K\u1ebeT\n\u0110\u1ecba ch\u1ec9 : 27 Nguy\u1ec5n Th\u1ecb \u0110\u1ecbnh, Ph\u01b0\u1eddng An Ph\u00fa, TP. Th\u1ee7 \u0110\u1ee9c, TP. H\u1ed3 Ch\u00ed Minh\nM\u00e3 s\u1ed1 thu\u1ebf : 0314009892\n\nThanh to\u00e1n: chuy\u1ec3n kho\u1ea3n.\nKH c\u1ecdc 30 tr\u01b0\u1edbc khi s\u1ea3n xu\u1ea5t B\u00fat.\nKH thanh to\u00e1n 70 sau khi nh\u1eadn \u0111\u1ee7 h\u00e0ng h\u00f3a t\u1eeb 1 - 3 ng\u00e0y, theo th\u1ecfa thu\u1eadn h\u1ee3p \u0111\u1ed3ng mua b\u00e1n.\n\n\u0110en caro:\nNguy\u1ec5n Tr\u1ecdng H\u00e0o\nCh\u00e2u V\u0103n Tr\u1edf\t\nL\u00ea Tu\u1ea5n Anh\t\nPh\u1ea1m Xu\u00e2n D\u0169ng\t\n\nTr\u1eafng:\nTr\u1ea7n Kim Ph\u01b0\u1ee3ng\t\nNguy\u1ec5n Th\u1ecb Phan Th\u00fay\t\nPhan Th\u1ecb H\u1ed3ng \u0110\u1ee9c \t\n\nTr\u1eafng \u0110en aw\nPh\u1ea1m \u0110\u0103ng Tr\u1ecdng T\u01b0\u1eddng\t\nNguy\u1ec5n Thanh H\u00f9ng\t\nNguy\u1ec5n V\u0169 Ho\u00e0ng \nTr\u1ea7n Nguy\u00ean H\u00e0 \t\nPhan T\u1ea5n Thu\u1eadn  bsung \n\nCamPP:\nV\u0169 Th\u1ecb Ph\u01b0\u01a1ng Th\u1ea3o\t\nV\u00f5 Th\u1ecb \u0110oan", "UF_CRM_1628149922667": "notfulfilled", "UF_CRM_1628149984252": "confirmed", "UF_CRM_1630417292478": "zalo", "ID": 5665}

# res = bitrix24_service.Deal.update(data_fields)
# print(res)

# res = webapp_service.get_sync('orders',1258983116)
# print(res)

# res = bitrix24_service.Deal.get(7655)
# print(res)

res = bitrix24_service.DealProductRow.get(7713)
print(res)

# webapp_service.check_duplicates()

# my_date = datetime.now()
# print(my_date.strftime('%Y-%m-%dT%H:%M:%S'))

# # res = haravan_service.Product.updateVariant(1063936869,{'updated_at': datetime.now().isoformat()})
# # res = haravan_service.Product.getVariant(1063936869)

# res = haravan_service.Customer.update(1023539137, {'updated_at': my_date.strftime('%Y-%m-%dT%H:%M:%S')})

# # res = haravan_service.Customer.get(1023539137)
# print(res)

# res =  retryjob_service.insert(haravan_id='1261838819',type='ORDERS')
# print(res)