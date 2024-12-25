-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Dec 06, 2023 at 06:16 AM
-- Server version: 10.4.28-MariaDB
-- PHP Version: 8.2.4

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `project_qrcode`
--

-- --------------------------------------------------------

--
-- Table structure for table `bang_gia`
--

CREATE TABLE `bang_gia` (
  `loai_xe` varchar(50) NOT NULL,
  `phi_xe` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `bang_gia`
--

INSERT INTO `bang_gia` (`loai_xe`, `phi_xe`) VALUES
('Xe khác', 3000),
('Xe máy', 2000),
('Xe ô tô', 10000),
('Xe đạp', 500),
('Xe đạp điện', 1000);

-- --------------------------------------------------------

--
-- Table structure for table `phuong_tien`
--

CREATE TABLE `phuong_tien` (
  `bien_so` varchar(20) NOT NULL,
  `mssv` varchar(50) NOT NULL,
  `loai_xe` varchar(100) NOT NULL,
  `ten_xe` varchar(100) NOT NULL,
  `mau_xe` varchar(100) NOT NULL,
  `anh_xe_dang_ky` text NOT NULL,
  `dung_tich` varchar(20) NOT NULL,
  `so_khung` varchar(30) NOT NULL,
  `so_may` varchar(30) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `phuong_tien`
--

INSERT INTO `phuong_tien` (`bien_so`, `mssv`, `loai_xe`, `ten_xe`, `mau_xe`, `anh_xe_dang_ky`, `dung_tich`, `so_khung`, `so_may`) VALUES
('65a1', 'b2', 'Xe máy', 'sh', 'do', 'C:/project_qrcode_old_3cam/img/sample/main-bike-blue-catalogue-1654.jpg', '122', 'a12', 'a12');

-- --------------------------------------------------------

--
-- Table structure for table `quan_ly_gui_xe`
--

CREATE TABLE `quan_ly_gui_xe` (
  `stt` int(11) NOT NULL,
  `mssv` varchar(50) NOT NULL,
  `ma_qr` text NOT NULL,
  `thoi_gian_vao` datetime NOT NULL,
  `thoi_gian_ra` datetime NOT NULL,
  `anh_pTruoc_luc_vao` text NOT NULL,
  `anh_pSau_luc_vao` text NOT NULL,
  `anh_pTruoc_luc_ra` text NOT NULL,
  `anh_pSau_luc_ra` text NOT NULL,
  `trang_thai` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `user`
--

CREATE TABLE `user` (
  `mssv` varchar(20) NOT NULL,
  `ten` varchar(50) NOT NULL,
  `anh_nguoi_dang_ky` text NOT NULL,
  `gioi_tinh` varchar(10) NOT NULL,
  `ma_qr` text NOT NULL,
  `ngay_dang_ky` date NOT NULL,
  `ngay_het_han` date NOT NULL,
  `thoi_han` varchar(20) NOT NULL,
  `sdt` varchar(20) NOT NULL,
  `email` varchar(100) NOT NULL,
  `phi_nop` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `user`
--

INSERT INTO `user` (`mssv`, `ten`, `anh_nguoi_dang_ky`, `gioi_tinh`, `ma_qr`, `ngay_dang_ky`, `ngay_het_han`, `thoi_han`, `sdt`, `email`, `phi_nop`) VALUES
('b2', 'loc', 'C:/project_qrcode_old_3cam/img/sample/images.jpg', 'Nam', '1128285099327371709', '2000-01-01', '2000-01-02', '1 ngày', '1111-111-111', 'loc@gmail.com', 2000);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `bang_gia`
--
ALTER TABLE `bang_gia`
  ADD PRIMARY KEY (`loai_xe`);

--
-- Indexes for table `phuong_tien`
--
ALTER TABLE `phuong_tien`
  ADD PRIMARY KEY (`bien_so`),
  ADD KEY `mssv_ngoai` (`mssv`),
  ADD KEY `loai_xe_ngoai` (`loai_xe`);

--
-- Indexes for table `quan_ly_gui_xe`
--
ALTER TABLE `quan_ly_gui_xe`
  ADD PRIMARY KEY (`stt`),
  ADD KEY `mssv5` (`mssv`);

--
-- Indexes for table `user`
--
ALTER TABLE `user`
  ADD PRIMARY KEY (`mssv`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `quan_ly_gui_xe`
--
ALTER TABLE `quan_ly_gui_xe`
  MODIFY `stt` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=26;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `phuong_tien`
--
ALTER TABLE `phuong_tien`
  ADD CONSTRAINT `loai_xe_ngoai` FOREIGN KEY (`loai_xe`) REFERENCES `bang_gia` (`loai_xe`),
  ADD CONSTRAINT `mssv2` FOREIGN KEY (`mssv`) REFERENCES `user` (`mssv`),
  ADD CONSTRAINT `mssv_ngoai` FOREIGN KEY (`mssv`) REFERENCES `user` (`mssv`);

--
-- Constraints for table `quan_ly_gui_xe`
--
ALTER TABLE `quan_ly_gui_xe`
  ADD CONSTRAINT `mssv5` FOREIGN KEY (`mssv`) REFERENCES `user` (`mssv`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
