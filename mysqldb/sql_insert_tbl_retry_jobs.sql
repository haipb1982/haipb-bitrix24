INSERT INTO tbl_retry_job(haravan_id, bitrix24_id, haravan_data, bitrix_data, type, action)

SELECT haravan_id, NULL, haravan_data, NULL, 'ORDERS', 'UPDATED' FROM tbl_deal_order LIMIT 1