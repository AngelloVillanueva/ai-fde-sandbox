# PROGRESS — Estado del plan FDE

> Snapshot actualizado: **Jul 2026 (Mes ~1.5 de 18)**  
> Complementa `CONTEXT.md` (proyecto) y `CAREER.md` (carrera). Actualizar al cierre de cada fase o sesión relevante.

---

## Resumen ejecutivo

| Dimensión | Estado | Nota |
|---|---|---|
| **Técnico (sandbox)** | ✅ Adelantado | 8/8 hitos build completados · MCP ~3 meses antes de lo planeado |
| **Visibilidad / mercado** | ⚠️ Atrás | Headline ✅ · 0 posts técnicos · sin inbound recruiter aún |
| **Inglés hablado** | ⚠️ Riesgo #1 | Lectura 95% · Habla 75% · retomar práctica conversacional |
| **Formación Microsoft** | 🟢 En curso | Jul 2026 – Feb 2027 · 266.5h · incluye AB-620 |
| **Plan 18 meses** | 🟢 Viable (Escenario B) | Primer rol internacional mes 12–15 · $150K+ Palantir/Google más realista mes 24–30 |

**Diagnóstico central:** vas adelantado construyendo, atrás emitiendo señal al mercado. No es falta de capacidad — es priorización pendiente en visibilidad e inglés hablado.

---

## Posición en el timeline (18 meses)

**Inicio:** Jun 2026 · **Hoy:** ~Mes 1.5 · **Meta:** Dic 2027 · **Quedan:** ~16.5 meses

### Fases de carrera

```
FASE 1 (Meses 1–4)  Python sólido          ████████░░  ~75%  [EN CURSO · build adelantado]
FASE 2 (Meses 4–8)  Agentes full-code      ██░░░░░░░░  ~15%  [base lista · falta RAG/ADK/narrativa]
FASE 3 (Meses 8–14) Producción             ░░░░░░░░░░   0%   [LangGraph · Evals · PMLE/PCA Google]
FASE 4 (Meses 14–18) Entrevistas           ░░░░░░░░░░   0%   [Portfolio #3 · mocks · behavioral EN]
```

### Sesiones sandbox

| Sesión | Hito | Estado |
|--------|------|--------|
| 1–4 | settings · pnl_tool · comuna · tests mock | ✅ |
| 5–6 | bq_cliente async · integración API + redeploy | ✅ |
| 7 | Agente Gemini tool calling | ✅ |
| 8 | MCP server FastMCP | ✅ |
| **9** | Narrativa GitHub/LinkedIn + demo portfolio | ⏳ pendiente |
| 10–11 | docker-compose · async endpoints | opcional |

**Proyecto:** 8/8 hits técnicos ✅ · 1 hito visibilidad pendiente · **commits cerrados Jul 2026**

---

## Scorecard por pilar

```
PROYECTO SANDBOX     ████████████████████  95%  (falta narrativa pública)
FASE 1 CARRERA       ███████████████░░░░░  75%  (build ✅ · mercado ⚠️)
FASE 2 CARRERA       ███░░░░░░░░░░░░░░░░░  15%
VISIBILIDAD          ████░░░░░░░░░░░░░░░░  20%  (headline ✅ · posts técnicos ❌)
INGLÉS HABLADO       ███████████████░░░░░  75%  (filtro duro entrevistas)
FORMACIÓN MICROSOFT  ██░░░░░░░░░░░░░░░░░░  10%  (empieza Jul 2026)
LECTURAS (O'Reilly)  ░░░░░░░░░░░░░░░░░░░░   0%  (pausado — retomar 30–45 min/sem)
```

---

## Debilidades identificadas (camino FDE)

Priorizadas por impacto en el north star:

| # | Debilidad | Impacto | Acción |
|---|-----------|---------|--------|
| 1 | **Visibilidad de negocio** — impacto medible no conectado públicamente con arquitectura | Alto · bloquea inbound recruiter | 1 post/semana (1 EN técnico + 1 ES negocio/mes) · Sesión 9 |
| 2 | **Inglés hablado** — 75% vs filtro duro mes 14 | Alto · bloquea entrevistas $150K+ | 1 sesión conversacional/semana (Cambly, iTalki, mock, o peer) |
| 3 | **Señal algorítmica LinkedIn** — post reconocimiento sin keywords técnicas | Medio | Posts con stack: FastAPI · Cloud Run · MCP · agents |
| 4 | **Referrals / red target** — 402 conexiones, sin contacto Google activado | Medio | Activar contacto Google mes 1 · mentores Microsoft MX |
| 5 | **Lecturas pausadas** — O'Reilly + empresariales | Bajo–medio (largo plazo) | 30–45 min/semana al retomar, no recuperar de golpe |
| 6 | **Certs Google** — PMLE/PCA aún no iniciadas | Medio (mes 8+) | Paralelo a Microsoft; no compiten en corto plazo |

