# CONTEXT — ai-fde-sandbox

> Agentes: lee esto antes de codear. Detalle en `README.md`.

## North star
**Carrera:** Senior AI FDE @ Palantir/Google Cloud, remoto Chile, $150K–220K.
**Proyecto:** API P&L → URL pública → agente con tool calling.
**Walmart (separado):** P&L real + BQ + Cloud Run. No replicar aquí.

## Método
11h/sem · 1 concepto + 1 mini build + 1 commit · anti-vibe-coding · Viernes OFF

## Protocolo sesión (resumen)
- Apunta a North Star FDE Palantir/Google.
- Conceptos: técnico + analogía + por qué FDE + "reclutador pregunta X → respondes Y".
- Respuestas cortas · glosario al inicio · **ruta exacta** al sugerir cambios.
- **Angello escribe; agente guía.** No codear sin pedido. No sobrediseñar. Commit al cierre.
- Verificación simple (`pytest`, `python scripts/...`). No one-liners crípticos.

## Estado (Fase 2 — bq_cliente integrado en API)
| ✅ | Detalle |
|---|---|
| API | FastAPI `src/main.py`, 5 endpoints, seed 42 |
| Async | `GET /api/v1/pnl/{tienda_id}` → `get_tienda_por_id_async` → `bq_cliente` |
| Deploy | Cloud Run LIVE · redeploy Jul 2026 · Docker · 4 tests API |
| Cliente | `scripts/pnl_tool.py` — `--tienda_id` / `--comuna` |
| Config | `config/settings.py` → `$env:API_BASE_URL` |
| Tests tools | `test/test_pnl_tool.py` — 5 unit tests mock httpx |
| BQ simulado | `src/services/bq_cliente.py` — `BigQuerySimulatedClient` async · `TiendaPL` · seed 42 |
| Tests BQ | `test/test_bq_client.py` — 3 tests `@pytest.mark.asyncio` · **12 total** |

**URL:** `https://fde-pnl-api-198971893116.europe-west1.run.app`
**Tienda ref (seed 42):** id 45 · La Granja · opinc 6127.51
**IDs:** 1–100 (no `store_001`)

## Arquitectura
`pnl_tool (cliente local)` → httpx GET → `Cloud Run/uvicorn` → `main.py` → `PNLService` → `TiendaPL`

**Por tienda (async):** `GET /api/v1/pnl/{id}` → `get_tienda_por_id_async` → `BigQuerySimulatedClient` → envelope `{status, data}` → `TiendaPL`

**List/comuna/opinc (sync):** `PNLService` → `_database` (= `bq.mock_database`, seed 42)

- Redeploy Cloud Run **solo** si cambia `src/`. Script tool no se despliega.
- Endpoints list/comuna/opinc **aún sync** — migración incremental pendiente.

## Comandos (cwd = `cloud_run_rewrite/`)
```powershell
uvicorn src.main:app --reload --port 8000
pytest -v
python -m src.services.bq_cliente
$env:API_BASE_URL="http://127.0.0.1:8000"; python scripts/pnl_tool.py --tienda_id 45
$env:API_BASE_URL="https://fde-pnl-api-198971893116.europe-west1.run.app"; python scripts/pnl_tool.py --comuna "La Granja"
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
| Más trampas | Ver `README.md` |

## Roadmap
1. [x] settings · 2. [x] pnl_tool · 3. [x] tool comuna · 4. [x] tests pnl_tool mock
5. [x] `bq_cliente.py` async + tests
6. [x] Integrar `bq_cliente` en `GET /api/v1/pnl/{id}` (async) + redeploy Cloud Run
7. [x] `pnl_agent.py` escrito — Gemini tool calling + REPL (pendiente verificar en prod)
8. [ ] **Próximo:** probar agente + commit + MCP server
9. [ ] Migrar endpoints list/comuna/opinc a async (opcional)

## Archivos clave
`src/main.py` · `pnl_services.py` · `bq_cliente.py` · `models.py` · `config/settings.py` · `scripts/pnl_tool.py` · `scripts/tool_registry.py` · `scripts/pnl_agent.py` · `test/test_main.py` · `test/test_pnl_tool.py` · `test/test_bq_client.py`

## Última sesión
`pnl_agent.py`: Gemini tool calling con `google-genai` SDK · `chat_once()` con 2 viajes · REPL `main()` · `sys.path` fix · `tool_registry.py` limpio (sin SDK). Agente escrito pero **aún no verificado en ejecución** — pendiente correr con venv activo.
Commit pendiente: `Add PnL conversational agent with Gemini tool calling`

## No asumir
Sin BQ real · Solo 1 endpoint async · Sin LLM en API · No mezclar Walmart · Portfolio MCP = Fase 2

## Conceptos clave (para el agente y para Angello)

### Tool calling — los 2 viajes
El LLM no ejecuta código. Solo pide que lo ejecutes tú.

```
VIAJE 1  usuario → Gemini (pregunta + tool schemas)
         Gemini  → function_call {name, args}   ← Gemini NO ejecuta

VIAJE 2  tú ejecutas run_tool(name, args) → resultado real
         resultado → Gemini → respuesta en prosa → usuario
```

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

## Referencia carrera
Ver `CAREER.md` para perfil completo, stack target, checkpoints de mercado y frases de entrevista.
