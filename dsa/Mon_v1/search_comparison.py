import json
import time
import random

class TransactionSearch:
    """Compare different search algorithms for transaction lookup"""
    
    def __init__(self, json_file='transactions.json'):
        self.json_file = json_file
        self.transactions_list = []
        self.transactions_dict = {}
        self.load_data()
    
    def load_data(self):
        """Load transactions from JSON file"""
        try:
            with open(self.json_file, 'r', encoding='utf-8') as f:
                self.transactions_list = json.load(f)
            
            # Create dictionary for O(1) lookup
            # Key: transaction ID, Value: transaction data
            for txn in self.transactions_list:
                self.transactions_dict[txn['id']] = txn
            
            print(f"✓ Loaded {len(self.transactions_list)} transactions")
            print(f"✓ Created dictionary with {len(self.transactions_dict)} entries")
            return True
            
        except FileNotFoundError:
            print(f"✗ Error: '{self.json_file}' not found")
            return False
        except json.JSONDecodeError as e:
            print(f"✗ Error decoding JSON: {e}")
            return False
    
    def linear_search(self, target_id):
        """
        Linear Search - O(n) time complexity
        Searches through the list sequentially until target is found
        """
        for transaction in self.transactions_list:
            if transaction['id'] == target_id:
                return transaction
        return None
    
    def dictionary_lookup(self, target_id):
        """
        Dictionary Lookup - O(1) time complexity
        Uses hash table for constant-time access
        """
        return self.transactions_dict.get(target_id, None)
    
    def measure_performance(self, target_id, iterations=1000):
        """
        Measure performance of both search methods
        Run multiple iterations for accurate timing
        """
        # Measure Linear Search
        start_time = time.perf_counter()
        for _ in range(iterations):
            result_linear = self.linear_search(target_id)
        end_time = time.perf_counter()
        linear_time = (end_time - start_time) * 1000  # Convert to milliseconds
        
        # Measure Dictionary Lookup
        start_time = time.perf_counter()
        for _ in range(iterations):
            result_dict = self.dictionary_lookup(target_id)
        end_time = time.perf_counter()
        dict_time = (end_time - start_time) * 1000  # Convert to milliseconds
        
        return {
            'linear_time': linear_time,
            'dict_time': dict_time,
            'speedup': linear_time / dict_time if dict_time > 0 else 0,
            'result_found': result_linear is not None
        }
    
    def run_comprehensive_test(self, num_searches=20):
        """
        Run comprehensive performance comparison
        Tests different positions in the dataset
        """
        print("\n" + "=" * 70)
        print("COMPREHENSIVE PERFORMANCE TEST")
        print("=" * 70)
        
        if len(self.transactions_list) < num_searches:
            num_searches = len(self.transactions_list)
        
        # Generate random IDs to search for
        test_ids = random.sample(range(1, len(self.transactions_list) + 1), num_searches)
        
        results = []
        
        print(f"\nTesting {num_searches} random transaction IDs...")
        print(f"Running 1000 iterations per search for accurate timing\n")
        
        for idx, target_id in enumerate(test_ids, 1):
            perf = self.measure_performance(target_id, iterations=1000)
            results.append(perf)
            
            print(f"Test {idx}/{num_searches} - ID: {target_id}")
            print(f"  Linear Search:     {perf['linear_time']:.4f} ms")
            print(f"  Dictionary Lookup: {perf['dict_time']:.4f} ms")
            print(f"  Speedup:           {perf['speedup']:.2f}x faster")
            print()
        
        # Calculate averages
        avg_linear = sum(r['linear_time'] for r in results) / len(results)
        avg_dict = sum(r['dict_time'] for r in results) / len(results)
        avg_speedup = sum(r['speedup'] for r in results) / len(results)
        
        return {
            'avg_linear_time': avg_linear,
            'avg_dict_time': avg_dict,
            'avg_speedup': avg_speedup,
            'num_tests': num_searches
        }
    
    def display_summary(self, summary):
        """Display summary of performance comparison"""
        print("=" * 70)
        print("PERFORMANCE SUMMARY")
        print("=" * 70)
        print(f"\nDataset Size: {len(self.transactions_list)} transactions")
        print(f"Number of Tests: {summary['num_tests']}")
        print(f"Iterations per Test: 1000")
        
        print(f"\n{'Method':<25} {'Avg Time':<15} {'Difference'}")
        print("-" * 70)
        print(f"{'Linear Search':<25} {summary['avg_linear_time']:>10.4f} ms")
        print(f"{'Dictionary Lookup':<25} {summary['avg_dict_time']:>10.4f} ms  {summary['avg_speedup']:.2f}x faster")
        
        print("\n" + "=" * 70)
        print("ANALYSIS")
        print("=" * 70)
        print(f"Dictionary lookup is ~{summary['avg_speedup']:.1f}x faster than linear search")
        print(f"Time saved per lookup: {summary['avg_linear_time'] - summary['avg_dict_time']:.4f} ms")
        print(f"\nFor {len(self.transactions_list)} transactions:")
        print(f"  - Linear Search has O(n) complexity - checks up to {len(self.transactions_list)} items")
        print(f"  - Dictionary Lookup has O(1) complexity - direct access regardless of size")
    
    def demo_search(self, target_id):
        """Demonstrate both search methods with a specific ID"""
        print("\n" + "=" * 70)
        print(f"SEARCHING FOR TRANSACTION ID: {target_id}")
        print("=" * 70)
        
        # Linear Search
        print("\n1. LINEAR SEARCH (Sequential)")
        print("   Method: Check each transaction one by one")
        start = time.perf_counter()
        result_linear = self.linear_search(target_id)
        end = time.perf_counter()
        linear_time = (end - start) * 1000000  # microseconds
        
        if result_linear:
            print(f"   ✓ Found transaction")
            print(f"   Time: {linear_time:.2f} microseconds")
            print(f"   Type: {result_linear['transaction_type']}")
            print(f"   Amount: {result_linear['amount']} RWF")
        else:
            print(f"   ✗ Transaction not found")
        
        # Dictionary Lookup
        print("\n2. DICTIONARY LOOKUP (Hash Table)")
        print("   Method: Direct access using hash key")
        start = time.perf_counter()
        result_dict = self.dictionary_lookup(target_id)
        end = time.perf_counter()
        dict_time = (end - start) * 1000000  # microseconds
        
        if result_dict:
            print(f"   ✓ Found transaction")
            print(f"   Time: {dict_time:.2f} microseconds")
            print(f"   Type: {result_dict['transaction_type']}")
            print(f"   Amount: {result_dict['amount']} RWF")
        else:
            print(f"   ✗ Transaction not found")
        
        # Comparison
        if linear_time > 0 and dict_time > 0:
            speedup = linear_time / dict_time
            print(f"\n   COMPARISON:")
            print(f"   Dictionary lookup was {speedup:.2f}x faster")