**Fortalezas que compensan:**
- Rol FDE real @ Walmart con números ($1M+ OPINC, 472–730 hrs/mes)
- Stack híbrido: full-code (FastAPI, MCP) + low-code (Copilot Studio, Power Automate) — diferenciador vs DS que solo codea
- Sandbox end-to-end verificado antes del módulo MCP de Microsoft (Sep 2026)
- Agent Control Tower — governance enterprise poco común en perfiles junior FDE

---

## Stack técnico — estado real (Jul 2026)

| Tecnología | Estado | Notas |
|---|---|---|
| FastAPI + Pydantic + pytest | ✅ | Sandbox + Walmart |
| Docker + Cloud Run | ✅ | URL pública live |
| httpx + tool calling | ✅ | `tool_registry.py` dispatcher único |
| pydantic-settings | ✅ | Multi-entorno |
| MCP (FastMCP) | ✅ | Adelantado ~3 meses vs plan original |
| Gemini tool calling | ✅ | `pnl_agent.py` verificado |
| BigQuery async | 🟡 | Simulado sandbox · real en Walmart (no replicar) |
| Google ADK + LangGraph | 🟡 | ADK en Walmart · sandbox pendiente |
| RAG + Evals + OpenTelemetry | ❌ | Microsoft RAG Jul 2026 · sandbox post-Sesión 9 |
| Copilot Studio + Power Automate | ✅ | Producción Walmart |

---

## Formación Microsoft (Walmart) — cronograma completo

**Total:** ~266.5 horas · Jul 2026 – Feb 2027  
**Nota:** Complementa el north star, no lo reemplaza. Microsoft es target explícito en `CAREER.md`. El stack híbrido (full-code + low-code según problema) es diferenciador FDE.

### Fase 1 — Fundamentos (Jul–Ago 2026)

| Item | Contenido | Horas | Fechas |
|------|-----------|-------|--------|
| Módulo 3 | Fundamentos de LLMs y Patrones RAG | 12 | Jul 9–16, 2026 |
| Challenge 1 | Sistema de Conocimiento Inteligente | 9 | Jul 23–30, 2026 |
| **Cert 1** | **PL-400** — Power Platform Developer Associate | 22 | Ago 3–6, 2026 |

### Fase 2 — Desarrollo Low-Code (Ago–Sep 2026)

| Item | Contenido | Horas | Fechas |
|------|-----------|-------|--------|
| Módulo 6 | Prácticas de ALM en Power Platform | 9 | Ago 13–20, 2026 |
| Challenge 2 | Agente conversacional para procedimientos bajo demanda | 9 | Ago 27 – Sep 3, 2026 |
| **Cert 2** | **AB-410** — Intelligent Applications Builder Associate | 22 | Sep 7–10, 2026 |

### Fase 3 — Arquitecturas Avanzadas (Sep–Dic 2026)

| Item | Contenido | Horas | Fechas | Alineación sandbox |
|------|-----------|-------|--------|---------------------|
| Módulo 7 | Desarrollo de MCP Servers | 24 | Sep 17 – Oct 8, 2026 | 🟢 Ya dominado — ventaja en cohorte |
| Módulo 8 | Orquestación Multiagéntica | 18 | Oct 15–29, 2026 | 🟢 Alinea LangGraph/ADK |
| Módulo 9 | Agentes Autónomos y Event-Driven | 12 | Nov 5–12, 2026 | 🟢 Fase 2–3 carrera |
| Challenge 3 | Ecosistema Multiagente Empresarial | 12.5 | Nov 19 – Dic 3, 2026 | 🟢 Case study Walmart |
| **Cert 3** | **AB-620** — AI Agent Builder Associate | 30 | Dic 7–10, 2026 | 🟢 Cert agentes Microsoft |

### Fase 4 — Arquitectura Empresarial (Dic 2026 – Feb 2027)

| Item | Contenido | Horas | Fechas |
|------|-----------|-------|--------|
| Módulo 10 | Seguridad, Gobernanza y Responsible AI | 12 | Dic 17–24, 2026 |
| Módulo 11 | Arquitectura de Soluciones Empresariales | 18 | Dic 31, 2026 – Feb 4, 2027 |
| Challenge 4 | Diseño Arquitectónico End-to-End | 9 | Feb 11–18, 2027 |

### Certificaciones Microsoft del programa

| Cert | Cuándo | Relevancia FDE |
|------|--------|----------------|
| PL-400 | Ago 2026 | Power Platform · Copilot Studio · Walmart |
| AB-410 | Sep 2026 | Intelligent apps · agentes low-code |
| **AB-620** | Dic 2026 | **AI Agent Builder** — alineada con rol FDE agentes |

> **Corrección vs plan original:** el manifiesto referenciaba AI-620; la cert del programa es **AB-620** (AI Agent Builder Associate). PMLE + PCA Google siguen en Fase 3 carrera (mes 8–14), independientes del programa Microsoft.

