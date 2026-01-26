import xml.etree.ElementTree as ET
import json
import re
from datetime import datetime

class MoMoSMSParser:
    """Parser for Mobile Money SMS XML data"""
    
    def __init__(self, xml_file):
        self.xml_file = xml_file
        self.transactions = []
    
    def parse_body(self, body_text):
        """Extract transaction details from SMS body text"""
        transaction_data = {
            'transaction_type': None,
            'amount': None,
            'recipient': None,
            'sender': None,
            'new_balance': None,
            'fee': None,
            'transaction_id': None,
            'raw_body': body_text
        }
        
        # Extract transaction type
        if 'received' in body_text.lower():
            transaction_data['transaction_type'] = 'receive'
        elif 'payment' in body_text.lower():
            transaction_data['transaction_type'] = 'payment'
        elif 'deposit' in body_text.lower():
            transaction_data['transaction_type'] = 'deposit'
        elif 'withdrawal' in body_text.lower():
            transaction_data['transaction_type'] = 'withdrawal'
        else:
            transaction_data['transaction_type'] = 'unknown'
        
        # Extract amount (various patterns)
        amount_patterns = [
            r'received (\d+(?:,\d+)*)\s*RWF',
            r'payment of (\d+(?:,\d+)*)\s*RWF',
            r'deposit of (\d+(?:,\d+)*)\s*RWF',
            r'withdrawal of (\d+(?:,\d+)*)\s*RWF'
        ]
        for pattern in amount_patterns:
            match = re.search(pattern, body_text, re.IGNORECASE)
            if match:
                transaction_data['amount'] = match.group(1).replace(',', '')
                break
        
        # Extract sender (for received money)
        sender_match = re.search(r'from ([A-Za-z\s]+)\s*\(\*+(\d+)\)', body_text)
        if sender_match:
            transaction_data['sender'] = sender_match.group(1).strip()
        
        # Extract recipient (for payments)
        recipient_match = re.search(r'to ([A-Za-z\s]+)\s*(\d+)', body_text)
        if recipient_match:
            transaction_data['recipient'] = recipient_match.group(1).strip()
        
        # Extract new balance
        balance_match = re.search(r'new balance[:\s]*(\d+(?:,\d+)*)\s*RWF', body_text, re.IGNORECASE)
        if balance_match:
            transaction_data['new_balance'] = balance_match.group(1).replace(',', '')
        
        # Extract fee
        fee_match = re.search(r'Fee was (\d+(?:,\d+)*)\s*RWF', body_text)
        if fee_match:
            transaction_data['fee'] = fee_match.group(1).replace(',', '')
        
        # Extract transaction ID
        txid_patterns = [
            r'TxId:\s*(\d+)',
            r'Financial Transaction Id:\s*(\d+)',
            r'Transaction Id:\s*(\d+)'
        ]
        for pattern in txid_patterns:
            match = re.search(pattern, body_text)
            if match:
                transaction_data['transaction_id'] = match.group(1)
                break
        
        return transaction_data
    
    def parse_xml(self):
        """Parse XML file and convert to JSON structure"""
        try:
            tree = ET.parse(self.xml_file)
            root = tree.getroot()
            
            # Get metadata
            metadata = {
                'total_count': root.get('count'),
                'backup_set': root.get('backup_set'),
                'backup_date': root.get('backup_date'),
                'type': root.get('type')
            }
            
            # Parse each SMS
            for idx, sms in enumerate(root.findall('sms'), start=1):
                # Get basic SMS attributes
                sms_data = {
                    'id': idx,
                    'address': sms.get('address'),
                    'date': sms.get('date'),
                    'readable_date': sms.get('readable_date'),
                    'type': sms.get('type'),
                    'body': sms.get('body'),
                    'read': sms.get('read'),
                    'contact_name': sms.get('contact_name')
                }
                
                # Parse transaction details from body
                body_text = sms.get('body', '')
                transaction_details = self.parse_body(body_text)
                
                # Merge all data
                complete_transaction = {**sms_data, **transaction_details}
                
                self.transactions.append(complete_transaction)
            
            print(f"✓ Successfully parsed {len(self.transactions)} transactions")
            return self.transactions
            
        except FileNotFoundError:
            print(f"✗ Error: File '{self.xml_file}' not found")
            return None
        except ET.ParseError as e:
            print(f"✗ Error parsing XML: {e}")
            return None
        except Exception as e:
            print(f"✗ Unexpected error: {e}")
            return None
    
    def save_to_json(self, output_file='transactions.json'):
        """Save parsed transactions to JSON file"""
        if not self.transactions:
            print("✗ No transactions to save. Parse XML first.")
            return False
        
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(self.transactions, f, indent=2, ensure_ascii=False)
            print(f"✓ Saved {len(self.transactions)} transactions to '{output_file}'")
            return True
        except Exception as e:
            print(f"✗ Error saving JSON: {e}")
            return False
    
    def get_summary(self):
        """Get summary statistics of parsed data"""
        if not self.transactions:
            return None
        
        summary = {
            'total_transactions': len(self.transactions),
            'by_type': {},
            'total_amount': 0
        }
        
        for txn in self.transactions:
            # Count by type
            txn_type = txn.get('transaction_type', 'unknown')
            summary['by_type'][txn_type] = summary['by_type'].get(txn_type, 0) + 1
            
            # Sum amounts
            if txn.get('amount'):
                try:
                    summary['total_amount'] += float(txn['amount'])
                except ValueError:
                    pass
        
        return summary


def main():
    """Main function to demonstrate usage"""
    
    # Initialize parser
    parser = MoMoSMSParser('modified_sms_v2.xml')
    
    # Parse XML file
    print("=" * 50)
    print("MoMo SMS Parser")
    print("=" * 50)
    
    transactions = parser.parse_xml()
    
    if transactions:
        # Save to JSON
        parser.save_to_json('transactions.json')
        
        # Display summary
        summary = parser.get_summary()
        print("\n" + "=" * 50)
        print("Summary Statistics")
        print("=" * 50)
        print(f"Total Transactions: {summary['total_transactions']}")
        print(f"\nBreakdown by Type:")
        for txn_type, count in summary['by_type'].items():
            print(f"  {txn_type.capitalize()}: {count}")
        print(f"\nTotal Amount: {summary['total_amount']:,.0f} RWF")
        
        # Show first 3 transactions as sample
        print("\n" + "=" * 50)
        print("Sample Transactions (First 3)")
        print("=" * 50)
        for txn in transactions[:3]:
            print(f"\nID: {txn['id']}")
            print(f"Type: {txn['transaction_type']}")
            print(f"Amount: {txn['amount']} RWF")
            print(f"Date: {txn['readable_date']}")
            if txn['sender']:
                print(f"From: {txn['sender']}")
            if txn['recipient']:
                print(f"To: {txn['recipient']}")
            print(f"New Balance: {txn['new_balance']} RWF")


if __name__ == "__main__":
    main()