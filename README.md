# ai-fde-sandbox

Sandbox de práctica para construir una **API de análisis financiero P&L** orientada a tiendas retail. Expone datos sintéticos vía HTTP, un agente conversacional con Gemini tool calling, y (próximo paso) un servidor MCP para portfolio FDE.

El caso de uso simula consultas del tipo: *¿Cómo le fue a la tienda 45?* o *¿Qué tiendas hay en Providencia?*

**North star del proyecto:** API P&L → URL pública → agente con tool calling — **completado**. Siguiente: MCP server + narrativa portfolio.

> **Handoff para sesiones AI:** ver [`CONTEXT.md`](CONTEXT.md) (estado del proyecto, north star, trampas conocidas).

---

## Demo en producción (Cloud Run)

**Base URL:** https://fde-pnl-api-198971893116.europe-west1.run.app

| Recurso | URL |
|---|---|
| Health check | https://fde-pnl-api-198971893116.europe-west1.run.app/health |
| Swagger UI | https://fde-pnl-api-198971893116.europe-west1.run.app/docs |
| P&L tienda 45 | https://fde-pnl-api-198971893116.europe-west1.run.app/api/v1/pnl/45 |
| Filtro por comuna | https://fde-pnl-api-198971893116.europe-west1.run.app/api/v1/pnl?comuna=La%20Granja |

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
    │   ├── pnl_tool.py          # Tools: HTTP → texto humano
    │   ├── tool_registry.py     # Schemas de tools + dispatcher run_tool()
    │   └── pnl_agent.py         # Agente REPL con Gemini tool calling
    ├── src/
    │   ├── main.py              # FastAPI app y endpoints
    │   ├── models.py            # Schema TiendaPL
    │   └── services/
    │       ├── pnl_services.py  # Fuente única de datos sintéticos (API)
    │       └── bq_cliente.py    # Simulador BigQuery async (TiendaPL, conectado a GET /pnl/{id})
    ├── test/
    │   ├── test_main.py         # Integration tests API
    │   ├── test_pnl_tool.py     # Unit tests tools (mock httpx)
    │   └── test_bq_client.py    # Unit tests BQ simulado (pytest-asyncio)
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
cd cloud_run_rewrite
pytest -v                         # todos (12 tests)
pytest test/test_main.py -v       # API integration (4)
pytest test/test_pnl_tool.py -v   # tools unitarios (5)
pytest test/test_bq_client.py -v  # BQ simulado async (3)
```

| Archivo | Tipo | Qué prueba |
|---|---|---|
| `test/test_main.py` | Integration | API vía `TestClient` (sin red externa) |
| `test/test_pnl_tool.py` | Unit | Tools con `@patch` + `MagicMock` (httpx fake) |
| `test/test_bq_client.py` | Unit async | `BigQuerySimulatedClient` con `@pytest.mark.asyncio` |

**Integration tests API** (`test_main.py`):

- Health check (`200`)
- Happy path tienda 45 (contrato completo `TiendaPL`)
- Tienda inexistente (`404`)
- Filtro por comuna (`?comuna=La+Granja`)

**Unit tests pnl_tool** (`test_pnl_tool.py`) — sin uvicorn ni Cloud Run:

- `formatear_tienda` / `formatear_comuna` (lista vacía)
- `consultar_tienda` 200 y 404
- `consultar_comuna` 200

Patrón: `@patch("scripts.pnl_tool.httpx.get")` intercepta la red; `MagicMock` simula `status_code` y `.json()`.

**Unit tests bq_cliente** (`test_bq_client.py`) — sin GCP ni uvicorn:

- `get_tienda_por_id` existente (tienda 45, seed 42)
- Tienda inexistente (`status: error`)
- Consistencia de datos con `PNLService` (mismo `opinc` / `comuna`)

Patrón: `@pytest.mark.asyncio` + `await client.get_tienda_por_id(...)`.

Verificación manual del simulador:

```powershell
cd cloud_run_rewrite
python -m src.services.bq_cliente
```

### Agente conversacional (`pnl_agent.py`) — verificado

Agente REPL con **Gemini tool calling** (modelo `gemini-3.1-flash-lite`). Acepta preguntas en lenguaje natural; Gemini elige la tool y el script ejecuta `run_tool()` contra la API en Cloud Run.

**Requisitos:** venv activo, `GEMINI_API_KEY` en `.env`, modelo con cuota > 0 en AI Studio.

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
Agente P&L · escribe 'salir' para terminar

Tú: ¿Cómo le fue a la tienda 45?
Agente: La tienda 45 ubicada en La Granja registró ventas de $18,569,
        costos de $7,918.98, OPEX de $4,522.51 y un ingreso operativo
        neto (OPINC) de $6,127.51.

Tú: ¿Qué tiendas hay en La Granja?
Agente: En La Granja se encuentran las tiendas 12, 45 y 78...

Tú: salir
Chao.
```

