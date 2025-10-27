
import datetime
import random

def generate_ref(prefix="MT"):
    return f"{prefix}{random.randint(100000,999999)}"

def now():
    return datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")

def gen_mt103(data):
    ref = data.get("transaction_ref") or generate_ref("MT103")
    block4 = f""":20:{ref}
:23B:CRED
:32A:{data['value_date']}{data['currency']}{data['amount']}
:50K:/{data['sender_account']}
{data.get('sender_name','')}
{data.get('sender_bank_name','')}
:59:/{data['receiver_account']}
{data.get('receiver_name','')}
{data.get('receiver_bank_name','')}
:70:{data.get('details','')}
:71A:{data['charges']}"""
    return block4

def gen_generic_79(mt, data):
    ref = data.get("transaction_ref") or generate_ref(mt)
    body = f""":20:{ref}
:21:{data.get('subject','')}
:79:{data.get('body','')}"""
    return body

def gen_mt700(data):
    ref = data.get("transaction_ref") or generate_ref("MT700")
    return f""":20:{ref}
:31C:{data['date_of_issue']}
:41D:{data['available_with']}
:50:{data['applicant']}
:59:{data['beneficiary']}
:32B:{data['currency']}{data['amount']}
:47A:{data.get('additional_conditions','')}"""

def gen_mt760(data):
    ref = data.get("transaction_ref") or generate_ref("MT760")
    return f""":20:{ref}
:21:{data['contract_ref']}
:32B:{data['currency']}{data['amount']}
:50:{data['applicant']}
:59:{data['beneficiary']}
:77B:{data['details']}"""

def gen_mt542(data):
    ref = data.get("transaction_ref") or generate_ref("MT542")
    return f""":20:{ref}
:22H:{data['instruction_code']}
:82A:{data['account_with']}
:87A:{data['party']}
:77H:{data['details']}"""

def gen_rwa(data):
    ref = data.get("transaction_ref") or generate_ref("RWA")
    return f"""RWA Notice
Ref: {ref}
Date: {now()}
Body:
{data['body']}"""

def generate_swift_message(mt_type, data):
    generators = {
        "MT103": gen_mt103,
        "MT199": lambda d: gen_generic_79("MT199", d),
        "MT799": lambda d: gen_generic_79("MT799", d),
        "MT999": lambda d: gen_generic_79("MT999", d),
        "MT700": gen_mt700,
        "MT760": gen_mt760,
        "MT542": gen_mt542,
        "RWA": gen_rwa,
    }
    if mt_type not in generators:
        raise ValueError(f"Unsupported message type: {mt_type}")
    return generators[mt_type](data)
