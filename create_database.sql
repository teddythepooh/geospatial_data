create database geospatial_analysis;
\c geospatial_analysis

\i src/create_dictionaries.sql
\i src/estimate_neighborhood_statistics.sql
\i src/clean_crimes_data.sql