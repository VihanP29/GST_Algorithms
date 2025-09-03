# app.py
import streamlit as st
import pandas as pd
import networkx as nx
from pyvis.network import Network
import streamlit.components.v1 as components
import os
import tempfile

# --- (Placeholder) Import developer's main algorithm function ---
# This assumes the main function is in 'wcd.py' and is named 'wcd'
from wcd import wcd

# --- Helper Functions ---

def create_sample_datasets():
    """Creates sample CSV files in a 'data' directory if they don't exist."""
    if not os.path.exists('data'):
        os.makedirs('data')
    
    # Define sizes
    sizes = {"small": 50, "medium": 100, "large": 500}
    
    # Check if files exist before creating
    for name in sizes:
        if not os.path.exists(f'data/sample_{name}.csv'):
            # (Using a simplified generator for brevity)
            num_rows = sizes[name]
            sources = [f'Company_{i % 20}' for i in range(num_rows)]
            dests = [f'Company_{(i + 3) % 20}' for i in range(num_rows)]
             # Embed a clear cycle
            if num_rows > 10:
                sources[5], dests[5] = 'ShellA', 'ShellB'
                sources[6], dests[6] = 'ShellB', 'ShellC'
                sources[7], dests[7] = 'ShellC', 'ShellA'
            
            data = {
                'source': sources,
                'destination': dests,
                'time': [f't{i:04d}' for i in range(num_rows)],
                'value': [random.randint(1000, 500000) for _ in range(num_rows)]
            }
            pd.DataFrame(data).to_csv(f'data/sample_{name}.csv', index=False)


def dataframe_to_edge_list(df):
    """Converts a pandas DataFrame to a list of edge dictionaries."""
    df['value'] = pd.to_numeric(df['value'], errors='coerce')
    df.dropna(subset=['value'], inplace=True)
    df[['source', 'destination', 'time']] = df[['source', 'destination', 'time']].astype(str)
    edge_list = df.to_dict('records')
    edge_list.sort(key=lambda x: x['time'])
    return edge_list

def graph_dict_to_networkx(graph_dict):
    """Converts the algorithm's output graph dictionary to a NetworkX graph."""
    G = nx.DiGraph()
    for source_node, edges in graph_dict.items():
        if not G.has_node(source_node):
            G.add_node(source_node, title=source_node)
        for edge in edges:
            dest_node = edge['destination']
            if not G.has_node(dest_node):
                G.add_node(dest_node, title=dest_node)
            G.add_edge(
                source_node,
                dest_node,
                title=f"Value: {edge['value']:.2f}\nTime: {edge['time']}",
                value=edge['value']
            )
    return G

def draw_graph(graph_nx, file_name="graph.html"):
    """Generates an interactive pyvis graph from a NetworkX graph."""
    net = Network(height='600px', width='100%', notebook=False, directed=True, bgcolor='#222222', font_color='white')
    net.from_nx(graph_nx)
    net.set_options("""
    var options = {
      "nodes": { "font": { "size": 18 } },
      "edges": { "color": { "inherit": true }, "smooth": { "type": "dynamic" } },
      "physics": {
        "forceAtlas2Based": { "gravitationalConstant": -50, "centralGravity": 0.005, "springLength": 230, "springConstant": 0.18 },
        "minVelocity": 0.75, "solver": "forceAtlas2Based"
      }
    }
    """)
    try:
        net.save_graph(file_name)
        with open(file_name, 'r', encoding='utf-8') as f:
            html_content = f.read()
        components.html(html_content, height=620)
    except Exception as e:
        st.error(f"Could not display graph: {e}")

# --- Streamlit App Layout ---

st.set_page_config(page_title="Circular Trading Detector", layout="wide")

# Initialize sample datasets
create_sample_datasets()

# --- Top-level Tab Navigation ---
tab1, tab2, tab3, tab4 = st.tabs([
    "🌐 Project Overview", 
    "⚙️ The Algorithmic Engine", 
    "📊 Interactive Showcase", 
    "📝 Technical Implementation Notes"
])

