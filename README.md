# BgChanger

BgChanger is a project that leverages advanced AI models to remove and replace backgrounds in images. It combines background removal using DIS and inpainting with Stable Diffusion.

## Background Removal (BgRemover)

BgRemover uses the DIS model to remove backgrounds from images.

Repository: [DIS Background Remover](https://github.com/xuebinqin/DIS)

## Background Replacement (BgReplacer)

BgReplacer employs Stable Diffusion Inpainting to replace backgrounds in images.

Repository: [Stable Diffusion Inpainting](https://huggingface.co/runwayml/stable-diffusion-inpainting)

## Results

Examples of background removal and replacement:
- ![Shoe Result](shoe_result.png)
- ![Keyboard Result](keyboard_result.png)

## How to Use

```bash
git clone https://github.com/kumargopal/BgChanger.git
cd BgChanger
open BgChanger.ipynb in Google Colab