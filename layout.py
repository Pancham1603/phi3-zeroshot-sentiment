from pdf2image import convert_from_path
import os, sys
from PIL import Image
import img2pdf
import layoutparser as lp
import cv2
import numpy as np
from sklearn.cluster import KMeans

# Step 1: Convert PDF to PNGs

pdf_path = sys.argv[1]
output_folder = os.path.join(os.path.dirname(pdf_path), 'pdf_layout')
os.makedirs(output_folder, exist_ok=True)

images = convert_from_path(pdf_path, poppler_path=r"C:\Users\Pancham\Downloads\Release-24.07.0-0\poppler-24.07.0\Library\bin")
png_files = []

model = lp.models.Detectron2LayoutModel(config_path=r'C:\Users\Pancham\Desktop\Projects\phi3-zeroshot-sentiment\models\config.yaml',
                                model_path=r"C:\Users\Pancham\Desktop\Projects\phi3-zeroshot-sentiment\models\model_final.pth",
                                 extra_config=["MODEL.ROI_HEADS.SCORE_THRESH_TEST", 0.8],
                                 label_map={0: "Text", 1: "Title", 2: "List", 3:"Table", 4:"Figure"})

# model = lp.AutoLayoutModel('lp://EfficientDete/PubLayNet')

def clean_layout(layout):
    text_blocks = lp.Layout([b for b in layout if b.type=='Text'])
    figure_blocks = lp.Layout([b for b in layout if b.type=='Figure'])
    text_blocks = lp.Layout([b for b in text_blocks \
                   if not any(b.is_in(b_fig) for b_fig in figure_blocks)])
    h, w = image.shape[:2]

    left_interval = lp.Interval(0, w/2*1.05, axis='x').put_on_canvas(image)

    left_blocks = text_blocks.filter_by(left_interval, center=True)
    left_blocks.sort(key = lambda b:b.coordinates[1], inplace=True)
    # The b.coordinates[1] corresponds to the y coordinate of the region
    # sort based on that can simulate the top-to-bottom reading order 
    right_blocks = lp.Layout([b for b in text_blocks if b not in left_blocks])
    right_blocks.sort(key = lambda b:b.coordinates[1], inplace=True)

    # And finally combine the two lists and add the index
    text_blocks = lp.Layout([b.set(id = idx) for idx, b in enumerate(left_blocks + right_blocks)])
    return text_blocks

def get_dominant_color(image, k=1):
    pixels = image.reshape((-1, 3))
    kmeans = KMeans(n_clusters=k, n_init=10)
    kmeans.fit(pixels)
    dominant_color = kmeans.cluster_centers_[0]
    return dominant_color

def is_dominant_color_black(image, threshold=50):
    dominant_color = get_dominant_color(image, k=1)
    dominant_color = [int(c) for c in dominant_color]
    return all(c < threshold for c in dominant_color)

def force_contrast_black(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    
    if is_dominant_color_black(cv2.cvtColor(binary, cv2.COLOR_GRAY2BGR)):
        return Image.fromarray(binary)
    else:
        _, binary = cv2.threshold(binary, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
        return Image.fromarray(binary)

for i, image in enumerate(images):
    # pillow images to opencv
    image = cv2.cvtColor(cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR), cv2.COLOR_BGR2RGB)
    image = force_contrast_black(image)
    png_file = os.path.join(output_folder, f'page_{i+1}.png')
    # layout = clean_layout(model.detect(image))
    # layout_image = lp.draw_box(image, layout, box_width=5, show_element_id=True)
    layout = model.detect(image)
    layout_image = lp.draw_box(image, layout, box_width=7)
    layout_image.save(png_file)
    png_files.append(png_file)
    print(png_file)


# Step 3: Merge PNGs Back into a PDF
merged_pdf_path = os.path.join(output_folder, 'merged_output.pdf')

with open(merged_pdf_path, 'wb') as f:
    f.write(img2pdf.convert(png_files))

print(f'Merged PDF saved to {merged_pdf_path}')
