import math 

def belleville_material_select(material: str) -> dict:  
    """Returns material properties in PSI"""
    if material == 'Phosphor Bronze':
        v = 0.2
        Ed = 15000000  # psi
        Es = 15000000  # psi
    elif material == '17-7 PH':
        v = 0.34
        Ed = 23000000  # psi
        Es = 29000000  # psi
    elif material == '302 Stainless':
        v = 0.3
        Ed = 28000000  # psi
        Es = 28000000  # psi
    elif material == 'BeCu 172':
        v = 0.33
        Ed = 18500000  # psi
        Es = 21000000  # psi
    elif material == 'Inconel':
        v = 0.29
        Ed = 31000000  # psi
        Es = 31000000  # psi
    elif material == 'Inconel X':
        v = 0.29
        Ed = 31000000  # psi
        Es = 31000000  # psi
    else:
        raise ValueError("Material not recognized")
    return {'v': v, 'Ed': Ed, 'Es': Es}

def calculator(slotted: bool, belleville_material: str, OD: float, ID: float, t: float, 
               Htratio: float, Stroke: float, RHd: float, HCd: float, dt_mult: float,
               N_Par: int, N_Ser: int) -> dict:
    """
    Belleville Spring Calculator
    All inputs in INCHES - All outputs in INCHES, LBF, DEGREES, PSI
    """
    
    belleville_props = belleville_material_select(belleville_material)
    v = belleville_props['v']
    Ed = belleville_props['Ed']  # in psi
    Es = belleville_props['Es']  # in psi

    # Handle non-slotted case
    if not slotted:
        RHd = 1.0
        HCd = ID
        dt_mult = 1.0

    # ===== CALCULATIONS (all in INCHES) =====
    
    # Basic geometry
    dt = dt_mult * RHd + HCd
    LR = (OD - ID) / (OD - dt)
    alpha_rad = math.atan(Htratio * t / ((OD - dt) / 2))
    alpha_deg = math.degrees(alpha_rad)
    a = OD / dt
    Z = (Htratio ** 2 - 2) / 3
    ln_a = math.log(a)
    
    # Stress coefficients
    C0 = math.pi * ln_a / 6 * (a / (a - 1)) ** 2
    C2 = 6 / (math.pi * ln_a) * ((a - 1) / ln_a - 1)
    C3 = 3 * (a - 1) / (math.pi * ln_a)
    C4 = 6 / (math.pi * ln_a) * (1 - ((a - 1) / (a * ln_a)))
    C5 = 6 / (math.pi * ln_a) * ((a - 1) / (2 * a))
    
    # Material correction factors
    k = 1 / (1 - v ** 2)
    M = OD / 2 / t
    
    # Dimensional parameters
    if slotted:
        S_W = RHd / 2
        num_holes = math.pi * ID / S_W / 4
    else:
        S_W = 0
        num_holes = 0
    
    # Spring performance - forces (in lbf)
    Coeff = C0 * k * Ed * t ** 4 / (OD / 2) ** 2
    
    C1H = Htratio + Z ** 1.5
    F_hi = Coeff * C1H / LR
    d_hi = (Htratio - math.sqrt(Z)) * t * LR
    
    C1M = Htratio
    F_mid = Coeff * C1M / LR
    d_mid = Htratio * t * LR
    
    C1L = Htratio - Z ** 1.5
    F_lo = Coeff * C1L / LR
    d_lo = (Htratio + math.sqrt(Z)) * t * LR
    
    # Deflection
    d_hi_lo = d_lo - d_hi
    dmax = 2 * d_hi_lo
    usable_stroke = (d_lo - d_mid) / 2 + (d_mid - d_hi) / 2
    Rate = -1.375 * C0 * k * Ed * t ** 3 / ((OD / 2) ** 2 * LR ** 2) * Z
    
    # Stresses (in psi)
    Sa_max = C0 * k * Es / M ** 2 * (C2 / 2 * (Htratio + C3 / C2) ** 2)
    Sb_max = C0 * k * Es / M ** 2 * (C2 / 2 * (Htratio - C3 / C2) ** 2)
    Sc_max = -C0 * k * Es / M ** 2 * (C4 / 2 * (Htratio + C5 / C4) ** 2)
    
    # Geometry for drawing
    Free_Height = Htratio * t * LR + t
    Deflection_from_FH = d_mid - Stroke / 2
    Starting_BV_Angle = math.degrees(
        math.atan(((Free_Height - Deflection_from_FH - t) / LR) / ((OD - dt) / 2))
    )
    D_effective = math.sqrt(1 / 3 * (OD ** 2 + ID ** 2 + OD * ID))
    A_effective = math.pi / 4 * D_effective ** 2
    
    # Stack performance
    Total_Springs = N_Par * N_Ser
    F_hi_parallel = F_hi * N_Par
    d_hi_series = d_hi * N_Ser
    F_mid_parallel = F_mid * N_Par
    d_mid_series = d_mid * N_Ser
    F_lo_parallel = F_lo * N_Par
    d_lo_series = d_lo * N_Ser
    d_hi_lo_series = d_hi_lo * N_Ser
    
    return {
        'dt': dt,
        'LR': LR,
        'alpha_rad': alpha_rad,
        'alpha': alpha_deg,
        'a': a,
        'Z': Z,
        'C0': C0,
        'C2': C2,
        'C3': C3,
        'C4': C4,
        'C5': C5,
        'k': k,
        'M': M,
        'S_W': S_W,
        'num_holes': num_holes,
        'Coeff': Coeff,
        'C1H': C1H,
        'F_hi': F_hi,
        'd_hi': d_hi,
        'C1M': C1M,
        'F_mid': F_mid,
        'd_mid': d_mid,
        'C1L': C1L,
        'F_lo': F_lo,
        'd_lo': d_lo,
        'd_hi_lo': d_hi_lo,
        'dmax': dmax,
        'usable_stroke': usable_stroke,
        'Rate': abs(Rate),
        'Sa_max': Sa_max,
        'Sb_max': Sb_max,
        'Sc_max': Sc_max,
        'Free_Height': Free_Height,
        'Deflection_from_FH': Deflection_from_FH,
        'Starting_BV_Angle': Starting_BV_Angle,
        'D_effective': D_effective,
        'A_effective': A_effective,
        'Total_Springs': Total_Springs,
        'F_hi_parallel': F_hi_parallel,
        'd_hi_series': d_hi_series,
        'F_mid_parallel': F_mid_parallel,
        'd_mid_series': d_mid_series,
        'F_lo_parallel': F_lo_parallel,
        'd_lo_series': d_lo_series,
        'd_hi_lo_series': d_hi_lo_series,
    }


