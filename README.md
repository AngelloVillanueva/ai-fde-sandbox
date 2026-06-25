# ai-fde-sandbox

Sandbox de práctica para construir una **API de análisis financiero P&L** orientada a tiendas retail. Expone datos sintéticos vía HTTP para consumo desde un dashboard, pruebas automatizadas y, en fases posteriores, un agente con tool calling.

El caso de uso simula consultas del tipo: *¿Cómo le fue a la tienda 45?* o *¿Qué tiendas hay en Providencia?*

---

## Stack

| Capa | Tecnología |
|---|---|
| API | [FastAPI](https://fastapi.tiangolo.com/) |
| Validación / schema | [Pydantic](https://docs.pydantic.dev/) |
| Servidor local | [Uvicorn](https://www.uvicorn.org/) |
| Tests | [pytest](https://docs.pytest.org/) + `TestClient` |
| Despliegue (planificado) | Docker + Google Cloud Run |

---

## Estructura del repositorio

```
ai-fde-sandbox/
├── .gitignore
├── README.md
└── cloud_run_rewrite/
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
    ├── Dockerfile               # WIP
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

### Ejemplos

```http
GET /health
GET /api/v1/pnl/45
GET /api/v1/pnl?comuna=La%20Granja
GET /api/v1/pnl/45/opinc
```

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

---

## Arquitectura

```
Cliente (navegador / agente / tests)
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
- [ ] Dockerfile funcional + deploy en Cloud Run
- [ ] `config/settings.py` con variables de entorno
- [ ] Integrar `bq_cliente.py` como capa de datos async
- [ ] Capa de agente (tool calling / MCP) sobre la API

---

## Licencia

Uso educativo / sandbox. Sin licencia explícita por ahora.
