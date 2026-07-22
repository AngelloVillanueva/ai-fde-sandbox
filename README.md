# ai-fde-sandbox

Sandbox de práctica para construir una **API de análisis financiero P&L** orientada a tiendas retail. Expone datos sintéticos vía HTTP, un agente conversacional con Gemini tool calling, y un servidor MCP integrado con Cursor.

El caso de uso simula consultas del tipo: *¿Cómo le fue a la tienda 45?*, *¿Está por encima del promedio?* o *¿Cuál tienda rinde mejor en La Granja?*

**North star del proyecto:** API P&L → URL pública → agente con tool calling → MCP server — **completado**. **Capa agente ampliada (Jul 2026):** 6 tools · insights · evals · multi-turn REPL. Siguiente: narrativa portfolio + redeploy `/analisis`.

> **Handoff para sesiones AI:** ver [`CONTEXT.md`](CONTEXT.md) (estado del proyecto, north star, trampas conocidas).

---

## Demo en producción (Cloud Run)

**Base URL:** https://fde-pnl-api-198971893116.europe-west1.run.app

| Recurso | URL |
|---|---|
| Health check | https://fde-pnl-api-198971893116.europe-west1.run.app/health |
| Swagger UI | https://fde-pnl-api-198971893116.europe-west1.run.app/docs |
| P&L tienda 45 | https://fde-pnl-api-198971893116.europe-west1.run.app/api/v1/pnl/45 |
| Análisis tienda 45 | https://fde-pnl-api-198971893116.europe-west1.run.app/api/v1/pnl/45/analisis |
| Filtro por comuna | https://fde-pnl-api-198971893116.europe-west1.run.app/api/v1/pnl?comuna=La%20Granja |

> `/analisis` requiere **redeploy** reciente de Cloud Run. Endpoints previos siguen live.

> Región: `europe-west1` · Proyecto GCP personal · Datos sintéticos (no BigQuery).

---

## Stack