---

## Balance de tiempo semanal (11h)

```
Microsoft sesiones + homework:  ~5–6h  (obligatorio — trabajo)
Sandbox / coding north star:     ~3–4h  (mantener — no abandonar)
Inglés conversacional:           ~1h  (riesgo #1 entrevista)
LinkedIn (1 post/semana):       ~30min
Lecturas (O'Reilly + negocio):  ~30–45min cuando retomes
Italiano:                       meta personal — no compite con north star
```

**Principio FDE:** la herramienta depende del problema. Power Automate cuando basta · FastAPI + MCP cuando hace falta. No es desviación — es el perfil que contratan en enterprise.

---

## Checkpoints de mercado — estado vs plan

| Mes | Técnico (plan) | Mercado (plan) | Estado Jul 2026 |
|-----|----------------|----------------|-----------------|
| 1.5 | Cloud Run + tools | Headline FDE | ✅ build completo · ✅ headline · ⚠️ posts |
| 3 | GitHub + tests | Headline | ✅ commits · ⏳ narrativa pública |
| 4 | Cloud Run + **AB-620**/certs | 1 recruiter orgánico | ⏳ PL-400 Ago · AB-620 Dic |
| 6 | Portfolio #1 en construcción | Conversación informal target | 🟡 técnico listo · narrativa falta |
| 9 | Portfolio #1 completo | Articular $$$ en entrevista | ⏳ |
| 12 | Portfolio #2 + PMLE | Referral empresa target | ⏳ |
| 14 | Entrevistas activas | Mock behavioral EN | ⏳ |
| 18 | Portfolio #3 | **Oferta aceptada** | ⏳ |

---

## ¿18 meses es viable?

### Escenario A — North star aspiracional ($150K–220K · Palantir/Google directo)
**Probabilidad mes 18:** ~25–35%  
Pool pequeño · inglés hablado · pocos años en rol FDE internacional · referrals escasos.

### Escenario B — Plan ejecutable (primer rol internacional $80–120K)
**Probabilidad mes 18:** ~70–80% si cierras gaps visibilidad + inglés

| Meta | ¿Alcanzable? | Condición |
|------|--------------|-----------|
| Fase 1 completa (Mes 4) | ✅ Sí | Sesión 9 + 1 post/sem + speaking |
| Portfolio #1 visible (Mes 9) | ✅ Sí | Sandbox + narrativa + RAG del programa |
| PL-400 + AB-410 + AB-620 | ✅ Sí | Programa Microsoft Jul 2026 – Dic 2026 |
| Primer contacto recruiter (Mes 4) | 🟡 Posible | Post técnico EN con keywords |
| Rol $80–120K remoto (Mes 12–15) | 🟡 Posible | Inglés + referrals + certs |
| Oferta $150K+ Palantir/Google (Mes 18) | 🔴 Optimista | Más realista mes 24–30 (Año 2–3 del plan) |

---

## Acciones inmediatas — visibilidad (prioridad ahora)

| Acción | Estado | Prioridad |
|--------|--------|-----------|
| LinkedIn headline FDE | ✅ Hecho | — |
| Commits agente + MCP | ✅ Hecho Jul 2026 | — |
| **Sesión 9:** post LinkedIn + GitHub Featured | ⏳ próxima sesión | 🔴 Alta |
| 1 post/semana LinkedIn | ⏳ iniciar | 🔴 Alta |
| Inglés conversacional 1x/semana | ⏳ retomar | 🔴 Alta |
| Activar contacto Google | ❌ pendiente | 🟡 Media |
| Sync CV_EN.md (GitHub real, MCP ✅) | ⏳ con Sesión 9 | 🟡 Media |
| O'Reilly AI Agents | ⏳ pausado | 🟢 Baja (retomar gradual) |

---

## Lo que queda por delante (quantificado)

### Corto plazo (Mes 2–4)
- Sesión 9: narrativa portfolio
- 6–8 posts LinkedIn
- Speaking 1x/semana
- PL-400 (Ago) · AB-410 (Sep)
- Contacto Google

### Medio plazo (Mes 4–8)
- Portfolio #1 narrativa $$$ completa
- RAG en sandbox (post Microsoft Módulo 3)
- AB-620 (Dic 2026)
- O'Reilly retomado
- ADK en sandbox (opcional)

### Largo plazo (Mes 8–18)
- Portfolio #2 (LangGraph + RAG profundo)
- PMLE + PCA Google
- Portfolio #3 + entrevistas + mocks EN
- Historias STAR documentadas

---

## Historial de actualizaciones

| Fecha | Cambio |
|-------|--------|
| Jul 2026 | Creación documento · corrección AI-620 → AB-620 · cronograma Microsoft completo Fases 1–4 · commits cerrados · diagnóstico visibilidad/inglés |

---

*Ver también: `CONTEXT.md` (handoff técnico) · `CAREER.md` (north star y frases entrevista)*
