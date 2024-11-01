from transformers import AutoProcessor, AutoTokenizer
from transformers import BlipForConditionalGeneration
from transformers import Blip2Processor, Blip2ForConditionalGeneration
from transformers import BartForConditionalGeneration, PegasusForConditionalGeneration
from transformers import VisionEncoderDecoderModel, ViTImageProcessor
from transformers import T5ForConditionalGeneration
from pathlib import Path
from PIL import Image
import torch

device = "cuda" if torch.cuda.is_available() else "cpu"

## COMPUTER VISION MODELS

class GenerateBLIP():
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
    
class GenerateGPT2():
     def __init__(self):
             self.model = VisionEncoderDecoderModel.from_pretrained("nlpconnect/vit-gpt2-image-captioning").to(device)
             self.feature_extractor = ViTImageProcessor.from_pretrained("nlpconnect/vit-gpt2-image-captioning")
             self.tokenizer = AutoTokenizer.from_pretrained("nlpconnect/vit-gpt2-image-captioning")

     def predict(self, image_path: Path):
             image = Image.open(image_path).convert(mode="RGB")
             pixel_values = self.feature_extractor(images=image, return_tensors="pt").pixel_values
             pixel_values = pixel_values.to(device)
             
             output = self.model.generate(pixel_values, max_length=16, num_beams=4)
             predictions = self.tokenizer.batch_decode(output, skip_special_tokens=True)
             
             return predictions[0]

### UNUSED - NOT ENOUGH VRAM TO RUN MODEL

class GenerateBLIP2():
     def __init__(self):
             self.processor = Blip2Processor.from_pretrained("Salesforce/blip2-opt-2.7b")
             self.model = Blip2ForConditionalGeneration.from_pretrained("Salesforce/blip2-opt-2.7b").to(device)
                
     def predict(self, image_path: Path):
             raw_image = Image.open(image_path).convert('RGB')
             inputs = self.processor(raw_image, return_tensors="pt").to(device, torch.int8)
             out = self.model.generate(**inputs)
             return self.processor.decode(out[0], skip_special_tokens=True).strip()
     
### NLP MODELS           
    
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
            summary_ids = self.model.generate(inputs["input_ids"], max_length=100, min_length=50)
            summary = self.tokenizer.batch_decode(summary_ids, skip_special_tokens=True, clean_up_tokenization_spaces=False)[0]
            return summary
    
class GenerateT5():
    def __init__(self):
           self.model = T5ForConditionalGeneration.from_pretrained("t5-base")
           self.tokenizer = AutoTokenizer.from_pretrained("t5-base")  

    def predict(self, text: str):
           inputs = self.tokenizer(f"Summarize: {text}", max_length=1024, return_tensors="pt").input_ids
           summary_ids = self.model.generate(inputs, max_length=100, min_length=50)
           summary = self.tokenizer.decode(summary_ids[0], skip_special_tokens=True)
           return summary