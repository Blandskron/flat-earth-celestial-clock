![Image](https://m.media-amazon.com/images/I/61405s43vNL.jpg)
![Image](https://upload.wikimedia.org/wikipedia/commons/thumb/a/a6/Analemma_Earth.png/500px-Analemma_Earth.png)
![Image](https://www.simonhanmer52.ca/uploads/8/3/4/8/83482100/slide07_28_orig.jpg)
![Image](https://m.media-amazon.com/images/I/61NLn8W18OL._AC_UF894%2C1000_QL80_.jpg)

# Flat Earth Celestial Clock

**A geometric–temporal eclipse prediction model on a stationary flat Earth  
using analemma-based time geometry and UTC anchoring**

---

## Abstract

This repository presents a **deterministic celestial clock model** that represents the Earth as a **stationary plane** and the Sun and Moon as **local moving luminarias** governed by temporal geometry rather than orbital mechanics.

The purpose of this project is **not cosmological ontology**, but the construction of a **mathematically coherent predictive system** capable of determining **solar and lunar eclipses** through:

- harmonic solar analemma,
- synodic lunar phase synchronization,
- nodal temporal windows,
- and explicit UTC-based geodetic anchoring.

The system behaves as a **celestial chronograph**:  
a geometric clock in which **time determines form**, not the inverse.

---

## 1. Foundational Hypotheses

1. **Stationary Plane**  
   The Earth is modeled as a Euclidean disk.  
   No rotation, axial tilt, or translational motion is introduced.

2. **Local Luminarias**  
   The Sun and Moon follow circular trajectories above the plane, with **variable effective radius**.

3. **Time as the Primary Variable**  
   Spatial geometry is derived from UTC time.  
   There is no kinematic causality from space to time.

4. **Eclipses Without Terrestrial Shadow**  
   Eclipse detection is performed via **temporal–angular alignment** and **relative altitude geometry**, not via Earth-cast umbra.

These hypotheses define a **self-consistent mathematical framework**, evaluated solely by **predictive capability and internal stability**.

---

## 2. Planar Cartography and UTC Anchoring

The Earth is projected using an **azimuthal equidistant projection** centered on the pole of the plane.

Each geographic coordinate \((\lambda, \varphi)\) is mapped to polar coordinates:

- **Angular position**  
  \[
  \theta = -\lambda - \frac{\pi}{2}
  \]

- **Radial distance**  
  \[
  r = R \cdot \frac{90^\circ - \varphi}{180^\circ}
  \]

This preserves radial distance and allows the superposition of a **24-hour temporal dial**.

### UTC Geodetic Anchors

Fixed anchor points are used to validate temporal coherence:

- Santiago (UTC −3)
- London (UTC 0)
- Sydney (UTC +11)

These anchors are **references**, not calibration parameters.

---

## 3. System B – Reindexed Temporal Dial

Instead of raw UTC, the system employs a **symmetrically reindexed temporal dial (System B)**.

This bijective remapping:

- preserves 24-hour periodicity,
- removes discontinuities at the meridian,
- simplifies detection of angular opposition and conjunction.

System B is a **reading system**, not a time modification.

---

## 4. Solar Analemma as Relative Altitude (Z-Offset)

The solar analemma is modeled as a **harmonic function of annual phase**:

\[
Z_\odot(f) =
a_1 \sin(2\pi f) +
a_2 \sin(4\pi f) +
a_3 \sin(6\pi f)
\]

Where \(f\) is the fractional solar year.

- The fundamental term captures annual variation.
- Higher harmonics correct asymmetry.
- **Geometric meaning**:  
  \(Z_\odot\) modulates the **effective solar radius** above the plane.

This transforms the analemma from a descriptive artifact into an **active geometric parameter**.

---

## 5. Synodic Lunar Phase Synchronization

The synodic phase is defined as:

\[
\phi = \operatorname{frac}\!\left(\frac{t - t_{\text{ref}}}{M}\right)
\]

Where \(M\) is the synodic month.

- \(\phi \approx 0\): New Moon  
- \(\phi \approx 0.5\): Full Moon

In the planar model, the Moon’s angular separation from the Sun is **phase-determined**, not orbit-determined.

---

## 6. Nodal Seasons Without Orbital Inclination

Instead of tilted orbital planes, the model introduces an **effective draconic year** that defines **temporal nodal windows**:

\[
\psi = \operatorname{frac}\!\left(\frac{t - t_{\text{ref}}}{E}\right)
\]

Distance to node:

\[
d_{\text{node}} = \min(\psi,\;1-\psi,\;|\psi-0.5|)
\]

Only when \(d_{\text{node}}\) falls below a defined threshold can eclipses occur.

This **translates inclination into time**, preserving planar geometry.

---

## 7. Eclipse Detection Criteria

### Solar Eclipse

Conditions:

1. New Moon (\(\phi \approx 0\))
2. Within nodal season
3. Relative altitude geometry permits occultation

Classification by nodal proximity:

- Annular
- Total
- Partial

### Lunar Eclipse

Conditions:

1. Full Moon (\(\phi \approx 0.5\))
2. Within nodal season
3. Exact angular opposition

Classification:

- Total
- Partial
- Penumbral

> No Earth shadow is projected.  
> Lunar eclipses arise from **temporal–angular opposition modulated by analemma height**.

---

## 8. Temporal Refinement and Long Cycles

Detected events are locally refined to minimize nodal distance.

Long-term recurrence emerges naturally from the quasi-resonance of:

- Solar year
- Synodic month
- Draconic year

This reproduces **Saros-like behavior** without spatial precession.

---

## 9. Visualization as Scientific Instrument

The visual interface is **not illustrative** — it is **instrumental**.

- Planar map → geometric substrate
- Temporal dial → time-angle mapping
- Dynamic Sun & Moon → radius modulation by analemma
- Complication panels:
  - Solar analemma (Z-offset)
  - Synodic lunar phase

Together they form a **celestial clock**, where each element is a measurable variable.

---

## Conclusion

By reinterpreting the sky as a **precision time system**, this model demonstrates that eclipses can be described as **synchronization events** between harmonic cycles and planar geometry.

This repository presents a **Flat Earth Celestial Clock**:  
a deterministic mathematical machine where **time governs form**.

---

**Keywords**  
flat earth, analemma, synodic phase, draconic year, eclipses, temporal geometry, celestial clock
