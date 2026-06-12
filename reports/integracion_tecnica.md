# Integración Técnica — ePayco Pagos Divididos para DuniPets
**Pasarela**: ePayco | **Característica clave**: Pagos Divididos (Split Payments)  
**Fecha**: junio 2026 | **Documentación oficial**: https://docs.epayco.com

---

## Resumen de la arquitectura

```
┌─────────────────────────────────────────────────────────────────────┐
│                    ARQUITECTURA DE INTEGRACIÓN                       │
│                                                                      │
│   Frontend DuniPets          Backend DuniPets         ePayco API    │
│   (Web / App)                (Node / Python / PHP)                  │
│                                                                      │
│   Usuario hace checkout  →   Crear token de pago  →   POST /token   │
│                              con parámetros split                    │
│                                                                      │
│   Checkout embebido      ←   Retornar tokenId     ←   tokenId       │
│   ePayco (JS plugin)                                                 │
│                                                                      │
│   Usuario completa pago  →   ePayco procesa       →   Split:        │
│                              tarjeta/PSE/Daviplata     - 80% sitter  │
│                                                        - 20% DuniPets│
│                                                                      │
│   Confirmación           ←   Webhook notifica     ←   POST webhook  │
│   al usuario                 estado del pago                        │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Paso 0 — Prerrequisitos de configuración

### En el panel de ePayco (admin.epayco.co):

1. **Crear cuenta principal** (DuniPets): registro como persona natural con cédula + RUT + comprobante domicilio.
2. **Activar Pagos Divididos**: enviar ticket de soporte solicitando activación del feature. Proporcionar:
   - Descripción del modelo de negocio (marketplace de cuidado de mascotas)
   - Porcentajes de distribución esperados
3. **Registrar Receptores (Receivers)**: cada cuidador debe ser registrado como receptor. ePayco solicita:
   - Nombre completo
   - Número de cuenta bancaria o Daviplata
   - Tipo de cuenta (ahorros / corriente)
   - Banco (código)
4. **Registrar Comercios secundarios (Merchants)**: para el flujo de split, los cuidadores pueden también operar como sub-merchants.
5. **Obtener credenciales API**:
   - `P_CUST_ID_CLIENTE` (Customer ID)
   - `P_KEY` (Secret key — solo para backend)
   - `PUBLIC_KEY` (para frontend)
   - Activar webhook URL en el panel

---

## Paso 1 — Frontend: cargar el SDK de ePayco

```html
<!-- En el <head> de la página de checkout -->
<script src="https://checkout.epayco.co/checkout.js"></script>
```

```javascript
// Configuración del handler de pago
const handler = ePayco.checkout.configure({
  key: 'TU_PUBLIC_KEY',   // Pública — seguro poner en frontend
  test: false              // true en sandbox, false en producción
});
```

---

## Paso 2 — Backend: crear el token de pago con split

El split se define en el **backend** para evitar manipulación desde el cliente.

### Endpoint: `POST https://secure.epayco.co/payment/process`

```python
# Python — ejemplo con requests
import requests
import hashlib

def crear_pago_con_split(reserva_id, monto_total_cop, sitter_id, sitter_cuenta):
    """
    monto_total_cop: int, ej. 50000
    sitter_id: str, ID del receptor registrado en ePayco
    """
    # Firma de seguridad (HMAC SHA256)
    # Documentación: https://docs.epayco.com/docs/firma
    firma = hashlib.sha256(
        f"{P_CUST_ID}^{P_KEY}^{reserva_id}^{monto_total_cop}^COP".encode()
    ).hexdigest()

    payload = {
        # Identificación del comercio
        "P_CUST_ID_CLIENTE": P_CUST_ID,
        "P_KEY": P_KEY,

        # Detalles de la transacción
        "x_ref_payco": reserva_id,          # ID único de la reserva
        "x_amount": monto_total_cop,         # Valor total que paga el cliente
        "x_currency_code": "COP",
        "x_description": f"Reserva DuniPets #{reserva_id}",
        "x_signature": firma,

        # URLs de retorno
        "x_redirect_url": "https://dunipets.co/reserva/confirmacion",
        "x_response_url": "https://dunipets.co/reserva/respuesta",

        # Configuración de Pagos Divididos (Split)
        # Tipo 02 = porcentaje; Tipo 01 = monto fijo
        "split": [
            {
                "id_receiver": sitter_id,    # ID del cuidador en ePayco
                "type": "02",                # Tipo 02: porcentaje
                "value": "80"               # 80% va al cuidador
            }
            # El 20% restante queda automáticamente en la cuenta principal DuniPets
        ]
    }

    response = requests.post(
        "https://secure.epayco.co/payment/process",
        json=payload,
        headers={"Content-Type": "application/json"}
    )
    return response.json()
```

