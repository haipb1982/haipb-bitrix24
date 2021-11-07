
--
-- Database: `sql6449388`
--

-- --------------------------------------------------------

--
-- Table structure for table `tbl_deal_order`
--

CREATE TABLE `tbl_deal_order` (
  `id` int(4) NOT NULL,
  `haravan_id` int(4) NOT NULL,
  `bitrix24_id` int(4) NOT NULL,
  `haravan_data` text NOT NULL,
  `bitrix_data` text NOT NULL,
  `status` varchar(50) NOT NULL,
  `update_ts` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `tbl_deal_order`
--
ALTER TABLE `tbl_deal_order`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `haravan_id` (`haravan_id`),
  ADD UNIQUE KEY `bitrix24_id` (`bitrix24_id`);
COMMIT;

