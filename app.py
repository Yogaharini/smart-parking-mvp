import cv2
import streamlit as st
from ultralytics import YOLO
import numpy as np
from PIL import Image
import io

# Set page config
st.set_page_config(page_title="Smart Parking MVP", layout="wide", initial_sidebar_state="expanded")

# Predefined parking slots: slot_name: (x1, y1, x2, y2)
SLOTS = {
    "A1": (120, 100, 220, 220),
    "A2": (240, 100, 340, 220),
    "A3": (360, 100, 460, 220),
    "A4": (480, 100, 580, 220),
    "B1": (120, 260, 220, 380),
    "B2": (240, 260, 340, 380),
    "B3": (360, 260, 460, 380),
    "B4": (480, 260, 580, 380),
}

# Load YOLOv8 model
@st.cache_resource
def load_model():
    return YOLO("yolov8n.pt")

model = load_model()

def slot_contains(slot_box, car_box):
    """Check if a car is inside a parking slot"""
    sx1, sy1, sx2, sy2 = slot_box
    cx1, cy1, cx2, cy2 = car_box
    # Check if car center is inside slot box
    cx = (cx1 + cx2) / 2
    cy = (cy1 + cy2) / 2
    return sx1 <= cx <= sx2 and sy1 <= cy <= sy2

def detect_parking(image):
    """Detect cars and classify parking slots as occupied/available"""
    results = model(image, conf=0.45, verbose=False)
    detected_cars = []
    
    # Extract car detections
    for r in results:
        for box in r.boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0].tolist())
            cls = int(box.cls[0])
            name = r.names[cls]
            # Detect cars and trucks
            if name in ["car", "truck"]:
                detected_cars.append((x1, y1, x2, y2))
    
    # Classify each slot
    occupied = set()
    for slot_name, slot_box in SLOTS.items():
        for car_box in detected_cars:
            if slot_contains(slot_box, car_box):
                occupied.add(slot_name)
                break
    
    status = {slot: "Occupied" if slot in occupied else "Available" for slot in SLOTS}
    return status, detected_cars

def draw_results(image, status, detected_cars):
    """Draw parking slots and detected cars on image"""
    result_image = image.copy()
    
    # Draw parking slots
    for slot_name, slot_box in SLOTS.items():
        x1, y1, x2, y2 = slot_box
        color = (0, 255, 0) if status[slot_name] == "Available" else (0, 0, 255)
        cv2.rectangle(result_image, (x1, y1), (x2, y2), color, 2)
        cv2.putText(result_image, slot_name, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)
    
    # Draw detected cars
    for x1, y1, x2, y2 in detected_cars:
        cv2.rectangle(result_image, (x1, y1), (x2, y2), (255, 0, 0), 2)
        cv2.putText(result_image, "Car", (x1, y1 - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 1)
    
    return result_image

# Header
st.title("🅿️ Smart Parking Management MVP")
st.markdown("**Hackathon Project** - Real-time parking slot detection using YOLOv8")
st.divider()

# Sidebar
with st.sidebar:
    st.header("ℹ️ About")
    st.markdown("""
    This MVP demonstrates intelligent parking space detection using:
    - **YOLOv8**: Pre-trained object detection model
    - **OpenCV**: Image processing and annotation
    - **Streamlit**: Interactive web interface
    
    **Features:**
    - Upload parking lot images
    - Automatic car detection
    - Slot occupancy classification
    - Real-time availability stats
    - Visual annotation of results
    """)
    
    st.header("📊 How It Works")
    st.markdown("""
    1. Upload a parking lot image
    2. YOLOv8 detects all vehicles
    3. System checks which slots contain cars
    4. Dashboard shows availability
    5. Visual results with annotations
    """)

# Main content
st.header("Upload Parking Lot Image")
uploaded_file = st.file_uploader("Choose a parking image (JPG, JPEG, PNG)", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Read image
    file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
    image = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
    
    # Perform detection
    with st.spinner("🔍 Detecting parking spaces..."):
        status, detected_cars = detect_parking(image)
    
    # Calculate statistics
    total_slots = len(SLOTS)
    available_count = sum(1 for v in status.values() if v == "Available")
    occupied_count = total_slots - available_count
    occupancy_rate = (occupied_count / total_slots) * 100
    
    # Display statistics
    st.header("📈 Parking Statistics")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Slots", total_slots)
    col2.metric("Available", available_count, delta=f"{100 - occupancy_rate:.0f}%")
    col3.metric("Occupied", occupied_count, delta=f"{occupancy_rate:.0f}%")
    col4.metric("Detected Cars", len(detected_cars))
    
    st.divider()
    
    # Draw and display results
    st.header("🖼️ Detection Results")
    result_image = draw_results(image, status, detected_cars)
    st.image(
    result_image,
    channels="BGR",
    caption="Annotated Parking Lot (Green=Available, Red=Occupied)"
)
    
    st.divider()
    
    # Slot-by-slot status
    st.header("🔍 Slot Status Details")
    col1, col2 = st.columns(2)
    
    with col1:
        available_slots = [s for s, st in status.items() if st == "Available"]
        st.success(f"✅ Available Slots ({len(available_slots)})")
        for slot in sorted(available_slots):
            st.write(f"  • {slot}")
    
    with col2:
        occupied_slots = [s for s, st in status.items() if st == "Occupied"]
        st.error(f"❌ Occupied Slots ({len(occupied_slots)})")
        for slot in sorted(occupied_slots):
            st.write(f"  • {slot}")
    
    st.divider()
    
    # Detailed table
    st.header("📋 Complete Slot Status Table")
    table_data = [
        {"Slot ID": slot, "Status": status[slot], "Color": "🟢 Available" if status[slot] == "Available" else "🔴 Occupied"}
        for slot in sorted(status.keys())
    ]
    st.table(table_data)

else:
    st.info("👆 Upload a parking lot image to get started!")
    st.markdown("""
    ### Sample Use Cases:
    - **Parking lot management**: Real-time occupancy monitoring
    - **Driver assistance**: Find available spots quickly
    - **Analytics**: Track parking patterns and trends
    - **Smart city**: Optimize urban parking infrastructure
    """)
