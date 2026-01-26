import xml.etree.ElementTree as ET
import json
import re
from datetime import datetime
def parse_momo_messages(body):

    transaction = {
        "type": "unknown",
        "amount": None,
        "currency": "RWF",
        "sender": None,
        "recipient": None,
        "balance": None,
        "fee": None,
        "transaction_id": None,
        "timestamp": None,
        "message": None,
        "raw_body": body
    }
    # handle received with regex    
    received_match = re.search(
        r'You have received (\d+(?:,\d+)*) RWF from ([^(]+)\s*\(\*+(\d+)\).*?at (\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}).*?new balance[:\s]*(\d+(?:,\d+)*) RWF.*?Transaction Id[:\s]*(\d+)',
        body, re.IGNORECASE | re.DOTALL
    )
    if received_match:
        transaction["type"] = "received"
        transaction["amount"] = int(received_match.group(1).replace(",", ""))
        transaction["sender"] = received_match.group(2).strip()
        transaction["timestamp"] = received_match.group(4)
        transaction["balance"] = int(received_match.group(5).replace(",", ""))
        transaction["transaction_id"] = received_match.group(6)
        return transaction
    
    # handle payment (*162) regex
    payment_match = re.search(
        r'TxId[:\s]*(\d+).*?payment of (\d+(?:,\d+)*) RWF to ([^\d]+?)(\d+).*?completed at (\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}).*?new balance[:\s]*(\d+(?:,\d+)*) RWF.*?Fee was (\d+(?:,\d+)*) RWF',
        body, re.IGNORECASE | re.DOTALL
    )
    if payment_match:
        transaction["type"] = "payment"
        transaction["transaction_id"] = payment_match.group(1)
        transaction["amount"] = int(payment_match.group(2).replace(",", ""))
        transaction["recipient"] = payment_match.group(3).strip()
        transaction["timestamp"] = payment_match.group(5)
        transaction["balance"] = int(payment_match.group(6).replace(",", ""))
        transaction["fee"] = int(payment_match.group(7).replace(",", ""))
        return transaction
    
    # handle transfer to another person pattern (*165*S* format)
    transfer_match = re.search(
        r'\*165\*S\*(\d+(?:,\d+)*) RWF transferred to ([^(]+)\s*\((\d+)\).*?at (\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}).*?Fee was[:\s]*(\d+(?:,\d+)*) RWF.*?New balance[:\s]*(\d+(?:,\d+)*) RWF',
        body, re.IGNORECASE | re.DOTALL
    )
    if transfer_match:
        transaction["type"] = "transfer_out"
        transaction["amount"] = int(transfer_match.group(1).replace(",", ""))
        transaction["recipient"] = transfer_match.group(2).strip()
        transaction["recipient_phone"] = transfer_match.group(3)
        transaction["timestamp"] = transfer_match.group(4)
        transaction["fee"] = int(transfer_match.group(5).replace(",", ""))
        transaction["balance"] = int(transfer_match.group(6).replace(",", ""))
        return transaction
    
    # handle bank deposit pattern (*113*R* format)
    deposit_match = re.search(
        r'\*113\*R\*.*?bank deposit of (\d+(?:,\d+)*) RWF.*?at (\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}).*?NEW BALANCE\s*[:\s]*(\d+(?:,\d+)*) RWF',
        body, re.IGNORECASE | re.DOTALL
    )
    if deposit_match:
        transaction["type"] = "bank_deposit"
        transaction["amount"] = int(deposit_match.group(1).replace(",", ""))
        transaction["timestamp"] = deposit_match.group(2)
        transaction["balance"] = int(deposit_match.group(3).replace(",", ""))
        return transaction
    
    # handle cash withdrawal pattern
    withdrawal_match = re.search(
        r'withdrawn (\d+(?:,\d+)*) RWF.*?at (\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}).*?new balance[:\s]*(\d+(?:,\d+)*) RWF.*?Fee paid[:\s]*(\d+(?:,\d+)*) RWF.*?Transaction Id[:\s]*(\d+)',
        body, re.IGNORECASE | re.DOTALL
    )
    if withdrawal_match:
        transaction["type"] = "withdrawal"
        transaction["amount"] = int(withdrawal_match.group(1).replace(",", ""))
        transaction["timestamp"] = withdrawal_match.group(2)
        transaction["balance"] = int(withdrawal_match.group(3).replace(",", ""))
        transaction["fee"] = int(withdrawal_match.group(4).replace(",", ""))
        transaction["transaction_id"] = withdrawal_match.group(5)
        return transaction
    
    # handle Airtime/Bill payment pattern (*162* format)
    bill_match = re.search(
        r'\*162\*TxId[:\s]*(\d+).*?payment of (\d+(?:,\d+)*) RWF to ([^w]+)with token\s*([^\s]*).*?completed at (\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}).*?Fee was (\d+(?:,\d+)*) RWF.*?new balance[:\s]*(\d+(?:,\d+)*) RWF',
        body, re.IGNORECASE | re.DOTALL
    )
    if bill_match:
        transaction["type"] = "bill_payment"
        transaction["transaction_id"] = bill_match.group(1)
        transaction["amount"] = int(bill_match.group(2).replace(",", ""))
        transaction["recipient"] = bill_match.group(3).strip()
        token = bill_match.group(4).strip()
        if token:
            transaction["token"] = token
        transaction["timestamp"] = bill_match.group(5)
        transaction["fee"] = int(bill_match.group(6).replace(",", ""))
        transaction["balance"] = int(bill_match.group(7).replace(",", ""))
        return transaction
    
    # handle Direct payment/debit pattern (*164*S* format)
    debit_match = re.search(
        r'\*164\*S\*.*?transaction of (\d+(?:,\d+)*) RWF by ([^o]+)on your.*?at (\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}).*?new balance[:\s]*(\d+(?:,\d+)*) RWF.*?Fee was (\d+(?:,\d+)*) RWF.*?Transaction Id[:\s]*(\d+)',
        body, re.IGNORECASE | re.DOTALL
    )
    if debit_match:
        transaction["type"] = "direct_debit"
        transaction["amount"] = int(debit_match.group(1).replace(",", ""))
        transaction["recipient"] = debit_match.group(2).strip()
        transaction["timestamp"] = debit_match.group(3)
        transaction["balance"] = int(debit_match.group(4).replace(",", ""))
        transaction["fee"] = int(debit_match.group(5).replace(",", ""))
        transaction["transaction_id"] = debit_match.group(6)
        return transaction
    
    # OTP (few like 8 otps)
    otp_match = re.search(r'one-time password is\s*[:\s]*(\d+)', body, re.IGNORECASE)
    if otp_match:
        transaction["type"] = "otp"
        transaction["otp_code"] = otp_match.group(1)
        return transaction
    
    return transaction


