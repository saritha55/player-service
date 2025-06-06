import numpy
from transformers import pipeline

print("NumPy version:", numpy.__version__)

try:
    pipe = pipeline("text-generation", model="TinyLlama/TinyLlama-1.1B-Chat-v1.0")
    result = pipe("Suggest a nickname for a player from Brazil.", max_new_tokens=20)
    print("Result:", result)
except Exception as e:
    print("Error:", e)
