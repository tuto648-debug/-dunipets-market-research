# Flujo de Pagos DuniPets — Diseño Financiero
**Fecha**: junio 2026

---

## Flujo completo (Fase 2 — ePayco Pagos Divididos)

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         FLUJO DE PAGO DUNIPETS                              │
│                    (ePayco Pagos Divididos — Fase 2)                        │
└─────────────────────────────────────────────────────────────────────────────┘

  DUEÑO DE MASCOTA                 DUNIPETS                    CUIDADOR (SITTER)
  (Cliente)                        (Marketplace)               (Proveedor)
       │                               │                              │
       │  1. Reserva servicio          │                              │
       │──────────────────────────────►│                              │
       │                               │                              │
       │  2. Recibe link de pago       │                              │
       │◄──────────────────────────────│                              │
       │   ($50,000 COP por ejemplo)   │                              │
       │                               │                              │
       │  3. Paga con tarjeta/         │                              │
       │     PSE/Daviplata             │                              │
       │──────────────────────────────►│                              │
       │                         [ePayco procesa]                     │
       │                               │                              │
       │  4. Confirmación de pago      │                              │
       │◄──────────────────────────────│                              │
       │                               │                              │
       │                         [ePayco deduce comisión propia]      │
       │                         ~$2,495 COP (2.68% + $900 + IVA)    │
       │                               │                              │
       │                         Neto disponible: ~$47,505           │
       │                               │                              │
       │                         [ePayco Pagos Divididos]             │
       │                         Split automático por porcentaje       │
       │                               │                              │
       │                         ┌─────┴─────┐                       │
       │                         │           │                        │
       │                    20% DuniPets  80% Sitter                  │
       │                    $9,501 COP    $38,004 COP──────────────► │
       │                         │                              Cuenta banco /
       │                         │                              Daviplata del cuidador
       │                    Cuenta DuniPets                           │
       │                    (ePayco panel)                            │
       │                         │                                    │
       │                    [1–3 días hábiles]                   [1–3 días hábiles]
       │                    DuniPets retira                      Sitter recibe
       │                    a su banco                           en su cuenta
```

---

## Flujo Fase 1 (manual, sin código)

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    FLUJO FASE 1 — OPERACIÓN MANUAL                          │
│                    (ePayco links de pago — sin desarrollo)                   │
└─────────────────────────────────────────────────────────────────────────────┘

  DUEÑO DE MASCOTA            DUNIPETS (operador)           CUIDADOR (SITTER)
       │                           │                              │
       │  1. Contacta por          │                              │
       │     WhatsApp/Instagram    │                              │
       │──────────────────────────►│                              │
       │                           │  2. Coordina con cuidador    │
       │                           │─────────────────────────────►│
       │                           │                              │
       │                           │  3. Genera link de pago ePayco│
       │                           │     ($50,000 COP)            │
       │                           │                              │
       │  4. Recibe link en WhatsApp│                             │
       │◄──────────────────────────│                              │
       │                           │                              │
       │  5. Paga con tarjeta/PSE/ │                              │
       │     Daviplata             │                              │
       │──────────────────────────►│                              │
       │                           │                              │
       │  6. ePayco notifica pago  │                              │
       │     confirmado (webhook   │                              │
       │     o email)              │                              │
       │                           │                              │
       │  7. Confirmación al       │                              │
       │     cliente               │                              │
       │◄──────────────────────────│                              │
       │                           │                              │
       │                      [1–3 días]                          │
       │                      ePayco acredita                     │
       │                      en cuenta DuniPets                  │
       │                           │                              │
       │                      [Pago manual semanal]               │
       │                      DuniPets transfiere 80%────────────►│
       │                      ($40,000 COP) por Nequi             │
       │                      o transferencia bancaria            │
       │                           │                              │
       │                      DuniPets retiene 20%                │
       │                      ($10,000 COP) como comisión         │
```

---

## Timing de flujos de dinero

### Escenario: servicio pagado el lunes a las 10 a.m.

| Evento | Día / Hora | Quién recibe |
|---|---|---|
| Cliente paga en ePayco | Lunes 10:00 a.m. | ePayco recibe |
| Confirmación a DuniPets (webhook) | Lunes 10:01 a.m. | DuniPets notificado |
| Dinero disponible en panel ePayco | Martes–Miércoles (1–3 días hábiles) | DuniPets |
| DuniPets retira a su banco | Miércoles (costo: $6,500 + IVA) | DuniPets en su banco |
| Cuidador recibe su parte (Fase 1 manual) | Viernes (pago semanal) | Sitter |
| Cuidador recibe su parte (Fase 2 split auto) | Martes–Miércoles (mismo ciclo) | Sitter directo |

