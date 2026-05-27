import requests
from PIL import Image
import io

BASE_URL = "http://localhost:8000"

# Step 1: Login
print("Logging in...")
login_response = requests.post(f"{BASE_URL}/login", json={
    "email": "nanda@gmail.com",
    "password": "nanda123"
})

print("Login status:", login_response.status_code)
data = login_response.json()
token = data.get("token")
print("Token received:", token[:30] if token else "NO TOKEN!")

if not token:
    print("Login failed!")
    exit()

# Step 2: Create a simple test image locally
print("\nCreating test image...")
img = Image.new('RGB', (400, 200), color='white')

# Save it
img.save("test_medicine.jpg")
print("Test image created!")

# Step 3: Upload image
print("\nUploading medicine image...")
headers = {"Authorization": f"Bearer {token}"}

with open("test_medicine.jpg", "rb") as f:
    files = {"file": ("medicine.jpg", f, "image/jpeg")}
    upload_response = requests.post(
        f"{BASE_URL}/upload-image",
        headers=headers,
        files=files
    )

print("Upload status:", upload_response.status_code)
print("Response:", upload_response.json())