```javascript
// Node.js — alternativa
const epayco = require('epayco-sdk-node')({
  apiKey: process.env.EPAYCO_PUBLIC_KEY,
  privateKey: process.env.EPAYCO_PRIVATE_KEY,
  lang: 'ES',
  test: false
});

async function crearPagoConSplit(reservaId, monto, sitterId) {
  const pago = await epayco.charge.create({
    // Token de tarjeta (obtenido desde frontend)
    token_card: tokenDeTarjeta,

    // Datos de la transacción
    name: "DuniPets - Servicio de cuidado",
    description: `Reserva #${reservaId}`,
    invoice: reservaId,
    currency: "cop",
    amount: monto,
    tax_base: "0",
    tax: "0",

    // Pagos divididos
    split: [
      {
        id_receiver: sitterId,
        type: "02",    // porcentaje
        value: "80"
      }
    ]
  });
  return pago;
}
```

---

## Paso 3 — Frontend: abrir el checkout con el token

```javascript
// Después de que el backend crea el token
async function iniciarPago(reservaId, monto) {
  // Llamar al backend propio de DuniPets para crear el token
  const res = await fetch('/api/crear-pago', {
    method: 'POST',
    body: JSON.stringify({ reserva_id: reservaId, monto })
  });
  const { tokenId } = await res.json();

  // Abrir checkout ePayco
  handler.open({
    name: "DuniPets",
    description: `Reserva #${reservaId}`,
    invoice: reservaId,
    currency: "COP",
    amount: monto,
    tax_base: "0",
    tax: "0",
    country: "CO",
    lang: "es",
    external: "false",         // Checkout embebido en la página (no redirect)
    confirmation: "https://dunipets.co/api/webhook/epayco",
    response: "https://dunipets.co/reserva/respuesta",

    // Métodos de pago a mostrar
    methodsDisable: ["SP", "CASH"]  // Deshabilitar Safetypay y efectivo si se prefiere
  });
}
```

---

## Paso 4 — Backend: recibir webhook de confirmación

ePayco envía un POST a la URL de confirmación cuando el pago es aprobado/rechazado.

```python
# Python (FastAPI) — endpoint webhook
from fastapi import FastAPI, Request
import hashlib

app = FastAPI()

@app.post("/api/webhook/epayco")
async def webhook_epayco(request: Request):
    data = await request.json()

    # 1. Validar firma para evitar fraudes
    firma_esperada = hashlib.sha256(
        f"{P_CUST_ID}^{P_KEY}^{data['x_ref_payco']}^{data['x_amount']}^{data['x_currency_code']}^{data['x_transaction_state']}".encode()
    ).hexdigest()

    if firma_esperada != data.get('x_signature'):
        return {"error": "Firma inválida"}, 400

    # 2. Procesar según estado
    estado = data['x_transaction_state']
    reserva_id = data['x_ref_payco']

    if estado == "Aceptada":
        # Pago aprobado — actualizar reserva en base de datos
        await actualizar_reserva(reserva_id, estado="pagada")
        await notificar_cuidador(reserva_id)  # WhatsApp / email
        await notificar_cliente(reserva_id)

    elif estado == "Rechazada":
        await actualizar_reserva(reserva_id, estado="fallida")
        await notificar_cliente_pago_fallido(reserva_id)

    elif estado == "Pendiente":
        # PSE o efectivo — esperar confirmación final
        await actualizar_reserva(reserva_id, estado="pendiente")

    return {"status": "ok"}
```

### Campos clave del webhook ePayco

| Campo | Descripción |
|---|---|
| `x_ref_payco` | Referencia de la transacción (= `invoice` enviado) |
| `x_transaction_state` | `Aceptada`, `Rechazada`, `Pendiente`, `Fallida` |
| `x_amount` | Monto total pagado |
| `x_amount_ok` | Monto aprobado efectivamente |
| `x_bank_name` | Banco / método usado |
| `x_signature` | Firma SHA256 para validar autenticidad |
| `split_results` | Array con resultados de cada receptor del split |

---

## Paso 5 — Registrar un nuevo cuidador como receptor

Cada vez que un cuidador se une a DuniPets, debe ser registrado como Receiver en ePayco.

```python
# Llamada a la API para crear un receptor (sitter)
def registrar_cuidador_epayco(nombre, banco_codigo, numero_cuenta, tipo_cuenta):
    """
    banco_codigo: código bancario ePayco (ej. "1022" = Bancolombia)
    tipo_cuenta: "01" ahorros, "02" corriente
    """
    payload = {
        "P_CUST_ID_CLIENTE": P_CUST_ID,
        "P_KEY": P_KEY,
        "name": nombre,
        "bank": banco_codigo,
        "account": numero_cuenta,
        "type_account": tipo_cuenta
    }
    response = requests.post(
        "https://secure.epayco.co/restpagos/receiver/create",
        json=payload
    )
    return response.json()  # Retorna id_receiver para almacenar en DB

