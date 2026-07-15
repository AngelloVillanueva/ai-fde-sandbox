# CONTEXT — ai-fde-sandbox

> Agentes: lee esto antes de codear. Detalle en `README.md`.

## North star
**Carrera:** Senior AI FDE @ Palantir/Google Cloud, remoto Chile, $150K–220K.
**Proyecto:** API P&L → URL pública → agente con tool calling → MCP server.
**Walmart (separado):** P&L real + BQ + Cloud Run. No replicar aquí.

### Progreso north star (proyecto)
| Hito | Estado |
|---|---|
| API FastAPI + tests | ✅ |
| Deploy Cloud Run (URL pública) | ✅ |
| Tools HTTP (`pnl_tool.py`) | ✅ |
| Agente Gemini tool calling | ✅ verificado |
| MCP server (portfolio FDE) | ✅ **verificado Jul 2026** |
| Narrativa GitHub/LinkedIn | ⏳ **Sesión 9** |

## Método
11h/sem · 1 concepto + 1 mini build + 1 commit · anti-vibe-coding · Viernes OFF

## Protocolo sesión (resumen)
- Apunta a North Star FDE Palantir/Google.
- Conceptos: técnico + analogía + por qué FDE + "reclutador pregunta X → respondes Y".
- Respuestas cortas · glosario al inicio · **ruta exacta** al sugerir cambios.
- **Angello escribe; agente guía.** No codear sin pedido. No sobrediseñar. Commit al cierre.
- Verificación simple (`pytest`, `python scripts/...`). No one-liners crípticos.

## Estado (Fase 2 — MCP LIVE)
| ✅ | Detalle |
|---|---|
| API | FastAPI `src/main.py`, 5 endpoints, seed 42 |
| Async | `GET /api/v1/pnl/{tienda_id}` → `get_tienda_por_id_async` → `bq_cliente` |
| Deploy | Cloud Run LIVE · redeploy Jul 2026 · Docker · 4 tests API |
| Cliente | `scripts/pnl_tool.py` — `--tienda_id` / `--comuna` |
| Config | `config/settings.py` → `API_BASE_URL` + `GEMINI_API_KEY` vía `.env` |
| Tests tools | `test/test_pnl_tool.py` — 5 unit tests mock httpx |
| BQ simulado | `src/services/bq_cliente.py` — `BigQuerySimulatedClient` async · `TiendaPL` · seed 42 |
| Tests BQ | `test/test_bq_client.py` — 3 tests `@pytest.mark.asyncio` · **12 total** |
| Agente | `scripts/pnl_agent.py` — Gemini tool calling · REPL · verificado |
| Registry | `scripts/tool_registry.py` — `TOOL_SCHEMAS` + `run_tool()` (dispatcher único) |
| MCP server | `scripts/mcp_server.py` — FastMCP · 2 tools · **verificado Jul 2026** |
| MCP config | `.cursor/mcp.json` — Cursor lanza el server con Python del venv |

**URL:** `https://fde-pnl-api-198971893116.europe-west1.run.app`
**Tienda ref (seed 42):** id 45 · La Granja · opinc 6127.51
**Modelo agente:** `gemini-3.1-flash-lite` (ver cuotas en AI Studio — no usar modelos con 0/0)
**IDs:** 1–100 (no `store_001`)

## Árbol del proyecto

> **cwd habitual:** `cloud_run_rewrite/` · **venv:** `.venv/` en la raíz del repo (no dentro de `cloud_run_rewrite/`)

