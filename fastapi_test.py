from fastapi import FastAPI
from pydantic import BaseModel

class ReceiptData(BaseModel):
    date: str
    time: str|None = None
    fuel_type: str
    volume: float
    amount: float
    rate: float
    receipt_no: str

fake_db = [
    {'date': '2023-06-17', 'time': '19:45:37', 'fuel_type': 'PETROL', 'volume': 20, 'rate': 19.7 , 'amount': 2000.0, 'receipt_no': 'jun-217412', 'amount_validation': False},
    {'date': '2018-08-16', 'time': '09:29', 'fuel_type': 'PETROL', 'volume': 36.62, 'rate': 77.24, 'amount': 2828.52, 'receipt_no': '200086938', 'amount_validation': True},
    {'date': '2017-09-05', 'time': '22:59:34', 'fuel_type': 'DIESEL', 'volume': 1.0, 'rate': 78.0, 'amount': 78.0, 'receipt_no': '927267', 'amount_validation': True}
]

app = FastAPI()

@app.get("/")
async def health_check():
    return {"message": "OCR Receipt API running"}


@app.get("/receipts/search/{receipt_id}")
async def search_receipt(receipt_id: str):
    for data in fake_db:
        if data["receipt_no"] == receipt_id:
            return {"message":f"Here is the receipt_id ({receipt_id}) details", **data}
    return {"error":f"receipt_id: {receipt_id} not found"}
          

@app.post("/receipts/validate")
async def validate_receipt(data: ReceiptData):
    return {"message": "Receipt Validated", **data.model_dump()}

@app.put("/receipts/update/{receipt_id}")
async def update_receipt(receipt_id: str, new_data: ReceiptData):
    new_data_dict = new_data.model_dump()
    for i, data in enumerate(fake_db):
         if data["receipt_no"] == receipt_id:
              fake_db[i] = new_data_dict #db also gets updated
              return {"message": "Receipt updated successfully", **new_data_dict}
    return {"error":f"receipt_id: {receipt_id} not found"}
    
# this operation is defined for user reviewing in the frontend and and clicks confirm receipt
@app.put("/receipts/{receipt_id}")
async def verify_receipt(receipt_id: str, receipt_data: ReceiptData, verified: bool = False):
        return {"verified": verified,**receipt_data.model_dump()}

@app.post("/receipts/export")
async def export_receipt_data(parsed_data: ReceiptData):
    receipt_no = parsed_data.receipt_no
    return {"message": "Receipt exported succefully", "receipt_no": receipt_no}