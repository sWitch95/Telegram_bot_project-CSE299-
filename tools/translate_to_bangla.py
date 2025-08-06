import pandas as pd
from deep_translator import GoogleTranslator
from tqdm import tqdm
import re

def clean(text):
    return re.sub(r'\s+', ' ', str(text)).strip()

def translate_to_bangla(text):
    try:
        return GoogleTranslator(source='en', target='bn').translate(text)
    except:
        return text  # fallback if translation fails

# Load original CSV
df = pd.read_csv("data/medicine_data.csv")

# Columns to translate (you can change based on your CSV structure)
columns_to_translate = [
    "generic name",
    "indication description",
    "dosage description",
    "side effects description",
    "precautions description",
    "pregnancy and lactation description"
]

# Add Bangla translations as new columns
for col in tqdm(columns_to_translate, desc="🔁 Translating to Bangla"):
    new_col = f"{col} (bn)"
    df[new_col] = df[col].apply(lambda x: translate_to_bangla(clean(x)))

# Save enriched bilingual CSV
df.to_csv("data/medicine_data_bilingual.csv", index=False)
print("✅ Bilingual CSV created: data/medicine_data_bilingual.csv")
