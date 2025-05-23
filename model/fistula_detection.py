import numpy as np
import cv2
import os

# Define the path to the image file
script_dir = os.path.dirname(os.path.abspath(__file__))
image_path = os.path.join(script_dir, "handimage4.png")
output_dir = os.path.join(script_dir, "output")

# Ensure that the output directory exists
os.makedirs(output_dir, exist_ok=True)
# #Preprocessing the images

def morphology_diff(contrast_green, clahe):
    # 1st
    open1 = cv2.morphologyEx(contrast_green, cv2.MORPH_OPEN, cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(5,5)), iterations=1)
    close1 = cv2.morphologyEx(open1, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(5,5)), iterations=1)
    # 2nd
    open2 = cv2.morphologyEx(close1, cv2.MORPH_OPEN, cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(11,11)), iterations=1)
    close2 = cv2.morphologyEx(open2, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(11,11)), iterations=1)
    # 3rd
    open3 = cv2.morphologyEx(close2, cv2.MORPH_OPEN, cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(23,23)), iterations=1)
    close3 = cv2.morphologyEx(open3, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(23,23)), iterations=1)

    contrast_morph = cv2.subtract(close3, contrast_green)
    return clahe.apply(contrast_morph)

# Noise Removal

def remove_noise(morph_image):
    ret, thr = cv2.threshold(morph_image, 15, 255, cv2.THRESH_BINARY)
    mask = np.ones(morph_image.shape[:2], dtype="uint8") * 255
    # Correct line:
    contours, hierarchy = cv2.findContours(thr.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    for cnt in contours:
        if cv2.contourArea(cnt) <= 200:
            cv2.drawContours(mask, [cnt], -1, 0, -1)
    im = cv2.bitwise_and(morph_image, morph_image, mask=mask)
    ret, fin_thr = cv2.threshold(im, 15, 255, cv2.THRESH_BINARY_INV)
    new_img = cv2.erode(fin_thr, cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(3,3)), iterations=1)
    return new_img

# Blob Removal

def remove_blob(clear_image, org_image):
    fundus_eroded = cv2.bitwise_not(clear_image)
    xmask = np.ones(org_image.shape[:2], dtype="uint8") * 255
    xcontours, xhierarchy = cv2.findContours(fundus_eroded.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    for cnt in xcontours:
        shape = "unidentified"
        peri = cv2.arcLength(cnt, True)
        approx = cv2.approxPolyDP(cnt, 0.04 * peri, False)
        if len(approx) > 4 and cv2.contourArea(cnt) <= 3000 and cv2.contourArea(cnt) >= 100:
            shape = "circle"
        else:
            shape = "veins"
        if(shape == "circle"):
            cv2.drawContours(xmask, [cnt], -1, 0, -1)

    finimage = cv2.bitwise_and(fundus_eroded, fundus_eroded, mask=xmask)
    blood_vessels = cv2.bitwise_not(finimage)
    return blood_vessels

# Vein detection

def detect_vessel(org_image):
    copy_org_image = org_image.copy()
    blue, green, red = cv2.split(org_image)
    clahe = cv2.createCLAHE(clipLimit=5.0, tileGridSize=(8,8))
    contrast_green = clahe.apply(green)
    morph_image = morphology_diff(contrast_green, clahe)
    clear_image = remove_noise(morph_image)
    fin_image = remove_blob(clear_image, org_image)
    i = 0
    j = 0
    for gr, fin in zip(green, fin_image):
        for g, f in zip(gr, fin):
            if(f == 0):
                green[i][j] = 255
            j = j + 1
        j = 0
        i = i + 1
    return fin_image, cv2.merge((blue, green, red))

if __name__ == "__main__":
    # Load the image file
    org_image = cv2.imread(image_path)
    if org_image is None:
        print(f"Error: Image file '{image_path}' not found.")
    else:
        # Perform vessel detection
        raw_vessel, vessel_image = detect_vessel(org_image)
        # Save the results
        out_name = os.path.splitext(os.path.basename(image_path))[0]
        raw_vessel_path = os.path.join(output_dir, f"{out_name}_raw_vessel.jpg")
        vessel_image_path = os.path.join(output_dir, f"{out_name}_vessel_image.jpg")
        cv2.imwrite(raw_vessel_path, raw_vessel)
        cv2.imwrite(vessel_image_path, vessel_image)
        
        print("Output files saved successfully.")