| Capa | Tecnología |
|---|---|
| API | [FastAPI](https://fastapi.tiangolo.com/) |
| Validación / schema | [Pydantic](https://docs.pydantic.dev/) |
| Servidor | [Uvicorn](https://www.uvicorn.org/) |
| Tests | [pytest](https://docs.pytest.org/) + `TestClient` + [pytest-asyncio](https://pytest-asyncio.readthedocs.io/) |
| Cliente HTTP (tool) | [httpx](https://www.python-httpx.org/) |
| Config por entorno | [pydantic-settings](https://docs.pydantic.dev/latest/concepts/pydantic_settings/) |
| Contenedor | Docker |
| Despliegue | [Google Cloud Run](https://cloud.google.com/run) |
| LLM / Agente | [Google Gemini API](https://ai.google.dev/) (`google-genai`) |
| MCP server | [FastMCP](https://gofastmcp.com/) 3.4.x — protocolo estándar para tools |

---

## Estructura del repositorio

```
ai-fde-sandbox/
├── .gitignore
├── README.md
└── cloud_run_rewrite/
    ├── .dockerignore
    ├── config/
    │   └── settings.py          # Env vars (API_BASE_URL, GEMINI_API_KEY)
    ├── .env                     # GEMINI_API_KEY local (gitignored)
    ├── scripts/
    │   ├── pnl_tool.py          # 6 tools: HTTP → texto humano
    │   ├── tool_registry.py     # Schemas + dispatcher run_tool()
    │   ├── agent_prompt.py      # System prompt del agente Gemini
    │   ├── pnl_agent.py         # Agente REPL · multi-turn · Gemini tool calling
    │   ├── mcp_server.py        # MCP server (FastMCP) · 6 tools
    │   └── run_agent_evals.py   # Eval live manual (requiere GEMINI_API_KEY)
    ├── src/
    │   ├── main.py              # FastAPI · 6 endpoints
    │   ├── models.py            # Schema TiendaPL
    │   └── services/
    │       ├── pnl_services.py  # PNLService · analizar_tienda() · seed 42
    │       └── bq_cliente.py    # Simulador BigQuery async
    ├── test/
    │   ├── test_main.py         # Integration tests API (10)
    │   ├── test_pnl_tool.py     # Unit tests tools (11)
    │   ├── test_bq_client.py    # Unit tests BQ async (3)
    │   ├── test_agent_eval.py   # Routing agente + run_tool (16)
    │   └── fixtures/
    │       └── agent_eval_cases.json
    ├── Dockerfile
    └── requirements.txt
```

---

## Modelo de datos

Contrato central: `TiendaPL` (100 tiendas, IDs `1`–`100`).

| Campo | Descripción |
|---|---|
| `tienda_id` | Identificador entero de la tienda |
| `ventas` | Ingresos por ventas |
| `costos` | Costo de ventas (COGS) |
| `opex` | Gastos operativos |
| `opinc` | Ingreso operativo (`ventas - costos - opex`) |
| `comuna` | Ubicación geográfica (filtro por query param) |

Los datos se generan en memoria en `PNLService` con `random.seed(42)` para garantizar **reproducibilidad** en tests y demos.

El módulo `bq_cliente.py` replica el mismo contrato (`TiendaPL`, seed 42) como **cliente async simulado** de BigQuery. Alimenta `GET /api/v1/pnl/{tienda_id}` vía `PNLService.get_tienda_por_id_async`. List/comuna/opinc siguen leyendo `_database` sync.

---

## Endpoints

| Método | Ruta | Descripción |
|---|---|---|
| `GET` | `/health` | Health check del servicio |
| `GET` | `/docs` | Documentación interactiva (Swagger UI) |
| `GET` | `/api/v1/pnl` | Lista todas las tiendas |
| `GET` | `/api/v1/pnl?comuna={nombre}` | Filtra tiendas por comuna |
| `GET` | `/api/v1/pnl/{tienda_id}` | P&L completo de una tienda |
| `GET` | `/api/v1/pnl/{tienda_id}/opinc` | Solo el ingreso operativo |
| `GET` | `/api/v1/pnl/{tienda_id}/analisis` | Margen y comparación vs promedio del portfolio |

**Respuesta `/analisis` (tienda 45, seed 42):** incluye `margen_pct`, `promedio_portfolio_opinc`, `diff_opinc_vs_promedio`, `diff_pct_vs_promedio`.

**Referencia fija (seed 42, tienda 45):**

```json
{
  "tienda_id": 45,
  "ventas": 18569.0,
  "costos": 7918.98,
  "opex": 4522.51,
  "opinc": 6127.51,
  "comuna": "La Granja"
}
```

---

## Desarrollo local

### Requisitos

- Python 3.11+ (probado con 3.14)
- `pip`

### Instalación

```bash
cd cloud_run_rewrite
python -m venv .venv

# Windows
.venv\Scripts\activate

pip install -r requirements.txt
```

### Arrancar la API

```bash
cd cloud_run_rewrite
uvicorn src.main:app --reload --port 8000
```

Abrir en el navegador:

- http://127.0.0.1:8000/health
- http://127.0.0.1:8000/docs
- http://127.0.0.1:8000/api/v1/pnl/45

> Ejecutar `uvicorn` desde `cloud_run_rewrite/` para que los imports (`src.main`) resuelvan correctamente.

### Tests

```bash
# Desde raíz del repo o cloud_run_rewrite/
pytest -v                              # todos (40 tests)
pytest cloud_run_rewrite/test/test_main.py -v       # API (10)
pytest cloud_run_rewrite/test/test_pnl_tool.py -v   # tools (11)
pytest cloud_run_rewrite/test/test_bq_client.py -v  # BQ async (3)
pytest cloud_run_rewrite/test/test_agent_eval.py -v # agent eval (16)
```

| Archivo | Tipo | Qué prueba |
|---|---|---|
| `test/test_main.py` | Integration | API vía `TestClient` — health, P&L, opinc, analisis, list |
| `test/test_pnl_tool.py` | Unit | 6 tools + formatters con `@patch` httpx |
| `test/test_bq_client.py` | Unit async | `BigQuerySimulatedClient` |
| `test/test_agent_eval.py` | Unit mock | `run_tool()` dispatch · routing Gemini (mock `get_client`) |

Los tests de agente **no requieren** `GEMINI_API_KEY` (cliente lazy + mocks). Eval live: `python scripts/run_agent_evals.py`.

Verificación manual del simulador:

```powershell
cd cloud_run_rewrite
python -m src.services.bq_cliente
```

### MCP server (`mcp_server.py`) — 6 tools verificadas

Servidor MCP que expone **6 tools** al IDE Cursor. **No usa Gemini** — el LLM de Cursor invoca las tools vía MCP (stdio JSON-RPC).

| Tool MCP | Uso típico |
|---|---|
| `consultar_tienda` | P&L completo de una tienda |
| `consultar_opinc` | Solo OPINC |
| `consultar_comuna` | Agregado por comuna |
| `comparar_tiendas` | Ranking OPINC en comuna |
| `resumen_portfolio` | Vista ejecutiva 100 tiendas |
| `analizar_tienda` | Margen vs promedio portfolio |

**Principio:** cada `@mcp.tool` delega a `run_tool()` — mismo dispatcher que Gemini.

**Configurar en Cursor** — crear `.cursor/mcp.json` en la raíz del repo:

```json
{
  "mcpServers": {
    "pnl-tools": {
      "command": "RUTA_ABSOLUTA\\.venv\\Scripts\\python.exe",
      "args": ["RUTA_ABSOLUTA\\cloud_run_rewrite\\scripts\\mcp_server.py"],
      "cwd": "RUTA_ABSOLUTA\\cloud_run_rewrite",
      "env": {
        "API_BASE_URL": "https://fde-pnl-api-198971893116.europe-west1.run.app"
      }
    }
  }
}
```

> `command` debe apuntar al `.exe` del venv, no a `python` del sistema. Cursor no activa el venv — lanza el proceso directamente. Todas las rutas son absolutas (JSON en Windows usa `\\`).

**Verificar:** `Ctrl+Shift+J` → MCP → `pnl-tools` con punto verde y **6 tools** listadas.

**Probar en chat de Cursor** (chat nuevo para no gastar tokens de esta sesión):

```
Usa la tool consultar_tienda con tienda_id 45
```

Resultado esperado: `opinc 6127.51 · La Granja`.

---

### Agente conversacional (`pnl_agent.py`)

Agente REPL con **Gemini tool calling** (`gemini-3.1-flash-lite`). System prompt en `agent_prompt.py`. Soporta **multi-turn** (memoria en sesión) y comando `reset`.

**Comandos REPL:** `salir` · `reset` (nueva conversación)

**Requisitos:** venv activo · `GEMINI_API_KEY` en `cloud_run_rewrite/.env` · cuota > 0 en AI Studio

```powershell
# Activar venv primero (obligatorio)
Set-Location "c:\Users\Angello\Desktop\AI FDE\ai-fde-sandbox"
.\.venv\Scripts\Activate.ps1

Set-Location cloud_run_rewrite
# GEMINI_API_KEY en .env · API_BASE_URL opcional (default localhost)
$env:API_BASE_URL="https://fde-pnl-api-198971893116.europe-west1.run.app"

python scripts/pnl_agent.py
```

```
Agente P&L · escribe 'salir' para terminar · 'reset' para nueva conversacion

Tú: ¿Cómo le fue a la tienda 45?
Agente: [P&L completo con cifras grounded]

Tú: ¿Está por encima del promedio?
Agente: [usa analizar_tienda · compara vs portfolio]

Tú: reset
Conversacion reiniciada.
```

### Script tool (`pnl_tool.py`)

Cliente local con **6 tools** que llaman la API y devuelven texto legible:

| Tool | CLI | Endpoint API |
|---|---|---|
| P&L tienda | `--tienda_id 45` | `GET /api/v1/pnl/{id}` |
| Solo OPINC | `--opinc 45` | `GET /api/v1/pnl/{id}/opinc` |
| Por comuna | `--comuna "La Granja"` | `GET /api/v1/pnl?comuna=X` |
| Ranking comuna | `--ranking "La Granja"` | `GET /api/v1/pnl?comuna=X` + sort |
| Portfolio | `--portfolio` | `GET /api/v1/pnl` |
| Análisis vs promedio | `--analisis 45` | `GET /api/v1/pnl/{id}/analisis` |

**Local** (requiere uvicorn corriendo en otra terminal):

```powershell
cd cloud_run_rewrite
$env:API_BASE_URL="http://127.0.0.1:8000"
python scripts/pnl_tool.py --tienda_id 45
python scripts/pnl_tool.py --opinc 45
python scripts/pnl_tool.py --comuna "La Granja"
python scripts/pnl_tool.py --ranking "La Granja"
python scripts/pnl_tool.py --portfolio
python scripts/pnl_tool.py --analisis 45
```

**Producción** (Cloud Run — no requiere redeploy del script):

```powershell
$env:API_BASE_URL="https://fde-pnl-api-198971893116.europe-west1.run.app"
python scripts/pnl_tool.py --tienda_id 45
python scripts/pnl_tool.py --opinc 45
python scripts/pnl_tool.py --comuna "La Granja"
python scripts/pnl_tool.py --ranking "La Granja"
python scripts/pnl_tool.py --portfolio
python scripts/pnl_tool.py --analisis 45
```

Default sin `$env:API_BASE_URL`: `http://127.0.0.1:8000` (definido en `config/settings.py`).

---

## Docker (local)

Desde `cloud_run_rewrite/`:

```bash
docker build -t fde-pnl-api .
docker run -p 8080:8080 fde-pnl-api
```

Abrir en el navegador (**usar `localhost`, no `0.0.0.0`**):

- http://localhost:8080/health
- http://localhost:8080/api/v1/pnl/45

`0.0.0.0` en el Dockerfile es la dirección de **escucha dentro del contenedor**. Desde tu PC accedes vía `localhost`.

---

## Deploy en Cloud Run

### Requisitos

- [Google Cloud SDK (`gcloud`)](https://cloud.google.com/sdk/docs/install) instalado y autenticado
- Proyecto GCP con facturación activada (free tier aplica para tráfico bajo)

### Deploy desde código (recomendado)

Desde `cloud_run_rewrite/`, **en una sola línea** (PowerShell):

```powershell
gcloud run deploy fde-pnl-api --source=. --region=europe-west1 --allow-unauthenticated --port=8080
```

La primera vez pedirá habilitar Cloud Build y crear un repositorio en Artifact Registry — responder `Y`.

Si falla con `could not find source`, usar ruta absoluta:

```powershell
gcloud run deploy fde-pnl-api --source="RUTA_COMPLETA\cloud_run_rewrite" --region=europe-west1 --allow-unauthenticated --port=8080
```

Al terminar, `gcloud` imprime la **Service URL** pública (`https://....run.app`).

---

## Arquitectura

### Visión general del sistema

```
┌─────────────────────────────────────────────────────────────────┐
│  CAPA AGENTE (local)                                            │
│                                                                 │
│   Usuario escribe pregunta en español                           │
│         │                                                       │
│         ▼                                                       │
│   pnl_agent.py ──── tool_registry.py (TOOL_SCHEMAS)            │
│         │                  │                                    │
│         │           "menú" de tools disponibles                 │
│         ▼                                                       │
│   Gemini API ◄──── VIAJE 1: pregunta + schemas                 │
│         │                                                       │
│         │  Gemini devuelve: function_call{name, args}           │
│         ▼                                                       │
│   run_tool(name, args)                                          │
│         │                                                       │
└─────────┼───────────────────────────────────────────────────────┘
          │
          ▼
┌─────────────────────────────────────────────────────────────────┐
│  CAPA TOOLS (local)                                             │
│                                                                 │
│   pnl_tool.py · 6 tools                                         │
│   consultar_tienda / consultar_opinc / consultar_comuna /       │
│   comparar_tiendas / resumen_portfolio / analizar_tienda        │
│         │              httpx GET ───►  Cloud Run API              │
│                                                                 │
│   ◄── JSON TiendaPL ──────────────────────────────────────────  │
│   ◄── texto en prosa (formatear_tienda / formatear_comuna)      │
│                                                                 │
└─────────┬───────────────────────────────────────────────────────┘
          │ resultado (texto)
          ▼
┌─────────────────────────────────────────────────────────────────┐
│  CAPA AGENTE (vuelta)                                           │
│                                                                 │
│   Gemini API ◄──── VIAJE 2: resultado de la tool               │
│         │                                                       │
│         │  Gemini genera respuesta en prosa con datos reales    │
│         ▼                                                       │
│   Usuario recibe: "La tienda 45 en La Granja tuvo OPINC..."    │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Flujo de tool calling — los 2 viajes explicados

El LLM **no ejecuta código**. Solo puede pedirte que lo ejecutes tú.

```
                    VIAJE 1 — "¿Qué necesitas?"
 ┌──────────┐  pregunta + schemas   ┌─────────┐
 │ pnl_agent│ ─────────────────────►│  Gemini │
 └──────────┘                       └────┬────┘
                                         │ function_call:
                                         │ {name: "consultar_tienda",
                                         │  args: {tienda_id: 45}}
                                         ▼
                              [Gemini NO ejecuta — solo pide]

                    VIAJE 2 — "Aquí está el resultado"
 ┌──────────┐  run_tool() → API     ┌─────────┐
 │ pnl_agent│ ──────────────────────►│  API    │
 │          │ ◄── "La tienda 45..." │  Cloud  │
 │          │                       │  Run    │
 │          │  candidates[0].content + resultado (thought_signature)
 │          │ ─────────────────────►┌─────────┐
 │          │ ◄── respuesta en prosa│  Gemini │
 └──────────┘                       └─────────┘
      │
      ▼
 "La tienda 45 en La Granja registró ventas de $18,569..."
```

### Cómo Gemini elige la tool correcta

El usuario **no necesita mencionar la tool**. Gemini infiere la intención leyendo la `description` de cada schema:

```
Usuario escribe                          Tool elegida por Gemini
──────────────────────────────────────   ──────────────────────
"¿Cómo le fue a la tienda 45?"        → consultar_tienda(45)
"¿Cuánto OPINC tiene la 45?"          → consultar_opinc(45)
"¿Qué tiendas hay en La Granja?"      → consultar_comuna("La Granja")
"¿Cuál rinde mejor en La Granja?"     → comparar_tiendas("La Granja")
"Resumen del portfolio"               → resumen_portfolio()
"¿La 45 está sobre el promedio?"      → analizar_tienda(45)
```

### API + capa de datos

```
                    ┌── scripts/pnl_tool.py  ← CLIENTE (local)
                    │      httpx GET → JSON → texto humano
                    │
Cliente ────────────┼── navegador / tests
(navegador,         │
 tool, tests)       ▼
              Cloud Run / uvicorn  ← SERVIDOR (GCP)
                    │
                    ▼
               main.py            ← rutas HTTP
                    │
                    ▼
               PNLService
                 ├─ async: get_tienda_por_id_async → bq_cliente (GET /pnl/{id})
                 ├─ sync:  _database (= bq.mock_database) → list/comuna/opinc
                 └─ analizar_tienda() → GET /pnl/{id}/analisis
                    │
                    ▼
               TiendaPL          ← schema Pydantic (contrato único)
```

- **Servidor** (`src/main.py` + `pnl_services.py`): expone JSON vía REST. Redeploy a Cloud Run si cambias `src/`.
- **Cliente tool** (`scripts/pnl_tool.py`): corre en tu PC; consume la API sin deploy.
- **Simulador BQ** (`bq_cliente.py`): capa async para consulta por tienda; envelope `{status, data}` traducido a HTTP 404 en `main.py`.
- **Agente** (`pnl_agent.py`): orquesta Gemini + tools; corre local, conecta con la API en prod. Modelo actual: `gemini-3.1-flash-lite`.
- **MCP server** (`mcp_server.py`): expone las mismas tools vía protocolo MCP. Cursor lo lanza automáticamente con `.cursor/mcp.json`. No usa Gemini — el LLM es el de Cursor.
- **Config** (`config/settings.py`): `API_BASE_URL` y `GEMINI_API_KEY` vía `.env` / pydantic-settings.

Principio aplicado: **un solo dispatcher `run_tool()`** sirve a dos LLMs distintos (Gemini vía `pnl_agent.py` y el LLM de Cursor vía MCP) sin duplicar lógica. El contrato único `TiendaPL` + seed 42 se mantiene en todas las capas.

### Comparativa: Agente Gemini vs MCP Cursor

| | `pnl_agent.py` | `mcp_server.py` |
|---|---|---|
| **LLM** | Gemini (tu API key) | LLM de Cursor |
| **Interfaz** | Terminal REPL | Chat de Cursor |
| **Protocolo** | Custom SDK google-genai | MCP estándar (stdio) |
| **Lanzamiento** | Manual: `python scripts/pnl_agent.py` | Automático: Cursor lee `.cursor/mcp.json` |
| **Tools** | `run_tool()` | `run_tool()` (mismo dispatcher) |
| **Cloud Run** | ✅ misma API | ✅ misma API |

### Configuración Gemini

| Variable | Dónde | Uso |
|---|---|---|
| `GEMINI_API_KEY` | `.env` (local, gitignored) | Autenticación SDK `google-genai` |
| `API_BASE_URL` | `.env` o `$env:` | Base URL de la API P&L |

**Trampas frecuentes:**

| Síntoma | Causa | Fix |
|---|---|---|
| `limit: 0` / 429 | Modelo sin cuota en tu tier | AI Studio → Límites por modelo; usar solo RPD > 0 |
| Error `thought_signature` | Viaje 2 reconstruye el `function_call` | Pasar `response.candidates[0].content` completo |
| `ModuleNotFoundError: config` | Script sin `sys.path` | Bloque `_ROOT` al inicio de scripts en `scripts/` |
| Agente sin paquetes | venv no activado | `.\.venv\Scripts\Activate.ps1` desde raíz del repo |
| pytest sin API key | Import de pnl_agent | OK: `get_client()` lazy; tests usan mock |

### Evals del agente

| Recurso | Uso |
|---|---|
| `test/fixtures/agent_eval_cases.json` | 10 casos: input → tool esperada |
| `test/test_agent_eval.py` | Routing mock (CI, sin Gemini) |
| `scripts/run_agent_evals.py` | Eval live manual (requiere API key + red) |

---

## Roadmap

- [x] Schema Pydantic + datos sintéticos reproducibles
- [x] Endpoints P&L + health check
- [x] Integration tests con pytest
- [x] Dockerfile + deploy en Cloud Run
- [x] `config/settings.py` con variables de entorno
- [x] Script tool `pnl_tool.py` (HTTP → texto humano)
- [x] Segunda tool: filtro por comuna (`--comuna`)
- [x] Unit tests `test_pnl_tool.py` (mock httpx)
- [x] Simulador `bq_cliente.py` async (`TiendaPL`, seed 42)
- [x] Unit tests `test_bq_client.py` (pytest-asyncio)
- [x] Integrar `bq_cliente.py` en `GET /api/v1/pnl/{tienda_id}` (async) + redeploy Cloud Run
- [x] Agente conversacional `pnl_agent.py` con Gemini tool calling (REPL) — **verificado Jul 2026**
- [x] MCP server `mcp_server.py` con FastMCP — **verificado Jul 2026**
- [x] **Capa agente ampliada (Jul 2026):** 6 tools · `/analisis` · system prompt · multi-turn · evals · **40 tests**
- [ ] Redeploy Cloud Run (`/analisis` en prod)
- [ ] **Próximo:** Narrativa GitHub/LinkedIn + demo del portfolio
- [ ] `docker-compose.yml` — portabilidad sin Cloud Run (opcional)
- [ ] Migrar endpoints list/comuna/opinc a async (opcional)

---

## Licencia

Uso educativo / sandbox. Sin licencia explícita por ahora.
