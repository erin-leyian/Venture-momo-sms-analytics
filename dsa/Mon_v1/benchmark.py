print("DEBUG: Script is actually starting...")
import timeit
import sys
import os

# Ensure the script can find parse_xml.py
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from parse_xml import MoMoSMSParser

def linear_search(tx_list, target_id):
    """Scan list sequentially - O(n)"""
    for tx in tx_list:
        if str(tx.get('transaction_id')) == str(target_id):
            return tx
    return None

def dictionary_lookup(tx_dict, target_id):
    """Direct access via hash map - O(1)"""
    return tx_dict.get(str(target_id))

def run_benchmark():
    # 1. Load Data using your existing Parser
    parser = MoMoSMSParser('modified_sms_v2.xml')
    transactions_list = parser.parse_xml()
    
    if not transactions_list:
        print("Error: Could not load transactions for benchmarking.")
        return

    # 2. Prepare Data Structures
    # Create a dictionary where key is transaction_id for O(1) access
    transactions_dict = {str(tx['transaction_id']): tx for tx in transactions_list if tx['transaction_id']}
    
    # 3. Pick a target ID to search for (choose one from the middle of the dataset)
    # We use a string because TxIds are often long numbers
    sample_id = str(transactions_list[len(transactions_list)//2].get('transaction_id'))
    
    print(f"\n--- Benchmarking Search Efficiency (Target ID: {sample_id}) ---")
    print(f"Dataset Size: {len(transactions_list)} records")
    
    # 4. Define the test runs (Running 10,000 times to get measurable data)
    iterations = 10000

    # Benchmark Linear Search
    linear_time = timeit.timeit(
        lambda: linear_search(transactions_list, sample_id), 
        number=iterations
    )

    # Benchmark Dictionary Lookup
    dict_time = timeit.timeit(
        lambda: dictionary_lookup(transactions_dict, sample_id), 
        number=iterations
    )

    # 5. Results & Reflection Logic for the Report
    print(f"\nResults over {iterations} iterations:")
    print(f"Total Linear Search Time:     {linear_time:.6f} seconds")
    print(f"Total Dictionary Lookup Time: {dict_time:.6f} seconds")
    
    speed_diff = linear_time / dict_time
    print(f"\nConclusion: Dictionary Lookup is {speed_diff:.2f}x faster than Linear Search.")
    
    if speed_diff > 1:
        print("Reflection: Dictionary lookup is faster because it uses a Hash Table (O(1)),")
        print("whereas Linear Search must check every element until a match is found (O(n)).")

if __name__ == "__main__":
    run_benchmark()