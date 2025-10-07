# 🚀 Deployment Guide for Streamlit Cloud

This guide will help you deploy the USPTO Opposition Trademark Scraper to Streamlit Cloud.

## Prerequisites

- A GitHub account
- USPTO API Key
- Anthropic (Claude) API Key

## Step-by-Step Deployment

### 1. Prepare Your Repository

Your repository is already configured and ready at:
```
https://github.com/Nagavenkatasai7/uspto.git
```

### 2. Sign in to Streamlit Cloud

1. Go to https://streamlit.io/cloud
2. Click **"Sign in"** or **"Sign up"**
3. Choose **"Continue with GitHub"**
4. Authorize Streamlit to access your GitHub account

### 3. Create a New App

1. Click the **"New app"** button
2. In the deployment settings:
   - **Repository**: `Nagavenkatasai7/uspto`
   - **Branch**: `main`
   - **Main file path**: `web_app.py`
   - **App URL** (optional): Choose a custom URL or use the auto-generated one

### 4. Configure Secrets (API Keys)

⚠️ **IMPORTANT**: You must add your API keys before deploying!

1. Click **"Advanced settings"** at the bottom
2. In the **"Secrets"** section, paste the following (with your actual keys):

```toml
USPTO_API_KEY = "your_actual_uspto_api_key_here"
ANTHROPIC_API_KEY = "your_actual_anthropic_api_key_here"
```

**Example:**
```toml
USPTO_API_KEY = "22tljOtfx4tyI7uld3rp2iRqy2UsAvUE"
ANTHROPIC_API_KEY = "sk-ant-api03-abc123xyz..."
```

### 5. Deploy

1. Click **"Deploy!"**
2. Wait 2-3 minutes for the app to build and deploy
3. Your app will be live at: `https://[your-app-name].streamlit.app`

## Updating Your App

Streamlit Cloud automatically redeploys when you push changes to GitHub:

```bash
# Make your changes locally
git add .
git commit -m "Your update message"
git push origin main
```

The app will automatically redeploy within 1-2 minutes.

## Managing Secrets

To update your API keys after deployment:

1. Go to https://share.streamlit.io/
2. Click on your app
3. Click the **⋮** menu (three dots)
4. Select **"Settings"**
5. Go to **"Secrets"**
6. Update your keys and click **"Save"**

## Troubleshooting

### "No module named..." errors

- Check that all dependencies are in `requirements.txt`
- Streamlit Cloud automatically installs from this file

### "API Key not found" errors

- Verify secrets are properly formatted in TOML:
  ```toml
  KEY_NAME = "value_in_quotes"
  ```
- No spaces before the equals sign
- Values must be in quotes

### App won't start

- Check the **"Manage app"** logs for error messages
- Verify `web_app.py` is the correct entry point
- Ensure all Python syntax is valid

### System dependencies (tesseract)

The `packages.txt` file contains system dependencies:
```
tesseract-ocr
libtesseract-dev
```

These are automatically installed by Streamlit Cloud.

## Resource Limits

**Streamlit Cloud Free Tier:**
- 1 GB RAM
- 1 CPU core
- 1 app can run at a time
- Sleeps after 7 days of inactivity

If your app needs more resources, consider upgrading or using alternative hosting.

## Alternative Deployment Options

If Streamlit Cloud doesn't meet your needs:

1. **Heroku**: Python app hosting with free tier
2. **Railway.app**: Modern deployment platform
3. **Google Cloud Run**: Containerized deployments
4. **AWS EC2**: Full control, requires more setup

## Support

- Streamlit Docs: https://docs.streamlit.io/streamlit-community-cloud
- Streamlit Forum: https://discuss.streamlit.io/
- GitHub Issues: https://github.com/Nagavenkatasai7/uspto/issues

---

**🎉 That's it! Your app should now be live and accessible to anyone with the URL.**

