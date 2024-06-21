import numpy as np
from PIL import Image
import torch
from torch.autograd import Variable
from torchvision import transforms
import torch.nn.functional as F
import requests
from io import BytesIO
from BgRemover.data_loader_cache import normalize, im_reader, im_preprocess
from BgRemover.models import *



class GOSNormalize(object):
    '''
    Normalize the Image using torch.transforms
    '''
    def __init__(self, mean=[0.485,0.456,0.406], std=[0.229,0.224,0.225]):
        self.mean = mean
        self.std = std

    def __call__(self,image):
        image = normalize(image,self.mean,self.std)
        return image



class BgRemover:
    def __init__(self, model_path, restore_model, device='cuda' if torch.cuda.is_available() else 'cpu'):
        self.device = device
        self.hypar = self._set_parameters(model_path, restore_model)
        self.net = self._build_model(self.hypar, self.device)
        self.transform = transforms.Compose([GOSNormalize([0.5, 0.5, 0.5], [1.0, 1.0, 1.0])])

    def _set_parameters(self, model_path, restore_model):
        hypar = {}
        hypar["model_path"] = model_path
        hypar["restore_model"] = restore_model
        hypar["interm_sup"] = False
        hypar["model_digit"] = "full"
        hypar["seed"] = 0
        hypar["cache_size"] = [1024, 1024]
        hypar["input_size"] = [1024, 1024]
        hypar["crop_size"] = [1024, 1024]
        hypar["model"] = ISNetDIS()
        return hypar

    def _build_model(self, hypar, device):
        net = hypar["model"]
        if hypar["model_digit"] == "half":
            net.half()
            for layer in net.modules():
                if isinstance(layer, nn.BatchNorm2d):
                    layer.float()
        net.to(device)
        if hypar["restore_model"] != "":
            net.load_state_dict(torch.load(hypar["model_path"] + "/" + hypar["restore_model"], map_location=device))
        net.eval()
        return net

    def _load_image(self, im_path, hypar):
        if im_path.startswith("http"):
            im_path = BytesIO(requests.get(im_path).content)
        im = im_reader(im_path)
        im, im_shp = im_preprocess(im, hypar["cache_size"])
        im = torch.divide(im, 255.0)
        shape = torch.from_numpy(np.array(im_shp))
        return self.transform(im).unsqueeze(0), shape.unsqueeze(0)  # make a batch of image, shape

    def _predict(self, net, inputs_val, shapes_val, hypar, device):
        net.eval()
        inputs_val = inputs_val.type(torch.FloatTensor)
        inputs_val_v = Variable(inputs_val, requires_grad=False).to(device)  # wrap inputs in Variable
        ds_val = net(inputs_val_v)[0]  # list of 6 results
        pred_val = ds_val[0][0, :, :, :]  # B x 1 x H x W    # we want the first one which is the most accurate prediction
        pred_val = torch.squeeze(F.upsample(torch.unsqueeze(pred_val, 0), (shapes_val[0][0], shapes_val[0][1]), mode='bilinear'))
        ma = torch.max(pred_val)
        mi = torch.min(pred_val)
        pred_val = (pred_val - mi) / (ma - mi)  # max = 1
        if device == 'cuda':
            torch.cuda.empty_cache()
        return (pred_val.detach().cpu().numpy() * 255).astype(np.uint8)  # it is the mask we need

    def remove_background(self, image_path):
        image_tensor, orig_size = self._load_image(image_path, self.hypar)
        mask = self._predict(self.net, image_tensor, orig_size, self.hypar, self.device)

        # Load the original image
        if image_path.startswith("http"):
            original_image = Image.open(BytesIO(requests.get(image_path).content)).convert("RGBA")
        else:
            original_image = Image.open(image_path).convert("RGBA")

        # Create the mask image
        mask_image = Image.fromarray(mask).convert("L")

        # Create an image with a transparent background
        background_removed = Image.composite(original_image, Image.new("RGBA", original_image.size), mask_image)

        return background_removed


