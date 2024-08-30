import torch
import os
from clipcap import GenerateClipCap
from pathlib import Path
from openai import OpenAI
from transformers import pipeline

device = 'cuda' if torch.cuda.is_available() else 'cpu'
curr_path = Path(__file__).parent.absolute()

def create_alttext(text: str, img_path: Path):
    summarizer = pipeline("summarization", model="facebook/bart-large-cnn", device=device)
    summarized_text = summarizer(text, max_length=100, min_length=50)[0]['summary_text']
    print(f"Summarized Text: {summarized_text}")

    del summarizer
    torch.cuda.empty_cache()

    vision_transformer = GenerateClipCap()
    image_caption = vision_transformer.predict(img_path, 'coco', False)
    print(f"Image Caption: {image_caption}")

    del vision_transformer
    torch.cuda.empty_cache()

    client = OpenAI(
            api_key = "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"
    )
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You have two inputs - Summary Context and Image Caption. Create an alt-text from these two inputs. Max character limit is 125 characters."},
            {
                "role": "user",
                "content": f"SUMMARY CONTEXT: {summarized_text}. IMAGE CAPTION: {image_caption}"
            }
        ]
    )

    print(f"Generated Alt-Text: {completion.choices[0].message.content}")

    return completion.choices[0].message.content
