# CONTEXT — ai-fde-sandbox

> **Para agentes/sesiones nuevas:** lee esto antes de codear. Detalle operativo en `README.md`.

## North star

**Carrera (18 meses):** Senior AI FDE @ Palantir/Google Cloud, remoto Chile, $150K–220K USD.

**Proyecto:** API P&L tiendas (sintéticas) → **URL pública** → **agente** que responde en lenguaje natural vía tool calling.

**Trabajo Walmart (separado):** dashboard P&L real + BigQuery + Cloud Run + escritura BQ. **No replicar en sandbox** (sin BQ personal, datos confidenciales).

## Método de estudio (Angello)

- 1.5h/día Lu–Mi + 3h Sáb + 3.5h Dom = **11h/semana coding**
- **1 concepto + 1 mini build + 1 commit** por sesión
- **Anti-vibe-coding:** entender antes de copiar; saber qué assert/comando verifica el cambio
- Viernes = psicólogo + pareja (coding solo BONUS)

## Protocolo de sesión (acuerdos permanentes)

### Orientación
- Toda sesión apunta al North Star: AI FDE nivel Palantir / Google Cloud.
- Cada sesión = **1 concepto + 1 mini build** mínimo. Puede haber más si el tiempo lo permite.

### Cómo explico conceptos
Cada concepto nuevo viene con **3 partes obligatorias**:
1. **Descripción técnica** — qué es en términos de ingeniería.
2. **Analogía** — explicación que puedas usar con compañeros de trabajo sin background técnico.
3. **Por qué importa para FDE** — qué rol juega en el nivel Palantir/Google.

Cuando aplique: *"Si un reclutador te pregunta X, respondes Y."*

### Formato de respuestas
- Cortas, sin relleno, orientadas a aprendizaje rápido.
- Al inicio de cada sesión: **glosario** de palabras, librerías, métodos o arquitectura que se usarán.
- Si se entrega código: explicación línea por línea + analogía + auto-auditoría de por qué se hace así.
- **Siempre indicar ruta exacta** al sugerir crear o modificar algo. Formato obligatorio:
  - Crear: `cloud_run_rewrite/scripts/pnl_tool.py` → función `formatear_tienda()`
  - Modificar: `cloud_run_rewrite/config/settings.py` → agregar campo `api_base_url`
  - Sin ruta explícita = instrucción incompleta; no avanzar.

### Anti-Vibe-Coding (regla dura)
- **No crear archivos ni funciones** que no hayan sido pedidos explícitamente.
- **No sobrediseñar**: la solución más simple que funciona.
- Angello escribe el código guiado; el agente explica y revisa.
- Verificación obligatoria antes de seguir al siguiente paso.

### Trampas de sesión
- No crear tests automáticamente si no se pidieron.
- No avanzar al siguiente mini build sin verificar el anterior.
- Si Angello dice "issue reproduced / proceed", confirmar qué se procederá antes de codear.
- Angello escribe el código; el agente guía y revisa — no implementar sin pedido explícito.
- Commit al cierre de cada sesión: `<verbo> <qué>`.
- Comandos de verificación simples (evitar one-liners crípticos de Python).

## Estado actual (Fase 1 completa)

| Hecho | Detalle |
|---|---|
| API FastAPI | `cloud_run_rewrite/src/main.py` |
| SSOT datos | `PNLService` + `random.seed(42)` en `_generador_datos_sinteticos()` |
| Schema | `TiendaPL`: tienda_id, ventas, costos, opex, opinc, comuna |
| Tests API | 4 integration tests en `test/test_main.py` — todos pasan |
| Docker | `Dockerfile` + `.dockerignore` |
| Cloud Run | **LIVE** — ver URL abajo |
| Settings | `config/settings.py` — `api_base_url`, lee `$env:API_BASE_URL` |
| Script tool | `scripts/pnl_tool.py` — 2 tools: `--tienda_id` y `--comuna` |

## URL producción

```
https://fde-pnl-api-198971893116.europe-west1.run.app
```

- GCP project: `sanguine-orb-354623`
- Región: `europe-west1`
- Auth: pública (`--allow-unauthenticated`)
- Puerto contenedor: **8080**

## Endpoints

| Ruta | Notas |
|---|---|
| `GET /health` | Probe Cloud Run |
| `GET /docs` | Swagger |
| `GET /api/v1/pnl` | Lista; `?comuna=X` filtra |
| `GET /api/v1/pnl/{id}` | P&L completo |
| `GET /api/v1/pnl/{id}/opinc` | Solo opinc; handler usa `if opinc is None` |

**ID tienda:** entero `1`–`100` (no `store_001`).

## Referencia seed 42 — tienda 45

```json
{"tienda_id":45,"ventas":18569.0,"costos":7918.98,"opex":4522.51,"opinc":6127.51,"comuna":"La Granja"}
```

## Arquitectura

```
Cliente local (pnl_tool.py) ──httpx GET──► Cloud Run / uvicorn
                                              │
                                              ▼
                                         main.py → PNLService → TiendaPL
```

