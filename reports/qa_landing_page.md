# Reporte de Auditoría y QA: Landing Page de DuniPets Bogotá

Este reporte contiene la auditoría del archivo [landing_page.html](file:///C:/Users/tuto6/.gemini/antigravity/scratch/project/reports/landing_page.html) con respecto a la consistencia de precios, alineación con las brechas de mercado identificadas, errores de código (HTML/CSS/JS) y coherencia de diseño con la propuesta de valor de DuniPets.

---

## 1. Validación de Precios (vs. Benchmark en `/data/`)

**Estado:**  **Alineado con observaciones**

El archivo de datos reales del proyecto es [servicios_y_precios.json](file:///C:/Users/tuto6/.gemini/antigravity/scratch/project/data/servicios_y_precios.json) (el cual se resume en el archivo [reporte_consolidado.md](file:///C:/Users/tuto6/.gemini/antigravity/scratch/project/reporte_consolidado.md) bajo la sección de Benchmark). 

A continuación se detalla la comparación de precios promedio (COP):

| Servicio | Promedio Real (JSON) | Precio en HTML | Estado |
| :--- | :--- | :--- | :--- |
| **Hospedaje Nocturno (Perro Mediano)** | $47.500 | $47.500 / noche |  **Coincide** |
| **Paseo de 1 Hora** | $13.500 | $13.500 / paseo |  **Coincide** |
| **Visita Gatos (Cat Sitting)** | $26.500 | $26.500 / visita |  **Coincide** |

### Observaciones de Precios:
1. **Servicios Adicionales:** La landing page incluye dos servicios adicionales que **no** forman parte del benchmark en el archivo JSON:
   - *Guardería Diurna:* $35.000 COP / día.
   - *Cuidado en Casa:* $55.000 COP / día.
   Aunque no hay datos de competidores para contrastar estos precios en [servicios_y_precios.json](file:///C:/Users/tuto6/.gemini/antigravity/scratch/project/data/servicios_y_precios.json), su inclusión es coherente para dar una oferta comercial completa.
2. **Claridad de Tarifas:** Las tarjetas de servicio especifican correctamente que son tarifas base e incluyen las condiciones (ej. "perro mediano" o "hasta 10 horas"), lo cual aporta transparencia.

---

## 2. Alineación con Gaps de Mercado

**Estado:**  **Excelente alineación**

Los 3 gaps identificados en el archivo de estrategia [reporte_consolidado.md](file:///C:/Users/tuto6/.gemini/antigravity/scratch/project/reporte_consolidado.md) (mencionado como `oportunidades_mercado.md` en las instrucciones) están representados con gran precisión en la sección **"El Estándar que Tu Mascota Merece"** (`#ventajas`):

1. **Brecha 1 (Ansiedad por falta de reportes - Wakypet):**
   - *Representación:* Se presenta la solución *"Reportes Obligatorios antes de las 12 PM"* con el compromiso de fotos/videos automatizados.
   - *Elemento Interactivo:* Un mock-up de chat simulado donde el Sitter avisa del paseo en el parque Virrey a las 10:15 AM.
2. **Brecha 2 (Cancelaciones de paseadores a última hora - Wakypet):**
   - *Representación:* Se presenta la solución *"Cuidadores de Respaldo en 30 Minutos"*.
   - *Elemento Interactivo:* Un mock-up con un indicador visual parpadeante ("pulse") que muestra el "Respaldo Activo" listo para actuar en Chapinero, Cedritos y Usaquén.
3. **Brecha 3 (Abandono del nicho de gatos - CuidaMiMascota):**
   - *Representación:* Se presenta la solución *"Cat Sitting Especializado a Domicilio"* con cuidadores entrenados en etología felina.
   - *Elemento Interactivo:* Etiquetas de características específicas de gatos ("Sin estrés en casa", "Juegos y mimos", "Limpieza de arenero").

---

## 3. Reporte de Errores en HTML, CSS y JS

Durante la auditoría del código de la landing page, se identificaron varios problemas técnicos y de UX/Accesibilidad que deben ser corregidos:

###  Error 1: Estilos CSS de Lucide Icons (Selector `i` roto)
* **Descripción:** El CSS define estilos para los iconos usando el selector de etiqueta `i` (ej. `.hero-feature-item i`, `.faq-question i` y `.faq-item.active .faq-question i`). Sin embargo, la librería Lucide reemplaza dinámicamente las etiquetas `i` por elementos `svg` en el DOM. Esto causa que:
  - Los checkmarks del hero no tomen el color verde brillante.
  - El chevron de las FAQ no tome el color verde ni realice la animación de rotación (`transform: rotate(180deg)`) al abrir una pregunta.
* **Gravedad:** Media-Alta (Afecta elementos visuales e interactivos clave).
* **Solución Recomendada:** Cambiar los selectores CSS de `i` a `svg` o `.lucide` (ej. cambiar `.faq-question i` por `.faq-question svg`).

###  Error 2: Bug de Responsividad al Redimensionar (JS Inline Styles)
* **Descripción:** En la lógica del menú móvil (líneas 1948-1967), cuando se abre el menú, se inyectan múltiples estilos directamente al elemento `.nav-menu` usando Javascript (`navMenu.style.position = 'absolute'`, `navMenu.style.flexDirection = 'column'`, etc.). Al cerrar el menú, solo se limpia `navMenu.style.display`, dejando el resto de propiedades inline. Si un usuario abre el menú en móvil y luego expande la ventana del navegador a tamaño de escritorio, la barra de navegación de escritorio se renderiza rota por culpa de estos estilos inline persistentes.
* **Gravedad:** Media (Afecta la responsividad y adaptabilidad del layout).
* **Solución Recomendada:** En lugar de manipular estilos inline con JS, se debe definir una clase `.nav-menu.open` en el CSS dentro del media query móvil, y alternarla en JS mediante `navMenu.classList.toggle('open')`.

###  Error 3: Media Query Anidado Vacío
* **Descripción:** En las líneas 1187-1189 del CSS, hay un bloque `@media (min-width: 992px)` vacío anidado dentro de `@media (max-width: 1024px)`:
  ```css
  @media (min-width: 992px) {
      /* Skip since parent media query is <= 1024 */
  }
  ```
  Esto es código redundante y representa un error sintáctico en entornos que no soporten anidamiento CSS moderno.
* **Gravedad:** Baja.
* **Solución Recomendada:** Eliminar este bloque.

###  Error 4: UX Rota en Móvil (Botones de Conversión del Header Ocultos)
* **Descripción:** En pantallas móviles (ancho <= 768px), los botones principales "Soy Dueño" y "Ser Cuidador" se ocultan por completo de la cabecera mediante `.nav-actions .btn { display: none; }` en la línea 1202. Sin embargo, estos botones no se reincorporaron dentro del menú desplegable móvil. Un usuario móvil que abra la navegación no tiene ninguna llamada a la acción (CTA) directa disponible en el menú superior.
* **Gravedad:** Alta (Afecta directamente la tasa de conversión en dispositivos móviles).
* **Solución Recomendada:** Agregar copias de los botones "Soy Dueño" y "Ser Cuidador" dentro de la lista de navegación móvil (`.nav-menu`) que solo se muestren en pantallas pequeñas.

###  Error 5: Falta de Accesibilidad (a11y)
* **Descripción:**
  - Los botones interactivos que no contienen texto descriptivo directo (como el botón para cerrar modales `<button class="modal-close">` y el menú móvil `#menuToggle`) no tienen atributos `aria-label` para lectores de pantalla.
  - Los enlaces a redes sociales en el footer carecen de `aria-label`.
* **Gravedad:** Baja-Media (Importante para cumplimiento de estándares).
* **Solución Recomendada:** Agregar atributos `aria-label` descriptivos (ej. `aria-label="Cerrar modal"`, `aria-label="Menú principal"`).

---

## 4. Coherencia del Diseño con la Propuesta de Valor

**Estado:**  **Excelente (Muy premium)**

El diseño general de la página web es sobresaliente y comunica perfectamente la identidad de DuniPets Bogotá:

* **Paleta de Colores:** La combinación de verde bosque profundo (`#0F6A42`) para la marca, verde menta suave (`#EAF7F0`) para fondos de tarjetas, blanco limpio y toques dorados (`#F5B041`) para calificaciones genera una estética de "paz mental, profesionalismo y cuidado premium".
* **Tipografía:** La selección de *Outfit* para títulos (moderno y con carácter) junto con *Plus Jakarta Sans* para textos de lectura proporciona una legibilidad limpia y sofisticada.
* **Detalles Premium (Wow Effect):**
  - La tarjeta flotante en el Hero de "Reporte Diario Enviado" materializa de inmediato la promesa de tranquilidad.
  - El uso de la animación de parpadeo ("pulse") en la sección de cuidadores de respaldo da dinamismo y sensación de "tecnología en tiempo real".
  - La integración de confeti animado (`canvas-confetti`) tras enviar los formularios ofrece una respuesta de éxito interactiva memorable.

---

## 5. Código de Corrección Recomendado

Para corregir los errores identificados en la sección 3, se recomiendan los siguientes cambios en [landing_page.html](file:///C:/Users/tuto6/.gemini/antigravity/scratch/project/reports/landing_page.html):

### A. Modificaciones en el CSS (Líneas 308, 890, 903 y Menú Móvil)

```css
/* 1. Corrección de Selectores Lucide (Reemplazar 'i' por 'svg') */
.hero-feature-item svg {
    color: var(--primary-light);
}

.faq-question svg {
    color: var(--primary);
    transition: var(--transition);
}

.faq-item.active .faq-question svg {
    transform: rotate(180deg);
}

/* 2. Definición limpia para el menú móvil abierto */
@media (max-width: 768px) {
    .nav-menu {
        display: none; /* Oculto por defecto en móvil */
    }
    
    .nav-menu.open {
        display: flex !important;
        flex-direction: column;
        position: absolute;
        top: 80px;
        left: 0;
        width: 100%;
        background-color: var(--white);
        padding: 24px;
        border-bottom: 1px solid var(--border);
        box-shadow: var(--shadow-md);
        gap: 20px;
    }
    
    /* Mostrar CTAs en el menú móvil para UX */
    .nav-menu .mobile-cta-btn {
        display: block !important;
        width: 100%;
        text-align: center;
        margin-top: 8px;
    }
}
```

### B. Modificación en el HTML (Menú Móvil con CTAs y aria-labels)

```html
<!-- Cabecera Corregida con Accesibilidad y CTAs Móviles -->
<header class="header" id="header">
    <div class="container">
        <div class="nav-wrapper">
            <a href="#" class="logo" aria-label="DuniPets Inicio">
                <i data-lucide="paw-print"></i> Duni<span>Pets</span>
            </a>
            <nav class="nav-menu">
                <a href="#ventajas" class="nav-link">Por qué Duni</a>
                <a href="#servicios" class="nav-link">Servicios y Tarifas</a>
                <a href="#testimonios" class="nav-link">Testimonios</a>
                <a href="#faqs" class="nav-link">Preguntas Frecuentes</a>
                <!-- CTAs duplicados exclusivos para móvil -->
                <button class="btn btn-secondary mobile-cta-btn open-owner-modal" style="display: none;">Soy Dueño</button>
                <button class="btn btn-primary mobile-cta-btn open-sitter-modal" style="display: none;">Ser Cuidador</button>
            </nav>
            <div class="nav-actions">
                <button class="btn btn-secondary open-owner-modal">Soy Dueño</button>
                <button class="btn btn-primary open-sitter-modal">Ser Cuidador</button>
                <button class="mobile-menu-btn" id="menuToggle" aria-label="Abrir menú de navegación">
                    <i data-lucide="menu"></i>
                </button>
            </div>
        </div>
    </div>
</header>
```

### C. Modificación del Script del Menú Móvil (Evita inyección inline)

```javascript
// JS del Menú Móvil Limpio de Estilos Inline
const menuToggle = document.getElementById('menuToggle');
const navMenu = document.querySelector('.nav-menu');
let isMenuOpen = false;

menuToggle.addEventListener('click', () => {
    isMenuOpen = !isMenuOpen;
    if (isMenuOpen) {
        navMenu.classList.add('open');
        menuToggle.innerHTML = '<i data-lucide="x"></i>';
        menuToggle.setAttribute('aria-label', 'Cerrar menú de navegación');
    } else {
        navMenu.classList.remove('open');
        menuToggle.innerHTML = '<i data-lucide="menu"></i>';
        menuToggle.setAttribute('aria-label', 'Abrir menú de navegación');
    }
    lucide.createIcons();
});

// Cerrar menú móvil al hacer click en un link
document.querySelectorAll('.nav-link').forEach(link => {
    link.addEventListener('click', () => {
        if (isMenuOpen) {
            navMenu.classList.remove('open');
            menuToggle.innerHTML = '<i data-lucide="menu"></i>';
            isMenuOpen = false;
            lucide.createIcons();
        }
    });
});
```