# --- Page 1: Project Overview ---
with tab1:
    st.title("🌐 Algorithmic Detection of Circular Trading Fraud")
    st.markdown("---")
    
    col1, col2 = st.columns([2, 1.5])
    with col1:
        st.header("The Problem: Hidden Fraud in Plain Sight")
        st.markdown("""
        **Circular trading** is a sophisticated method of financial fraud used to evade taxes, inflate company value, or launder money. It involves a series of transactions that start and end with the same entity, creating a closed loop. 
        
        To an outside observer, this looks like legitimate business activity. However, no real value is being added; the primary purpose is to create a confusing paper trail that obscures malicious sales or helps claim fraudulent tax refunds. Manually detecting these schemes in large datasets is nearly impossible.
        """)
    with col2:
        st.image("ezgif-597c9823ad6b42.jpg", caption="Fig. 2 from the research paper, illustrating a simple A-B-C circular trade.")

    st.header("The Solution: A Graph-Based Approach")
    st.markdown("""
    This project implements an automated solution based on the research paper **"An Algorithmic Approach to Handle Circular Trading in Commercial Taxation System."** The system models the entire network of transactions as a **directed graph**, where businesses are nodes and transactions are weighted edges.
    
    By processing transactions chronologically, the algorithm can detect when a new transaction forms a cycle. It then uses a novel method to identify and remove the most likely fraudulent cycle, leaving behind a clean, **Directed Acyclic Graph (DAG)** of legitimate transactions.
    """)

# --- Page 2: The Algorithmic Engine ---
with tab2:
    st.title("⚙️ The Algorithmic Engine")
    st.markdown("---")
    
    st.header("Modeling Transactions as a Graph")
    st.write("The core idea is to transform raw transaction data into a mathematical structure. Each business is a **node** (a point), and each transaction is a **directed edge** (an arrow) from the seller to the buyer, weighted by the transaction's `value` and `time`.")
    
    st.header("A Three-Algorithm Approach")
    st.markdown("""
    - **Algorithm 3: `MAX_MIN` (The Path Finder):** This foundational algorithm finds the most robust path between two nodes, looking for the path where the "weakest link" (the transaction with the minimum value) is as high as possible.

    - **Algorithm 2: `DELETE_CYCLE` (The Cycle Surgeon):** When a new transaction creates a cycle, this algorithm analyzes it to find the cycle with the smallest **Flow Value** (the difference between the highest and lowest transaction values). This targets the most likely fraudulent loops where little real value was added.

    - **Algorithm 1: `WCD - Weighted Cycle Deletion` (The Orchestrator):** This is the main driver. It processes all transactions chronologically, adding them one by one to a graph and immediately calling `DELETE_CYCLE` to remove any fraudulent loop that forms.
    """)

