# Requerimientos funcionales

| ID    | Requerimiento                                               |
| ----- | ----------------------------------------------------------- |
| RF-01 | El sistema debe permitir vincular una cuenta GitHub         |
| RF-02 | El sistema debe permitir desvincular una cuenta GitHub      |
| RF-03 | El sistema debe consultar comentarios recientes del usuario |
| RF-04 | El sistema debe consultar issues asignadas                  |
| RF-05 | El sistema debe manejar múltiples usuarios simultáneamente  |
| RF-06 | El sistema debe almacenar vinculaciones en SQLite           |
| RF-07 | El sistema debe mostrar mensajes de ayuda                   |
| RF-08 | El sistema debe manejar errores de GitHub API               |
| RF-09 | El sistema debe dividir mensajes largos automáticamente     |
| RF-10 | El sistema debe aplicar cooldown para evitar spam           |

# Requerimientos no funcionales

| ID     | Requerimiento                                                           |
| ------ | ----------------------------------------------------------------------- |
| RNF-01 | El sistema debe responder en menos de 10 segundos                       |
| RNF-02 | El sistema debe funcionar 24/7                                          |
| RNF-03 | El sistema debe soportar múltiples usuarios                             |
| RNF-04 | El sistema debe proteger tokens sensibles mediante variables de entorno |
| RNF-05 | El sistema debe ser compatible con Linux                                |
| RNF-06 | El sistema debe ser mantenible y modular                                |
| RNF-07 | El sistema debe minimizar consultas innecesarias a GitHub API           |