def main():
    """Main function to run DSA comparison"""
    
    print("=" * 70)
    print("DATA STRUCTURES & ALGORITHMS COMPARISON")
    print("Linear Search vs Dictionary Lookup")
    print("=" * 70)
    
    # Initialize search system
    search_system = TransactionSearch('transactions.json')
    
    if not search_system.transactions_list:
        print("Failed to load data. Exiting.")
        return
    
    # Demo: Search for a specific transaction
    search_system.demo_search(100)
    
    # Run comprehensive performance test
    summary = search_system.run_comprehensive_test(num_searches=20)
    
    # Display summary
    search_system.display_summary(summary)
    
    # Additional insights
    print("\n" + "=" * 70)
    print("KEY INSIGHTS")
    print("=" * 70)
    print("""
1. TIME COMPLEXITY:
   - Linear Search: O(n) - time increases with dataset size
   - Dictionary Lookup: O(1) - constant time regardless of size

2. SPACE COMPLEXITY:
   - Linear Search: O(1) - no extra space needed
   - Dictionary Lookup: O(n) - stores additional hash table

3. WHEN TO USE:
   - Linear Search: Small datasets, one-time searches, unsorted data
   - Dictionary Lookup: Large datasets, frequent searches, when space is available

4. OTHER EFFICIENT DATA STRUCTURES:
   - Binary Search Tree: O(log n) search on sorted data
   - Hash Table: O(1) average case (what we use for dictionary)
   - Trie: Efficient for string prefix searches
   - B-Tree: Database indexing for large datasets
    """)
    
    print("=" * 70)
    print("TEST COMPLETE")
    print("=" * 70)


if __name__ == "__main__":
    main()
