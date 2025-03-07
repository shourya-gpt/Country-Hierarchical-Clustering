# Hierarchical Clustering of Socioeconomic Data
This project implements hierarchical agglomerative clustering (HAC) on real-world socioeconomic data from various countries. Each country is represented as a 9-dimensional feature vector derived from key economic and social indicators, including GDP per capita, child mortality, and life expectancy.

# Features:
1. Data Processing: Load and normalize country-level socioeconomic data.
2. Feature Extraction: Convert raw data into numerical feature vectors.
3. Hierarchical Clustering: Implement complete-linkage clustering using Euclidean distance.
4. Visualization: Generate dendrograms to illustrate clustering results.
5. 
This implementation strictly avoids the use of scipy.cluster.hierarchy.linkage() and is built using Python with numpy, scipy, and matplotlib.
