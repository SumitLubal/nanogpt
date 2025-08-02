import torch
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    TextDataset,
    DataCollatorForLanguageModeling,
    Trainer,
    TrainingArguments,
)

# --- 1. Configuration for RTX 3080 ---

# The name of the pre-trained model we want to fine-tune
MODEL_NAME = "gpt2"

# The path to your training data
TRAIN_FILE = "input.txt"

# The directory where the fine-tuned model will be saved
OUTPUT_DIR = "./fine-tuned-model"

# Training parameters optimized for a 10GB/12GB GPU
TRAIN_BATCH_SIZE = 2  # Reduced from 4
EVAL_BATCH_SIZE = 2   # Reduced from 4
GRADIENT_ACCUMULATION_STEPS = 8 # Simulate a larger batch size (2 * 8 = 16)
NUM_TRAIN_EPOCHS = 3
SAVE_STEPS = 10_000
LEARNING_RATE = 5e-5

# --- 2. Load Tokenizer and Model ---

print("Loading tokenizer and model...")
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForCausalLM.from_pretrained(MODEL_NAME)

# --- 3. Prepare the Dataset ---

print("Preparing dataset...")
# Load the text file into a dataset object
train_dataset = TextDataset(
    tokenizer=tokenizer,
    file_path=TRAIN_FILE,
    block_size=128  # A moderate block size to manage memory
)

# A data collator is used to form batches of data for training
data_collator = DataCollatorForLanguageModeling(
    tokenizer=tokenizer,
    mlm=False  # We are not doing masked language modeling
)

# --- 4. Set Up the Trainer with Optimizations ---

print("Setting up the trainer...")
# Define the training arguments for the Trainer
training_args = TrainingArguments(
    output_dir=OUTPUT_DIR,
    overwrite_output_dir=True,
    num_train_epochs=NUM_TRAIN_EPOCHS,
    per_device_train_batch_size=TRAIN_BATCH_SIZE,
    per_device_eval_batch_size=EVAL_BATCH_SIZE,
    gradient_accumulation_steps=GRADIENT_ACCUMULATION_STEPS,
    learning_rate=LEARNING_RATE,
    save_steps=SAVE_STEPS,
    save_total_limit=2,
    fp16=True,  # Enable mixed-precision training
)

# Instantiate the Trainer, which will handle the training loop
trainer = Trainer(
    model=model,
    args=training_args,
    data_collator=data_collator,
    train_dataset=train_dataset,
)

# --- 5. Train the Model ---

print("Starting training...")
trainer.train()
print("Training finished.")

# --- 6. Save the Fine-Tuned Model ---

print("Saving the fine-tuned model...")
trainer.save_model()
tokenizer.save_pretrained(OUTPUT_DIR)
print(f"Model saved to {OUTPUT_DIR}")

# --- 7. Run Inference ---

print("\n--- Running Inference ---")

# Load the fine-tuned model and tokenizer for inference
print("Loading fine-tuned model for inference...")
model = AutoModelForCausalLM.from_pretrained(OUTPUT_DIR)
tokenizer = AutoTokenizer.from_pretrained(OUTPUT_DIR)

# Set the device to GPU
device = torch.device("cuda")
model.to(device)

# Get a prompt from the user
prompt = input("Enter a prompt to generate text (or type 'exit' to quit): ")

# Generate text based on the prompt
while prompt.lower() != "exit":
    # Encode the prompt into token IDs
    input_ids = tokenizer.encode(prompt, return_tensors="pt").to(device)

    # Generate text using the model
    output = model.generate(
        input_ids,
        max_length=150,
        num_return_sequences=1,
        no_repeat_ngram_size=2,
        pad_token_id=tokenizer.eos_token_id,
        attention_mask=torch.ones_like(input_ids) # Explicitly create attention_mask
    )

    # Decode the generated token IDs back to text
    generated_text = tokenizer.decode(output[0], skip_special_tokens=True)

    print("\nGenerated Text:")
    print(generated_text)

    # Get the next prompt
    prompt = input("\nEnter a new prompt (or type 'exit' to quit): ")

print("Inference finished.")