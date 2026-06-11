import json
import os

def load_data(filename):
    # Ensure it works dynamically based on the script location
    filepath = os.path.join(os.path.dirname(__file__), '..', 'data', filename)
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)

def main():
    # Cargar datos
    try:
        competidores = load_data('competidores.json')
        servicios = load_data('servicios_y_precios.json')
        brechas = load_data('brechas_reviews.json')
        sitters = load_data('estrategia_sitters.json')
        gtm = load_data('estrategia_gtm.json')
    except Exception as e:
        print(f"Error cargando datos: {e}")
        return

    # Mapear competidores por ID para fácil acceso
    comp_map = {c['id']: c['nombre'] for c in competidores}

    print("="*85)
    print(" " * 20 + "REPORTE DE MERCADO - DUNI PETS BOGOTÁ")
    print("="*85)
    print("\n1. BENCHMARK DE PRECIOS PROMEDIO POR SERVICIO\n")
    print("-" * 85)
    print(f"{'Servicio':<40} | {'Precio Promedio (COP)':>25}")
    print("-" * 85)

    # Calcular precio promedio por servicio
    service_prices = {}
    for s in servicios:
        name = s['nombre_servicio']
        if name not in service_prices:
            service_prices[name] = []
        service_prices[name].append(s['precio_cop'])
    
    for name, prices in service_prices.items():
        avg_price = sum(prices) / len(prices)
        # Formatear el precio con separador de miles (usamos punto para estilo local)
        formatted_price = f"${int(avg_price):,}".replace(",", ".")
        print(f"{name:<40} | {formatted_price:>25} COP")

    print("\n" + "="*85)
    print("2. ANÁLISIS DE BRECHAS CRÍTICAS Y OPORTUNIDADES ESTRATÉGICAS")
    print("="*85 + "\n")

    # Agrupar brechas por competidor
    gaps_by_comp = {}
    for b in brechas:
        cid = b['competidor_id']
        if cid not in gaps_by_comp:
            gaps_by_comp[cid] = []
        gaps_by_comp[cid].append(b)

    for cid, gaps in gaps_by_comp.items():
        comp_name = comp_map.get(cid, "Desconocido")
        print(f"COMPETIDOR: {comp_name.upper()}")
        print("-" * 85)
        for g in gaps:
            print(f"  [!] DOLOR (Gravedad {g['gravedad_fallo']}): {g['resumen_dolor']}")
            print(f"      Review Real: \"{g['review_original']}\"")
            print(f"  [+] OPORTUNIDAD DUNI: {g['oportunidad_duni']}\n")
            
    print("="*85)
    print("3. ESTRATEGIA DE CAPTURA DE SUPER SITTERS BOGOTÁ")
    print("="*85 + "\n")
    
    for s in sitters:
        print(f"PERFIL: {s['perfil_sitter'].upper()}")
        print(f"  Zonas Clave: {s['zonas_clave']}")
        print(f"  [!] Barrera Bogotana: {s['barrera_bogotana']}")
        print(f"  [+] Estrategia Duni: {s['estrategia_duni']}")
        print(f"  [>] Canal: {s['canal_reclutamiento']}\n")

    print("="*85)
    print("4. ESTRATEGIA DE GO-TO-MARKET (LANZAMIENTO BOGOTÁ)")
    print("="*85 + "\n")
    
    for g in gtm:
        print(f"BARRIO OBJETIVO: {g['barrio_objetivo'].upper()}")
        print(f"  Canal de Adquisición: {g['canal_adquisicion']}")
        print(f"  [+] Táctica de Conversión: {g['tactica_conversion']}")
        print(f"  [>] Métrica de Éxito: {g['metrica_exito']}\n")

    print("="*85)
    print("FIN DEL REPORTE".center(85))
    print("="*85)

if __name__ == '__main__':
    main()
