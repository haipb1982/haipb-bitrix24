# Các trạng thái của bitrix:
## Trạng thái và Entity `crm.status.entity.types`
```
res = bx24.callMethod("crm.status.entity.types")
```
```json 
[
  {
    "ID": "STATUS",
    "NAME": "Lead statuses",
    "SEMANTIC_INFO": {
      "START_FIELD": "NEW",
      "FINAL_SUCCESS_FIELD": "CONVERTED",
      "FINAL_UNSUCCESS_FIELD": "JUNK",
      "FINAL_SORT": 0
    },
    "ENTITY_TYPE_ID": 1
  },
  {
    "ID": "SOURCE",
    "NAME": "Sources"
  },
  {
    "ID": "CONTACT_TYPE",
    "NAME": "Contact Type"
  },
  {
    "ID": "COMPANY_TYPE",
    "NAME": "Company Type"
  },
  {
    "ID": "EMPLOYEES",
    "NAME": "Employees"
  },
  {
    "ID": "INDUSTRY",
    "NAME": "Industry"
  },
  {
    "ID": "DEAL_TYPE",
    "NAME": "Deal Type"
  },
  {
    "ID": "INVOICE_STATUS",
    "NAME": "Invoice statuses",
    "SEMANTIC_INFO": {
      "START_FIELD": "N",
      "FINAL_SUCCESS_FIELD": "P",
      "FINAL_UNSUCCESS_FIELD": "D",
      "FINAL_SORT": 0
    }
  },
  {
    "ID": "DEAL_STAGE",
    "NAME": "Deal Stage",
    "SEMANTIC_INFO": {
      "START_FIELD": "NEW",
      "FINAL_SUCCESS_FIELD": "WON",
      "FINAL_UNSUCCESS_FIELD": "LOSE",
      "FINAL_SORT": 0
    },
    "FIELD_ATTRIBUTE_SCOPE": "",
    "ENTITY_TYPE_ID": 2
  },
  {
    "ID": "QUOTE_STATUS",
    "NAME": "Quote statuses",
    "SEMANTIC_INFO": {
      "START_FIELD": "DRAFT",
      "FINAL_SUCCESS_FIELD": "APPROVED",
      "FINAL_UNSUCCESS_FIELD": "DECLAINED",
      "FINAL_SORT": 0
    }
  },
  {
    "ID": "HONORIFIC",
    "NAME": "Salutations"
  },
  {
    "ID": "EVENT_TYPE",
    "NAME": "Event Type"
  },
  {
    "ID": "CALL_LIST",
    "NAME": "Call statuses"
  }
]
```

## crm.status.list Danh sách các phần tử thư mục đã lọc
- Lấy dữ liệu của trạng thái
- ENTITY_ID là crm status ID ở bước trên
```
res = bx24.callMethod("crm.status.list") # Lay trang thai va id cua stage deal
```
