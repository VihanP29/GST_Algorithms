# GST_Algorithms
GST Algorithm for Detecting Circular Trading
An interactive web application that implements and visualizes algorithms from the research paper, "An Algorithmic Approach to Handle Circular Trading in Commercial Taxation System," to detect and eliminate fraudulent transaction cycles. 

📜 Project Description
Circular trading is a method of tax evasion where a group of businesses create fictitious transactions among themselves to inflate sales, hide malicious purchases, and fraudulently claim tax credits.  These schemes create cycles in the transaction network that are difficult to detect manually in large datasets.


This project provides an interactive tool to combat this issue. It models transaction data as a directed graph and applies a specialized Weighted Cycle Deletion (WCD) algorithm to identify and surgically remove the most likely fraudulent cycles.  The result is a "cleaned" transaction graph, revealing the underlying flow of legitimate business activities for auditors.


✨ Key Features
Interactive Web Interface: Built with Streamlit for a user-friendly and responsive experience.

Advanced Graph Visualization: Uses Pyvis and NetworkX to render "before" and "after" views of the transaction network.

Cycle Detection & Analysis: Automatically identifies all cycles in the initial dataset and lists the participating entities.

Fraudulent Transaction Reporting: After processing, the app explicitly lists the specific transactions that were identified as fraudulent and removed from the network.

Flexible Data Input: Supports analysis on pre-loaded sample datasets of varying sizes (50, 100, 500 transactions) or user-uploaded CSV files.

🚀 Live Demo & Screenshots
Below is a demonstration of the application's core functionality: selecting a dataset, viewing the initial cyclic graph, running the analysis, and observing the resulting acyclic graph along with the identified fraudulent transactions.

🛠️ Technical Stack
Backend & Logic: Python

Web Framework: Streamlit

Data Manipulation: Pandas

Graph Modeling: NetworkX

Interactive Visualization: Pyvis

⚙️ Installation & Usage
To run this application locally, please follow these steps:

1. Prerequisites

Python 3.8+

pip package manager

2. Clone the Repository

Bash

git clone https://github.com/your-username/your-repository-name.git
cd your-repository-name
3. Set Up a Virtual Environment (Recommended)

Bash

# For Windows
python -m venv venv
venv\Scripts\activate

# For macOS/Linux
python3 -m venv venv
source venv/bin/activate
4. Install Dependencies
Create a requirements.txt file with the following content:

streamlit
pandas
networkx
pyvis
Then, run the installation command:

Bash

pip install -r requirements.txt
5. Run the Streamlit Application

Bash

streamlit run app.py
The application should now be running and accessible in your web browser.

📂 Project Structure
The repository is organized as follows:

.
├── 📄 app.py                  # Main Streamlit application file (UI and workflow)
├── 📄 wcd.py                   # Implements the main Weighted Cycle Deletion algorithm (Algorithm 1)
├── 📄 delete_cycles.py        # Implements the cycle removal logic (Algorithm 2)
├── 📄 maxflow.py              # Implements the Max-Flow Path logic (Algorithm 3)
├── 📄 standard_functions.py   # Utility functions (DFS cycle check, priority queue, etc.)
├── 📁 data/
│   ├── 📄 sample_small.csv    # 50-transaction sample dataset
│   ├── 📄 sample_medium.csv   # 100-transaction sample dataset
│   └── 📄 sample_large.csv    # 500-transaction sample dataset
└── 📄 requirements.txt        # Python package dependencies
🔬 The Algorithm Explained
The core of this project is the three-part algorithm designed to intelligently remove cycles from the transaction graph. 

MAX_MIN (The Path Finder): This is the foundational component. When a cycle is formed, this algorithm finds the most robust path within that cycle. It identifies the path where the "weakest link" (the transaction with the minimum value) is as high as possible. 



DELETE_CYCLE (The Cycle Surgeon): This algorithm is invoked when a new transaction creates a cycle. It uses 

MAX_MIN to analyze the newly formed cycle and calculates its Flow Value—the difference between the highest and lowest transaction values. Cycles with a very low Flow Value are considered suspicious because they indicate that little to no real economic value was added, which is a key characteristic of circular trading. 




WCD - Weighted Cycle Deletion (The Orchestrator): This is the main driver that processes all transactions chronologically.  It builds the graph one transaction at a time. Whenever a new transaction closes a loop and forms a cycle, 

WCD immediately calls DELETE_CYCLE to analyze and remove it before proceeding to the next transaction. 

This structured approach ensures that fraudulent cycles are removed as soon as they appear, resulting in a final Directed Acyclic Graph (DAG) that represents legitimate commerce.

🙏 Acknowledgments
This project is an implementation of the concepts and algorithms presented in the following research paper:

Mathews, J., Mehta, P., Babu, C. S., & Rao, S. V. K. V. (2018). An Algorithmic Approach to Handle Circular Trading in Commercial Taxation System. 

2018 IEEE 3rd International Conference on Big Data Analysis (ICBDA).
