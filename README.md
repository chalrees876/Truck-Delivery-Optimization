# 📦 WGUPS Truck Delivery Optimization

A Python-based package delivery routing system designed for the Western Governors University Parcel Service (WGUPS). This program uses a greedy nearest-neighbor algorithm and custom hash table to optimize delivery efficiency, minimize mileage, and meet time-sensitive delivery constraints.


## Features

- **Optimized Routing**: Greedy `O(n³)` algorithm to minimize truck mileage  
- **Custom Hash Table**: Constant-time `O(1)` lookups for 40+ packages  
- **CSV Parsing**: Converts address and distance data into a 2D matrix (`O(n²)` space)  
- **Time Tracking**: Simulates real-time delivery, truck return trips, and package status by user-defined time  
- **Constraint Handling**:
  - Delayed packages
  - Grouped deliveries
  - Truck-specific assignments

---

## 🛠️ Technologies

- **Language**: Python 3  
- **Data Structures**: Hash Table, 2D Matrix (Adjacency Table)  
- **Algorithms**: Greedy Nearest-Neighbor  
- **Concepts**: Simulation, Scheduling, Graph Traversal, Command Line Interface  

---

## 📂 Project Structure
