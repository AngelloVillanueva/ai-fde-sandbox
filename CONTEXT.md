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

## Estado (Fase 1 completa + tests tools)
| ✅ | Detalle |
|---|---|
| API | FastAPI `src/main.py`, 5 endpoints, seed 42 |
| Deploy | Cloud Run LIVE · Docker · 4 tests API |
| Cliente | `scripts/pnl_tool.py` — `--tienda_id` / `--comuna` |
| Config | `config/settings.py` → `$env:API_BASE_URL` |
| Tests tools | `test/test_pnl_tool.py` — 5 unit tests mock httpx · **9 total** |

**URL:** `https://fde-pnl-api-198971893116.europe-west1.run.app`
**Tienda ref (seed 42):** id 45 · La Granja · opinc 6127.51
**IDs:** 1–100 (no `store_001`)

## Arquitectura
`pnl_tool (cliente local)` → httpx GET → `Cloud Run/uvicorn` → `main.py` → `PNLService` → `TiendaPL`
- Redeploy Cloud Run **solo** si cambia `src/`. Script tool no se despliega.
- No conectar `bq_cliente.py` aún.

## Comandos (cwd = `cloud_run_rewrite/`)
```powershell
uvicorn src.main:app --reload --port 8000
pytest -v
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
| Más trampas | Ver `README.md` |

## Roadmap
1. [x] settings · 2. [x] pnl_tool · 3. [x] tool comuna · 4. [x] tests pnl_tool mock
5. [ ] **Próximo:** `bq_cliente.py` async (Fase 2)
6. [ ] Agente / MCP (Fase 2)

## Archivos clave
`src/main.py` · `pnl_services.py` · `models.py` · `config/settings.py` · `scripts/pnl_tool.py` · `test/test_main.py` · `test/test_pnl_tool.py`

## Última sesión
Unit tests pnl_tool: `@patch` + `MagicMock`, 5 tests, 9 total green.
Commit: `Add unit tests for pnl_tool with httpx mock`

## No asumir
Sin BQ · Sin LLM aún · No mezclar Walmart · Portfolio MCP = Fase 2
