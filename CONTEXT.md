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

## Estado actual (Fase 1 ~completa)

| Hecho | Detalle |
|---|---|
| API FastAPI | `cloud_run_rewrite/src/main.py` |
| SSOT datos | `PNLService` + `random.seed(42)` en `_generador_datos_sinteticos()` |
| Schema | `TiendaPL`: tienda_id, ventas, costos, opex, opinc, comuna |
| Tests | 4 integration tests en `test/test_main.py` — todos pasan |
| Docker | `Dockerfile` + `.dockerignore` |
| Cloud Run | **LIVE** — ver URL abajo |

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
HTTP → main.py → PNLService → TiendaPL (memoria)
```

- **NO conectar** `bq_cliente.py` aún (Fase async/BQ, esquema distinto).
- `config/settings.py` vacío (pendiente pydantic-settings).

## Comandos clave

```bash
# Local
cd cloud_run_rewrite && uvicorn src.main:app --reload --port 8000
cd cloud_run_rewrite && pytest -v

# Docker local → navegador usa localhost:8080 (NO 0.0.0.0)
docker build -t fde-pnl-api .
docker run -p 8080:8080 fde-pnl-api

# Redeploy Cloud Run (PowerShell, UNA línea)
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

## Roadmap — siguiente (orden)

1. [ ] `config/settings.py` (env vars)
2. [ ] Script tool: HTTP → respuesta texto humano (puente agente)
3. [ ] Integrar `bq_cliente.py` (async, Fase 2)
4. [ ] Agente / MCP sobre la API (Fase 2 plan maestro)

## Archivos que importan

| Archivo | Rol |
|---|---|
| `src/main.py` | Rutas |
| `src/models.py` | Contrato |
| `src/services/pnl_services.py` | Datos + lógica |
| `test/test_main.py` | Tests |
| `Dockerfile` | Imagen Cloud Run |
| `README.md` | Docs humanas + URLs |

## Qué NO asumir

- No hay BigQuery en sandbox.
- No hay agente LLM aún.
- No mezclar datos/API del trabajo Walmart con este repo.
- Portfolio #1 (ADK/MCP/$170K story) = **Fase 2**, no es este repo hoy.
