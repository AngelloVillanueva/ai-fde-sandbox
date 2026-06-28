# ai-fde-sandbox

Sandbox de práctica para construir una **API de análisis financiero P&L** orientada a tiendas retail. Expone datos sintéticos vía HTTP para consumo desde un dashboard, pruebas automatizadas y, en fases posteriores, un agente con tool calling.

El caso de uso simula consultas del tipo: *¿Cómo le fue a la tienda 45?* o *¿Qué tiendas hay en Providencia?*

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
| Tests | [pytest](https://docs.pytest.org/) + `TestClient` |
| Contenedor | Docker |
| Despliegue | [Google Cloud Run](https://cloud.google.com/run) |

---

## Estructura del repositorio

```
ai-fde-sandbox/
├── .gitignore
├── README.md
└── cloud_run_rewrite/
    ├── .dockerignore
    ├── config/
    │   └── settings.py          # Configuración por entorno (WIP)
    ├── src/
    │   ├── main.py              # FastAPI app y endpoints
    │   ├── models.py            # Schema TiendaPL
    │   └── services/
    │       ├── pnl_services.py  # Fuente única de datos sintéticos
    │       └── bq_cliente.py    # Simulador BigQuery async (WIP, no conectado)
    ├── test/
    │   └── test_main.py         # Integration tests
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
pytest -v
```

Cobertura actual:

- Health check (`200`)
- Happy path tienda 45 (contrato completo `TiendaPL`)
- Tienda inexistente (`404`)
- Filtro por comuna (`?comuna=La+Granja`)

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

```
Cliente (navegador / agente / tests)
        │
        ▼
   Cloud Run / uvicorn
        │
        ▼
   main.py          ← rutas HTTP, validación de params
        │
        ▼
   PNLService       ← lógica de negocio + datos sintéticos
        │
        ▼
   TiendaPL         ← schema Pydantic (contrato de respuesta)
```

Principio aplicado: **una sola fuente de verdad** (`pnl_services.py`). El módulo `bq_cliente.py` es un ejercicio aparte para simular consultas async a BigQuery y aún no está integrado a la API.

---

## Roadmap

- [x] Schema Pydantic + datos sintéticos reproducibles
- [x] Endpoints P&L + health check
- [x] Integration tests con pytest
- [x] Dockerfile + deploy en Cloud Run
- [ ] `config/settings.py` con variables de entorno
- [ ] Integrar `bq_cliente.py` como capa de datos async
- [ ] Capa de agente (tool calling / MCP) sobre la API

---

## Licencia

Uso educativo / sandbox. Sin licencia explícita por ahora.
