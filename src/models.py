from transformers import AutoProcessor, BlipForConditionalGeneration
from transformers import AutoTokenizer, BartForConditionalGeneration, PegasusForConditionalGeneration
from pathlib import Path
from PIL import Image
import torch

device = "cuda" if torch.cuda.is_available() else "cpu"

class GenerateBLIP2():
    def __init__(self): 
            self.processor = AutoProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
            self.model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base").to(device)
    
    def predict(self, image_path: Path):
            image = Image.open(image_path)
            inputs = self.processor(images=image, return_tensors="pt").to(device)
            pixel_values = inputs.pixel_values
            generated_ids = self.model.generate(pixel_values=pixel_values, max_length=50).to(device)
            generated_caption = self.processor.batch_decode(generated_ids, skip_special_tokens=True)[0]
            return generated_caption   
    
class GenerateBART():
    def __init__(self):
            self.model = BartForConditionalGeneration.from_pretrained("facebook/bart-large-cnn")
            self.tokenizer = AutoTokenizer.from_pretrained("facebook/bart-large-cnn")

    def predict(self, text: str):
            inputs = self.tokenizer([text], max_length=1024, return_tensors="pt")
            summary_ids = self.model.generate(inputs["input_ids"], num_beams=2, min_length=50, max_length=100)
            summary = self.tokenizer.batch_decode(summary_ids, skip_special_tokens=True, clean_up_tokenization_spaces=False)[0]
            return summary
    
class GeneratePEGASUS():
    def __init__(self):
            self.model = PegasusForConditionalGeneration.from_pretrained("google/pegasus-xsum")
            self.tokenizer = AutoTokenizer.from_pretrained("google/pegasus-xsum")

    def predict(self, text: str):
            inputs = self.tokenizer(text, max_length=1024, return_tensors="pt")
            summary_ids = self.model.generate(inputs["input_ids"])
            summary = self.tokenizer.batch_decode(summary_ids, skip_special_tokens=True, clean_up_tokenization_spaces=False)[0]
            return summary