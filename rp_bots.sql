-- phpMyAdmin SQL Dump
-- version 5.1.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1:3306
-- Tiempo de generación: 08-12-2022 a las 19:48:08
-- Versión del servidor: 10.5.12-MariaDB-cll-lve
-- Versión de PHP: 7.2.34

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `u197027072_rp_bots`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `armas`
--

CREATE TABLE `armas` (
  `entidad` int(11) NOT NULL,
  `psico` char(5) COLLATE utf8mb4_unicode_ci NOT NULL,
  `cliente_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `autorizado`
--

CREATE TABLE `autorizado` (
  `disc_id` bigint(20) NOT NULL,
  `entidad` int(11) NOT NULL,
  `nombre` text COLLATE utf8_unicode_ci DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;



-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `bancos_preguntas`
--

CREATE TABLE `bancos_preguntas` (
  `entidad` int(11) NOT NULL,
  `id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;




-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `cita`
--

CREATE TABLE `cita` (
  `server` int(11) NOT NULL,
  `entidad` int(11) NOT NULL,
  `persona_id` bigint(20) NOT NULL,
  `fecha` date NOT NULL,
  `franja` text COLLATE utf8mb4_unicode_ci NOT NULL,
  `message_id` bigint(20) NOT NULL,
  `motivo` text COLLATE utf8mb4_unicode_ci NOT NULL,
  `nombre_ic` text COLLATE utf8mb4_unicode_ci NOT NULL,
  `id` int(11) NOT NULL,
  `estado` text COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT 'Por Confirmar',
  `si` int(11) NOT NULL DEFAULT 0,
  `no` int(11) NOT NULL DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;



-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `clientes`
--

CREATE TABLE `clientes` (
  `cliente_id` int(11) NOT NULL,
  `entidad` int(11) NOT NULL,
  `tipo` text COLLATE utf8_unicode_ci NOT NULL,
  `nombre` text COLLATE utf8_unicode_ci DEFAULT NULL,
  `sexo` char(1) COLLATE utf8_unicode_ci DEFAULT NULL,
  `sangre` char(3) COLLATE utf8_unicode_ci DEFAULT NULL,
  `nace` date DEFAULT NULL,
  `tel` char(15) COLLATE utf8_unicode_ci DEFAULT NULL,
  `al` longtext COLLATE utf8_unicode_ci DEFAULT NULL,
  `med` longtext COLLATE utf8_unicode_ci DEFAULT NULL,
  `chan` bigint(20) DEFAULT NULL,
  `ms` bigint(20) DEFAULT NULL,
  `ini` char(4) COLLATE utf8_unicode_ci DEFAULT NULL,
  `seguro_med` date DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `empleados`
--

CREATE TABLE `empleados` (
  `entidad` int(11) NOT NULL,
  `discord_id` bigint(20) NOT NULL,
  `nombre` text COLLATE utf8_unicode_ci DEFAULT NULL,
  `rango` text COLLATE utf8_unicode_ci DEFAULT NULL,
  `trabajado` double DEFAULT NULL,
  `entrado_trabajar` double DEFAULT NULL,
  `en_servicio` int(1) DEFAULT NULL,
  `numero_de_placa` char(4) COLLATE utf8_unicode_ci DEFAULT NULL,
  `certificados` int(11) NOT NULL DEFAULT 0 COMMENT 'Número de certificados',
  `alumnos` int(4) NOT NULL DEFAULT 0 COMMENT 'Relación con los alumnos',
  `certificados_aviacion` int(11) NOT NULL DEFAULT 0,
  `telefono` char(9) COLLATE utf8_unicode_ci DEFAULT NULL,
  `Nacionalidad` text COLLATE utf8_unicode_ci DEFAULT NULL,
  `Nacimiento` date DEFAULT NULL,
  `tablon` bigint(20) NOT NULL DEFAULT 1
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `entidad`
--

CREATE TABLE `entidad` (
  `id` int(11) NOT NULL,
  `servidor` int(20) NOT NULL,
  `nombre` text COLLATE utf8_unicode_ci DEFAULT NULL,
  `discord` bigint(20) DEFAULT NULL,
  `actualizado` date NOT NULL DEFAULT current_timestamp(),
  `tipo_entidad` char(30) COLLATE utf8_unicode_ci DEFAULT NULL COMMENT 'tipo de entidad, LSFD, LSPD o MEC',
  `canal_cita` bigint(20) NOT NULL DEFAULT 968143285363310652,
  `logo` text COLLATE utf8_unicode_ci DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `examen`
--

CREATE TABLE `examen` (
  `entidad` int(11) NOT NULL,
  `id` int(11) NOT NULL,
  `Titulo` text COLLATE utf8mb4_unicode_ci NOT NULL,
  `banco_preguntas` int(11) DEFAULT NULL,
  `num_preguntas` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `examen_asigna`
--

CREATE TABLE `examen_asigna` (
  `empleado` bigint(20) NOT NULL,
  `examen` int(11) NOT NULL,
  `entidad` int(11) NOT NULL,
  `info_adicional` text COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `nota` float NOT NULL DEFAULT -1
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `fallecimiento`
--

CREATE TABLE `fallecimiento` (
  `entidad` int(11) NOT NULL,
  `nombre` char(30) COLLATE utf8mb4_unicode_ci NOT NULL,
  `fecha_nacimiento` date NOT NULL,
  `fecha_defuncion` date NOT NULL,
  `forenses_encargados` text COLLATE utf8mb4_unicode_ci NOT NULL,
  `cargo_med_forense` text COLLATE utf8mb4_unicode_ci NOT NULL,
  `causas` text COLLATE utf8mb4_unicode_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `monitor`
--

CREATE TABLE `monitor` (
  `entidad` int(11) NOT NULL,
  `mensaje` bigint(20) NOT NULL,
  `canal` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `pregunta`
--

CREATE TABLE `pregunta` (
  `banco` int(11) NOT NULL,
  `id` int(11) NOT NULL,
  `Pregunta` text COLLATE utf8mb4_unicode_ci NOT NULL,
  `Tipo` int(11) NOT NULL,
  `opcion_ok` text COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `opcion_ko_num` int(11) DEFAULT 3,
  `opcion_ko_1` text COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `opcion_ko_2` text COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `opcion_ko_3` text COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `opcion_ko_4` text COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `puntuacion_max` int(11) NOT NULL DEFAULT 1
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `respuestas`
--

CREATE TABLE `respuestas` (
  `examen` int(11) NOT NULL,
  `pregunta` int(11) NOT NULL,
  `puntuacion` int(11) NOT NULL,
  `texto` text COLLATE utf8mb4_unicode_ci NOT NULL,
  `empleado_discord` bigint(20) NOT NULL,
  `empleado_entidad` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `servidores`
--

CREATE TABLE `servidores` (
  `id` int(11) NOT NULL,
  `nombre` text COLLATE utf8_unicode_ci NOT NULL,
  `logo` text COLLATE utf8_unicode_ci NOT NULL,
  `server_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- Volcado de datos para la tabla `servidores`
--

INSERT INTO `servidores` (`id`, `nombre`, `logo`, `server_id`) VALUES
(1, 'Your server', 'YOUR_LOGO', 1),;
-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `sincronizaciones`
--

CREATE TABLE `sincronizaciones` (
  `nombre_dispensable` char(30) COLLATE utf8mb4_unicode_ci NOT NULL,
  `entidad_origen` int(11) NOT NULL,
  `canal` bigint(20) NOT NULL,
  `precio` int(11) NOT NULL,
  `entidad_destino` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `usuarios_conectados`
--

CREATE TABLE `usuarios_conectados` (
  `nombre` varchar(150) COLLATE utf8mb4_unicode_ci NOT NULL,
  `conectado` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `vehiculo`
--

CREATE TABLE `vehiculo` (
  `entidad` int(11) NOT NULL,
  `cliente_id` int(11) NOT NULL,
  `tipo` text COLLATE utf8mb4_unicode_ci NOT NULL,
  `marca` text COLLATE utf8mb4_unicode_ci NOT NULL,
  `modelo` text COLLATE utf8mb4_unicode_ci NOT NULL,
  `matricula` char(12) COLLATE utf8mb4_unicode_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `armas`
--
ALTER TABLE `armas`
  ADD PRIMARY KEY (`entidad`,`cliente_id`),
  ADD KEY `cliente_armas` (`cliente_id`);

--
-- Indices de la tabla `autorizado`
--
ALTER TABLE `autorizado`
  ADD PRIMARY KEY (`disc_id`,`entidad`),
  ADD KEY `entidad` (`entidad`);

--
-- Indices de la tabla `bancos_preguntas`
--
ALTER TABLE `bancos_preguntas`
  ADD PRIMARY KEY (`id`),
  ADD KEY `entidad_banco_fk` (`entidad`);

--
-- Indices de la tabla `cita`
--
ALTER TABLE `cita`
  ADD PRIMARY KEY (`id`),
  ADD KEY `server` (`server`),
  ADD KEY `entidad_cita` (`entidad`);

--
-- Indices de la tabla `clientes`
--
ALTER TABLE `clientes`
  ADD PRIMARY KEY (`cliente_id`),
  ADD UNIQUE KEY `chan` (`chan`),
  ADD KEY `entidad` (`entidad`);

--
-- Indices de la tabla `empleados`
--
ALTER TABLE `empleados`
  ADD PRIMARY KEY (`entidad`,`discord_id`);

--
-- Indices de la tabla `entidad`
--
ALTER TABLE `entidad`
  ADD PRIMARY KEY (`id`),
  ADD KEY `servidor` (`servidor`);

--
-- Indices de la tabla `examen`
--
ALTER TABLE `examen`
  ADD PRIMARY KEY (`id`),
  ADD KEY `entidad_examen_id` (`entidad`),
  ADD KEY `banco_preguntas` (`banco_preguntas`);

--
-- Indices de la tabla `examen_asigna`
--
ALTER TABLE `examen_asigna`
  ADD PRIMARY KEY (`empleado`,`examen`,`entidad`),
  ADD KEY `examen_examen_asigna` (`examen`),
  ADD KEY `examen_emplado_asigna_valor` (`entidad`,`empleado`);

--
-- Indices de la tabla `fallecimiento`
--
ALTER TABLE `fallecimiento`
  ADD PRIMARY KEY (`entidad`,`nombre`,`fecha_nacimiento`);

--
-- Indices de la tabla `monitor`
--
ALTER TABLE `monitor`
  ADD PRIMARY KEY (`entidad`,`canal`);

--
-- Indices de la tabla `pregunta`
--
ALTER TABLE `pregunta`
  ADD PRIMARY KEY (`id`),
  ADD KEY `pregunta_banco_preguntas` (`banco`);

--
-- Indices de la tabla `respuestas`
--
ALTER TABLE `respuestas`
  ADD PRIMARY KEY (`examen`,`pregunta`,`empleado_discord`,`empleado_entidad`),
  ADD KEY `examen_respuesta_preguna_jsjsjsj` (`pregunta`);

--
-- Indices de la tabla `servidores`
--
ALTER TABLE `servidores`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `sincronizaciones`
--
ALTER TABLE `sincronizaciones`
  ADD PRIMARY KEY (`nombre_dispensable`,`entidad_origen`,`entidad_destino`),
  ADD KEY `entidad_or` (`entidad_origen`),
  ADD KEY `entidad_des` (`entidad_destino`);

--
-- Indices de la tabla `usuarios_conectados`
--
ALTER TABLE `usuarios_conectados`
  ADD PRIMARY KEY (`nombre`);

--
-- Indices de la tabla `vehiculo`
--
ALTER TABLE `vehiculo`
  ADD PRIMARY KEY (`entidad`,`cliente_id`,`matricula`),
  ADD KEY `cliente_fk` (`cliente_id`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `bancos_preguntas`
--
ALTER TABLE `bancos_preguntas`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT de la tabla `cita`
--
ALTER TABLE `cita`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=28;

--
-- AUTO_INCREMENT de la tabla `clientes`
--
ALTER TABLE `clientes`
  MODIFY `cliente_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=69;

--
-- AUTO_INCREMENT de la tabla `entidad`
--
ALTER TABLE `entidad`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT de la tabla `examen`
--
ALTER TABLE `examen`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT de la tabla `pregunta`
--
ALTER TABLE `pregunta`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT de la tabla `servidores`
--
ALTER TABLE `servidores`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `armas`
--
ALTER TABLE `armas`
  ADD CONSTRAINT `cliente_armas` FOREIGN KEY (`cliente_id`) REFERENCES `clientes` (`cliente_id`) ON DELETE CASCADE,
  ADD CONSTRAINT `entidad_armas` FOREIGN KEY (`cliente_id`) REFERENCES `entidad` (`id`) ON DELETE CASCADE;

--
-- Filtros para la tabla `autorizado`
--
ALTER TABLE `autorizado`
  ADD CONSTRAINT `entidad_autoriza` FOREIGN KEY (`entidad`) REFERENCES `entidad` (`id`) ON DELETE CASCADE;

--
-- Filtros para la tabla `bancos_preguntas`
--
ALTER TABLE `bancos_preguntas`
  ADD CONSTRAINT `entidad_banco_fk` FOREIGN KEY (`entidad`) REFERENCES `entidad` (`id`);

--
-- Filtros para la tabla `cita`
--
ALTER TABLE `cita`
  ADD CONSTRAINT `entidad_cita` FOREIGN KEY (`entidad`) REFERENCES `entidad` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `server` FOREIGN KEY (`server`) REFERENCES `servidores` (`id`);

--
-- Filtros para la tabla `clientes`
--
ALTER TABLE `clientes`
  ADD CONSTRAINT `entidad_fk_fk_cliente` FOREIGN KEY (`entidad`) REFERENCES `entidad` (`id`) ON DELETE CASCADE;

--
-- Filtros para la tabla `empleados`
--
ALTER TABLE `empleados`
  ADD CONSTRAINT `entidad_empleados` FOREIGN KEY (`entidad`) REFERENCES `entidad` (`id`) ON DELETE CASCADE;

--
-- Filtros para la tabla `entidad`
--
ALTER TABLE `entidad`
  ADD CONSTRAINT `entidad_ibfk_1` FOREIGN KEY (`servidor`) REFERENCES `servidores` (`id`);

--
-- Filtros para la tabla `examen`
--
ALTER TABLE `examen`
  ADD CONSTRAINT `banco_preguntas` FOREIGN KEY (`banco_preguntas`) REFERENCES `bancos_preguntas` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `entidad_examen_id` FOREIGN KEY (`entidad`) REFERENCES `entidad` (`id`) ON DELETE CASCADE;

--
-- Filtros para la tabla `examen_asigna`
--
ALTER TABLE `examen_asigna`
  ADD CONSTRAINT `examen_emplado_asigna_valor` FOREIGN KEY (`entidad`,`empleado`) REFERENCES `empleados` (`entidad`, `discord_id`) ON DELETE CASCADE,
  ADD CONSTRAINT `examen_examen_asigna` FOREIGN KEY (`examen`) REFERENCES `examen` (`id`);

--
-- Filtros para la tabla `fallecimiento`
--
ALTER TABLE `fallecimiento`
  ADD CONSTRAINT `entidad` FOREIGN KEY (`entidad`) REFERENCES `entidad` (`id`);

--
-- Filtros para la tabla `monitor`
--
ALTER TABLE `monitor`
  ADD CONSTRAINT `entidad_fk_fk` FOREIGN KEY (`entidad`) REFERENCES `entidad` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Filtros para la tabla `pregunta`
--
ALTER TABLE `pregunta`
  ADD CONSTRAINT `pregunta_banco_preguntas` FOREIGN KEY (`banco`) REFERENCES `bancos_preguntas` (`id`);

--
-- Filtros para la tabla `respuestas`
--
ALTER TABLE `respuestas`
  ADD CONSTRAINT `examen_respuesta_fk` FOREIGN KEY (`examen`) REFERENCES `examen` (`id`),
  ADD CONSTRAINT `examen_respuesta_preguna_jsjsjsj` FOREIGN KEY (`pregunta`) REFERENCES `pregunta` (`id`);

--
-- Filtros para la tabla `sincronizaciones`
--
ALTER TABLE `sincronizaciones`
  ADD CONSTRAINT `entidad_des` FOREIGN KEY (`entidad_destino`) REFERENCES `entidad` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `entidad_or` FOREIGN KEY (`entidad_origen`) REFERENCES `entidad` (`id`) ON DELETE CASCADE;

--
-- Filtros para la tabla `vehiculo`
--
ALTER TABLE `vehiculo`
  ADD CONSTRAINT `cliente_fk` FOREIGN KEY (`cliente_id`) REFERENCES `clientes` (`cliente_id`) ON DELETE CASCADE,
  ADD CONSTRAINT `entidad_fk` FOREIGN KEY (`entidad`) REFERENCES `entidad` (`id`) ON DELETE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
