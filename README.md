# Truck Delivery Optimization

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

## Technical overview

- **Language**: Python 3  
- **Data Structures**: Hash Table, 2D Matrix (Adjacency Table)  
- **Algorithms**: Greedy Nearest-Neighbor  
- **Concepts**: Simulation, Scheduling, Graph Traversal, Command Line Interface  

---

## Project Structure
.
├── main.py # Main execution logic and simulation
├── truck.py # Truck class for delivery simulation
├── package.py # Package class with delivery metadata
├── hash.py # Custom HashTable implementation
├── Resources/
│ ├── distances.csv # Symmetric distance matrix between delivery addresses
│ └── packages.csv # Package delivery metadata

## How It Works

1. **Hash Packages**: Loads all package data into a custom hash table  
2. **Distance Matrix**: Builds a 2D array from CSV data for efficient lookups  
3. **Load Trucks**: Packages loaded based on zip code and delivery constraints  
4. **Deliver**:
   - First package delivered based on earliest deadline  
   - Remaining packages delivered using nearest-neighbor logic  
5. **Return to Hub**: Each truck returns to the hub after completing delivery  
