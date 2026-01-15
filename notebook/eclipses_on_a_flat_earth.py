import math
from datetime import datetime, timedelta

# ============================================================
# RANGO TEMPORAL
# ============================================================
START_DATE = datetime(2026, 1, 13)
END_DATE   = datetime(2036, 1, 13)
STEP_HOURS = 1

# ============================================================
# CONSTANTES TEMPORALES (ESTABLES)
# ============================================================
YEAR_DAYS      = 365.242189
SYNODIC_MONTH  = 29.53058885
SAROS_DAYS     = 6585.3211
ECLIPSE_YEAR   = 346.620075   # Año dracónico (temporadas nodales)

# ============================================================
# UMBRALES (NO CALIBRADOS AUTOMÁTICAMENTE)
# ============================================================
PHASE_TOL = 0.006     # ~4.2 horas
NODE_TOL  = 0.045     # Ventana nodal estricta

# ============================================================
# ANCLAJES (REFERENCIAS, NO AJUSTES)
# ============================================================
REF_DATE = datetime(2026, 2, 17, 12, 0)   # Eclipse solar de referencia
EPOCH    = datetime(2000, 1, 1, 12, 0)

# ============================================================
# UTILIDADES
# ============================================================
def frac(x):
    return x - math.floor(x)

def days_between(a, b):
    return (a - b).total_seconds() / 86400.0

# ============================================================
# ANALÉMA SOLAR (12 PUNTOS / 3 ARMÓNICOS)
# ============================================================
def analemma_height(year_frac):
    return (
        0.25 * math.sin(2 * math.pi * year_frac) +
        0.08 * math.sin(4 * math.pi * year_frac) +
        0.03 * math.sin(6 * math.pi * year_frac)
    )

# ============================================================
# GEOMETRÍA TEMPORAL DEL MODELO
# ============================================================
def get_geometry(t):
    d_ref = days_between(t, REF_DATE)
    d_ep  = days_between(t, EPOCH)

    # 1. Fracción anual (analema / constelaciones)
    year_frac = frac(d_ep / YEAR_DAYS)

    # 2. Fase sinódica (Sol–Luna)
    syn_phase = frac(d_ref / SYNODIC_MONTH)

    # 3. Temporada nodal (dos por año)
    node_sync = frac(d_ref / ECLIPSE_YEAR)
    dist_node = min(
        node_sync,
        1.0 - node_sync,
        abs(node_sync - 0.5)
    )

    return syn_phase, dist_node, year_frac

# ============================================================
# DETECCIÓN DE ECLIPSES
# ============================================================
def detect_eclipse(t):
    syn_phase, dist_node, year_frac = get_geometry(t)

    # Filtros de fase
    is_new  = (syn_phase < PHASE_TOL) or (syn_phase > (1.0 - PHASE_TOL))
    is_full = abs(syn_phase - 0.5) < PHASE_TOL

    # Sin temporada nodal → no hay eclipse
    if dist_node > NODE_TOL:
        return None

    # Altura solar (analema)
    z_s = analemma_height(year_frac)

    # ============================
    # ECLIPSE SOLAR
    # ============================
    if is_new:
        if dist_node < 0.011:
            return "SOLAR", "Annular"
        if dist_node < 0.028:
            return "SOLAR", "Total"
        return "SOLAR", "Partial"

    # ============================
    # ECLIPSE LUNAR
    # ============================
    if is_full:
        if dist_node < 0.016:
            return "LUNAR", "Total"
        if dist_node < 0.036:
            return "LUNAR", "Partial"
        return "LUNAR", "Penumbral"

    return None

# ============================================================
# REFINAMIENTO TEMPORAL DEL EVENTO
# ============================================================
def refine_peak(t0):
    best_t = t0
    _, min_node, _ = get_geometry(t0)

    for h in range(-12, 13):
        tt = t0 + timedelta(hours=h)
        _, d_node, _ = get_geometry(tt)
        if d_node < min_node:
            min_node = d_node
            best_t = tt

    return best_t

# ============================================================
# SIMULACIÓN
# ============================================================
results = []
t = START_DATE
last_event = None
cooldown = timedelta(days=10)

while t < END_DATE:
    res = detect_eclipse(t)
    if res:
        best_t = refine_peak(t)
        res_final = detect_eclipse(best_t) or res

        if last_event is None or (best_t - last_event) > cooldown:
            results.append((best_t.date(), res_final[0], res_final[1]))
            last_event = best_t

            # Salto para buscar el par de la temporada
            t = best_t + timedelta(days=13)
            continue

    t += timedelta(hours=STEP_HOURS)

# ============================================================
# SALIDA
# ============================================================
print("ECLIPSES (MODELO PLANO + ANALÉMA + NODOS + SAROS + LUMINARIAS LOCALES)\n")
print(f"{'FECHA':<12} | {'TIPO':<6} | {'SUBTIPO'}")
print("-" * 36)

for d, kind, subtype in results:
    print(f"{d}  |  {kind:<6} | {subtype}")


"""
ECLIPSES (MODELO PLANO + ANALÉMA + NODOS + SAROS + LUMINARIAS LOCALES)

FECHA        | TIPO   | SUBTIPO
------------------------------------
2026-02-03  |  LUNAR  | Penumbral
2026-02-17  |  SOLAR  | Annular
2026-03-03  |  LUNAR  | Penumbral
2026-07-30  |  LUNAR  | Partial
2026-08-13  |  SOLAR  | Annular
2027-01-23  |  LUNAR  | Partial
2027-02-06  |  SOLAR  | Total
2027-07-19  |  LUNAR  | Total
2027-08-02  |  SOLAR  | Partial
2027-12-29  |  SOLAR  | Partial
2028-01-11  |  LUNAR  | Total
2028-01-26  |  SOLAR  | Partial
2028-06-23  |  SOLAR  | Partial
2028-07-07  |  LUNAR  | Total
2028-12-17  |  SOLAR  | Total
2028-12-31  |  LUNAR  | Partial
2029-06-12  |  SOLAR  | Annular
2029-06-26  |  LUNAR  | Partial
2029-11-22  |  LUNAR  | Penumbral
2029-12-05  |  SOLAR  | Annular
2030-05-18  |  LUNAR  | Partial
2030-05-31  |  SOLAR  | Total
2030-11-11  |  LUNAR  | Partial
2030-11-25  |  SOLAR  | Total
2031-05-07  |  LUNAR  | Total
2031-05-21  |  SOLAR  | Partial
2031-10-17  |  SOLAR  | Partial
2031-10-30  |  LUNAR  | Total
2032-04-11  |  SOLAR  | Total
2032-04-24  |  LUNAR  | Partial
2032-10-05  |  SOLAR  | Total
2032-10-19  |  LUNAR  | Partial
2033-03-17  |  LUNAR  | Penumbral
2033-03-31  |  SOLAR  | Annular
2033-04-14  |  LUNAR  | Penumbral
2033-09-09  |  LUNAR  | Partial
2033-09-23  |  SOLAR  | Annular
2034-03-06  |  LUNAR  | Partial
2034-03-19  |  SOLAR  | Total
2034-08-30  |  LUNAR  | Total
2034-09-13  |  SOLAR  | Partial
2035-02-08  |  SOLAR  | Partial
2035-02-23  |  LUNAR  | Total
2035-03-09  |  SOLAR  | Partial
2035-08-04  |  SOLAR  | Partial
2035-08-18  |  LUNAR  | Total
"""
