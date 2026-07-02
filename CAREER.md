# CAREER — Angello: AI Forward Deployed Engineer

> Referencia rápida para sesiones AI y autoevaluación de progreso.
> Plan completo: `plan-maestro-carrera-genai_DEFINITIVO.md` + `plan-ejecutable-FDE.md`

---

## North Star

**Rol:** Senior AI Forward Deployed Engineer  
**Targets:** Palantir (aspiracional/cúspide) · Google Cloud · Microsoft · OpenAI · Startups AI Series B-D  
**Salario:** $150K–220K USD remoto desde Chile  
**Timeline:** 18 meses (Jun 2026 – Dic 2027)  
**Primer salto realista:** $80–120K en consultora GCP o startup AI (Mes 12–15) → Palantir/Google en Año 2–3

---

## Perfil actual (Jul 2026)

| Dimensión | Estado |
|---|---|
| Rol | AI FDE @ Walmart Chile desde 15 Jul 2026 |
| Anterior | Senior Data Analyst |
| Experiencia total | 7 años tech · 5 datos · 2 IA/ML |
| Python | Intermedio–avanzado (PySpark incluido) |
| APIs/Agentes | Comenzando — este sandbox es primer proyecto serio |
| Inglés | Lectura/escucha 95% · Habla 75% (pronunciación en desarrollo) |
| Contactos target | 2 mentores Microsoft MX (visita Chile pendiente) · 1 contacto Google |
| LinkedIn | Activo, optimizando |
| GitHub | Público, construyendo portafolio |

---

## Lo que hace un FDE (para que el agente lo sepa)

Un FDE no es developer ni consultor — es el puente entre el producto de IA y el cliente enterprise:
- **Deployer:** pone la herramienta a funcionar en el entorno real del cliente
- **Builder:** construye tools, agents, pipelines personalizados en días/semanas, no meses
- **Communicator:** explica ROI en $$$ a ejecutivos no-técnicos
- **Debugger en vivo:** diagnostica por qué el agente falla con datos reales del cliente

Palantir lo inventó. Google Cloud y Microsoft lo adoptaron. El mercado LATAM lo está descubriendo.

---

## Stack técnico que estoy construyendo (alineación mercado)

| Nivel | Tecnología | Estado | Para qué sirve en FDE |
|---|---|---|---|
| ✅ Base | FastAPI + Pydantic + pytest | Completado | APIs production-grade · contratos de datos |
| ✅ Deploy | Docker + Cloud Run | Completado | Deployar en infra cliente |
| ✅ Tools | httpx + tool calling pattern | Completado | Tools del agente que llaman APIs |
| ✅ Config | pydantic-settings + env vars | Completado | Multi-entorno dev/staging/prod |
| ✅ Testing | @patch + MagicMock | Completado | CI sin dependencias externas |
| ⏳ Datos | BigQuery async | Siguiente | Fuente de datos enterprise real |
| ❌ Agente | Google ADK + LangGraph | Fase 2 | Orquestación de agentes |
| ❌ Protocolo | MCP (Model Context Protocol) | Fase 2 | Standard de mercado 2026 |
| ❌ Producción | RAG + Evals + OpenTelemetry | Fase 3 | Sistemas enterprise robustos |

---

## Fases de construcción

```
FASE 1 (Meses 1–4): Python sólido — [EN CURSO]
  Build: Cloud Run app + tools + tests
  Cert: AI-620 Microsoft (voucher disponible, examen mes 4)
  Entregable: App en GitHub + AI-620 ✓

FASE 2 (Meses 4–8): Agentes full-code
  Build: Portfolio #1 — Financial Reconciliation Agent (ADK + BQ + MCP)
  Referencia: O'Reilly AI Agents book
  Entregable: Portfolio #1 en GitHub con narrativa $170K/año savings

FASE 3 (Meses 8–14): Producción
  Build: Portfolio #2 — Multi-Agent Operations Intelligence (LangGraph + RAG)
  Cert: PMLE + PCA Google
  Entregable: Portfolio #2 + certs + historias STAR en inglés

FASE 4 (Meses 14–18): Entrevistas
  Build: Portfolio #3 — Production AI Gateway
  Actividad: LeetCode medium + System Design mocks + behavioral EN
  Entregable: Oferta aceptada
```

