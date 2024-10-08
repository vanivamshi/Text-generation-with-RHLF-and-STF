# -*- coding: utf-8 -*-
"""Text generation with RHLF and STF.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/16uGS39Zr9tC1o4HwlInHCUk8jmIUTssx
"""

pip install transformers torch

pip install rouge-score

from transformers import GPT2LMHeadModel, GPT2Tokenizer
import time
import psutil
import torch
from nltk.translate.bleu_score import sentence_bleu
from rouge_score import rouge_scorer

# Load pre-trained model and tokenizer
model_name = "gpt2"
model = GPT2LMHeadModel.from_pretrained(model_name)
tokenizer = GPT2Tokenizer.from_pretrained(model_name)

# Function to measure memory usage
def get_memory_usage():
    process = psutil.Process()
    return process.memory_info().rss / 1024 / 1024  # Convert bytes to MB

# Function to generate text
def generate_text(prompt, max_length=100, temperature=1.0, top_k=50, repetition_penalty=1.2, length_penalty=1.0):
    # Encode the prompt
    inputs = tokenizer(prompt, return_tensors="pt")
    input_ids = inputs.input_ids

    # Generate text
    outputs = model.generate(
        input_ids,
        max_length=max_length,
        temperature=temperature,
        top_k=top_k,
        repetition_penalty=repetition_penalty,
        length_penalty=length_penalty,
        num_return_sequences=1
    )

    # Decode the generated text
    text = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return text

# Function to calculate BLEU score
def calculate_bleu_score(reference, generated):
    reference = reference.split()
    generated = generated.split()
    return sentence_bleu([reference], generated)

# Function to calculate ROUGE score
def calculate_rouge_score(reference, generated):
    scorer = rouge_scorer.RougeScorer(['rouge1', 'rouge2', 'rougeL'], use_stemmer=True)
    scores = scorer.score(reference, generated)
    return scores

# Function to calculate efficiency and quality metrics
def calculate_metrics(prompt, reference, max_length=100, temperature=1.0, top_k=50, repetition_penalty=1.2, length_penalty=1.0):
    # Track memory usage before generation
    mem_before = get_memory_usage()

    start_time = time.time()

    # Generate text
    generated_text = generate_text(prompt, max_length, temperature, top_k, repetition_penalty, length_penalty)

    end_time = time.time()

    # Track memory usage after generation
    mem_after = get_memory_usage()

    time_taken = end_time - start_time
    num_tokens = len(tokenizer.tokenize(generated_text))

    # Calculate BLEU and ROUGE scores
    bleu_score = calculate_bleu_score(reference, generated_text)
    rouge_scores = calculate_rouge_score(reference, generated_text)

    # Print metrics
    print("Configuration:")
    print(f"Temperature: {temperature}")
    print(f"Top-k: {top_k}")
    print(f"Repetition Penalty: {repetition_penalty}")
    print(f"Length Penalty: {length_penalty}")
    print()

    print("Metrics:")
    print(f"Time taken: {time_taken:.4f} seconds")
    print(f"Memory usage: {mem_after - mem_before:.2f} MB")
    print(f"Number of tokens generated: {num_tokens}")
    print(f"BLEU score: {bleu_score:.4f}")
    print(f"ROUGE scores: {rouge_scores}")
    print()

# Sample prompt and reference
prompt = "Once upon a time"
reference = "Once upon a time in a land far away"

# A/B Testing configurations
configurations = [
    {"temperature": 0.7, "top_k": 50, "repetition_penalty": 1.2, "length_penalty": 1.0},
    {"temperature": 1.0, "top_k": 0, "repetition_penalty": 1.0, "length_penalty": 1.0},
    {"temperature": 1.2, "top_k": 50, "repetition_penalty": 1.5, "length_penalty": 0.8},
]

# Perform A/B Testing
for config in configurations:
    print("Testing configuration:", config)
    calculate_metrics(prompt, reference, temperature=config["temperature"], top_k=config["top_k"], repetition_penalty=config["repetition_penalty"], length_penalty=config["length_penalty"])