import cv2
import numpy as np

CAM_INDEX = 1  # change to 0 if needed

# Hough params
DP = 1.2
MIN_DIST = 60
PARAM1 = 100
PARAM2 = 28
MIN_RADIUS = 30
MAX_RADIUS = 160

# calibrated radii for 1 and 2 rupee (pixels)
CALIB_RAD_1 = 72.8
CALIB_RAD_2 = 81.4

def circle_region_mean_hsv(img, cx, cy, r, inner_ratio=1.0, outer_ratio=None):
    h_img, w_img = img.shape[:2]
    if outer_ratio is None:
        r_use = max(1, int(r * inner_ratio))
        x1 = max(cx - r_use, 0); x2 = min(cx + r_use, w_img - 1)
        y1 = max(cy - r_use, 0); y2 = min(cy + r_use, h_img - 1)
        roi = img[y1:y2+1, x1:x2+1]
        if roi.size == 0:
            return None, None, None
        mask = np.zeros((y2 - y1 + 1, x2 - x1 + 1), dtype=np.uint8)
        cx_rel = int(cx - x1); cy_rel = int(cy - y1)
        cv2.circle(mask, (cx_rel, cy_rel), r_use, 255, -1)
    else:
        r_outer = max(1, int(r * outer_ratio))
        r_inner = max(1, int(r * inner_ratio))
        x1 = max(cx - r_outer, 0); x2 = min(cx + r_outer, w_img - 1)
        y1 = max(cy - r_outer, 0); y2 = min(cy + r_outer, h_img - 1)
        roi = img[y1:y2+1, x1:x2+1]
        if roi.size == 0:
            return None, None, None
        mask = np.zeros((y2 - y1 + 1, x2 - x1 + 1), dtype=np.uint8)
        cx_rel = int(cx - x1); cy_rel = int(cy - y1)
        cv2.circle(mask, (cx_rel, cy_rel), r_outer, 255, -1)
        cv2.circle(mask, (cx_rel, cy_rel), r_inner, 0, -1)

    hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
    m = mask.astype(bool)
    if m.sum() == 0:
        return None, None, None
    return float(np.mean(hsv[:,:,0][m])), float(np.mean(hsv[:,:,1][m])), float(np.mean(hsv[:,:,2][m]))

def is_gold(h, s, v):
    if h is None:
        return False
    return (h < 50 and s > 60 and v > 70)

def is_silver(h, s, v):
    if h is None:
        return False
    return (s < 100 and v > 100)

def classify_coin(r, hin, sin, vin, hout, sout, vout):
    # 10 rupee: outer gold + inner silver
    if is_gold(hout, sout, vout) and is_silver(hin, sin, vin):
        return 10
    # 5 rupee: inner gold-like
    if is_gold(hin, sin, vin):
        return 5
    # silver: decide 1 or 2 by nearest calibrated radius
    d1 = abs(r - CALIB_RAD_1)
    d2 = abs(r - CALIB_RAD_2)
    return 1 if d1 < d2 else 2

def main():
    cap = cv2.VideoCapture(CAM_INDEX)
    cap.set(3, 640)
    cap.set(4, 480)
    if not cap.isOpened():
        return

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        out = frame.copy()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (7,7), 1.5)

        circles = cv2.HoughCircles(blur, cv2.HOUGH_GRADIENT, dp=DP, minDist=MIN_DIST,
                                   param1=PARAM1, param2=PARAM2,
                                   minRadius=MIN_RADIUS, maxRadius=MAX_RADIUS)

        total = 0
        if circles is not None:
            circles = np.round(circles[0,:]).astype(int)
            for (x, y, r) in circles:
                hin, sin, vin = circle_region_mean_hsv(frame, x, y, r, inner_ratio=0.55)
                hout, sout, vout = circle_region_mean_hsv(frame, x, y, r, inner_ratio=0.72, outer_ratio=1.0)
                val = classify_coin(r, hin, sin, vin, hout, sout, vout)
                total += val
                cv2.circle(out, (x, y), r, (0,255,0), 2)
                cv2.putText(out, f"{val} Rs", (x - r, y - r - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255,255,255), 2)

        cv2.putText(out, f"Total: Rs {total}", (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (255,255,255), 3)
        cv2.imshow("Rupee Detector", out)

        if cv2.waitKey(1) & 0xFF == 27:
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
