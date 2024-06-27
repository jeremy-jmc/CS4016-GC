import os
import shutil
from datasets import load_dataset, DatasetDict
from transformers import AutoImageProcessor, AutoModelForImageClassification, TrainingArguments, Trainer

# Desactivar uso de GPU
os.environ["CUDA_VISIBLE_DEVICES"] = ""
os.environ["DISABLE_MLFLOW_INTEGRATION"] = "TRUE"

checkpoint = "nateraw/vit-base-beans"
image_processor = AutoImageProcessor.from_pretrained(checkpoint)

train_dir = "./casting_data/train"
test_dir = "./casting_data/test"

# Asegurarse de que el directorio de salida y el directorio mlruns están limpios
output_dir = "my_vit_model"
mlruns_dir = "mlruns"
trash_dir = os.path.join(mlruns_dir, ".trash")

# Function to ensure directory exists and is empty
def ensure_empty_dir(directory):
    if os.path.exists(directory):
        shutil.rmtree(directory)
    os.makedirs(directory, exist_ok=True)

# Ensure the necessary directories are empty
ensure_empty_dir(output_dir)
ensure_empty_dir(mlruns_dir)
if os.path.exists(trash_dir):
    shutil.rmtree(trash_dir)

dataset = DatasetDict()
train_dataset = load_dataset('imagefolder', data_dir=train_dir, split='train')
train_dataset = train_dataset.rename_column("label", "labels")
dataset['train'] = train_dataset

test_dataset = load_dataset('imagefolder', data_dir=test_dir, split='train')
test_dataset = test_dataset.rename_column("label", "labels")
dataset['test'] = test_dataset

def preprocess_function(examples):
    images = [image_processor(image.convert("RGB"), return_tensors="pt")["pixel_values"].squeeze(0) for image in examples["image"]]
    examples["pixel_values"] = images
    return examples

dataset['train'] = dataset['train'].map(preprocess_function, batched=True)
dataset['test'] = dataset['test'].map(preprocess_function, batched=True)

dataset['train'] = dataset['train'].remove_columns(["image"])
dataset['test'] = dataset['test'].remove_columns(["image"])

labels = ['def_front', 'ok_front']
id2label = {id: label for id, label in enumerate(labels)}
label2id = {label: id for id, label in enumerate(labels)}

model = AutoModelForImageClassification.from_pretrained(
    checkpoint,
    num_labels=len(labels),
    id2label=id2label,
    label2id=label2id,
)

training_args = TrainingArguments(
    output_dir=output_dir,
    remove_unused_columns=False,
    evaluation_strategy="epoch",
    save_strategy="epoch",
    learning_rate=5e-5,
    per_device_train_batch_size=16,
    gradient_accumulation_steps=4,
    per_device_eval_batch_size=16,
    num_train_epochs=3,
    warmup_ratio=0.1,
    logging_steps=10,
    metric_for_best_model="accuracy",
)

# Crear el Trainer sin MLflow
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=dataset["train"],
    eval_dataset=dataset["test"],
    tokenizer=image_processor,
)

trainer.train()
