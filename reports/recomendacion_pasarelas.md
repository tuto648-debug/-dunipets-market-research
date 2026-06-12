# Recomendación de Pasarela de Pagos — DuniPets
**Fecha**: junio 2026 | **Estado legal**: Sin registrar (SAS en formación)

---

## Recomendación principal: ePayco

**Justificación:**

ePayco es la opción más completa para DuniPets en su etapa actual por una razón estructural: es la única pasarela colombiana que ofrece **split payment automático dentro de la misma transacción** sin requerir que los cuidadores abran cuentas en un servicio externo. Cuando un dueño de mascota paga $50,000 COP, ePayco puede distribuir automáticamente $40,000 al cuidador y $10,000 a DuniPets (o cualquier porcentaje configurado), en el mismo evento de pago.

Criterios cumplidos:

| Criterio | Estado |
|---|---|
| Persona natural sin Cámara de Comercio | ✅ |
| Link de pago sin desarrollo técnico | ✅ |
| Daviplata nativo (20M+ usuarios Colombia) | ✅ |
| Split automático para pagar cuidadores | ✅ Sin costo adicional |
| Comisión competitiva | ✅ 2.68–2.99% + $900 |
| Documentación técnica disponible | ✅ docs.epayco.com |
| Empresa 100% colombiana | ✅ Medellín |

**Limitación principal:** Nequi no es integración nativa directa (funciona via PSE). Para el perfil de usuario Bogotá-millennial que prefiere Nequi, esto puede generar fricción. La tarifa fija de $900 COP por tarjeta también es alta para tickets de $13,500 COP (representa ~6.7% adicional sobre el ticket mínimo).

---

## Recomendación alternativa / complementaria: Wompi

Wompi es la mejor opción si los fundadores de DuniPets tienen cuenta Bancolombia — condición que elimina el mayor obstáculo del servicio.

**Ventajas sobre ePayco:**
- Nequi nativo (Bancolombia es propietario de Nequi) — dispersión a Nequi en segundos
- Comisión PSE más baja del mercado (~1.49% + $1,200 vs $2,000 plano de ePayco)
- Wompi Payouts permite pagar a cualquier banco colombiano + Nequi en un solo batch
- Red de corresponsales más grande (17,600 puntos de pago en efectivo)
- Respaldo institucional del Grupo Bancolombia — menor riesgo de discontinuidad

**Desventaja crítica:** Para recibir desembolsos como comercio en el modelo Agregador, DuniPets **debe tener cuenta corriente o de ahorros Bancolombia**. Sin esta cuenta, el modelo Wompi no funciona. Además, los Payouts son un proceso separado del cobro (no es split automático en la transacción) con planes mensuales desde $210,000 COP o tarifa por pago de $1,849 + 0.4%.

**Uso complementario con ePayco:** Si ePayco es la pasarela principal de cobro, Wompi Payouts puede usarse exclusivamente para la dispersión a cuidadores con cuenta Nequi (sin necesitar la pasarela de cobro de Wompi).

---

## Stack sugerido por fase

### Fase 1 — Lanzamiento (semanas 1–12, sin desarrollo técnico)

**Objetivo**: Validar demanda, procesar primeros pagos, operar con cero código.

| Componente | Herramienta | Costo | Acción |
|---|---|---|---|
| Cobro a clientes | **ePayco links de pago** | 2.68–2.99% + $900 por txn | Crear link por servicio desde panel admin |
| Pago a cuidadores | **Manual** (transferencia bancaria o Nequi desde cuenta DuniPets) | $0 (costo operativo interno) | Pagar semanalmente a cada cuidador desde extracto |
| Registro clientes | Google Forms / WhatsApp Business | $0 | |
| Registro cuidadores | Google Forms | $0 | |
| Comisión DuniPets | **20% retenido manualmente** | — | DuniPets transfiere 80% al cuidador |

**Tiempo de activación**: 1–3 días hábiles desde registro en ePayco.

**Riesgo aceptable**: Con pocos cuidadores en Fase 1 (<20), los pagos manuales son manejables. No escala, pero valida el modelo.

---

### Fase 2 — Escala (mes 3+, con desarrollo técnico mínimo)

**Objetivo**: Automatizar cobro + split, integrar app/web, escalar a 50+ cuidadores.

