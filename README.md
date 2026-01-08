# Belleville Springs Design Calculator

A comprehensive web application for designing and analyzing Belleville springs (disc springs) specifically for pressure regulator applications.

## Overview

Belleville springs, also known as disc springs or conical spring washers, are widely used in pressure regulators due to their ability to provide high load capacity in a compact space with predictable force-deflection characteristics. This calculator helps engineers design optimal spring configurations for pressure regulator applications.

## Features

- **Interactive Web Interface**: User-friendly form-based design interface
- **Comprehensive Calculations**: 
  - Spring rate calculations using Almen-Laszlo formulas
  - Load and deflection analysis
  - Stress analysis with safety factor calculations
  - Stack configuration support (single, series, parallel)
- **Helical Spring Combination**: Option to combine Belleville and helical springs in series for enhanced performance
- **Graphical Analysis**:
  - Force vs Displacement plots showing spring behavior
  - Stress vs Displacement plots with yield strength limits
  - Support for comparing Belleville, helical, and combined configurations
- **Material Presets**: Pre-configured properties for common materials:
  - Spring Steel (E=30 Mpsi)
  - Stainless Steel (E=28 Mpsi)
  - Bronze (E=16 Mpsi)
  - Custom material support
- **Pressure Regulator Specific Guidance**: Recommendations tailored for pressure regulator applications
- **Real-time Results**: Instant calculation and visualization of design parameters
- **Design Recommendations**: Automated suggestions for optimizing spring design
- **Reference Implementation**: Based on Belleville Spring Design Guide.pdf and Belleville_Springs.py

## How to Use

### Quick Start

1. Open `index.html` in any modern web browser
2. Fill in the spring geometry parameters
3. Select material properties
4. Enter loading requirements for your pressure regulator
5. Click "Calculate Design" to see results

### Input Parameters

#### 1. Spring Geometry
- **Outer Diameter (De)**: Outside diameter of the disc spring in inches
- **Inner Diameter (Di)**: Inside diameter of the disc spring in inches
- **Material Thickness (t)**: Thickness of the material in inches
- **Free Height (h₀)**: Cone height at no load in inches

#### 2. Material Properties
- **Material Type**: Select from preset materials or use custom
- **Young's Modulus (E)**: Elastic modulus in psi
- **Poisson's Ratio (ν)**: Typically 0.3 for steel materials
- **Yield Strength**: Material yield strength in psi

#### 3. Loading Requirements
- **Required Load (F)**: Operating load needed in pounds-force (lbf)
- **Required Deflection (s)**: Required deflection in inches
- **Regulator Pressure**: Operating pressure in psi
- **Stack Configuration**: Choose single, series, or parallel configuration
- **Number of Springs**: Number of springs in the stack
- **Include Helical Spring**: Optional checkbox to add a helical spring in series with the Belleville spring
  - **Wire Diameter (d)**: Diameter of the helical spring wire in inches
  - **Mean Coil Diameter (D)**: Mean diameter of the helical coil in inches
  - **Active Coils (Na)**: Number of active coils
  - **Shear Modulus (G)**: Shear modulus in psi (default 11.5 Mpsi for steel)

### Understanding Results

The calculator provides:

1. **Spring Rate (lbf/in)**: Stiffness of the spring (combined if helical is included)
2. **Load at Deflection (lbf)**: Actual load at the specified deflection
3. **Maximum Stress (psi)**: Peak stress in the Belleville spring material
4. **Safety Factor**: Ratio of yield strength to actual stress (≥1.5 recommended)
5. **Deflection Ratio (%)**: Percentage of cone height (should be <75%)
6. **Stack Load (lbf)**: Total load considering stack configuration
7. **Force vs Displacement Plot**: Interactive chart showing force curves for Belleville, helical (if included), and combined configurations
8. **Stress vs Displacement Plot**: Interactive chart showing stress buildup with yield strength limit

### Design Guidelines

#### Safety Factors
- **< 1.5**: Not recommended - increase thickness or change material
- **1.5 - 2.5**: Acceptable for most pressure regulator applications
- **> 2.5**: Conservative design with high reliability

#### Deflection Limits
- Maximum deflection should not exceed 75% of the free cone height
- Exceeding this limit risks permanent deformation

#### Diameter Ratios
- Optimal De/Di ratio: 1.5 to 3.0
- Ratios outside this range may have suboptimal performance

#### Stack Configurations
- **Series (Same Direction)**: Increases total deflection, maintains load
- **Parallel (Opposite Direction)**: Increases total load, maintains deflection
- **Single**: Individual spring performance

#### Combined Spring Systems
When a helical spring is combined with a Belleville spring in series:
- The combined spring rate is calculated as: 1/k_combined = 1/k_belleville + 1/k_helical
- This configuration provides more linear force-deflection characteristics
- Useful for applications requiring vibration damping
- The helical spring adds compliance while the Belleville maintains high load capacity

## Technical Background

### Calculation Methodology

The calculator uses the Almen-Laszlo formulas for Belleville spring calculations:

**Spring Rate:**
```
k = (4 * E * t⁴) / (K₁ * (1 - ν²) * De²)
```

**Load:**
```
F = k * s
```

**Stress:**
```
σ = (4 * E * t² * s) / (M * (1 - ν²) * De²)
```

Where:
- E = Young's modulus
- t = Material thickness
- ν = Poisson's ratio
- De = Outer diameter
- s = Deflection
- K₁, M = Constants based on diameter ratio

### Pressure Regulator Applications

Belleville springs in pressure regulators:
- Provide consistent force over deflection range
- Enable precise pressure control
- Offer compact design
- Handle cyclic loading effectively
- Can be stacked for custom force curves

## Example Use Case

**Design Scenario**: Pressure regulator for 1500 psi operating pressure

**Inputs:**
- Outer Diameter: 2.0 in
- Inner Diameter: 1.0 in
- Thickness: 0.08 in
- Free Height: 0.12 in
- Material: Spring Steel (E=30 Mpsi, Yield=203 ksi)
- Required Load: 110 lbf
- Required Deflection: 0.06 in
- Stack: Single spring

**Expected Results:**
- Spring rate: ~1850 lbf/in
- Load at deflection: ~110 lbf
- Maximum stress: ~115 ksi
- Safety factor: ~1.75 ✓
- Deflection ratio: 50% ✓

## Browser Compatibility

This application works in all modern browsers:
- Chrome (recommended)
- Firefox
- Safari
- Edge

No server or installation required - runs entirely in the browser.

## Limitations and Disclaimers

⚠️ **Important Notes:**
- This calculator is for engineering guidance only
- Always verify calculations independently
- Consult relevant standards (DIN 2092, ISO 19690)
- Consider additional factors: fatigue, temperature, environment
- Professional engineering review recommended for critical applications

## Contributing

This is an open-source educational tool. Improvements and contributions are welcome.

## License

This project is provided as-is for educational and engineering guidance purposes.

## References

- DIN 2092: Disc springs - Calculation
- ISO 19690: Disc springs - Quality specifications
- Almen, J. O., & Laszlo, A. (1936). "The Uniform-Section Disk Spring"
- Spring Manufacturers Institute guidelines
- **Belleville Spring Design Guide.pdf**: Comprehensive design reference (included in repository)
- **Belleville_Springs.py**: Python implementation of calculator formulas (included in repository)

---

**Version**: 1.0  
**Last Updated**: January 2025