```
ai-fde-sandbox/                              ← raíz del repo (git)
│
├── .venv/                                   ← entorno Python (gitignored · activar desde aquí)
├── .gitignore
│
├── README.md                                ← docs públicas · demo · arquitectura detallada
├── CONTEXT.md                               ← handoff agentes · estado · trampas · roadmap
├── CAREER.md                                ← north star carrera · stack FDE · fases
│
├── career-assets/
│   └── CV_EN.md                             ← CV en inglés (portfolio)
│
└── cloud_run_rewrite/                       ← ★ proyecto principal · cd aquí para trabajar
    │
    ├── .env                                 ← GEMINI_API_KEY local (gitignored)
    ├── .dockerignore
    ├── Dockerfile                           ← imagen para Cloud Run
    ├── requirements.txt                     ← deps Python (FastAPI, httpx, google-genai, …)
    ├── deploy-log.txt                       ← log local de deploys
    │
    ├── config/                              ← configuración por entorno
    │   └── settings.py                      ← API_BASE_URL + GEMINI_API_KEY (pydantic-settings)
    │
    ├── scripts/                             ← capa LOCAL · no se despliega a Cloud Run
    │   ├── pnl_tool.py                      ← tools: httpx → API → texto humano
    │   ├── tool_registry.py                 ← TOOL_SCHEMAS + run_tool() (dispatcher único)
    │   ├── pnl_agent.py                     ← agente REPL · Gemini tool calling (2 viajes)
    │   └── mcp_server.py                    ← MCP server · FastMCP · 2 tools · verificado
    │
    ├── src/                                 ← capa API · SÍ se despliega a Cloud Run
    │   ├── main.py                          ← FastAPI · 5 endpoints · HTTP 404 desde BQ envelope
    │   ├── models.py                        ← TiendaPL (contrato Pydantic)
    │   └── services/
    │       ├── pnl_services.py              ← PNLService · datos sintéticos seed 42
    │       └── bq_cliente.py                ← BigQuerySimulatedClient async (GET /pnl/{id})
    │
    └── test/                                ← 12 tests total
        ├── conftest.py                      ← fixtures compartidas pytest
        ├── test_main.py                     ← integration API (4 tests · TestClient)
        ├── test_pnl_tool.py                 ← unit tools (5 tests · mock httpx)
        └── test_bq_client.py                ← unit BQ async (3 tests · pytest-asyncio)
```

| Capa | Ruta | Deploy Cloud Run | Qué hace |
|---|---|---|---|
| Docs / carrera | `README.md`, `CONTEXT.md`, `CAREER.md` | — | Handoff, demo, north star |
| Config | `config/settings.py`, `.env` | — | URLs y API keys por entorno |
| Tools + agente | `scripts/` | No | Consumen la API; Gemini elige tools vía `tool_registry` |
| API | `src/` | **Sí** | Expone P&L JSON vía REST |
| Datos | `src/services/` | Sí (dentro de API) | Seed 42 · async en `/pnl/{id}` · sync en list/comuna |
| Tests | `test/` | — | CI local sin red externa (mock donde aplica) |
| Infra | `Dockerfile`, `requirements.txt` | Sí | Build y deps del contenedor |

## Arquitectura

**Agente REPL (Gemini):**
```
Terminal → pnl_agent.py → Gemini viaje 1 → run_tool() → pnl_tool.py → httpx → Cloud Run
        ← Gemini viaje 2 (prosa) ← resultado texto ←──────────────────────────────────
```

**MCP (Cursor):**
```
Cursor chat → Cursor LLM → MCP stdio → mcp_server.py → run_tool() → pnl_tool.py → httpx → Cloud Run
           ← Cursor LLM (prosa) ← resultado texto ←──────────────────────────────────────────────
```

Los dos sistemas comparten `run_tool()` + `pnl_tool.py` + Cloud Run API. El LLM es distinto (Gemini vs el de Cursor). MCP **no usa Gemini**.

**Por tienda (async):** `GET /api/v1/pnl/{id}` → `get_tienda_por_id_async` → `BigQuerySimulatedClient` → envelope `{status, data}` → `TiendaPL`

**List/comuna/opinc (sync):** `PNLService` → `_database` (= `bq.mock_database`, seed 42)

- Agente, MCP y tools corren **local** — no se despliegan en Cloud Run.
- Redeploy Cloud Run **solo** si cambia `src/`.

