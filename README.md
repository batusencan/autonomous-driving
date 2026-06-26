# Autonomous Driving Project 🏎️

This repository contains computer vision applications for autonomous driving, starting from basic lane detection algorithms to simulator integrations.

---
### 🚀 Structural Evolution: Complete Codebase Refactoring (v2.0)

Instead of patching the old monolithic script, I created a brand new architecture in a separate folder to implement clean, modular, and functional programming principles from scratch.

#### Key Architectural Changes:
- **Zero-Spaghetti Code:** Built a fully functional pipeline (`process_frame()`) for better memory management and scalability.
- **Goodbye Polyfit:** Completely abandoned the global linear regression (`np.polyfit`) model. Forcing the right solid lane and the center dashed lanes into a single line equation was mathematically incorrect, causing artificial "X" noise.
- **Direct Vector Tracking:** The new codebase now directly visualizes the raw `HoughLinesP` vectors strictly filtered inside a precisely tuned Region of Interest (ROI). This allows dashed lanes to appear naturally without distorting the tracking path.


## 📂 Project Structure

* **image_lane_detection:** Detects lane lines from a static highway image using Canny Edge Detection and Hough Transform.
* **lane_detection_system_prototype:** Real-time lane tracking application on dynamic video streams using Line Averaging (Single Line Theorem).

---

## 🛠️ Tech Stack & Dependencies

* Python 3.12
* OpenCV (Computer Vision library)
* NumPy (Mathematical operations)

---

## 🚀 Current Status & Challenges (MVP v2)

The current version (`lane_detection_system_prototype`) successfully tracks solid lines on high-speed roads. 

### Known Issues & Technical Challenges:
* **Dotted Lines:** Intersection noise ("X" shape artifacts) occurs during dotted (dashed) lanes due to slope estimation sensitivity in short pixel segments.
* **Sharp Curves:** The single-line linear equation (y = mx + b) tends to drift when encountering heavy curvature.

---

## 📈 Future Roadmap

- [ ] Add **Temporal Smoothing (Moving Average / Kalman Filter)** to handle dotted lane gaps using previous frame memory.
- [ ] Implement **2nd-Degree Polynomial Fitting** (y = ax^2 + bx + c) for curved lane tracking.
