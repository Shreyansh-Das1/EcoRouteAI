# EcoRoute AI

EcoRoute AI is a full-stack geospatial routing application designed for automated transmission line corridor planning. By utilizing fused geospatial layers—specifically digital elevation models and land-use/land-cover (LULC) data—the system generates a weighted cost surface to compute optimal, macro-engineered paths that minimize both environmental impact and construction expenditure.

---

## Project Overview

The core objective of EcoRoute AI is to automate the extraction of an optimal corridor path between two geographic points. The pipeline transforms a multi-layered environmental raster grid into a localized 4-connected graph network, allowing graph traversal algorithms to route around real-world obstacles like steep slopes, water bodies, and heavily urbanized areas.

### Key Technical Specs

* **Total Graph Nodes:** ~3.24 million pixels 
* **Total Graph Edges:** ~6.47 million edges 
* **Graph Footprint:** 361 MB serialized on disk 
---
## System Architecture & Routing Process

The routing mechanism handles data seamlessly between geographic space and graph coordinate space:

```
[Frontend Input] ➔ [Backend Transformation] ➔ [Node Mapping] ➔ [Routing Engine] ➔ [Path Conversion] ➔ [Frontend Rendering]

```

1. **Frontend Input:** The user interacts with the map interface to select coordinate-based start and end points.

2. **Backend Transformation:** Geodetic coordinates are mapped into raw pixel space coordinates based on the dataset's CRS.

3. **Node Mapping:** The backend identifies the nearest matching graph nodes corresponding to those pixel space positions.

4. **Routing Engine:** An optimized $A^*$ search or Dijkstra algorithm computes the path over the cost grid matrix.

5. **Path Conversion:** The node-based pixel path is transformed back into geospatial vector geometry.

6. **Frontend Rendering:** The optimized corridor is overlaid as a vector layer on the map UI.


---

## Dataset & Pre-processing

To avoid discrepancies caused by temporal vegetation changes, the pipeline utilizes historical datasets to ensure alignment across features.

* **Digital Elevation Model (DEM):** Copernicus DEM GLO-30 provides a base structural resolution of $30\text{m} \times 30\text{m}$.

* **LULC Labels:** ESA WorldCover 2021 labels are fetched from TerraScope.

* **Coordinate Reference System (CRS):** All data layers are reprojected, aligned, and tightly cropped to the target Area of Interest (AOI) bounding box using `EPSG:32645` (WGS 84 / UTM zone 45N).


### Feature Extraction

* **Slope Generation:** Terrain slope gradients are mathematically computed in degrees by applying the Pythagorean theorem across the spatial resolution step against the elevation variations from the DEM (`arctan` over the directional gradient).

* **Label Mapping:** Raw ESA WorldCover classes are re-indexed to localized integer IDs for lightweight matrix manipulations: `{10:1, 20:2, 30:3, 40:4, 50:5, 60:6, 80:7, 90:8}`.

---

## Cost Surface Modeling

The final traversal cost base map is generated using a weighted integration of environmental classification (60%) and land slope characteristics (40%). Values range from highly favorable (1) to extreme friction (10), while strict geographic barriers are designated as **Impassable (9999)**.

LULC Cost Metrics (60% Weight) 

| LULC Class | Cost Rating | Engineering & Environmental Rationale |
| --- | --- | --- |
| **50. Barren Land / Wasteland** | 1 | Ideal Path: Flat, open terrain; minimal environmental impact and low preparation costs.

 |
| **20. Shrubland / 30. Grassland** | 2 | Highly Favorable: Low-lying vegetation requires minimal clearing without canopy interference.

 |
| **40. Agricultural / Cropland** | 5 | Moderate Friction: High land acquisition, crop compensation costs, and harvest cycle dependencies.

 |
| **10. Dense Forest / Vegetation** | 8 | High Friction: Demands heavy tree felling, strict environmental clearances, and long-term right-of-way (ROW) maintenance.

 |
| **60. Built-up / Urban Area** | 10 | Extreme Friction: Tremens land costs, safety hazards, high legal hurdles, and community resistance.

 |
| **Water Bodies** | **9999** | <br>**Exclusion Zone:** Constructing towers in deep water is structurally unfeasible and cost-prohibitive.

 |

Slope Cost Metrics (40% Weight) 

| Slope (Degrees) | Cost Rating |
| --- | --- |
| $\le 5^\circ$ | 1 

 |
| $\le 10^\circ$ | 3 

 |
| $\le 15^\circ$ | 6 

 |
| $\le 25^\circ$ | 9 

 |
| $> 25^\circ$ | <br>**9999 (Impassable)** 

 |

---

## Graph Network & Performance Benchmarks

The aligned cost raster matrix is mapped directly into a NetworkX graph workspace where individual pixels function as nodes connected via a 4-neighbor layout. The weights assigned to edges are evaluated as the average cell cost between the two adjacent nodes.

### Routing Performance Summary

* **Dijkstra's Algorithm:** Blatantly explores uniformly in all directions. It handles heavily constrained environments with numerous dense "9999" barriers effectively, preventing heuristic misdirection.

* **$A^*$ Search (Manhattan Distance):** Introduces a directional search pattern towards the goal. On clear, less restricted corridors, it achieves a ~28.5% reduction in search time compared to Dijkstra.

---

## System Requirements

Due to the size of the uncompressed raster-derived network graphs, the following hardware thresholds must be observed:

* **RAM (Minimum):** **6 GB** (The compressed, serialized `.gpickle` graph environment requires approximately 5.2 GB of system memory to load into the active workspace, peaking around 7 GB during scratch generation).

* **Disk Storage:** ~400 MB allocated space for graph binaries and geospatial layers.


* 
**Geospatial Engine Requirements:** `GDAL` binary dependencies must be installed on the host machine to support high-performance spatial abstraction wrappers like `rasterio`.
