import fitz
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

pdf_path = input("Pdf path : ")
doc = fitz.open(pdf_path)
page = doc[0]
pix = page.get_pixmap()
image = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
image_np = np.array(image)

coords = []

def onclick(event):
    """Store clicked coordinates and close after 2 clicks."""
    if event.xdata is not None and event.ydata is not None:
        if len(coords) < 2:
            coords.append((event.xdata, event.ydata))
            print(f"Point {len(coords)}: {coords[-1]}")
        if len(coords) == 2:
            plt.close()
fig, ax = plt.subplots()
ax.imshow(image_np)
ax.set_title("Click two points: Top-left & Bottom-right")
fig.canvas.mpl_connect('button_press_event', onclick)

plt.show()
if len(coords) == 2:
    x0, y0 = coords[0]
    x1, y1 = coords[1]
    print(f"Bounding Box: ({x0}, {y0}, {x1}, {y1})")