def convert_xml_to_json(xml_file, json_file):
    """
    convert momo XML SMS to JSON format.
    
    Args:
        xml_file: input XML file
        json_file: output JSON file
    """
    tree = ET.parse(xml_file)
    root = tree.getroot()    
    sms_data = {
        "metadata": {
            "count": root.get("count"),
            "backup_set": root.get("backup_set"),
            "backup_date": root.get("backup_date"),
            "type": root.get("type"),
            "converted_at": datetime.now().isoformat()
        },
        "messages": []
    }
    
    for sms in root.findall("sms"):
        message = {
            "protocol": sms.get("protocol"),
            "address": sms.get("address"),
            "date": sms.get("date"),
            "message_type": sms.get("type"),
            "subject": sms.get("subject"),
            "body": sms.get("body"),
            "service_center": sms.get("service_center"),
            "read": sms.get("read"),
            "status": sms.get("status"),
            "locked": sms.get("locked"),
            "date_sent": sms.get("date_sent"),
            "sub_id": sms.get("sub_id"),
            "readable_date": sms.get("readable_date"),
            "contact_name": sms.get("contact_name")
        }
        #print(message["body"])
        if message["body"]:
            parsed_transaction = parse_momo_messages(message["body"])
            message["parsed_transaction"] = parsed_transaction
        
        sms_data["messages"].append(message)
    #file handling    
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(sms_data, f, indent=2, ensure_ascii=False)
    
    return sms_data



def main():
    """Main function to run the conversion."""
    # files
    xml_file = "modified_sms_v2.xml"
    json_file = "momo_transactions.json"
    
    print(f"Converting {xml_file} to {json_file}...")
    
    try:
        # conversion
        data = convert_xml_to_json(xml_file, json_file)
        
        print(f"\nSuccessfully {json_file}")
        
    except FileNotFoundError:
        print(f"Error: Could not find input file '{xml_file}'")
    except ET.ParseError as e:
        print(f"Error parsing XML: {e}")
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
