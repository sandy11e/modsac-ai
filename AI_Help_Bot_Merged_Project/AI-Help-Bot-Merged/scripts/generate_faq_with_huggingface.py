# generate_faq_with_huggingface.py

from transformers import pipeline
import json
import os

# Load a local Hugging Face model for Q&A
generator = pipeline("text2text-generation", model="google/flan-t5-base")

# Your input FAQ questions
faq_questions = [
    "What is MOSDAC?",
    "How can I download satellite images?",
    "Who operates the MOSDAC portal?",
    "What file types are supported?",
    "How to register on MOSDAC?"
]

# Generate answers from the model
faqs = []
for question in faq_questions:
    print(f"Generating answer for: {question}")
    try:
        prompt = f"Answer the following question about MOSDAC: {question}"
        response = generator(prompt, max_new_tokens=100, do_sample=True)[0]['generated_text']
        faqs.append({"question": question, "answer": response.strip()})
    except Exception as e:
        faqs.append({"question": question, "answer": f"⚠️ Error: {e}"})

# Save to data/processed/faqs.json
os.makedirs("data/processed", exist_ok=True)
with open("data/processed/faqs.json", "w") as f:
    json.dump(faqs, f, indent=2)

print("✅ FAQs generated and saved using Hugging Face model")