def main():
    """Interactive command-line interface for Belleville Spring Calculator"""
    print("\n" + "="*70)
    print("BELLEVILLE SPRING CALCULATOR")
    print("(All inputs in INCHES | Results in INCHES, LBF, DEGREES, PSI)")
    print("="*70 + "\n")
    
    # Belleville Spring Inputs
    print("--- BELLEVILLE SPRING GEOMETRY ---")
    print("\nAvailable materials: Phosphor Bronze, 17-7 PH, 302 Stainless, BeCu 172, Inconel, Inconel X")
    belleville_material = input("Belleville Material: ").strip()
    
    OD = float(input("Outer Diameter (in): "))
    ID = float(input("Inner Diameter (in): "))
    t = float(input("Thickness (in): "))
    Htratio = float(input("Height to Thickness Ratio (H/t): "))
    Stroke = float(input("Desired Stroke (in): "))
    
    # Get slotted input with validation
    while True:
        print("\nSlotted spring? (Yes/No): ", end="")
        slotted_input = input().strip().lower()
        if slotted_input in ['yes', 'y', 'no', 'n']:
            slotted = slotted_input in ['yes', 'y']
            break
        else:
            print("Invalid input. Please enter 'Yes' or 'No'.")
    
    if slotted:
        RHd = float(input("Relief Hole Diameter (in): "))
        HCd = float(input("Slot Diameter (in): "))
        dt_mult = float(input("DT Multiplier: "))
    else:
        RHd = 0.0
        HCd = 0.0
        dt_mult = 0.0
    
    # Stack Configuration
    print("\n--- STACK CONFIGURATION ---")
    N_Par = int(input("Springs in Parallel: "))
    N_Ser = int(input("Springs in Series: "))
    
    # Run calculation
    try:
        results = calculator(
            slotted=slotted,
            belleville_material=belleville_material,
            OD=OD,
            ID=ID,
            t=t,
            Htratio=Htratio,
            Stroke=Stroke,
            RHd=RHd if slotted else 1.0,
            HCd=HCd if slotted else 0.0,
            dt_mult=dt_mult if slotted else 0.0,
            N_Par=N_Par,
            N_Ser=N_Ser
        )
        
        # Display Results
        print("\n" + "="*70)
        print("CALCULATION RESULTS")
        print("="*70 + "\n")
        
        print("--- BASIC PARAMETERS ---")
        print(f"dt: {results['dt']:.6f} in")
        print(f"LR: {results['LR']:.6f}")
        print(f"Alpha (rad): {results['alpha_rad']:.6f}")
        print(f"Alpha (°): {results['alpha']:.6f}")
        print(f"a (OD/dt): {results['a']:.6f}")
        print(f"Z: {results['Z']:.6f}")
        
        print("\n--- SPRING PERFORMANCE - FORCES ---")
        print(f"F_hi: {results['F_hi']:.6f} lbf")
        print(f"F_mid: {results['F_mid']:.6f} lbf")
        print(f"F_lo: {results['F_lo']:.6f} lbf")
        
        print("\n--- SPRING PERFORMANCE - DEFLECTIONS ---")
        print(f"d_hi: {results['d_hi']:.6f} in")
        print(f"d_mid: {results['d_mid']:.6f} in")
        print(f"d_lo: {results['d_lo']:.6f} in")
        print(f"d_hi_lo: {results['d_hi_lo']:.6f} in")
        print(f"dmax: {results['dmax']:.6f} in")
        print(f"Usable Stroke: {results['usable_stroke']:.6f} in")
        print(f"Spring Rate: {results['Rate']:.6f} lbf/in")
        
        print("\n--- STRESS ANALYSIS ---")
        print(f"Sa_max: {results['Sa_max']:.6f} psi")
        print(f"Sb_max: {results['Sb_max']:.6f} psi")
        print(f"Sc_max: {results['Sc_max']:.6f} psi")
        
        print("\n--- GEOMETRY FOR DRAWING ---")
        print(f"Free Height: {results['Free_Height']:.6f} in")
        print(f"Deflection from FH: {results['Deflection_from_FH']:.6f} in")
        print(f"Starting BV Angle: {results['Starting_BV_Angle']:.6f}°")
        print(f"D_effective: {results['D_effective']:.6f} in")
        print(f"A_effective: {results['A_effective']:.6f} in²")
        
        print("\n--- STACK PERFORMANCE ---")
        print(f"Total Springs: {results['Total_Springs']}")
        print(f"F_hi (Parallel): {results['F_hi_parallel']:.6f} lbf")
        print(f"d_hi (Series): {results['d_hi_series']:.6f} in")
        print(f"F_mid (Parallel): {results['F_mid_parallel']:.6f} lbf")
        print(f"d_mid (Series): {results['d_mid_series']:.6f} in")
        print(f"F_lo (Parallel): {results['F_lo_parallel']:.6f} lbf")
        print(f"d_lo (Series): {results['d_lo_series']:.6f} in")
        print(f"d_hi_lo (Series): {results['d_hi_lo_series']:.6f} in")
        
        print("\n--- COEFFICIENTS & FACTORS ---")
        print(f"C0: {results['C0']:.6f}")
        print(f"C2: {results['C2']:.6f}")
        print(f"C3: {results['C3']:.6f}")
        print(f"C4: {results['C4']:.6f}")
        print(f"C5: {results['C5']:.6f}")
        print(f"k: {results['k']:.6f}")
        print(f"M: {results['M']:.6f}")
        print(f"Coeff: {results['Coeff']:.6f} lbf/in")
        print(f"S_W: {results['S_W']:.6f} in")
        
        if slotted:
            num_holes = results['num_holes']
            holes_status = "✓ GOOD" if num_holes >= 12 else "✗ BAD (< 12)"
            print(f"num_holes: {num_holes:.2f} {holes_status}")
        
        print(f"C1H: {results['C1H']:.6f}")
        print(f"C1M: {results['C1M']:.6f}")
        print(f"C1L: {results['C1L']:.6f}")
        
        print("\n" + "="*70)
        print("✓ Calculation completed successfully!")
        print("="*70 + "\n")
        
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")
        print("Please check your inputs and try again.\n")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()