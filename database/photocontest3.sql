-- phpMyAdmin SQL Dump
-- version 5.0.4
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Dec 15, 2020 at 09:34 AM
-- Server version: 10.4.16-MariaDB
-- PHP Version: 7.4.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `photocontest3`
--

-- --------------------------------------------------------

--
-- Table structure for table `accounts`
--

CREATE TABLE `accounts` (
  `id` int(255) NOT NULL,
  `username` varchar(50) NOT NULL,
  `email` varchar(50) NOT NULL,
  `password` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `accounts`
--

INSERT INTO `accounts` (`id`, `username`, `email`, `password`) VALUES
(1, 'palash', 'palash@gmail.com', 'palash');

-- --------------------------------------------------------

--
-- Table structure for table `contact`
--

CREATE TABLE `contact` (
  `sno` int(110) NOT NULL,
  `name` text NOT NULL,
  `email` varchar(50) NOT NULL,
  `phone_num` int(50) NOT NULL,
  `message` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `contact`
--

INSERT INTO `contact` (`sno`, `name`, `email`, `phone_num`, `message`) VALUES
(1, 'name', 'email@gmail.com', 96912751, 'kkk');

-- --------------------------------------------------------

--
-- Table structure for table `contestinfo`
--

CREATE TABLE `contestinfo` (
  `sno` int(50) NOT NULL,
  `name` text NOT NULL,
  `theme` text NOT NULL,
  `startson` date NOT NULL,
  `endson` date NOT NULL,
  `slug` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `register`
--

CREATE TABLE `register` (
  `sno` int(110) NOT NULL,
  `username` text NOT NULL,
  `email` varchar(110) NOT NULL,
  `image_id` varchar(110) NOT NULL,
  `image_name` varchar(50) NOT NULL,
  `description` varchar(110) NOT NULL,
  `slug` varchar(110) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `register`
--

INSERT INTO `register` (`sno`, `username`, `email`, `image_id`, `image_name`, `description`, `slug`) VALUES
(0, 'p1', 'email@gmail.com', '1sfhhOGDhhyXrd1YLHh2oyU5TofUbx9ul', 'image1', 'p11', '1sfhhOGDhhyXrd1YLHh2oyU5TofUbx9ul'),
(1, 'p2', 'dummy16174693@gmail.com', '13XOKLfv5MgWFe7LGIT3UBb4GOnmmDTJO', 'image2', 'p22', '13XOKLfv5MgWFe7LGIT3UBb4GOnmmDTJO'),
(2, 'p3', 'dummy16174693@gmail.com', '1lB5JWf_Vpky3T3T-BGrRe6vzRzatMYeQ', 'image3', 'p33', '1lB5JWf_Vpky3T3T-BGrRe6vzRzatMYeQ');

-- --------------------------------------------------------

--
-- Table structure for table `vote_count`
--

CREATE TABLE `vote_count` (
  `sno` int(255) NOT NULL,
  `user_email` varchar(50) NOT NULL,
  `vote` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `vote_count`
--

INSERT INTO `vote_count` (`sno`, `user_email`, `vote`) VALUES
(1, 'p1', 'p1'),
(2, 'p1', 'p1'),
(3, 'p1', 'p1'),
(4, 'p1', 'p1'),
(5, 'p1', 'p1'),
(6, 'p2', 'p2'),
(7, 'p2', 'p2'),
(8, 'p2', 'p2'),
(9, 'p3', 'p3'),
(10, 'palash@gmail.com', 'p1'),
(11, 'email.com', 'p3');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `accounts`
--
ALTER TABLE `accounts`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `contact`
--
ALTER TABLE `contact`
  ADD PRIMARY KEY (`sno`);

--
-- Indexes for table `contestinfo`
--
ALTER TABLE `contestinfo`
  ADD PRIMARY KEY (`sno`);

--
-- Indexes for table `register`
--
ALTER TABLE `register`
  ADD PRIMARY KEY (`sno`);

--
-- Indexes for table `vote_count`
--
ALTER TABLE `vote_count`
  ADD PRIMARY KEY (`sno`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `accounts`
--
ALTER TABLE `accounts`
  MODIFY `id` int(255) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `contact`
--
ALTER TABLE `contact`
  MODIFY `sno` int(110) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `contestinfo`
--
ALTER TABLE `contestinfo`
  MODIFY `sno` int(50) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `register`
--
ALTER TABLE `register`
  MODIFY `sno` int(110) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=12;

--
-- AUTO_INCREMENT for table `vote_count`
--
ALTER TABLE `vote_count`
  MODIFY `sno` int(255) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=19;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
