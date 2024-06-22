import inspect
from typing import List, Optional, Union

import numpy as np
import torch

import PIL
from diffusers import StableDiffusionInpaintPipeline

import requests
from io import BytesIO

class StableDiffusionInPaint:
    def __init__(self, model_path: str, device: str = "cuda", torch_dtype=torch.float16):
        self.device = device
        self.pipe = StableDiffusionInpaintPipeline.from_pretrained(
            model_path,
            torch_dtype=torch_dtype,
        ).to(self.device)

    def download_image(self, url: str) -> PIL.Image.Image:
        response = requests.get(url)
        return PIL.Image.open(BytesIO(response.content)).convert("RGB")

    def image_grid(self, imgs: List[PIL.Image.Image], rows: int, cols: int) -> PIL.Image.Image:
        assert len(imgs) == rows * cols

        w, h = imgs[0].size
        grid = PIL.Image.new('RGB', size=(cols * w, rows * h))
        grid_w, grid_h = grid.size

        for i, img in enumerate(imgs):
            grid.paste(img, box=(i % cols * w, i // cols * h))
        return grid

    def inpaint(self, image: Union[str, PIL.Image.Image], mask: Union[str, PIL.Image.Image], prompt: str, guidance_scale: float = 7.5, num_samples: int = 3, seed: int = 0) -> List[PIL.Image.Image]:
        if isinstance(image, str):
            image = self.download_image(image).resize((512, 512))
        else:
            image = image.resize((512, 512))

        if isinstance(mask, str):
            mask_image = self.download_image(mask).resize((512, 512))
        else:
            mask_image = mask.resize((512, 512))

        generator = torch.Generator(device=self.device).manual_seed(seed)

        images = self.pipe(
            prompt=prompt,
            image=image,
            mask_image=mask_image,
            guidance_scale=guidance_scale,
            generator=generator,
            num_images_per_prompt=num_samples,
        ).images

        images.insert(0, image)
        return images