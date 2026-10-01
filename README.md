# Smart Parking Management MVP

🅿️ **Hackathon Project** - Real-time parking slot detection using YOLOv8 and Streamlit

## Overview

This is a quick **3-hour hackathon MVP** that demonstrates intelligent parking space detection and availability management. The system uses computer vision (YOLOv8) to detect vehicles in parking lots and classify each slot as available or occupied.

## Features

✅ **Real-time Car Detection** - Uses YOLOv8 to detect vehicles  
✅ **Slot Occupancy Classification** - Determines if each spot is available  
✅ **Live Statistics Dashboard** - Shows total, available, and occupied slots  
✅ **Visual Annotation** - Color-coded parking slots (green=available, red=occupied)  
✅ **Slot-by-Slot Details** - View status of individual parking spots  
✅ **Easy to Use** - Simple web interface, no setup complexity  

## Tech Stack

- **YOLOv8** - Pre-trained object detection model for car detection
- **OpenCV** - Image processing and drawing annotations
- **Streamlit** - Interactive web interface
- **Python** - Core language

## Installation & Setup

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Steps

1. **Clone the repository**
   ```bash
   git clone https://github.com/Yogaharini/smart-parking-mvp.git
   cd smart-parking-mvp
   ```

2. **Create a virtual environment (recommended)**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   streamlit run app.py
   ```

5. **Access the app**
   - Open your browser and go to `http://localhost:8501`
   - The app will automatically load

## Usage

1. **Upload a parking lot image**
   - Click "Choose a parking image" and select a JPG/JPEG/PNG file
   - The system will process the image automatically

2. **View results**
   - See real-time statistics (total, available, occupied slots)
   - View annotated image with detected cars and slots
   - Check slot-by-slot status
   - View detailed table of all slots

## How It Works

```
┌──────────────────────┐
│  Parking Lot Image   │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│  YOLOv8 Detection    │ (Detects all vehicles)
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│ Slot Classification  │ (Check if car in slot)
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│ Dashboard Display    │ (Show availability)
└──────────────────────┘
```

## Project Structure

```
smart-parking-mvp/
├── app.py              # Main Streamlit application
├── requirements.txt    # Python dependencies
├── README.md           # This file
└── sample_parking/     # (Optional) Sample parking images for testing
```

## Key Components

### 1. **Model Loading** (`load_model()`)
   - Loads YOLOv8 Nano model (lightweight for laptops)
   - Uses Streamlit caching for fast subsequent loads

### 2. **Car Detection** (`detect_parking()`)
   - Runs inference on uploaded image
   - Extracts bounding boxes of detected vehicles
   - Classifies each slot based on detected cars

### 3. **Visualization** (`draw_results()`)
   - Draws parking slots with color coding
   - Overlays detected car boxes
   - Annotates with slot IDs and labels

### 4. **Statistics & Display**
   - Real-time availability metrics
   - Slot-by-slot status table
   - Occupancy rate calculation

## Sample Parking Lot Configuration

The MVP comes with a predefined parking lot layout:

```
Row A: [A1] [A2] [A3] [A4]
Row B: [B1] [B2] [B3] [B4]
```

You can customize slots by editing the `SLOTS` dictionary in `app.py`.

## Testing

### Without a Real Parking Image

1. Download a parking lot image from Google Images or Unsplash
2. Use stock photos of parking areas
3. Create a synthetic parking lot visualization

### With Sample Data

Place sample images in a `sample_parking/` folder and test with those.

## Future Enhancements

- 📹 **Video stream support** - Real-time detection from camera feeds
- 🗺️ **Map integration** - Show nearest available spots
- 🚗 **License plate recognition** - Vehicle identification
- 💾 **Database logging** - Historical occupancy data
- 📱 **Mobile app** - Native iOS/Android interface
- 🔐 **Admin dashboard** - Parking lot management
- 💳 **Payment integration** - Reservation and payment system
- 🔔 **Notifications** - Alert users when spots become available

## Performance Notes

- **First run**: May take 1-2 minutes to download YOLOv8 model (~100MB)
- **Subsequent runs**: Model is cached, inference is fast (1-3 seconds per image)
- **Best results**: Clear, well-lit parking lot images with distinct slot markings

## Hackathon Demo Script

1. **Introduction** (30 seconds)
   - "This is a smart parking management MVP built in 3 hours"
   - "We solve the problem of finding available parking quickly"

2. **Upload & Process** (1 minute)
   - Upload a sample parking lot image
   - Show the detection happening in real-time

3. **Results** (1 minute)
   - Highlight the statistics dashboard
   - Point out available vs. occupied slots
   - Show the annotated image with color coding

4. **Key Points** (30 seconds)
   - "Uses YOLOv8 for accurate car detection"
   - "Runs completely on a laptop"
   - "Can be extended to real-time video streams"
   - "Scalable to multiple parking lots"

## Limitations & Considerations

- ⚠️ **Slot configuration**: Currently uses hardcoded slots; can be made dynamic
- ⚠️ **Lighting**: Works best in good lighting conditions
- ⚠️ **Parking lot format**: Designed for rectangular slot layouts
- ⚠️ **Privacy**: Ensure compliance with local laws regarding parking lot monitoring

## License

MIT License - Feel free to use and modify for your projects

## Author

**Yogaharini** - Hackathon Participant

## Resources

- [YOLOv8 Documentation](https://docs.ultralytics.com/)
- [Streamlit Documentation](https://docs.streamlit.io/)
- [OpenCV Documentation](https://docs.opencv.org/)

---

**Built with ❤️ for the Hackathon** 🚀