# Códigos de banco ePayco más relevantes Colombia:
BANCOS = {
    "Bancolombia": "1007",
    "Banco de Bogotá": "1001",
    "Davivienda": "1051",
    "Nequi/Bancolombia digital": "1007",  # Nequi comparte código Bancolombia
    "BBVA": "1013",
    "Scotiabank Colpatria": "1019",
    "Banco Popular": "1002",
    "AV Villas": "1052"
}
```

---

## Consideraciones de seguridad

| Riesgo | Mitigación |
|---|---|
| Exposición de `P_KEY` | Nunca enviarlo al frontend. Solo en variables de entorno del servidor. |
| Manipulación del monto desde el cliente | El monto y el split se calculan y firman en el backend. El frontend solo muestra. |
| Webhook falso (fraude) | Siempre validar `x_signature` con HMAC SHA256 antes de procesar. |
| Double-spending | Usar `x_ref_payco` único por transacción + idempotencia en base de datos. |
| SQL injection en IDs | Usar ORM o queries parametrizadas con el `reserva_id`. |

---

## Ambiente de pruebas (sandbox)

```javascript
// Tarjetas de prueba ePayco (sandbox)
const TARJETAS_PRUEBA = {
  aprobada: {
    numero: "4575623182290326",
    cvv: "123",
    expiry: "12/26",
    nombre: "Duni Pets Test"
  },
  rechazada: {
    numero: "4111111111111111",
    cvv: "123",
    expiry: "12/26"
  }
};

// Activar modo test en el SDK:
// test: true  (en configure)
// URL sandbox: https://sandbox.checkout.epayco.co/checkout.js
```

---

## Stack técnico mínimo para Fase 2

| Componente | Tecnología sugerida | Alternativa |
|---|---|---|
| Backend | Node.js (Express) + SDK ePayco | Python FastAPI / PHP Laravel |
| Base de datos | PostgreSQL (reservas, cuidadores, transacciones) | MySQL / Supabase |
| Webhook | Endpoint HTTPS propio con SSL | Ngrok en desarrollo |
| Variables de entorno | `.env` con `dotenv` — nunca en código | AWS Secrets Manager / Vault |
| Notificaciones | SendGrid (email) + WhatsApp Business API | Twilio SMS |
| Frontend checkout | ePayco JS plugin embebido | Redirect a ePayco Webcheckout |

---

## Flujo técnico completo — secuencia de llamadas

```
1. POST /api/reservas (DuniPets backend)
   └── Crea reserva con estado "pendiente_pago"
   └── Retorna reserva_id + monto al frontend

2. GET /api/pagos/token?reserva={id} (DuniPets backend)
   └── Calcula split (20% DuniPets, 80% sitter)
   └── Obtiene id_receiver del sitter desde DB
   └── Firma la transacción con P_KEY
   └── Retorna datos de configuración al frontend

3. Frontend abre ePayco checkout con datos firmados

4. Usuario completa pago en checkout ePayco

5. ePayco → POST /api/webhook/epayco (DuniPets backend)
   └── Valida firma
   └── Actualiza reserva en DB
   └── Dispara notificaciones (cliente + cuidador)

6. ePayco ejecuta split automáticamente
   └── 80% → cuenta bancaria del cuidador (1–3 días hábiles)
   └── 20% → cuenta principal DuniPets (1–3 días hábiles)
```

---

## Recursos técnicos

| Recurso | URL |
|---|---|
| Documentación Split Payments | https://docs.epayco.com/docs/split-descripcion |
| SDK Node.js | https://github.com/epayco/epayco-node |
| SDK Python | https://github.com/epayco/epayco-python |
| SDK PHP | https://github.com/epayco/epayco-php |
| Panel Admin | https://admin.epayco.co |
| Sandbox checkout | https://sandbox.checkout.epayco.co |
| Soporte técnico | soporte@epayco.co |
| Lista códigos de banco | https://docs.epayco.com/docs/bancos-colombia |

---

*Basado en documentación oficial ePayco + research de junio 2026. Verificar versiones de API antes de implementar.*
