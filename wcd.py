from standard_functions import add_edge, detect_cycle, convert_csv_to_edge_list
from delete_cycles import delete_cycles


def wcd(transaction_list):
    graph_prime = {}
    for transaction in transaction_list:
        add_edge(graph_prime, transaction)
        if detect_cycle(graph_prime):
            graph_prime = delete_cycles(graph_prime, transaction)
    return graph_prime

list = convert_csv_to_edge_list("transactions.csv")
print(wcd(list))