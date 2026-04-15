from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import os

MODEL_PATH = os.path.join(os.path.dirname(__file__), "banglabert_bias_model")

LABEL_MAP = {
    0: ("Government-Favorable", "#22c55e"),
    1: ("Neutral", "#94a3b8"),
    2: ("Government-Critic", "#ef4444"),
}

print("Loading BanglaBERT model...")
tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)
model = AutoModelForSequenceClassification.from_pretrained(MODEL_PATH)
model.eval()
print("Model ready.")

def predict_bias(headline: str):
    inputs = tokenizer(
        headline,
        return_tensors="pt",
        truncation=True,
        padding=True,
        max_length=128
    )

    with torch.no_grad():
        outputs = model(**inputs)

    probs = torch.softmax(outputs.logits, dim=1).squeeze()
    pred = torch.argmax(probs).item()
    confidence = round(probs[pred].item() * 100, 2)
    prob_list = [round(p.item() * 100, 2) for p in probs]

    label, color = LABEL_MAP[pred]
    return label, color, confidence, prob_list
