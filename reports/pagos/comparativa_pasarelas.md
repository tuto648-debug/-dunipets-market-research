# Comparativa Pasarelas de Pago — DuniPets Colombia
**Fecha de investigación**: junio 2026  
**Contexto**: Marketplace de cuidado de mascotas en Bogotá. Sin registro legal (SAS en formación). Tickets entre $13,500 y $55,000 COP.

---

## Tabla comparativa principal

| Pasarela | Métodos de pago | Comisión tarjeta | Comisión PSE | Requiere SAS | Link sin código | Split / Dispersión | Puntuación DuniPets |
|---|---|---|---|---|---|---|---|
| **Wompi** | Tarjeta, PSE, Nequi (nativo), Daviplata, efectivo (17,600 corresponsales), Bre-B QR, Botón Bancolombia | 2.65% + $700 + IVA | ~1.49% + $1,200 + IVA | ❌ Persona natural OK — pero DEBE tener cuenta Bancolombia | ✅ | ✅ Payouts API ($1,849 + 0.4% + IVA por dispersión) | ⭐ 8.5/10 |
| **ePayco** | Tarjeta, PSE, Daviplata (nativo), efectivo (Efecty, Gana, PuntoRed, SafetyPay), PayPal | 2.68% + $900 + IVA (Davivienda) / 2.99% + $900 + IVA (otros) | $2,000 COP plano para txn <$60K + IVA | ❌ Persona natural OK — sin cámara de comercio | ✅ | ✅ **Pagos Divididos** (split automático por %) | ⭐ 9/10 |
| **PayU** | Tarjeta, PSE, Nequi, Google Pay, efectivo (Efecty, Davivienda) | 3.29% + $300 + IVA | 3.29% + mín $450 + IVA | ❌ Persona natural OK | ✅ | ⚠️ Payouts API separado (no split nativo para marketplace de servicios) | ⭐ 5.5/10 |
| **Mercado Pago** | Tarjeta, PSE, efectivo (Efecty), billetera MP | 3.29% + $800 + IVA (liquidación inmediata) / 2.79% + $800 + IVA (a 14 días) | ~1.99% + $800 + IVA | ❌ Persona natural OK | ✅ | ⚠️ Split Payments disponible — pero **cuidadores DEBEN tener cuenta Mercado Pago** | ⭐ 5/10 |
| **Kushki** | Tarjeta, PSE, efectivo (Cash Out código único) | **Negociado** (no público) | Negociado | ✅ **Requiere empresa constituida + Cámara de Comercio** | ❌ No no-code visible | ✅ PayOuts API | ⭐ 2/10 |
| **Bold** | Tarjeta, PSE, Nequi, Daviplata (limitado), QR Bre-B | ~2.80% + $500 + IVA | ~1.79% + IVA | ❌ Persona natural OK | ✅ Muy fácil | ❌ **No tiene split ni dispersión a terceros** | ⭐ 6/10 |
| **Clip** | N/A | N/A | N/A | N/A | N/A | N/A | ❌ No opera en Colombia |
| **PlaceToPay / Evertec** | Tarjeta, PSE, Nequi, Daviplata, efectivo | 2.9% + $700–$750 + IVA | Negociado | ✅ Orientado a empresas medianas/grandes | ✅ | ✅ Soporta distribución de fondos | ⭐ 3/10 |
| **Rebill** | Tarjeta, PSE, Nequi, cuotas | 4% + $500 + IVA | N/A | ❌ Persona natural OK | ✅ | ❌ No aplica (foco en suscripciones) | ⭐ 2/10 |

---

## Detalle por criterio DuniPets

### 1. Métodos de pago — cobertura comparada

| Pasarela | Visa/MC/Amex | PSE | Nequi | Daviplata | Efectivo |
|---|---|---|---|---|---|
| Wompi | ✅ | ✅ | ✅ Nativo | ✅ | ✅ 17,600 puntos |
| ePayco | ✅ | ✅ | ⚠️ via PSE | ✅ Nativo | ✅ Efecty, Gana |
| PayU | ✅ | ✅ | ✅ | ✅ | ✅ Efecty |
| Mercado Pago | ✅ | ✅ | ⚠️ Limitado | ⚠️ Limitado | ✅ Efecty |
| Bold | ✅ | ✅ | ✅ | ⚠️ Limitado | ❌ |
| Kushki | ✅ | ✅ | ⚠️ Sin confirmar | ⚠️ Sin confirmar | ✅ Cash Out |

### 2. Comisiones por transacción (Flujo 1 — cobro a clientes)

> Ejemplo: ticket de $50,000 COP

| Pasarela | Comisión efectiva aprox. (tarjeta) | Comisión efectiva aprox. (PSE) |
|---|---|---|
| Wompi | $1,325 × 1.19 IVA + $700 = **~$2,275** | ~$745 + $1,200 = ~$2,295 (con IVA) |
| ePayco (Davivienda) | $1,340 × 1.19 + $900 = **~$2,495** | **$2,000** + IVA = ~$2,380 |
| ePayco (otros) | $1,495 × 1.19 + $900 = **~$2,679** | $2,000 + IVA = ~$2,380 |
| PayU | $1,645 × 1.19 + $300 = **~$2,257** | $1,645 × 1.19 + $300 = ~$2,257 (igual) |
| Mercado Pago (inmediato) | $1,645 × 1.19 + $800 = **~$2,758** | ~$995 + $800 = ~$2,184 |
| Bold | $1,400 × 1.19 + $500 = **~$2,166** | ~$895 × 1.19 = ~$1,065 |

