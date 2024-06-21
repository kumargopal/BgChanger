from background_remover import BackgroundRemover
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
from io import BytesIO
import requests


# Example usage
model_path = "/content/drive/My Drive"
restore_model = "isnet.pth"

background_remover = BackgroundRemover(model_path, restore_model)

image_url = "https://i5.walmartimages.com/asr/43995148-22bf-4836-b6d3-e8f64a73be54.5398297e6f59fc510e0111bc6ff3a02a.jpeg"

result_image = background_remover.remove_background(image_url)

# Display the original and result image
f, ax = plt.subplots(1, 2, figsize=(35, 20))
ax[0].imshow(np.array(Image.open(BytesIO(requests.get(image_url).content))))  # Original image
ax[1].imshow(result_image)  # Background removed image

ax[0].set_title("Original Image")
ax[1].set_title("Background Removed")

plt.show()