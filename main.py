
'''
!pip install "jax[cuda12_local]==0.4.23" -f https://storage.googleapis.com/jax-releases/jax_cuda_releases.html
!pip install diffusers==0.11.1
!pip install transformers scipy ftfy accelerate
'''
from BgRemover.bg_remover import BgRemover
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
from io import BytesIO
import requests
from BgReplacer import StableDiffusionInPaint

# Example usage
model_path = "/content/gdrive/My Drive"
restore_model = "isnet.pth"

background_remover =BgRemover(model_path, restore_model)

image_url = "https://i5.walmartimages.com/asr/43995148-22bf-4836-b6d3-e8f64a73be54.5398297e6f59fc510e0111bc6ff3a02a.jpeg"

result_image = background_remover.remove_background(image_url)

# result_image is already a PIL Image, no conversion needed
result_pil = result_image 

# Load the original image
original_image = Image.open(BytesIO(requests.get(image_url).content))

# Convert to numpy arrays
original_np = np.array(original_image)
result_np = np.array(result_pil)

# Create mask image (white background, black foreground)
# Assumption: result_image has transparent background where background was removed
mask_np = np.all(result_np[:, :, :3] == 0, axis=-1).astype(np.uint8) * 255  # Background is black in result_image

mask_pil = Image.fromarray(mask_np)

# Display the images
f, ax = plt.subplots(1, 3, figsize=(35, 20))
ax[0].imshow(original_image)  # Original image
ax[1].imshow(result_pil)  # Background removed image
ax[2].imshow(mask_pil, cmap='gray')  # Mask image

ax[0].set_title("Original Image")
ax[1].set_title("Background Removed")
ax[2].set_title("Mask Image")
plt.show()

# Example usage
model_path = "runwayml/stable-diffusion-inpainting"
inpaint_model = StableDiffusionInPaint(model_path)

img_url = "https://raw.githubusercontent.com/CompVis/latent-diffusion/main/data/inpainting_examples/overture-creations-5sI6fQgYIuo.png"
mask_url = "https://raw.githubusercontent.com/CompVis/latent-diffusion/main/data/inpainting_examples/overture-creations-5sI6fQgYIuo_mask.png"
prompt = "A tiger sitting on the bench"

result_image = inpaint_model.inpaint(img_url, mask_url, prompt)
result_image.show()