### Script tool (`pnl_tool.py`)

Cliente local con **2 tools** que llaman la API y devuelven texto legible:

| Tool | CLI | Endpoint API |
|---|---|---|
| Por tienda | `--tienda_id 45` | `GET /api/v1/pnl/{id}` |
| Por comuna | `--comuna "La Granja"` | `GET /api/v1/pnl?comuna=X` |

**Local** (requiere uvicorn corriendo en otra terminal):

```powershell
cd cloud_run_rewrite
$env:API_BASE_URL="http://127.0.0.1:8000"
python scripts/pnl_tool.py --tienda_id 45
python scripts/pnl_tool.py --comuna "La Granja"
```

**Producción** (Cloud Run — no requiere redeploy del script):

```powershell
$env:API_BASE_URL="https://fde-pnl-api-198971893116.europe-west1.run.app"
python scripts/pnl_tool.py --tienda_id 45
python scripts/pnl_tool.py --comuna "La Granja"
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
│   pnl_tool.py                                                   │
│   consultar_tienda(id) ──── httpx GET ───►  Cloud Run API      │
│   consultar_comuna(c)  ──── httpx GET ───►  Cloud Run API      │
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
"Dame el P&L de la 45"                → consultar_tienda(45)
"¿Qué tiendas hay en La Granja?"      → consultar_comuna("La Granja")
"Muéstrame la zona de Providencia"    → consultar_comuna("Providencia")
"¿Cuánto vendió la cuarenta y cinco?" → consultar_tienda(45)
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
                 └─ sync:  _database (= bq.mock_database) → list/comuna/opinc
                    │
                    ▼
               TiendaPL          ← schema Pydantic (contrato único)
```

- **Servidor** (`src/main.py` + `pnl_services.py`): expone JSON vía REST. Redeploy a Cloud Run si cambias `src/`.
- **Cliente tool** (`scripts/pnl_tool.py`): corre en tu PC; consume la API sin deploy.
- **Simulador BQ** (`bq_cliente.py`): capa async para consulta por tienda; envelope `{status, data}` traducido a HTTP 404 en `main.py`.
- **Agente** (`pnl_agent.py`): orquesta Gemini + tools; corre local, conecta con la API en prod. Modelo actual: `gemini-3.1-flash-lite`.
- **Config** (`config/settings.py`): `API_BASE_URL` y `GEMINI_API_KEY` vía `.env` / pydantic-settings.

Principio aplicado: **integración incremental** — contrato único `TiendaPL` + seed 42 en todas las capas. El agente no sabe cómo funciona la API; solo sabe que `consultar_tienda(id)` devuelve texto.

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
- [ ] **Próximo:** MCP server sobre las tools (portfolio FDE)
- [ ] Narrativa GitHub/LinkedIn + demo del portfolio
- [ ] Migrar endpoints list/comuna/opinc a async (opcional)

---

## Licencia

Uso educativo / sandbox. Sin licencia explícita por ahora.