## Comandos (cwd = `cloud_run_rewrite/`)
```powershell
# venv (desde raíz del repo)
Set-Location "c:\Users\Angello\Desktop\AI FDE\ai-fde-sandbox"
.\.venv\Scripts\Activate.ps1
Set-Location cloud_run_rewrite

uvicorn src.main:app --reload --port 8000
pytest -v
python -m src.services.bq_cliente
$env:API_BASE_URL="https://fde-pnl-api-198971893116.europe-west1.run.app"; python scripts/pnl_tool.py --tienda_id 45
$env:API_BASE_URL="https://fde-pnl-api-198971893116.europe-west1.run.app"; python scripts/pnl_agent.py
gcloud run deploy fde-pnl-api --source=. --region=europe-west1 --allow-unauthenticated --port=8080
```

## Trampas críticas
| Error | Fix |
|---|---|
| cwd ≠ `cloud_run_rewrite/` | Siempre `cd` ahí |
| `$venv:` vs `$env:` | Usar `$env:API_BASE_URL` |
| `endpoint: f"..."` | Usar `=` no `:` |
| `import Settings` | Importar `settings` (instancia) |
| Tool falla local | uvicorn :8000 o URL Cloud Run |
| `formatear_comuna(json)` | 2 args: `(comuna, lista)` |
| `@patch` ruta wrong | `"scripts.pnl_tool.httpx.get"` |
| Test async sin decorator | Usar `@pytest.mark.asyncio` + `await` |
| `result["data"]["comuna"]` | `data` es `TiendaPL` → `result["data"].comuna` |
| Borrar `get_tienda_por_id` sync | Rompe test consistencia + `get_opinc_por_id` |
| `result["status"]` vs HTTP 404 | BQ envelope → `HTTPException(404)` en `main.py` |
| Gemini `limit: 0` | Modelo sin cuota en tu tier — ver AI Studio, usar modelos con RPD > 0 |
| Gemini `thought_signature` | Viaje 2: pasar `response.candidates[0].content` completo, no reconstruir `function_call` |
| Agente sin venv | Activar `.venv` desde raíz del repo antes de `python scripts/pnl_agent.py` |
| SDK deprecado | Solo `google-genai` — no `google.generativeai` |
| MCP `command: "python"` | No apunta al venv → usar ruta absoluta al `.exe` del venv |
| MCP `args` ruta relativa | Cursor no usa `cwd` para resolver `args` → ruta absoluta en `args` |
| MCP activa venv en `command` | No se puede activar venv en MCP → apuntar directo al `.exe` del venv |
| Más trampas | Ver `README.md` |

## Roadmap
1. [x] settings · 2. [x] pnl_tool · 3. [x] tool comuna · 4. [x] tests pnl_tool mock
5. [x] `bq_cliente.py` async + tests
6. [x] Integrar `bq_cliente` en `GET /api/v1/pnl/{id}` (async) + redeploy Cloud Run
7. [x] Agente `pnl_agent.py` — Gemini tool calling + REPL · verificado
8. [x] MCP server `mcp_server.py` — FastMCP · 2 tools · verificado en Cursor
9. [ ] **Próximo:** Narrativa GitHub/LinkedIn + demo del portfolio
10. [ ] `docker-compose.yml` — portabilidad sin Cloud Run (opcional)
11. [ ] Migrar endpoints list/comuna/opinc a async (opcional)

## Archivos clave (atajo)
Ver **Árbol del proyecto** arriba. Los más tocados: `src/main.py` · `pnl_services.py` · `bq_cliente.py` · `scripts/pnl_tool.py` · `scripts/tool_registry.py` · `scripts/pnl_agent.py` · `scripts/mcp_server.py` · `.cursor/mcp.json`

