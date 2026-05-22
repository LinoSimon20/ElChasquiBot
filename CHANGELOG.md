# Changelog

All notable changes to this project will be documented in this file.

The format is based on Keep a Changelog and this project follows Semantic Versioning.

---

## [1.0.0] - 2026-05-22

### Added

- Telegram bot inicial funcional (ChasquiBot)
- Vinculación de usuarios de GitHub con Telegram
- Comando `/start` con guía de uso
- Comando `/vincular` para registrar usuario GitHub
- Comando `/mis_comentarios` para obtener comentarios en issues
- Comando `/mis_issues` para listar issues asignadas
- Comando `/mi_estado` para ver resumen de actividad en GitHub
- Comando `/ayuda` con documentación de comandos
- Comando `/desvincular` para eliminar cuenta vinculada
- Sistema de cooldown para evitar spam de comandos
- Manejo de mensajes largos en Telegram
- Integración con GitHub REST API
- Sistema de caché para reducir llamadas a GitHub API
- Base de datos SQLite para persistencia de usuarios

### Changed

- Mejorado sistema de logging para acciones del usuario y errores
- Optimización de manejo de respuestas de la API de GitHub
- Mejora en validación de usuarios de GitHub
- Mejor estructura modular del proyecto

### Fixed

- Manejo de errores de conexión con GitHub API
- Corrección de parsing de JSON en respuestas de GitHub
- Manejo de casos donde la API retorna rate limit
- Evita crashes cuando GitHub responde datos incompletos

### Security

- Validación de token de GitHub desde variables de entorno
- Prevención de uso del bot sin vinculación previa
- Protección básica contra abuso mediante cooldown

---

## [0.1.0] - 2026-05-16

### Added

- Versión inicial del bot
- Funciones básicas de consulta a GitHub
- Primer sistema de usuarios vinculados