# Timber Supply Chain and Inventory Management System

A multi-interface enterprise software solution designed to monitor, track, and manage lumber stock levels, raw material imports, and volume wastage (mermas) for timber distribution facilities. The ecosystem relies on a single relational SQLite database backend serving three distinct consumer layers: a core headless logic CLI, a local desktop administration GUI, and a data analytics web dashboard.

## System Architecture & Components

The project is structured into three independent tiers sharing a normalized data layer:

1. **Core Database and CLI Engine (`maderera.py`):** Manages the local SQLite initialization and handles low-level transactional queries. It enforces referential integrity between the physical stock (`inventario`) and structural losses (`mermas`). Features a multi-option Command Line Interface for direct system interaction.

2. **Desktop Management GUI (`app_visual.py`):** Built using Tkinter and advanced asynchronous `Treeview` styling components. This administrative client allows warehouse operators to visually audit stock levels, input imports through structured forms, select specific batches via graphical point-and-click to trigger stock deduction operations, and view dynamic logs.

3. **Analytics Web Dashboard (`app_web.py`):** A responsive web application built with Streamlit and Pandas. It queries the shared transactional database engine, converting structural logs into business intelligence. Features real-time stock matrix views, historical dataframes, and analytical bar-chart components tracking aggregated volumetric waste causes.

## Database Schema Structure

The storage layer relies on two relational tables with active constraints:
* **inventario:** Tracks standard product metrics including structural material identifiers (`tipo_madera`), volumetric quantity measurements in cubic meters (`metros_cubicos`), and market currency evaluations per unit (`precio_por_m3`).
* **mermas:** A transactional ledger tracking operational losses. Includes a cascading reference foreign key linking back to the source inventory ID, dynamic volumetric deduction tracks (`cantidad_perdida`), text-based operational causal variables, and auto-generated ISO timestamps.

## Operational Features & Data Integrity Rules
* **Safe Volumetric Update Pipelines:** The deduction algorithms perform programmatic database validation blocks (`SELECT`) prior to writing entry commits. If a requested wastage volume surpasses current batch records, transaction queries automatically abort, avoiding negative inventories.
* **Cascading Purge Procedures:** The deletion functions safely drop records from the asset table while clearing interconnected structural dependency IDs inside ledger history files.
* **Relational Multi-Table Joins:** The analytical web engine utilizes explicitly defined inner relational constraints (`INNER JOIN`) to map abstract indexing keys to human-readable dataset targets dynamically.

## Installation and Execution Guide

### Prerequisites
Ensure Python 3.8+ is installed on your environment. Install the necessary analytics dependencies via pip:
```bash
pip install streamlit pandas

### Running the Components
To launch the Command Line Interface utility:
```bash
python maderera.py

To run the administrative desktop application interface:
```bash
python app_visual.py

To deploy the web dashboard instance locally:
```bash
streamlit run app_web.py