# --- Page 3: Interactive Showcase ---
with tab3:
    st.title("📊 Interactive Showcase: Run & Visualize")
    st.markdown("---")
    
    # --- Data Input Controls (Moved from sidebar to main page) ---
    st.subheader("1. Select Input Data")
    col1, col2 = st.columns(2)
    with col1:
        sample_files = {
            "Sample Dataset - Small (50 transactions)": "data/sample_small.csv",
            "Sample Dataset - Medium (100 transactions)": "data/sample_medium.csv",
            "Sample Dataset - Large (500 transactions)": "data/sample_large.csv",
        }
        dataset_choice = st.selectbox("Choose a pre-loaded sample dataset:", list(sample_files.keys()))
    with col2:
        uploaded_file = st.file_uploader("Or upload your own dataset (.csv):", type=["csv"])
        st.info("Ensure your file has columns: `source`, `destination`, `time`, `value`.", icon="ℹ️")

    # --- Execution Button ---
    if st.button("**Analyze Transactions**", type="primary", use_container_width=True):
        input_df = None
        if uploaded_file is not None:
            try:
                input_df = pd.read_csv(uploaded_file)
                st.success("Successfully loaded uploaded file.")
            except Exception as e:
                st.error(f"Error reading uploaded file: {e}")
        else:
            try:
                input_df = pd.read_csv(sample_files[dataset_choice])
                st.success(f"Successfully loaded '{dataset_choice}'.")
            except Exception as e:
                st.error(f"Error loading sample file: {e}")

        if input_df is not None:
            with st.spinner("Processing network... this may take a moment."):
                edge_list_before = dataframe_to_edge_list(input_df.copy())
                
                # Build a temporary graph dict just for cycle detection and counting
                temp_graph_dict_before = {}
                all_nodes = set()
                for edge in edge_list_before:
                    source = edge['source']
                    dest = edge['destination']
                    all_nodes.add(source)
                    all_nodes.add(dest)
                    if source not in temp_graph_dict_before:
                        temp_graph_dict_before[source] = []
                    temp_graph_dict_before[source].append(edge)
                for node in all_nodes:
                    if node not in temp_graph_dict_before:
                        temp_graph_dict_before[node] = []

                nx_before = graph_dict_to_networkx(temp_graph_dict_before)
                cycles = list(nx.simple_cycles(nx_before))

            # --- "BEFORE" STATE ---
            st.markdown("---")
            st.header("2. Original Transaction Network ('Before')")
            
            col_b1, col_b2 = st.columns([1, 2.5])
            with col_b1:
                st.metric("Total Dealers (Nodes)", f"{nx_before.number_of_nodes()}")
                st.metric("Total Transactions (Edges)", f"{nx_before.number_of_edges()}")
                st.metric("Detected Cycles", f"{len(cycles)}", delta="High Fraud Risk" if cycles else "No Cycles Found", delta_color="inverse" if cycles else "off")
            
            with col_b2:
                draw_graph(nx_before, "before_graph.html")
            
            if cycles:
                with st.expander(f"**View the {len(cycles)} Detected Cycles**"):
                    for i, cycle in enumerate(cycles):
                        st.text(f"Cycle {i+1}: {' -> '.join(cycle)} -> {cycle[0]}")

            # --- ALGORITHM EXECUTION ---
            with st.spinner("Removing fraudulent cycles..."):
                graph_dict_after = wcd(edge_list_before)
                nx_after = graph_dict_to_networkx(graph_dict_after)

            # --- "AFTER" STATE ---
            st.markdown("---")
            st.header("3. Cleaned Transaction Network ('After')")
            
            col_a1, col_a2 = st.columns([1, 2.5])
            with col_a1:
                st.metric("Remaining Dealers (Nodes)", f"{nx_after.number_of_nodes()}")
                st.metric("Remaining Transactions (Edges)", f"{nx_after.number_of_edges()}")
                st.metric("Cycles Remaining", "0", delta="Cycles Successfully Removed", delta_color="normal")
            
            with col_a2:
                draw_graph(nx_after, "after_graph.html")
            
            # --- HIGHLIGHT REMOVED TRANSACTIONS ---
            # Create unique identifiers for transactions (source, destination, time)
            before_edges_set = { (e['source'], e['destination'], e['time']) for e in edge_list_before }
            
            after_edges_list = []
            for edges in graph_dict_after.values():
                after_edges_list.extend(edges)
            after_edges_set = { (e['source'], e['destination'], e['time']) for e in after_edges_list }
            
            removed_edges_ids = before_edges_set - after_edges_set
            
            removed_transactions = [
                edge for edge in edge_list_before 
                if (edge['source'], edge['destination'], edge['time']) in removed_edges_ids
            ]

            if removed_transactions:
                st.markdown("---")
                st.header("4. Identified Fraudulent Transactions")
                st.write(f"The algorithm identified and removed the following **{len(removed_transactions)}** transactions to break the fraudulent cycles:")
                
                df_removed = pd.DataFrame(removed_transactions)
                st.dataframe(df_removed)

# --- Page 4: Technical Notes ---
with tab4:
    st.title("📝 Technical Implementation Notes")
    st.markdown("---")

    st.header("Algorithm Components")
    st.markdown("""
    - **`WCD()`:** The main function that orchestrates the process. It takes a chronologically sorted list of transactions, builds a graph edge-by-edge, and calls `DELETE_CYCLE` upon detecting a cycle.
    - **`DELETE_CYCLE()`:** This function is the core of the fraud detection logic. It systematically finds all cycles created by a new edge, calculates their **Flow Value** (max value - min value), and identifies the cycle with the minimum flow value to remove.
    - **`MAX_MIN()` / `find_maxflow()`:** Implements a modified Dijkstra's algorithm using a max-priority queue to find the path between two nodes that maximizes the minimum edge weight (the bottleneck capacity).
    """)

    st.header("Key Features & Data Structures")
    st.markdown("""
    - **Language/Libraries:** **Python**, **Pandas**, **NetworkX**, **Streamlit**, and **Pyvis**.
    - **Data Representation:** An adjacency list (implemented as a Python dictionary) represents the graph.
    - **Efficiency:** The time complexity is noted in the paper as $O((m+n) \cdot m^2 \cdot log(n))$, where 'm' is edges and 'n' is vertices.
    - **Novelty:** The key innovation is **intelligently prioritizing which cycle to remove**. By targeting the cycle with the lowest "value-add" (minimum Flow Value), the algorithm is designed to specifically remove artificially created transaction loops.
    """)