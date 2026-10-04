import json
import time
import uuid
import hashlib

init_start = time.perf_counter()

for i in range(150000):
    hashlib.sha256(str(i).encode()).digest()

init_duration = (time.perf_counter() - init_start) * 1000

cold_start = True


def lambda_handler(event, context):

    global cold_start

    start = time.perf_counter()

    is_cold = cold_start
    cold_start = False

    transaction_id = str(uuid.uuid4())

    amount = 1000

    try:
        body = json.loads(event.get("body", "{}"))
        amount = body.get("amount", 1000)
    except:
        pass

    if not isinstance(amount, (int, float)) or amount <= 0:
        return {
            "statusCode": 400,
            "body": json.dumps({
                "error": "Invalid amount"
            })
        }

    time.sleep(0.03)

    processing_ms = (
        time.perf_counter() - start
    ) * 1000

    response = {
        "transaction_id": transaction_id,
        "status": "VALIDATED",
        "amount": amount,
        "cold_start": is_cold,
        "initialization_ms":
            round(init_duration, 2) if is_cold else 0,
        "processing_ms":
            round(processing_ms, 2),
        "request_id":
            context.aws_request_id
    }

    print(json.dumps(response))

    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json"
        },
        "body": json.dumps(response)
    }