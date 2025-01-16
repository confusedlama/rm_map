import cv2
import numpy as np


# beispielbild laden
img = cv2.imread("Drawing.png")
gray = 255 - cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# blurren um es ein wenig schöner zu machen und negativ damit es ein bisschen intuitiver ist
for i in range(20):
    gray = cv2.GaussianBlur(gray, ksize=(5, 5), sigmaX=20)

# flutlevel erstellen
flood_levels = np.linspace(0, 100, 10)

# flutkarten erstellen
for level in flood_levels:
    ### das was ab hier passiert ist das interessante
    # finde alle pixel mit werten die niedriger als das flutlevel sind 
    flood_mask = cv2.inRange(gray, lowerb=0, upperb=level)

    # konturen der flecken auf der flut maske finden
    contours, hierarchy = cv2.findContours(flood_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # finde kontur in der ein ankerpunkt liegt von dem aus sich das wasser ausbreiten kann (den ankerpunkt hab ich händisch rausgesucht die karte bleibt ja eig gleich)
    anchor_point = (697, 697)
    water_contour = []
    for contour in contours:
        if cv2.pointPolygonTest(contour, anchor_point, False) >= 0:
            water_contour = contour
            break
    ### ab hier kommt nur noch was um das bild anzuzeigen

    # draw water contour on blurred image
    temp_img = img
    if water_contour.any():
        cv2.drawContours(temp_img, [water_contour], color=(150, 15, 15), contourIdx=-1, thickness=cv2.FILLED)
    
    cv2.imshow(f"Water Level at {level} out of 100", temp_img)
    cv2.waitKey()
    