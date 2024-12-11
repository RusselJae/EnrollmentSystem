-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Dec 04, 2024 at 08:22 AM
-- Server version: 10.11.10-MariaDB
-- PHP Version: 8.0.28

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `enrollment_system`
--

-- --------------------------------------------------------

--
-- Table structure for table `app_cs_students`
--

CREATE TABLE `app_cs_students` (
  `id` int(11) NOT NULL,
  `student_number` int(50) NOT NULL,
  `first_name` varchar(50) NOT NULL,
  `middle_name` varchar(50) DEFAULT NULL,
  `last_name` varchar(50) NOT NULL,
  `suffix` varchar(50) DEFAULT NULL,
  `birthdate` date NOT NULL,
  `age` int(50) NOT NULL,
  `gender` varchar(50) NOT NULL,
  `program` varchar(50) NOT NULL,
  `year_level` varchar(50) NOT NULL,
  `section` int(50) NOT NULL,
  `status` varchar(50) NOT NULL,
  `email` varchar(50) NOT NULL,
  `mobile_number` varchar(50) NOT NULL,
  `soc_fee` varchar(100) NOT NULL,
  `date_enrolled` date DEFAULT NULL,
  `created_at` date NOT NULL,
  `updated_at` date NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `app_cs_students`
--

INSERT INTO `app_cs_students` (`id`, `student_number`, `first_name`, `middle_name`, `last_name`, `suffix`, `birthdate`, `age`, `gender`, `program`, `year_level`, `section`, `status`, `email`, `mobile_number`, `soc_fee`, `date_enrolled`, `created_at`, `updated_at`) VALUES
(2, 202211720, 'Russel Jae', 'Blanquera', 'Dahonog', NULL, '2004-09-27', 20, 'male', 'BS Computer Science', '3', 3, 'regular', 'neroooo27@gmail.com', '09692353537', 'paid', '2024-12-02', '2024-11-26', '2024-12-02'),
(5, 202211823, 'Ruel', NULL, 'Ramos', NULL, '2000-07-27', 24, 'male', 'BS Computer Science', '3', 3, 'regular', 'ruelramos@gmail.com', '09692353534', 'paid', NULL, '2024-12-02', '2024-12-02'),
(6, 202400001, 'Jay', '', 'Jay', '', '2004-07-22', 20, 'male', 'BS Computer Science', '1', 1, 'regular', 'jayjay@gmail.com', '09692353525', 'paid', NULL, '2024-12-02', '2024-12-02'),
(7, 202400002, 'Killua', '', 'Zoldyck', '', '2004-01-27', 20, 'male', 'BS Computer Science', '1', 1, 'regular', 'killua@gmail.com', '09692353505', 'paid', NULL, '2024-12-02', '2024-12-02'),
(8, 202400004, 'Anthony', NULL, 'San Diego', NULL, '2003-09-06', 21, 'male', 'BS Computer Science', '1', 3, 'regular', 'anthony@gmail.com', '09692253535', 'paid', '2024-12-02', '2024-12-02', '2024-12-02');

-- --------------------------------------------------------

--
-- Table structure for table `app_cs_students_sub`
--

CREATE TABLE `app_cs_students_sub` (
  `id` int(11) NOT NULL,
  `student_number` int(50) NOT NULL,
  `sub1` varchar(100) NOT NULL,
  `sub2` varchar(100) NOT NULL,
  `sub3` varchar(100) NOT NULL,
  `sub4` varchar(100) NOT NULL,
  `sub5` varchar(100) NOT NULL,
  `sub6` varchar(100) NOT NULL,
  `sub7` varchar(100) NOT NULL,
  `sub8` varchar(100) NOT NULL,
  `sub9` varchar(100) NOT NULL,
  `total_units` int(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `app_cs_students_sub`
--

INSERT INTO `app_cs_students_sub` (`id`, `student_number`, `sub1`, `sub2`, `sub3`, `sub4`, `sub5`, `sub6`, `sub7`, `sub8`, `sub9`, `total_units`) VALUES
(16, 202211720, 'GNED 02', 'GNED 05', 'GNED 11', 'COSC 50', '', '', '', '', '', 3),
(17, 202400004, 'GNED 02', '', '', '', '', '', '', '', '', 3);

-- --------------------------------------------------------

--
-- Table structure for table `app_it_students`
--

CREATE TABLE `app_it_students` (
  `id` int(11) NOT NULL,
  `student_number` int(50) NOT NULL,
  `first_name` varchar(50) NOT NULL,
  `middle_name` varchar(50) DEFAULT NULL,
  `last_name` varchar(50) NOT NULL,
  `suffix` varchar(50) DEFAULT NULL,
  `birthdate` date NOT NULL,
  `age` int(50) NOT NULL,
  `gender` varchar(50) NOT NULL,
  `program` varchar(50) NOT NULL,
  `year_level` varchar(50) NOT NULL,
  `section` varchar(50) NOT NULL,
  `status` varchar(50) NOT NULL,
  `email` varchar(50) NOT NULL,
  `mobile_number` varchar(50) NOT NULL,
  `soc_fee` varchar(100) NOT NULL,
  `date_enrolled` date DEFAULT NULL,
  `created_at` date NOT NULL,
  `updated_at` date NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `app_it_students`
--

INSERT INTO `app_it_students` (`id`, `student_number`, `first_name`, `middle_name`, `last_name`, `suffix`, `birthdate`, `age`, `gender`, `program`, `year_level`, `section`, `status`, `email`, `mobile_number`, `soc_fee`, `date_enrolled`, `created_at`, `updated_at`) VALUES
(2, 202211820, 'Vince Henry', 'Blanquera', 'Deres', NULL, '2004-10-15', 20, 'male', 'BS Information Technology', '3', '3', 'regular', 'vince15@gmail.com', '09992322322', 'paid', '2024-12-04', '2024-11-26', '2024-12-04'),
(4, 202018250, 'Cain', NULL, 'Sarcenon', NULL, '2000-07-02', 24, 'male', 'BS Information Technology', '4', '2', 'irregular', 'cainsarcenon@gmail.com', '09692353539', 'paid', NULL, '2024-11-28', '2024-12-02'),
(5, 202228950, 'John', 'None', 'Cena', 'Jr.', '2003-02-17', 21, 'male', 'BS Information Technology', '4', '1', 'irregular', 'cenajohn2@gmail.com', '09260982411', 'paid', NULL, '2024-11-29', '2024-12-04'),
(6, 202400003, 'Gon', '', 'Freecs', '', '2004-12-30', 19, 'male', 'BS Information Technology', '1', '1', 'regular', 'gonfreecs@gmail.com', '09692353537', 'paid', NULL, '2024-12-02', '2024-12-02'),
(7, 202011720, 'Ret', '', 'Ret', '', '2000-07-17', 24, 'male', 'BS Information Technology', '4', '1', 'regular', 'retret@gmail.com', '09692354537', 'paid', NULL, '2024-12-02', '2024-12-02');

-- --------------------------------------------------------

--
-- Table structure for table `app_it_students_sub`
--

CREATE TABLE `app_it_students_sub` (
  `id` int(11) NOT NULL,
  `student_number` int(50) NOT NULL,
  `sub1` varchar(100) NOT NULL,
  `sub2` varchar(100) NOT NULL,
  `sub3` varchar(100) NOT NULL,
  `sub4` varchar(100) NOT NULL,
  `sub5` varchar(100) NOT NULL,
  `sub6` varchar(100) NOT NULL,
  `sub7` varchar(100) NOT NULL,
  `sub8` varchar(100) NOT NULL,
  `sub9` varchar(100) NOT NULL,
  `total_units` int(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `app_it_students_sub`
--

INSERT INTO `app_it_students_sub` (`id`, `student_number`, `sub1`, `sub2`, `sub3`, `sub4`, `sub5`, `sub6`, `sub7`, `sub8`, `sub9`, `total_units`) VALUES
(11, 202211820, 'GNED 02', 'GNED 05', 'GNED 11', '', '', '', '', '', '', 9);

-- --------------------------------------------------------

--
-- Table structure for table `app_sub`
--

CREATE TABLE `app_sub` (
  `id` int(11) NOT NULL,
  `sub_code` varchar(50) NOT NULL,
  `sub_name` varchar(100) NOT NULL,
  `lab_units` int(11) NOT NULL,
  `lec_units` int(11) NOT NULL,
  `year_level` int(11) NOT NULL,
  `semester` int(11) NOT NULL,
  `cs` varchar(50) DEFAULT NULL,
  `it` varchar(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `app_sub`
--

INSERT INTO `app_sub` (`id`, `sub_code`, `sub_name`, `lab_units`, `lec_units`, `year_level`, `semester`, `cs`, `it`) VALUES
(1, 'GNED 02', 'Ethics', 0, 3, 1, 1, 'yes', 'yes'),
(2, 'GNED 05', 'Purposive Communication', 0, 3, 1, 1, 'yes', 'yes'),
(3, 'GNED 11', 'Kontekstwalisadong Komunikasyon sa Filipino', 0, 3, 1, 1, 'yes', 'yes'),
(4, 'COSC 50', 'Discrete Structures I', 0, 3, 1, 1, 'yes', 'yes'),
(5, 'DCIT 21', 'Introduction to Computing', 1, 2, 1, 1, 'yes', 'yes'),
(6, 'DCIT 22', 'Computer Programming 1', 2, 1, 1, 1, 'yes', 'yes'),
(7, 'FITT 1', 'Movement Enhancement', 0, 2, 1, 1, 'yes', 'yes'),
(8, 'NSTP 1', 'National Service Training Program 1', 0, 3, 1, 1, 'yes', 'yes'),
(9, 'CvSU 101', 'Institutional Orientation 1', 0, 1, 1, 1, 'yes', 'yes'),
(10, 'GNED 01', 'Art Appreciation', 0, 3, 1, 2, 'yes', 'yes'),
(11, 'GNED 03', 'Mathematics in Modern World', 0, 3, 1, 2, 'yes', 'yes'),
(12, 'GNED 06', 'Science, Technology and Society', 0, 3, 1, 2, 'yes', 'yes'),
(13, 'GNED 12', 'Dalumat Ng/Sa Filipino', 0, 3, 1, 2, 'yes', 'yes'),
(14, 'DCIT 23', 'Computer Programming 2', 2, 1, 1, 2, 'yes', 'yes'),
(15, 'ITEC 50', 'Web Systems and Technologies', 1, 2, 1, 2, 'yes', 'yes'),
(16, 'FITT 2', 'Fitness Exercises', 0, 2, 1, 2, 'yes', 'yes'),
(17, 'NSTP 2', 'National Service Training Program 2', 0, 3, 1, 2, 'yes', 'yes'),
(18, 'GNED 04', 'Mga Babasahin Hinggil sa Kasaysayan ng Pilipinas', 0, 3, 2, 1, 'yes', 'yes'),
(19, 'DCIT 24', 'Information Management', 1, 2, 2, 1, 'yes', 'yes'),
(20, 'DCIT 50', 'Object Oriented Programming', 1, 2, 2, 1, 'yes', 'yes'),
(21, 'MATH 1', 'Analytic Geometry', 0, 3, 2, 1, 'yes', ''),
(22, 'COSC 55', 'Discrete Structures 2', 0, 3, 2, 1, 'yes', NULL),
(23, 'COSC 60', 'Digital Logic Design', 1, 2, 2, 1, 'yes', NULL),
(24, 'INSY 50', 'Fundamentals of Information Systems', 0, 3, 2, 1, 'yes', ''),
(25, 'FITT 3', 'Physical Activities towards Health and Fitness 1', 0, 2, 2, 1, 'yes', 'yes'),
(26, 'GNED 07', 'The Contemporary World', 0, 3, 2, 1, NULL, 'yes'),
(27, 'GNED 10', 'Gender and Society', 0, 3, 2, 1, NULL, 'yes'),
(28, 'GNED 14', 'Panitikang Panlipunan', 0, 3, 2, 1, NULL, 'yes'),
(29, 'ITEC 55', 'Platform Technologies', 1, 2, 2, 1, NULL, 'yes'),
(30, 'GNED 08', 'Understanding the Self', 0, 3, 2, 2, 'yes', 'yes'),
(31, 'DCIT 25', 'Data Structures and Algorithm', 1, 2, 2, 2, 'yes', 'yes'),
(32, 'DCIT 55', 'Advance Database System', 1, 2, 2, 2, 'yes', 'yes'),
(33, 'FITT 4', 'Physical Activitives towards Health and FItness 2', 0, 2, 2, 2, 'yes', 'yes'),
(34, 'GNED 14', 'Panitikang Panlipunan', 0, 3, 2, 2, 'yes', NULL),
(35, 'MATH 2', 'Calculus', 0, 3, 2, 2, 'yes', NULL),
(36, 'COSC 65', 'Architecture and Organization', 1, 2, 2, 2, 'yes', NULL),
(37, 'COSC 70', 'Software Engineering 1', 0, 3, 2, 2, 'yes', NULL),
(38, 'ITEC 60', 'Integrated Programming and Technologies 1', 1, 2, 2, 2, NULL, 'yes'),
(39, 'ITEC 65', 'Open Source Technology', 1, 2, 2, 2, NULL, 'yes'),
(40, 'ITEC 70', 'Multimedia Systems', 1, 2, 2, 2, NULL, 'yes'),
(41, 'STAT 2', 'Applied Statistics', 0, 3, 2, 3, NULL, 'yes'),
(42, 'ITEC 75', 'System Integration and Architecture 1', 1, 2, 2, 3, NULL, 'yes'),
(43, 'MATH 3', 'Linear Algebra', 0, 3, 3, 1, 'yes', NULL),
(44, 'COSC 75', 'Software Engineering 2', 1, 2, 3, 1, 'yes', NULL),
(45, 'COSC 80', 'Operating Systems', 1, 2, 3, 1, 'yes', NULL),
(46, 'COSC 85', 'Networks and Communications', 1, 2, 3, 1, 'yes', NULL),
(47, 'COSC 101', 'CS Elective 1 (Computer Graphics and Visual Computing)', 1, 2, 3, 1, 'yes', NULL),
(48, 'DCIT 26', 'Applications Dev\'t and Emerging Technologies', 1, 2, 3, 1, 'yes', 'yes'),
(49, 'ITEC 80', 'Introduction to Human Computer Integration', 1, 2, 3, 1, NULL, 'yes'),
(50, 'ITEC 85', 'Information Assurance and Security 1', 1, 2, 3, 1, NULL, 'yes'),
(51, 'ITEC 90', 'Network Fundamentals', 1, 2, 3, 1, NULL, 'yes'),
(52, 'INSY 55', 'System Analysis and Design', 1, 2, 3, 1, NULL, 'yes'),
(53, 'DCIT 60', 'Methods of Research', 0, 3, 3, 1, NULL, 'yes'),
(54, 'GNED 09', 'Life and Works of Rizal', 0, 3, 3, 2, 'yes', 'yes'),
(55, 'MATH 4', 'Experimental Statistics', 1, 2, 3, 2, 'yes', NULL),
(56, 'COSC 90', 'Design and Analysis of Algorithm', 0, 3, 3, 2, 'yes', NULL),
(57, 'COSC 95', 'Programming Languages', 0, 3, 3, 2, 'yes', NULL),
(58, 'COSC 106', 'CS Elective 2 (Introduction to Game Development)', 1, 2, 3, 2, 'yes', NULL),
(59, 'DCIT 60', 'Methods of Research', 0, 3, 3, 2, 'yes', NULL),
(60, 'ITEC 85', 'Information Assurance and Security', 0, 3, 3, 2, 'yes', NULL),
(61, 'COSC 199', 'Practicum (240 hours)', 0, 3, 3, 3, 'yes', NULL),
(62, 'ITEC 95 ', 'Quantitative Methods (Modeling & Simulation)', 0, 3, 3, 2, NULL, 'yes'),
(63, 'ITEC 101', 'IT ELECTIVE 1 (Human Computer Interaction 2)', 1, 2, 3, 2, NULL, 'yes'),
(64, 'ITEC 106', 'IT ELECTIVE 2 (Web System and Technologies 2)', 1, 2, 3, 2, NULL, 'yes'),
(65, 'ITEC 100', 'Information Assurance and Security 2', 1, 2, 3, 2, NULL, 'yes'),
(66, 'ITEC 105', 'Network Management', 1, 2, 3, 2, NULL, 'yes'),
(67, 'ITEC 200A', 'Capstone Project and Research 1', 0, 3, 3, 2, NULL, 'yes'),
(68, 'ITEC 80', 'Human Computer Interaction', 0, 1, 4, 1, 'yes', NULL),
(69, 'COSC 100', 'Automata Theory and Formal Languages', 0, 3, 4, 1, 'yes', NULL),
(70, 'COSC 105', 'Intelligent Systems', 1, 2, 4, 1, 'yes', NULL),
(71, 'COSC 111', 'CS Elective 3 (Internet of Things)', 1, 2, 4, 1, 'yes', NULL),
(72, 'COSC 200A', 'Undergraduate Thesis 1', 0, 3, 4, 1, 'yes', NULL),
(73, 'DCIT 65', 'Social and Professional Issues', 0, 3, 4, 1, NULL, 'yes'),
(74, 'IT 111', 'IT ELECTIVE 3 (Integrated Programming and)', 1, 2, 4, 1, NULL, 'yes'),
(75, 'ITEC 116', 'IT ELECTIVE 4 (System Integration and Architecture 2)', 1, 2, 4, 1, NULL, 'yes'),
(76, 'ITEC 110', 'System Administration and Maintenance', 1, 2, 4, 1, NULL, 'yes'),
(77, 'ITEC 200B', 'Capstone Project and Research 2', 0, 3, 4, 1, NULL, 'yes'),
(78, 'GNED 07', 'The Contemporary World', 0, 3, 4, 2, 'yes', NULL),
(79, 'GNED 10', 'Gender and Society', 0, 3, 4, 2, 'yes', NULL),
(80, 'COSC 110', 'Numrical and Symbolic Computation', 1, 2, 4, 2, 'yes', NULL),
(81, 'COSC 200B', 'Undergraduate Thesis 2', 0, 3, 4, 2, 'yes', NULL),
(82, 'ITEC 109', 'Practicum (maximum 486 hours)', 0, 6, 4, 2, NULL, 'yes');

-- --------------------------------------------------------

--
-- Table structure for table `auth_group`
--

CREATE TABLE `auth_group` (
  `id` int(11) NOT NULL,
  `name` varchar(150) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `auth_group_permissions`
--

CREATE TABLE `auth_group_permissions` (
  `id` bigint(20) NOT NULL,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `auth_permission`
--

CREATE TABLE `auth_permission` (
  `id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `auth_permission`
--

INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES
(1, 'Can add log entry', 1, 'add_logentry'),
(2, 'Can change log entry', 1, 'change_logentry'),
(3, 'Can delete log entry', 1, 'delete_logentry'),
(4, 'Can view log entry', 1, 'view_logentry'),
(5, 'Can add permission', 2, 'add_permission'),
(6, 'Can change permission', 2, 'change_permission'),
(7, 'Can delete permission', 2, 'delete_permission'),
(8, 'Can view permission', 2, 'view_permission'),
(9, 'Can add group', 3, 'add_group'),
(10, 'Can change group', 3, 'change_group'),
(11, 'Can delete group', 3, 'delete_group'),
(12, 'Can view group', 3, 'view_group'),
(13, 'Can add user', 4, 'add_user'),
(14, 'Can change user', 4, 'change_user'),
(15, 'Can delete user', 4, 'delete_user'),
(16, 'Can view user', 4, 'view_user'),
(17, 'Can add content type', 5, 'add_contenttype'),
(18, 'Can change content type', 5, 'change_contenttype'),
(19, 'Can delete content type', 5, 'delete_contenttype'),
(20, 'Can view content type', 5, 'view_contenttype'),
(21, 'Can add session', 6, 'add_session'),
(22, 'Can change session', 6, 'change_session'),
(23, 'Can delete session', 6, 'delete_session'),
(24, 'Can view session', 6, 'view_session'),
(25, 'Can add cs students', 7, 'add_csstudents'),
(26, 'Can change cs students', 7, 'change_csstudents'),
(27, 'Can delete cs students', 7, 'delete_csstudents'),
(28, 'Can view cs students', 7, 'view_csstudents'),
(29, 'Can add CS Student', 8, 'add_appcsstudents'),
(30, 'Can change CS Student', 8, 'change_appcsstudents'),
(31, 'Can delete CS Student', 8, 'delete_appcsstudents'),
(32, 'Can view CS Student', 8, 'view_appcsstudents'),
(33, 'Can add IT Student', 9, 'add_appitstudents'),
(34, 'Can change IT Student', 9, 'change_appitstudents'),
(35, 'Can delete IT Student', 9, 'delete_appitstudents'),
(36, 'Can view IT Student', 9, 'view_appitstudents'),
(37, 'Can add app sub', 10, 'add_appsub'),
(38, 'Can change app sub', 10, 'change_appsub'),
(39, 'Can delete app sub', 10, 'delete_appsub'),
(40, 'Can view app sub', 10, 'view_appsub'),
(41, 'Can add app student sub', 11, 'add_appstudentsub'),
(42, 'Can change app student sub', 11, 'change_appstudentsub'),
(43, 'Can delete app student sub', 11, 'delete_appstudentsub'),
(44, 'Can view app student sub', 11, 'view_appstudentsub');

-- --------------------------------------------------------

--
-- Table structure for table `auth_user`
--

CREATE TABLE `auth_user` (
  `id` int(11) NOT NULL,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(150) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `auth_user`
--

INSERT INTO `auth_user` (`id`, `password`, `last_login`, `is_superuser`, `username`, `first_name`, `last_name`, `email`, `is_staff`, `is_active`, `date_joined`) VALUES
(1, 'pbkdf2_sha256$870000$i6eCq2Wfgbid7lAvAEa29Z$I2lE44zu/tg8olCUSjvkF0Ou9vEPArMFMqfzGpjbrsM=', NULL, 1, 'admin1', '', '', 'admin1@gmail.com', 1, 1, '2024-11-22 09:42:22.923409'),
(2, 'pbkdf2_sha256$870000$iXsTmjbd05VQk2XGzz8gnn$DeHximLfEp2WRn4lyWHrq/b8bIFTNdLopGIhzDDEPmA=', '2024-11-22 10:48:21.430213', 0, 'russeljae', '', '', 'russeljae@gmail.com', 0, 1, '2024-11-22 09:46:43.556487'),
(3, 'pbkdf2_sha256$870000$DOoY9r7xgPS1J8NAsKqjNM$RCUhCR72CFs+BfU2ft3tYoDxNHTNesdEf4Ui4QsTAwk=', '2024-12-04 10:50:45.145711', 1, 'admin', '', '', 'admin@gmail.comn', 1, 1, '2024-11-25 13:02:31.158982');

-- --------------------------------------------------------

--
-- Table structure for table `auth_user_groups`
--

CREATE TABLE `auth_user_groups` (
  `id` bigint(20) NOT NULL,
  `user_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `auth_user_user_permissions`
--

CREATE TABLE `auth_user_user_permissions` (
  `id` bigint(20) NOT NULL,
  `user_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `django_admin_log`
--

CREATE TABLE `django_admin_log` (
  `id` int(11) NOT NULL,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext DEFAULT NULL,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint(5) UNSIGNED NOT NULL CHECK (`action_flag` >= 0),
  `change_message` longtext NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `user_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `django_content_type`
--

CREATE TABLE `django_content_type` (
  `id` int(11) NOT NULL,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `django_content_type`
--

INSERT INTO `django_content_type` (`id`, `app_label`, `model`) VALUES
(1, 'admin', 'logentry'),
(8, 'app', 'appcsstudents'),
(9, 'app', 'appitstudents'),
(11, 'app', 'appstudentsub'),
(10, 'app', 'appsub'),
(7, 'app', 'csstudents'),
(3, 'auth', 'group'),
(2, 'auth', 'permission'),
(4, 'auth', 'user'),
(5, 'contenttypes', 'contenttype'),
(6, 'sessions', 'session');

-- --------------------------------------------------------

--
-- Table structure for table `django_migrations`
--

CREATE TABLE `django_migrations` (
  `id` bigint(20) NOT NULL,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `django_migrations`
--

INSERT INTO `django_migrations` (`id`, `app`, `name`, `applied`) VALUES
(1, 'contenttypes', '0001_initial', '2024-11-22 09:21:15.488868'),
(2, 'auth', '0001_initial', '2024-11-22 09:21:16.535951'),
(3, 'admin', '0001_initial', '2024-11-22 09:21:16.739968'),
(4, 'admin', '0002_logentry_remove_auto_add', '2024-11-22 09:21:16.751969'),
(5, 'admin', '0003_logentry_add_action_flag_choices', '2024-11-22 09:21:16.794975'),
(6, 'contenttypes', '0002_remove_content_type_name', '2024-11-22 09:21:17.066995'),
(7, 'auth', '0002_alter_permission_name_max_length', '2024-11-22 09:21:17.210005'),
(8, 'auth', '0003_alter_user_email_max_length', '2024-11-22 09:21:17.259010'),
(9, 'auth', '0004_alter_user_username_opts', '2024-11-22 09:21:17.274013'),
(10, 'auth', '0005_alter_user_last_login_null', '2024-11-22 09:21:17.368020'),
(11, 'auth', '0006_require_contenttypes_0002', '2024-11-22 09:21:17.373022'),
(12, 'auth', '0007_alter_validators_add_error_messages', '2024-11-22 09:21:17.388022'),
(13, 'auth', '0008_alter_user_username_max_length', '2024-11-22 09:21:17.442026'),
(14, 'auth', '0009_alter_user_last_name_max_length', '2024-11-22 09:21:17.492029'),
(15, 'auth', '0010_alter_group_name_max_length', '2024-11-22 09:21:17.547033'),
(16, 'auth', '0011_update_proxy_permissions', '2024-11-22 09:21:17.557034'),
(17, 'auth', '0012_alter_user_first_name_max_length', '2024-11-22 09:21:17.608040'),
(18, 'sessions', '0001_initial', '2024-11-22 09:21:17.696047'),
(19, 'app', '0001_initial', '2024-11-26 03:32:05.491609'),
(20, 'app', '0002_appcsstudents_appitstudents_delete_csstudents', '2024-11-26 08:36:44.073661'),
(21, 'app', '0003_alter_appcsstudents_options_and_more', '2024-11-26 09:05:12.631397'),
(22, 'app', '0004_remove_appcsstudents_specialization_and_more', '2024-11-26 09:13:29.479218'),
(23, 'app', '0005_alter_appcsstudents_year_level', '2024-11-27 14:50:48.379255'),
(24, 'app', '0006_appsub_appstudentsub', '2024-11-29 17:47:42.556552');

-- --------------------------------------------------------

--
-- Table structure for table `django_session`
--

CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `django_session`
--

INSERT INTO `django_session` (`session_key`, `session_data`, `expire_date`) VALUES
('gmh0yp62xv844hmzgwf6v4hgss5aare8', '.eJxVjEEOwiAQRe_C2pAOhba4dO8ZyAwzSNVAUtqV8e7apAvd_vfef6mA25rD1mQJM6uzMur0uxHGh5Qd8B3LrepYy7rMpHdFH7Tpa2V5Xg737yBjy986pUmIjE2WgBDIEHPkbhjFe0AHHURh1wsSiPN9HK1QL24wTtLEAOr9ASBDOQ8:1tERD3:ipPBW1s3pAu5ePjY7IIzFL7Y8LpfLVEKqyyy-MsCJUU', '2024-12-06 10:48:21.435213'),
('i48u93ujcuw4367xmdfx9gphfju7bbok', '.eJxVjDsOwjAQBe_iGlm28ZeSPmewdr0bHECOFCcV4u4QKQW0b2beS2TY1pq3zkueSFzEWZx-N4Ty4LYDukO7zbLMbV0mlLsiD9rlMBM_r4f7d1Ch12_NGJUpxqRiLUWMCGxAeW9tMqRHhb5oZ8jrkkIEVDhysMFpT-hc4iDeH-UyN9I:1tFa1n:zqX5pEINnXdr6uHfQZhKzOPZ_U2AZvTMWaPUXXveZO8', '2024-12-09 14:25:27.566358'),
('jd866tjx3x2lhpkrmbeij6imptalrdlz', '.eJxVjDsOwjAQBe_iGlm28ZeSPmewdr0bHECOFCcV4u4QKQW0b2beS2TY1pq3zkueSFzEWZx-N4Ty4LYDukO7zbLMbV0mlLsiD9rlMBM_r4f7d1Ch12_NGJUpxqRiLUWMCGxAeW9tMqRHhb5oZ8jrkkIEVDhysMFpT-hc4iDeH-UyN9I:1tIfTR:p3YNdMZmcL0K-GP-8ISV9g9lidN6FwnYthxuGdByaIo', '2024-12-18 10:50:45.150865'),
('pm13e5qfgp0zyvwe3o2urpnvh0wjzd0j', '.eJxVjDsOwjAQBe_iGlm28ZeSPmewdr0bHECOFCcV4u4QKQW0b2beS2TY1pq3zkueSFzEWZx-N4Ty4LYDukO7zbLMbV0mlLsiD9rlMBM_r4f7d1Ch12_NGJUpxqRiLUWMCGxAeW9tMqRHhb5oZ8jrkkIEVDhysMFpT-hc4iDeH-UyN9I:1tFadC:wcKEeDzP9dic2neqVPfh1tayK1krxrynsc99D6Td9vg', '2024-12-09 15:04:06.798050'),
('r2g9jkuh9ex1xn0yqat02qcgt6nsl47v', '.eJxVjDsOwjAQBe_iGlm28ZeSPmewdr0bHECOFCcV4u4QKQW0b2beS2TY1pq3zkueSFzEWZx-N4Ty4LYDukO7zbLMbV0mlLsiD9rlMBM_r4f7d1Ch12_NGJUpxqRiLUWMCGxAeW9tMqRHhb5oZ8jrkkIEVDhysMFpT-hc4iDeH-UyN9I:1tFb3q:MSJq7KN1jjTA79nkRoJBp2C0ZZTKGV93mI4gn4ba-1c', '2024-12-09 15:31:38.737944'),
('twdtxsecd6f3w9yrkq2dyrh6zc4e26u9', '.eJxVjDsOwjAQBe_iGlm28ZeSPmewdr0bHECOFCcV4u4QKQW0b2beS2TY1pq3zkueSFzEWZx-N4Ty4LYDukO7zbLMbV0mlLsiD9rlMBM_r4f7d1Ch12_NGJUpxqRiLUWMCGxAeW9tMqRHhb5oZ8jrkkIEVDhysMFpT-hc4iDeH-UyN9I:1tFmsH:ARGPCsxCt4lQPuGSj-8tvCSXO0p3Aa3hmwbzOvXXWoQ', '2024-12-10 04:08:29.016637');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `app_cs_students`
--
ALTER TABLE `app_cs_students`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `student_number` (`student_number`);

--
-- Indexes for table `app_cs_students_sub`
--
ALTER TABLE `app_cs_students_sub`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `student_number` (`student_number`);

--
-- Indexes for table `app_it_students`
--
ALTER TABLE `app_it_students`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `student_number` (`student_number`);

--
-- Indexes for table `app_it_students_sub`
--
ALTER TABLE `app_it_students_sub`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `student_number` (`student_number`);

--
-- Indexes for table `app_sub`
--
ALTER TABLE `app_sub`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `auth_group`
--
ALTER TABLE `auth_group`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `name` (`name`);

--
-- Indexes for table `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  ADD KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`);

--
-- Indexes for table `auth_permission`
--
ALTER TABLE `auth_permission`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`);

--
-- Indexes for table `auth_user`
--
ALTER TABLE `auth_user`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `username` (`username`);

--
-- Indexes for table `auth_user_groups`
--
ALTER TABLE `auth_user_groups`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_user_groups_user_id_group_id_94350c0c_uniq` (`user_id`,`group_id`),
  ADD KEY `auth_user_groups_group_id_97559544_fk_auth_group_id` (`group_id`);

--
-- Indexes for table `auth_user_user_permissions`
--
ALTER TABLE `auth_user_user_permissions`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_user_user_permissions_user_id_permission_id_14a6b632_uniq` (`user_id`,`permission_id`),
  ADD KEY `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` (`permission_id`);

--
-- Indexes for table `django_admin_log`
--
ALTER TABLE `django_admin_log`
  ADD PRIMARY KEY (`id`),
  ADD KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  ADD KEY `django_admin_log_user_id_c564eba6_fk_auth_user_id` (`user_id`);

--
-- Indexes for table `django_content_type`
--
ALTER TABLE `django_content_type`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`);

--
-- Indexes for table `django_migrations`
--
ALTER TABLE `django_migrations`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `django_session`
--
ALTER TABLE `django_session`
  ADD PRIMARY KEY (`session_key`),
  ADD KEY `django_session_expire_date_a5c62663` (`expire_date`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `app_cs_students`
--
ALTER TABLE `app_cs_students`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- AUTO_INCREMENT for table `app_cs_students_sub`
--
ALTER TABLE `app_cs_students_sub`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=18;

--
-- AUTO_INCREMENT for table `app_it_students`
--
ALTER TABLE `app_it_students`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- AUTO_INCREMENT for table `app_it_students_sub`
--
ALTER TABLE `app_it_students_sub`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=12;

--
-- AUTO_INCREMENT for table `app_sub`
--
ALTER TABLE `app_sub`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=83;

--
-- AUTO_INCREMENT for table `auth_group`
--
ALTER TABLE `auth_group`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `auth_permission`
--
ALTER TABLE `auth_permission`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=45;

--
-- AUTO_INCREMENT for table `auth_user`
--
ALTER TABLE `auth_user`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `auth_user_groups`
--
ALTER TABLE `auth_user_groups`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `auth_user_user_permissions`
--
ALTER TABLE `auth_user_user_permissions`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `django_admin_log`
--
ALTER TABLE `django_admin_log`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `django_content_type`
--
ALTER TABLE `django_content_type`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=12;

--
-- AUTO_INCREMENT for table `django_migrations`
--
ALTER TABLE `django_migrations`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=25;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  ADD CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  ADD CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`);

--
-- Constraints for table `auth_permission`
--
ALTER TABLE `auth_permission`
  ADD CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`);

--
-- Constraints for table `auth_user_groups`
--
ALTER TABLE `auth_user_groups`
  ADD CONSTRAINT `auth_user_groups_group_id_97559544_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  ADD CONSTRAINT `auth_user_groups_user_id_6a12ed8b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

--
-- Constraints for table `auth_user_user_permissions`
--
ALTER TABLE `auth_user_user_permissions`
  ADD CONSTRAINT `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  ADD CONSTRAINT `auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

--
-- Constraints for table `django_admin_log`
--
ALTER TABLE `django_admin_log`
  ADD CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  ADD CONSTRAINT `django_admin_log_user_id_c564eba6_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
