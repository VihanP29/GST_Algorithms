# Algorithmic Detection of Circular Trading Fraud

An interactive web application that implements and visualizes algorithms from the research paper, "An Algorithmic Approach to Handle Circular Trading in Commercial Taxation System," to detect and eliminate fraudulent transaction cycles.

---

## Project Description

Circular trading is a method of tax evasion where a group of businesses create fictitious transactions among themselves to inflate sales, hide malicious purchases, and fraudulently claim tax credits. These schemes create cycles in the transaction network that are difficult to detect manually in large datasets.

This project provides an interactive tool to combat this issue. It models transaction data as a directed graph and applies a specialized Weighted Cycle Deletion (WCD) algorithm to identify and surgically remove the most likely fraudulent cycles. The result is a "cleaned" transaction graph, revealing the underlying flow of legitimate business activities for auditors.

---

## Key Features

* **Interactive Web Interface**: Built with Streamlit for a user-friendly and responsive experience.
* **Advanced Graph Visualization**: Uses Pyvis and NetworkX to render "before" and "after" views of the transaction network.
* **Cycle Detection & Analysis**: Automatically identifies all cycles in the initial dataset and lists the participating entities.
* **Fraudulent Transaction Reporting**: After processing, the app explicitly lists the specific transactions that were identified as fraudulent and removed from the network.
* **Flexible Data Input**: Supports analysis on pre-loaded sample datasets of varying sizes (50, 100, 500 transactions) or user-uploaded CSV files.

---

## Live Demo & Screenshots

Below is a demonstration of the application's core functionality: selecting a dataset, viewing the initial cyclic graph, running the analysis, and observing the resulting acyclic graph along with the identified fraudulent transactions.



---

## Technical Stack

* **Backend & Logic**: Python
* **Web Framework**: Streamlit
* **Data Manipulation**: Pandas
* **Graph Modeling**: NetworkX
* **Interactive Visualization**: Pyvis

---

## Installation & Usage

To run this application locally, please follow these steps:

**1. Prerequisites**
* Python 3.8+
* `pip` package manager

**2. Clone the Repository**
```bash
git clone [https://github.com/your-username/your-repository-name.git](https://github.com/your-username/your-repository-name.git)
cd your-repository-name
