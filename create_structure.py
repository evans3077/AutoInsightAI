import os

files_to_create = [
    "main.py",
    "requirements.txt",
    ".env",
    ".gitignore",
    "README.md",
    "app/__init__.py",
    "backend/__init__.py",
    "core/__init__.py",
    "data/__init__.py",
    "models/__init__.py",
    "scripts/__init__.py",
    "tests/__init__.py",
    "utils/__init__.py",
    "notebooks/__init__.py",
    "core/config/settings.py",
    "core/security/auth.py",
    "backend/api/routes.py",
    "backend/api/controllers.py",
    "backend/auth/login.py",
    "backend/auth/register.py",
    "backend/db/database.py",
    "backend/ml/pipeline.py",
    "backend/scheduler/tasks.py",
    "backend/services/video_processor.py",
    "backend/services/insight_generator.py",
    "models/feature_extractors/image_features.py",
    "models/feature_extractors/text_features.py",
    "models/llm/predictor.py",
    "models/vision/vision_model.py",
    "scripts/setup/install_dependencies.py",
    "scripts/setup/check_requirements.py",
    "scripts/maintenance/cleanup.py",
    "scripts/maintenance/backup.py",
    "utils/helpers/common.py",
    "utils/serializers/json_serializer.py",
    "utils/validators/input_validator.py",
    "tests/test_api.py",
    "tests/test_models.py",
    "tests/test_utils.py",
    "notebooks/experiments/insight_tuning.ipynb",
    "notebooks/datasets/preprocess_data.ipynb"
]

def create_files(files):
    for file_path in files:
        # Get directory name (if any)
        dir_name = os.path.dirname(file_path)
        
        # Only create directory if it's not empty (like "main.py" has no directory)
        if dir_name:
            os.makedirs(dir_name, exist_ok=True)

        # Create empty file
        if not os.path.exists(file_path):
            with open(file_path, "w") as f:
                pass
            print(f"✅ Created: {file_path}")
        else:
            print(f"⚠️ Already exists: {file_path}")

if __name__ == "__main__":
    print("📁 Creating AutoInsightAI project structure...")
    create_files(files_to_create)
    print("\n✅ All files and folders created successfully.")
