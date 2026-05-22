# Casos de uso

## CU-01 Vincular cuenta GitHub

### Descripción

Permite a un usuario asociar su cuenta de Telegram con un nombre de usuario GitHub.

### Actor principal

Usuario

### Flujo principal

1. El usuario ejecuta `/vincular usuario_github`
2. El bot valida el usuario GitHub
3. El bot guarda la vinculación
4. El sistema confirma la operación

### Resultado esperado

La cuenta GitHub queda vinculada al usuario Telegram.

---

## CU-02 Consultar comentarios recientes

### Descripción

Permite visualizar comentarios recientes realizados por el usuario en issues.

### Actor principal

Usuario

### Flujo principal

1. El usuario ejecuta `/mis_comentarios`
2. El sistema consulta GitHub API
3. El sistema obtiene comentarios recientes
4. El bot muestra resultados al usuario

### Resultado esperado

El usuario visualiza sus comentarios recientes.

---

## CU-03 Consultar issues asignadas

### Descripción

Permite visualizar las issues asignadas actualmente al usuario.

### Actor principal

Usuario

### Flujo principal

1. El usuario ejecuta `/mis_issues`
2. El sistema consulta GitHub API
3. El sistema obtiene las issues asignadas
4. El bot muestra resultados

### Resultado esperado

El usuario visualiza sus issues asignadas.

---

## CU-04 Consultar estado general

### Descripción

Permite visualizar el estado general actual al usuario.

### Actor principal

Usuario

### Flujo principal

1. El usuario ejecuta `/mi_estado`
2. El sistema consulta GitHub API
3. El sistema obtiene el estado general
4. El bot muestra resultados

### Resultado esperado

El usuario visualiza su estado actual de GitHub.

---

## CU-05 Desvincular cuenta GitHub

### Descripción

Permite eliminar la vinculación entre Telegram y GitHub.

### Actor principal

Usuario

### Flujo principal

1. El usuario ejecuta `/desvincular`
2. El sistema elimina el registro
3. El bot confirma la operación

### Resultado esperado

La cuenta queda desvinculada.