**Nota:** En Fase 2 con ePayco Pagos Divididos, el split al cuidador es simultáneo al settlement de DuniPets. Ambos reciben en el mismo ciclo de 1–3 días.

---

## Modelo de comisiones DuniPets

### Estructura recomendada

| Componente | Porcentaje | Quién lo cobra |
|---|---|---|
| Tarifa pasarela (ePayco tarjeta) | ~2.68–2.99% + $900 | ePayco (se deduce antes del split) |
| Comisión DuniPets | **20%** del valor del servicio | DuniPets |
| Pago al cuidador | **80%** del valor del servicio | Cuidador |

### Ejemplos numéricos por ticket

| Precio del servicio | Comisión ePayco (aprox.) | Neto para split | DuniPets 20% | Cuidador 80% |
|---|---|---|---|---|
| $13,500 COP | ~$900 + $900 × 1.19 = ~$2,271 | ~$11,229 | $2,246 | $8,983 |
| $25,000 COP | ~$670 + $900 × 1.19 = ~$1,771 | ~$23,229 | $4,646 | $18,583 |
| $35,000 COP | ~$938 + $900 × 1.19 = ~$2,053 | ~$32,947 | $6,589 | $26,358 |
| $50,000 COP | ~$1,340 + $900 × 1.19 = ~$2,495 | ~$47,505 | $9,501 | $38,004 |
| $80,000 COP | ~$2,144 + $900 × 1.19 = ~$3,215 | ~$76,785 | $15,357 | $61,428 |

> Comisión ePayco = (precio × 2.68%) + $900, con IVA del 19% sobre la comisión total.

### Análisis de sostenibilidad

```
Con 100 transacciones/mes de ticket promedio $35,000 COP:

  Volumen bruto mensual:        $3,500,000 COP
  Comisión ePayco (~6.2%):     -$205,300 COP
  Comisión DuniPets (20%):      $658,940 COP  ← ingreso DuniPets
  Pago a cuidadores (80%):     $2,635,760 COP

  Costo retiros ePayco (2/mes × $6,500):  -$13,000 COP
  Ingreso neto DuniPets/mes:              ~$645,940 COP

Con 500 transacciones/mes de ticket promedio $45,000 COP:

  Volumen bruto mensual:       $22,500,000 COP
  Comisión ePayco (~5.8%):    -$1,305,000 COP
  Comisión DuniPets (20%):     $4,239,000 COP  ← ingreso DuniPets
  Pago a cuidadores (80%):    $16,956,000 COP

  Costo retiros ePayco (4/mes × $6,500):  -$26,000 COP
  Ingreso neto DuniPets/mes:              ~$4,213,000 COP
```

---

## Estructura de cuentas recomendada

```
┌──────────────────────────────────────────────────────────┐
│                   CUENTAS DUNIPETS                        │
│                                                           │
│  1. Panel ePayco (virtual)                                │
│     → Donde ingresan todos los cobros                     │
│     → Fuente de la dispersión automática (Fase 2)         │
│                                                           │
│  2. Cuenta bancaria operacional DuniPets                  │
│     → Cualquier banco colombiano                          │
│     → Destino de retiros desde ePayco                     │
│     → Desde aquí se pagan gastos operativos               │
│                                                           │
│  3. Cuenta Nequi / billetera (Fase 1 pagos manuales)      │
│     → Para transferir parte de los cuidadores             │
│       que prefieren Nequi                                 │
│     → Temporal — en Fase 2 usar Wompi Payouts             │
│                                                           │
│  OPCIONAL (Fase 2+):                                      │
│  4. Cuenta Bancolombia                                    │
│     → Para activar Wompi Payouts                          │
│     → Dispersión a Nequi de cuidadores                    │
│       en tiempo real                                      │
└──────────────────────────────────────────────────────────┘
```

---

## Consideraciones regulatorias

| Tema | Situación | Acción |
|---|---|---|
| SAGRILAFT (antilavado) | ePayco tiene controles automáticos; DuniPets debe reportar transacciones inusuales | Implementar T&C con política antilavado |
| IVA sobre comisión de plataforma | La comisión del 20% de DuniPets puede estar sujeta a IVA al registrar la SAS | Consultar contador antes de constituir |
| Retención en la fuente | Al superar umbrales, las transacciones pueden estar sujetas a retención | Revisar con contador |
| Límite persona natural | ePayco: $3M COP/txn (ampliable); Wompi: $2.5M COP/txn | Suficiente para pet sitting en Bogotá |
| 4×1000 GMF | Cada retiro de ePayco a cuenta bancaria causa 4×1000 ($6,500 × 0.4% = ~$26) | Incluir en modelo de costos |

---

*Ver `recomendacion_pasarelas.md` para justificación de la elección de ePayco.*
*Ver `integracion_tecnica.md` para el plan de integración técnica con ePayco Pagos Divididos.*