## Última sesión
MCP server **verificado** (Jul 2026): `mcp_server.py` · FastMCP 3.4.4 · 2 tools (`consultar_tienda`, `consultar_comuna`) · Cursor invocó `consultar_tienda(45)` → `opinc 6127.51 · La Granja` vía Cloud Run.
`requirements.txt` estabilizado: `fastapi>=0.115.0` · `google-genai>=2.10.0` · `fastmcp>=3.4.0` · 12 tests green.
Commits pendientes:
- `Add PnL conversational agent with Gemini tool calling`
- `Add MCP server exposing PnL tools via FastMCP`

## No asumir
Sin BQ real · Agente y MCP locales (no deployados) · MCP no usa Gemini — usa el LLM de Cursor · No mezclar Walmart

## Conceptos clave (para el agente y para Angello)

### Tool calling — los 2 viajes
El LLM no ejecuta código. Solo pide que lo ejecutes tú.

```
VIAJE 1  usuario → Gemini (pregunta + tool schemas)
         Gemini  → function_call {name, args}   ← Gemini NO ejecuta

VIAJE 2  tú ejecutas run_tool(name, args) → resultado real
         pasar response.candidates[0].content COMPLETO (thought_signature)
         resultado → Gemini → respuesta en prosa → usuario
```

### Gemini — modelos y cuotas
Verificar en AI Studio → "Límites de frecuencia por modelo". Solo usar modelos con cuota > 0 (ej. `gemini-3.1-flash-lite` 500 RPD). Modelos con 0/0 fallan con `limit: 0`.

### sys.path en scripts/
Scripts dentro de `scripts/` no ven `config/` ni `src/` sin esto:
```python
_ROOT = Path(__file__).resolve().parent.parent  # sube a cloud_run_rewrite/
sys.path.insert(0, str(_ROOT))
```
Todo script nuevo que importe `config.settings` necesita este bloque.

### SDK de Gemini — solo uno
Usar únicamente `google-genai` (`from google import genai`).
`google.generativeai` está deprecado desde 2025 — no usarlo.

### API key — flujo por entorno
| Entorno | Mecanismo |
|---|---|
| Sandbox (local) | `.env` → `pydantic-settings` → `settings.gemini_api_key` |
| Producción cloud | Secret Manager → inject en runtime |
| Enterprise GCP | Application Default Credentials (ADC), sin key explícita |

### Venv — activar siempre antes de correr el agente
```powershell
Set-Location "c:\Users\Angello\Desktop\AI FDE\ai-fde-sandbox"
.\.venv\Scripts\Activate.ps1
# prompt muestra (.venv) — ahora sí están los paquetes
```

### Tool schema — campos obligatorios
```python
{"name": "...",           # debe coincidir exacto con run_tool
 "description": "...",    # Gemini decide qué tool usar según esto
 "parameters": {
   "type": "object",
   "properties": {"param": {"type": "integer|string", "description": "..."}},
   "required": ["param"]
 }}
```

### MCP — principio de diseño
El MCP server **no duplica lógica**. Cada `@mcp.tool` delega a `run_tool()`:

```python
@mcp.tool()
def consultar_tienda(tienda_id: int) -> str:
    """Docstring = descripción que ve el LLM del host (Cursor)."""
    return run_tool("consultar_tienda", {"tienda_id": tienda_id})
```

El docstring equivale a `description` en `TOOL_SCHEMAS`. Los type hints (`int`, `str`) generan el schema automáticamente. Cursor no activa el venv — en `mcp.json` el `command` apunta directo al `.exe` del venv.

### MCP vs Agente Gemini — diferencia clave

| | `pnl_agent.py` | `mcp_server.py` |
|---|---|---|
| LLM | Gemini (API key propia) | El LLM de Cursor (Claude/GPT) |
| Protocolo | Custom (SDK google-genai) | MCP estándar (stdio JSON-RPC) |
| Lanzamiento | `python scripts/pnl_agent.py` | Cursor lo lanza automáticamente |
| Tools | `run_tool()` | `run_tool()` (mismo dispatcher) |
| Cloud Run | ✅ misma API | ✅ misma API |

## Referencia carrera
Ver `CAREER.md` para perfil completo, stack target, checkpoints de mercado y frases de entrevista.