---

## Acciones inmediatas de visibilidad (no-coding)

| Acción | Prioridad | Por qué |
|---|---|---|
| Actualizar LinkedIn headline a FDE | ESTA SEMANA | Es por qué tu compañero recibe mensajes y tú no |
| Activar contacto Google | MES 1 | Inteligencia de mercado, no pedir trabajo |
| 1 sesión Cambly/semana desde mes 1 | MES 1 | El inglés hablado es el riesgo #1 de entrevista |
| 2 posts LinkedIn/mes (1 técnico EN + 1 ES) | MENSUAL | Señal al mercado antes del mes 12 |
| Reunión con mentores Microsoft MX | Cuando vengan a Chile | Referral potencial + orientación de mercado |
| Contribuir a ADK/FastAPI open source | Mes 3+ | Visibilidad sin depender de ofertas |

**LinkedIn headline sugerido:**  
`AI Forward Deployed Engineer | Cloud Run · FastAPI · Agents | Building on Google Cloud`

---

## Checkpoints de mercado (no solo técnicos)

| Mes | Técnico | Mercado |
|---|---|---|
| 3 | FastAPI app en GitHub + tests | LinkedIn headline actualizado |
| 4 | Cloud Run app + AI-620 | 1+ recruiter contactado (orgánico) |
| 6 | Portfolio #1 en construcción | 1 conversación informal con empresa target |
| 9 | Portfolio #1 completo | Articular impacto en $$$ en entrevista informal |
| 12 | Portfolio #2 + PMLE | Referral en al menos 1 empresa target |
| 14 | En entrevistas activas | Mock behavioral passing en inglés |
| 18 | Portfolio #3 | **Oferta aceptada** |

---

## Por qué Walmart FDE ES parte del portfolio

Tu nuevo rol en Walmart desde julio 15 no es solo "lab de práctica" — es tu **case study #1 con impacto real**:
- Agentes con Copilot Studio/Gemini para Legal, Operaciones, People, Finance
- Automatizaciones Power Automate en producción para todas las gerencias
- **Cualquier resultado medible** (tiempo ahorrado, procesos automatizados, $$$ de impacto) es narrativa de portfolio directa

Documenta TODO. Aunque no puedas mostrar código por NDA, puedes mostrar la arquitectura y el impacto.

---

## Recursos para cada conversación

**Si un reclutador pregunta qué sabes hacer:**  
*"Construyo APIs production-grade con FastAPI, las despliego en Cloud Run, y las conecto como tools de agentes. Manejo testing con mocks para que el CI no dependa de servicios externos."*

**Si un FDE senior te pregunta sobre arquitectura:**  
*"Separo servidor (API) de cliente (tool) desde el diseño. El agente solo orquesta — las tools son determinísticas. La config va en env vars, no en código."*

**Si preguntan sobre tu stack target:**  
*"Google ADK + LangGraph para agentes full-code. MCP para interoperabilidad. BigQuery como capa de datos. Vertex AI para producción."*

---

## No hacer (anti-lista)

- CrewAI / AutoGen / Semantic Kernel profundo
- Fine-tuning de modelos
- Rust, Go, Java, Kubernetes profundo
- AWS certs / Azure AI-102 / Databricks certs
- Configurar entorno por 3 horas en vez de codear
- LinkedIn > Coding en horas de estudio
- Máster ahora (revisitar después de primer rol internacional si hay financiamiento)

---

## Regla única de estudio

```
1. Abrir proyecto
2. Codear
3. Commitear
4. Cerrar

Lo demás son hábitos de 15-20 min que se hacen solos.
```

---

*Creado: Jul 2026 · Basado en plan-maestro-carrera-genai_DEFINITIVO.md + plan-ejecutable-FDE.md*  
*Actualizar al cierre de cada fase o cambio relevante de contexto.*
