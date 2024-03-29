CREATE TABLE `tbl_deal_order` (
  `id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT,
  `haravan_id` bigint(20) UNSIGNED NOT NULL,
  `bitrix24_id` bigint(20) UNSIGNED NOT NULL,
  `haravan_data` text ,
  `bitrix_data` text,
  `haravan_status` varchar(20) ,
  `bitrix_status` varchar(20) ,
  `update_ts` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

ALTER TABLE `tbl_deal_order`
  ADD UNIQUE KEY `haravan_id` (`haravan_id`),
  ADD UNIQUE KEY `bitrix24_id` (`bitrix24_id`);

CREATE TABLE `tbl_product` (
                                  `id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT,
                                  `haravan_id` bigint(20) UNSIGNED NOT NULL,
                                  `bitrix24_id` bigint(20) UNSIGNED NOT NULL,
                                  `haravan_data` text ,
                                  `bitrix_data` text,
                                  `haravan_status` varchar(20) ,
                                  `bitrix_status` varchar(20) ,
                                  `update_ts` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
                                  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

ALTER TABLE `tbl_product`
    ADD UNIQUE KEY `haravan_id` (`haravan_id`),
    ADD UNIQUE KEY `bitrix24_id` (`bitrix24_id`);

CREATE TABLE `tbl_contact_customer` (
                                  `id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT,
                                  `haravan_id` bigint(20) UNSIGNED NOT NULL,
                                  `bitrix24_id` bigint(20) UNSIGNED NOT NULL,
                                  `haravan_data` text ,
                                  `bitrix_data` text,
                                  `haravan_status` varchar(20) ,
                                  `bitrix_status` varchar(20) ,
                                  `update_ts` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
                                  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

ALTER TABLE `tbl_contact_customer`
    ADD UNIQUE KEY `haravan_id` (`haravan_id`),
    ADD UNIQUE KEY `bitrix24_id` (`bitrix24_id`);