- **Servidor** (`src/`): expone JSON vía REST. Redeploy Cloud Run solo si cambia esto.
- **Cliente** (`scripts/pnl_tool.py`): corre en local; consume la API sin deploy.
- **Config** (`config/settings.py`): `API_BASE_URL` por entorno (12-factor).
- **NO conectar** `bq_cliente.py` aún (Fase async/BQ, esquema distinto).

## Comandos clave

```bash
# Local — API
cd cloud_run_rewrite && uvicorn src.main:app --reload --port 8000
cd cloud_run_rewrite && pytest -v

# Tool — local (requiere uvicorn en otra terminal)
cd cloud_run_rewrite
$env:API_BASE_URL="http://127.0.0.1:8000"
python scripts/pnl_tool.py --tienda_id 45
python scripts/pnl_tool.py --comuna "La Granja"

# Tool — Cloud Run (sin redeploy del script)
$env:API_BASE_URL="https://fde-pnl-api-198971893116.europe-west1.run.app"
python scripts/pnl_tool.py --tienda_id 45
python scripts/pnl_tool.py --comuna "La Granja"

# Docker local → navegador usa localhost:8080 (NO 0.0.0.0)
docker build -t fde-pnl-api .
docker run -p 8080:8080 fde-pnl-api

# Redeploy Cloud Run (PowerShell, UNA línea) — solo si cambia src/
gcloud run deploy fde-pnl-api --source=. --region=europe-west1 --allow-unauthenticated --port=8080
```

## Trampas aprendidas (no regresar)

| Error | Fix |
|---|---|
| `t.comuna` en tests | Usar `t["comuna"]` — `response.json()` = dicts, no Pydantic |
| Assert dict parcial vs API | Comparar **6 campos** de `TiendaPL` o asserts por campo |
| `docker build` sin `.` | Siempre `docker build -t fde-pnl-api .` desde `cloud_run_rewrite/` |
| PowerShell multilínea gcloud | Una sola línea o `--source=ruta` entre comillas |
| Navegador `0.0.0.0:8080` | Usar `localhost:8080` o URL `https://....run.app` |
| uvicorn desde repo root | Siempre cwd = `cloud_run_rewrite/` |
| `endpoint: f"..."` (con `:`) | Usar `endpoint = f"..."` — `:` anota tipo, `=` asigna valor |
| `$venv:API_BASE_URL` | Debe ser `$env:API_BASE_URL` |
| `$env` y `python` en una línea | Separar con Enter o `;` en PowerShell |
| `import Settings` vs `settings` | Importar `settings` (instancia), no la clase `Settings` |
| Tool no conecta a Cloud Run | No requiere redeploy — es cliente; verificar `$env:API_BASE_URL` |
| Redeploy innecesario del script | `pnl_tool.py` corre local; solo redeploy si cambia `src/` |
| `formatear_comuna(response.json())` | Pasar 2 args: `formatear_comuna(comuna, response.json())` |
| `httpx.RequestError` en tool local | uvicorn debe estar corriendo en `:8000` o usar URL Cloud Run |
| `python scripts/` desde repo root | Siempre `cd cloud_run_rewrite` primero |

## Roadmap — siguiente (orden)

1. [x] `config/settings.py` (env vars)
2. [x] Script tool: `scripts/pnl_tool.py` — HTTP → texto humano
3. [x] Segunda tool: consulta por comuna (`GET /api/v1/pnl?comuna=X`)
4. [ ] Tests de `pnl_tool` con mock httpx
5. [ ] Integrar `bq_cliente.py` (async, Fase 2)
6. [ ] Agente / MCP sobre la API (Fase 2 plan maestro)

## Archivos que importan

| Archivo | Rol |
|---|---|
| `src/main.py` | Rutas |
| `src/models.py` | Contrato |
| `src/services/pnl_services.py` | Datos + lógica |
| `test/test_main.py` | Tests |
| `Dockerfile` | Imagen Cloud Run |
| `README.md` | Docs humanas + URLs |
| `config/settings.py` | Env vars — `api_base_url` |
| `scripts/pnl_tool.py` | 2 tools: `consultar_tienda` + `consultar_comuna` |

## Última sesión (sesión corta — comuna tool)

**Logros:**
- `consultar_comuna()` — `GET /api/v1/pnl?comuna=X`
- `formatear_comuna()` — lista JSON → resumen con IDs + P&L agregado
- CLI: `--tienda_id` o `--comuna` (mutually exclusive)
- Verificado local + Cloud Run

**Conceptos:** query params, respuesta lista vs dict, múltiples tools, `RequestError` = API apagada.

**Commit sugerido:** `Add comuna filter tool to pnl_tool script`

**Próxima sesión:** tests de `pnl_tool` con mock httpx.

## Sesión anterior (Dom 28 Jun 2026)

- `config/settings.py`, primera tool `consultar_tienda`, README inicial del script tool
- Commit: `Add pnl_tool client script, settings, and update README`

## Qué NO asumir

- No hay BigQuery en sandbox.
- No hay agente LLM aún.
- No mezclar datos/API del trabajo Walmart con este repo.
- Portfolio #1 (ADK/MCP/$170K story) = **Fase 2**, no es este repo hoy.
