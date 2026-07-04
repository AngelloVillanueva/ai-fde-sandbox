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

## Estado (Fase 1 completa · Fase 2 iniciada — bq_cliente async)
| ✅ | Detalle |
|---|---|
| API | FastAPI `src/main.py`, 5 endpoints, seed 42 |
| Deploy | Cloud Run LIVE · Docker · 4 tests API |
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

`bq_cliente.py` (paralelo, no conectado): `BigQuerySimulatedClient` → `async get_tienda_por_id` → `TiendaPL` (mismo seed 42)

- Redeploy Cloud Run **solo** si cambia `src/main.py` o servicios conectados a la API. Script tool y `bq_cliente` local no se despliegan.
- **No conectar `bq_cliente` a `main.py` aún** — próximo paso de integración.

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
| Más trampas | Ver `README.md` |

## Roadmap
1. [x] settings · 2. [x] pnl_tool · 3. [x] tool comuna · 4. [x] tests pnl_tool mock
5. [x] `bq_cliente.py` async + tests (Fase 2 inicio)
6. [ ] **Próximo:** integrar `bq_cliente` en `PNLService` / endpoints async
7. [ ] Agente / MCP (Fase 2)

## Archivos clave
`src/main.py` · `pnl_services.py` · `bq_cliente.py` · `models.py` · `config/settings.py` · `scripts/pnl_tool.py` · `test/test_main.py` · `test/test_pnl_tool.py` · `test/test_bq_client.py`

## Última sesión
`bq_cliente.py`: alineado con `TiendaPL` + seed 42 · `get_tienda_por_id` async · 3 tests pytest-asyncio · **12 total green**.
Commit: `Align bq_cliente async client with TiendaPL schema and add tests`

## No asumir
Sin BQ real · `bq_cliente` no conectado a API · Sin LLM aún · No mezclar Walmart · Portfolio MCP = Fase 2

## Referencia carrera
Ver `CAREER.md` para perfil completo, stack target, checkpoints de mercado y frases de entrevista.