| Componente | Herramienta | Costo | Detalle |
|---|---|---|---|
| Cobro a clientes | **ePayco API + Pagos Divididos** | 2.68–2.99% + $900 | Integración API; split automático por transacción |
| Pago a cuidadores | **ePayco Pagos Divididos** (mismo flujo) | Sin costo adicional | Cuidador recibe su % automáticamente en su cuenta bancaria o Daviplata |
| Nequi (cuidadores con Nequi) | **Wompi Payouts** (complementario) | $1,849 + 0.4% + IVA por dispersión | Batch semanal para cuidadores con Nequi |
| Facturación | DIAN (obligatorio al registrar SAS) | Variable | |
| Antifraude | ePayco nativo (incluido) | Incluido | |

**Trigger para activar Fase 2**: 30+ transacciones/mes o cuando el esfuerzo manual supere 5 horas/semana.

---

### Fase 3 — Expansión (año 2+, SAS registrada, >$100M COP/mes)

| Componente | Herramienta | Motivo |
|---|---|---|
| Pasarela principal | **Wompi Gateway** (plan negociado con Bancolombia) | Tarifas más bajas, respaldo institucional |
| Dispersión | **Wompi Payouts Premium** | Escala de volumen justifica plan mensual |
| Alternativa alta escala | **PlaceToPay / Evertec** o **Kushki** | Enterprise-grade, tarifas negociadas, SLA garantizado |
| Financiamiento compras | Cuotas sin interés (Wompi / ePayco) | Aumenta ticket promedio para servicios premium |

---

## Riesgos y limitaciones

### Riesgo 1 — ePayco: tarifa fija alta en tickets bajos
La tarifa fija de $900 COP representa el 6.7% de un ticket de $13,500 COP, haciendo que la comisión total llegue a ~10% en el peor caso (PSE + tarifa fija). **Mitigación**: Establecer ticket mínimo de $25,000 COP en la plataforma para servicios donde la tarifa fija sea <3.6% del ticket.

### Riesgo 2 — Wompi: dependencia de cuenta Bancolombia
Si los fundadores no tienen cuenta Bancolombia, Wompi queda bloqueada para recibir pagos como comercio. **Mitigación**: Abrir cuenta de ahorros Bancolombia antes de integrar Wompi, o usar ePayco que acepta cualquier banco.

### Riesgo 3 — PSE de ePayco en tickets <$60,000 COP
$2,000 COP plano es costoso para un servicio de $20,000 COP (10% solo de comisión PSE). **Mitigación**: Incentivar pago con tarjeta (menor comisión proporcional en tickets medios) o establecer cobro adicional al usuario para PSE.

### Riesgo 4 — Registro DIAN / facturación
Al superar ciertos umbrales de facturación, ePayco o cualquier pasarela puede requerir NIT activo. **Mitigación**: Registrar la SAS antes de superar $4,800 UVT anuales (~$228M COP en 2026) para evitar bloqueo de cuenta.

### Riesgo 5 — PayU / Rapyd transición
PayU fue adquirida por Rapyd. En Colombia la operación continúa pero la continuidad de contratos, soporte y tarifas no está garantizada a largo plazo. **Mitigación**: No integrar PayU como proveedor principal en 2026.

### Riesgo 6 — Adoptión de Nequi por cuidadores
Si los cuidadores prefieren recibir en Nequi y ePayco no tiene dispersión nativa a Nequi, se necesita un proceso manual o complementar con Wompi Payouts. **Mitigación aceptable en Fase 1**: Pagar manualmente desde Nequi personal DuniPets a cada cuidador. En Fase 2: incorporar Wompi Payouts como canal de dispersión a Nequi.

---

## Decisión rápida — árbol de decisión

```
¿Los fundadores tienen cuenta Bancolombia?
├── SÍ → Wompi como pasarela única (cobro + dispersión en un proveedor)
└── NO → ePayco como pasarela principal
         ├── Cuidadores cobran en banco o Daviplata → ePayco Pagos Divididos (Fase 2)
         └── Cuidadores prefieren Nequi → ePayco (cobro) + Wompi Payouts (dispersión Nequi)
```

---

*Ver `comparativa_pasarelas.md` para datos completos por gateway.*
*Ver `flujo_pagos_dunipets.md` para el diagrama de flujo financiero.*
*Ver `integracion_tecnica.md` para el plan de integración API.*
