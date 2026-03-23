-- phpMyAdmin SQL Dump
-- version 5.2.2
-- https://www.phpmyadmin.net/
--
-- Хост: MySQL-8.4
-- Время создания: Мар 23 2026 г., 13:16
-- Версия сервера: 8.4.4
-- Версия PHP: 8.4.1

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- База данных: `admin_panel`
--

-- --------------------------------------------------------

--
-- Структура таблицы `admin_logs`
--

CREATE TABLE `admin_logs` (
  `id` int NOT NULL,
  `username` varchar(50) DEFAULT NULL,
  `action` varchar(255) NOT NULL,
  `action_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Дамп данных таблицы `admin_logs`
--

INSERT INTO `admin_logs` (`id`, `username`, `action`, `action_time`) VALUES
(1, 'admin', 'Вход в систему', '2026-03-18 17:46:18'),
(2, 'admin', 'Вход в систему', '2026-03-22 16:00:00'),
(3, 'admin', 'Выход из системы', '2026-03-22 16:07:05'),
(4, 'admin', 'Вход в систему', '2026-03-22 16:54:33'),
(5, 'admin', 'Выход из системы', '2026-03-22 16:55:48'),
(6, 'admin', 'Вход в систему', '2026-03-22 16:56:19'),
(7, 'admin', 'Выход из системы', '2026-03-22 17:01:19'),
(8, 'admin', 'Вход в систему', '2026-03-22 17:04:39'),
(9, 'admin', 'Выход из системы', '2026-03-22 17:07:54');

-- --------------------------------------------------------

--
-- Структура таблицы `users`
--

CREATE TABLE `users` (
  `id` int NOT NULL,
  `username` varchar(50) NOT NULL,
  `password` varchar(50) NOT NULL,
  `email` varchar(100) NOT NULL,
  `full_name` varchar(100) NOT NULL,
  `last_login` datetime DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Дамп данных таблицы `users`
--

INSERT INTO `users` (`id`, `username`, `password`, `email`, `full_name`, `last_login`, `created_at`) VALUES
(1, 'admin', 'admin123', 'admin@glazov-raion.ru', 'Администратор сайта', '2026-03-22 21:04:39', '2026-03-18 16:20:59'),
(2, 'secretary', 'secretary123', 'secretary@glazov-raion.ru', 'Секретарь', NULL, '2026-03-18 16:20:59');

--
-- Индексы сохранённых таблиц
--

--
-- Индексы таблицы `admin_logs`
--
ALTER TABLE `admin_logs`
  ADD PRIMARY KEY (`id`);

--
-- Индексы таблицы `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `username` (`username`),
  ADD UNIQUE KEY `email` (`email`);

--
-- AUTO_INCREMENT для сохранённых таблиц
--

--
-- AUTO_INCREMENT для таблицы `admin_logs`
--
ALTER TABLE `admin_logs`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;

--
-- AUTO_INCREMENT для таблицы `users`
--
ALTER TABLE `users`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
