# Naya file banao — upload_model.py
from huggingface_hub import HfApi

api = HfApi()

# Repo banao
api.create_repo(repo_id="scamshield-job-fraud-detector", private=False)

# Model upload karo
api.upload_folder(
    folder_path="models/scamshield_model",
    repo_id="muskii2004/scamshield-job-fraud-detector",
    repo_type="model"
)

print("✅ Model uploaded to HuggingFace Hub!")