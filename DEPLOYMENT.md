# Deployment

## GitHub

From PowerShell in this folder:

```powershell
git init
git add .
git commit -m "Initial AI hotel recommendation platform"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPOSITORY.git
git push -u origin main
```

Replace the remote URL with the repository URL created on GitHub.

## Streamlit Community Cloud

1. Push this project to GitHub.
2. Open https://share.streamlit.io/.
3. Select the repository and the `main` branch.
4. Set the main file to `app.py`.
5. Deploy.

The application uses the `requirements.txt` file automatically.

## Kaggle secrets

For a Kaggle dataset, add these in Streamlit Cloud under App settings > Secrets:

```toml
KAGGLE_DATASET_SLUG = "owner/dataset-name"
```

For a local CSV, use `KAGGLE_DATASET_PATH` locally. Do not commit `kaggle.json` or API tokens.