> IVA del 19% se aplica sobre la comisión, no sobre el total de la transacción.

### 3. Dispersión a cuidadores (Flujo 2 — pagar sitters)

| Pasarela | Dispersión disponible | Tipo | Destinos | Costo por pago | Requiere cuenta especial del cuidador |
|---|---|---|---|---|---|
| **Wompi Payouts** | ✅ | Batch API / panel admin | Cualquier banco + Nequi inmediato | $1,849 + 0.4% + IVA | No (cualquier cuenta bancaria) |
| **ePayco Pagos Divididos** | ✅ | Split en la misma transacción | Cuentas bancarias + Daviplata | Sin costo extra (incluido en la comisión de cobro) | No |
| PayU Payouts | ⚠️ | Proceso separado, validación antilavado hasta 24h | Cuentas bancarias ACH (sin Daviplata) | No divulgado | No |
| Mercado Pago Split | ⚠️ | OAuth por cuidador | Billetera Mercado Pago | Sin costo extra | **SÍ — cada cuidador necesita cuenta MP** |
| Kushki PayOuts | ✅ | API | Cuentas bancarias + efectivo | No divulgado | No (pero requiere empresa constituida) |
| Bold | ❌ | N/A | N/A | N/A | N/A |

### 4. Requisitos legales (empresa en formación)

| Pasarela | Persona Natural | SAS en formación | Documentos mínimos |
|---|---|---|---|
| Wompi | ✅ (sin Cámara de Comercio) | ✅ Como persona natural | RUT + **cuenta Bancolombia** + selfie |
| ePayco | ✅ | ✅ Como persona natural | Cédula + RUT + comprobante domicilio |
| PayU | ✅ | ✅ Como persona natural | Cédula + RUT + extractos 3 meses + descripción negocio |
| Mercado Pago | ✅ | ✅ Como persona natural | Cédula |
| Bold | ✅ | ✅ Como persona natural | Cédula colombiana (mayor 18) |
| Kushki | ❌ | ❌ Requiere Cámara de Comercio | NIT + CC + estados financieros |

### 5. Settlement (tiempo de acreditación)

| Pasarela | Tiempo a cuenta propia |
|---|---|
| Bold | Mismo día (segundos) |
| Wompi | Día siguiente hábil |
| ePayco | 1–3 días hábiles |
| PayU | 3 días hábiles (3 retiros gratis/mes; $6,500 adicionales) |
| Mercado Pago | 0 días (a billetera MP) / hasta 14 días (a cuenta bancaria) |
| Kushki | Negociado |

### 6. Panel sin código (lanzar sin desarrollo)

| Pasarela | Link de pago | Plugin e-commerce | WhatsApp / RRSS | QR |
|---|---|---|---|---|
| Wompi | ✅ | ✅ WooCommerce / Shopify / PrestaShop | ✅ | ✅ |
| ePayco | ✅ | ✅ WooCommerce / Shopify | ✅ | ✅ |
| PayU | ✅ | ✅ | ✅ | ✅ |
| Mercado Pago | ✅ | ✅ | ✅ | ✅ |
| Bold | ✅ Muy fácil | ✅ | ✅ | ✅ |
| Kushki | ❌ | ❌ | ❌ | ❌ |

---

## Matriz de puntuación DuniPets

| Criterio | Peso | Wompi | ePayco | PayU | Mercado Pago | Bold |
|---|---|---|---|---|---|---|
| Persona natural / SAS | 25% | 8 (req. cuenta Bancolombia) | **9** | 8 | 9 | **9** |
| Link sin código | 15% | 8 | 8 | 7 | 8 | **10** |
| Nequi / Daviplata | 15% | **10** (Nequi nativo) | 8 (Daviplata nativo) | 8 | 6 | 8 |
| Dispersión sitters | 30% | **9** (Payouts API) | **10** (Split automático) | 5 | 6 | 1 |
| Comisión competitiva | 15% | **9** (2.65%) | 8 (2.68–2.99%) | 6 (3.29%) | 5 (3.29%+$800) | 8 (2.80%) |
| **TOTAL** | 100% | **8.90** | **8.85** | 6.55 | 6.65 | 6.35 |

> **Empate técnico Wompi-ePayco.** La diferencia clave: Wompi requiere cuenta Bancolombia; ePayco tiene Split automático sin costo adicional.

---

## Notas sobre confiabilidad de datos

- Las tarifas de PSE de Wompi (1.49%) y Bold (1.79%) provienen de fuentes comparativas, no de la página oficial. Verificar con ejecutivo comercial antes de integrar.
- PayU está en proceso de transición a Rapyd (adquirida ~2024–2025). Verificar continuidad del servicio.
- ePayco: la tarifa de PSE para transacciones >$60,000 no fue confirmada oficialmente. Consultar directamente.
- El límite de $3,000,000 COP por transacción de ePayco para persona natural es ampliable bajo solicitud — no es una limitación permanente.

---

*Investigación realizada con fuentes oficiales de cada pasarela y fuentes comparativas actualizadas a junio 2026.*
