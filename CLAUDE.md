# Marca Personal — GoHighLevel Workspace

## Qué hago aquí

Asistente operativo de **GoHighLevel (GHL)** para la cuenta del usuario. Ejecuto acciones sobre la sub-cuenta (location) `QZXWRBXmom6lw3tOgxpC` usando dos canales:

1. **MCP-first** — vía el servidor MCP oficial de HighLevel (`.mcp.json` en la raíz).
2. **API REST como fallback** — vía `https://services.leadconnectorhq.com` cuando la acción no exista como herramienta MCP.

> Regla operativa: si una acción no se puede hacer por MCP, intentar inmediatamente por API REST con la misma PIT antes de pedir ayuda al usuario.

---

## Conexión

### MCP
- Endpoint: `https://services.leadconnectorhq.com/mcp/`
- Transport: HTTP (Streamable)
- Headers: `Authorization: Bearer <PIT>`, `locationId: <LOC_ID>`, `Version: 2021-07-28`
- Configurado en `.mcp.json` (se carga al iniciar la sesión de Claude Code; reiniciar tras cambios).

### API REST v2
- Base URL: `https://services.leadconnectorhq.com`
- Auth: `Authorization: Bearer pit-f1303ff1-db63-4865-acec-2967f070f210`
- Headers obligatorios en cada request:
  - `Authorization: Bearer <PIT>`
  - `Version: 2021-07-28`
  - `Content-Type: application/json` (para POST/PUT/PATCH/DELETE)
  - `Accept: application/json`
- Location ID a inyectar en query/body según endpoint: `QZXWRBXmom6lw3tOgxpC`

### Credenciales (en este workspace)
- **PIT**: `pit-f1303ff1-db63-4865-acec-2967f070f210`
- **Location ID**: `QZXWRBXmom6lw3tOgxpC`

> ⚠️ Las credenciales viven en `.mcp.json` en texto plano. Si esta carpeta se convierte en repo git, agregar `.mcp.json` a `.gitignore` y migrar a variables de entorno.

---

## Capacidades por MCP (categorías de tools)

- **Contacts** — CRUD, tags, tasks, custom fields
- **Conversations** — búsqueda, envío de mensajes (SMS/Email/etc.)
- **Calendars** — eventos, citas, notas de cita
- **Opportunities** — pipelines, stages, búsqueda
- **Payments** — órdenes, transacciones, suscripciones
- **Social Media** — publicación, edición, analytics
- **Blogs** — posts, categorías, autores
- **Emails** — templates
- **Locations / Sub-Accounts** — info y custom fields

Si la herramienta MCP no existe → **API REST**. Endpoints comunes:
- `GET /contacts/`, `POST /contacts/`, `PUT /contacts/{id}`
- `GET /conversations/search`, `POST /conversations/messages`
- `GET /calendars/`, `POST /calendars/events`
- `GET /opportunities/search`, `POST /opportunities/`
- `GET /workflows/` (no expuesto vía MCP en muchos casos → usar API)
- `GET /locations/{locationId}/customFields`

---

## Buenas prácticas (anotadas)

### Rate limits (V2 API)
- **Burst**: 100 requests / 10 segundos por app por recurso.
- **Diario**: 200,000 requests / día por app por recurso.
- Headers de respuesta para monitorear:
  - `X-RateLimit-Max`, `X-RateLimit-Remaining`, `X-RateLimit-Interval-Milliseconds`
  - `X-RateLimit-Limit-Daily`, `X-RateLimit-Daily-Remaining`

### Manejo de errores
- **429 / 5xx** → backoff exponencial con jitter. No reintentar más de 3-5 veces.
- **401** → PIT expirada/inválida → avisar al usuario para rotar.
- **403** → falta scope en la PIT → listar el scope faltante y pedir agregarlo.
- **404** → confirmar `locationId` antes de asumir que el recurso no existe.
- Operaciones no-idempotentes (POST de creación) → no reintentar a ciegas; verificar primero si el recurso ya se creó.

### Paginación
- API v2 usa `limit` + `startAfter` / `startAfterId` (cursor) en la mayoría de endpoints de listado.
- NO asumir paginación por `page`/`offset` salvo que el endpoint lo documente.
- Iterar hasta que la respuesta devuelva `meta.nextPageUrl` vacío o `< limit` resultados.

### Seguridad
- Rotar la PIT cada **90 días** (HighLevel da 7 días de gracia con ambos tokens activos).
- Si se compromete: en Settings → Private Integrations → "Rotate and expire this token now".
- Máximo **5 PITs** por location y por agency.
- Editar scopes de una PIT NO regenera el token — preferir esto a recrearla.
- Nunca pegar la PIT en logs, commits, mensajes, ni respuestas al usuario salvo que la pida explícitamente.

### Versionado
- El header `Version` es **obligatorio** en todas las llamadas v2 (excepto el endpoint de access token).
- Valor estable actual: `2021-07-28`.
- Si un endpoint requiere otra versión, el doc del endpoint lo dice explícitamente — usar la indicada.

### MCP específico
- Si el MCP devuelve un tool no documentado, validar con un dry-run de lectura antes de mutar.
- Para cargas grandes (export de contactos completo, etc.) preferir API REST con paginación; MCP no está optimizado para volumen.
- Si el MCP responde con timeout, fallback inmediato a API.

---

## Flujo de trabajo por defecto

1. Usuario pide una acción.
2. Confirmar **oneshot** (lista de pasos) antes de ejecutar.
3. Intentar vía MCP. Si falla / no existe la tool → API REST.
4. Verificar resultado (lectura del recurso afectado).
5. Reportar de forma concisa qué se hizo, IDs creados/modificados, y siguiente paso sugerido.

## Referencias
- Docs API v2: https://marketplace.gohighlevel.com/docs/
- Docs MCP: https://marketplace.gohighlevel.com/docs/other/mcp/index.html
- Private Integrations: https://help.gohighlevel.com/support/solutions/articles/155000003054
