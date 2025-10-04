import cv2
import pytesseract
import requests
import re
import xml.etree.ElementTree as ET
import json

API_URL = "https://www.regcheck.org.uk/api/reg.asmx/CheckIndia"
USERNAME = "atharva125" 
pattern = r"[A-Z]{2}\d{2}[A-Z]{1,2}\d{4}"

cap = cv2.VideoCapture(0)
last_detected = None

def fetch_vehicle_data(number):
    """Send number to CarReg API and return parsed JSON"""
    try:
        payload = {
            "RegistrationNumber": number,
            "username": USERNAME
        }
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        response = requests.post(API_URL, data=payload, headers=headers)

        root = ET.fromstring(response.text)
        vehicle_json = root.find(".//{http://regcheck.org.uk}vehicleJson")

        if vehicle_json is not None and vehicle_json.text:
            data = json.loads(vehicle_json.text)
            return data
        else:
            return {"error": "No vehicle data found"}

    except Exception as e:
        return {"error": str(e)}


while True:
    ret, frame = cap.read()
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    text = pytesseract.image_to_string(gray).strip()

    matches = re.findall(pattern, text)
    if matches:
        vehicle_number = matches[0]

        if vehicle_number != last_detected:
            last_detected = vehicle_number
            print(f"\n📸 Detected Vehicle Number: {vehicle_number}")

            data = fetch_vehicle_data(vehicle_number)

            if "error" not in data:
                vehicle_info = data.get("Description", "N/A")
                make = data.get("CarMake", {}).get("CurrentTextValue", "N/A")
                model = data.get("CarModel", "N/A")
                fuel = data.get("FuelType", {}).get("CurrentTextValue", "N/A")
                reg_year = data.get("RegistrationYear", "N/A")

                print("🚗 Vehicle Details:")
                print(f"   Make: {make}")
                print(f"   Model: {model}")
                print(f"   Fuel: {fuel}")
                print(f"   Registration Year: {reg_year}")
                print(f"   Description: {vehicle_info}")
            else:
                print("⚠️ API Error:", data["error"])

    cv2.imshow("Live OCR", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
