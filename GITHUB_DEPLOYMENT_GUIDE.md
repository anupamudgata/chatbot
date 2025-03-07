# GitHub and Streamlit Cloud Deployment Guide

## Step 1: Create a GitHub Repository

1. Go to [GitHub New Repository page](https://github.com/new)
2. Name your repository (e.g., 'openai-chatbot')
3. Choose public or private visibility
4. Do NOT initialize with README, .gitignore, or license (since you already have these files)
5. Click 'Create repository'

## Step 2: Connect Your Local Repository

After creating the repository, GitHub will show commands to connect your existing repository. Run these commands in your terminal:

```bash
git remote add origin https://github.com/YOUR-USERNAME/YOUR-REPOSITORY.git
git push -u origin main
```

Replace `YOUR-USERNAME` with your GitHub username and `YOUR-REPOSITORY` with your repository name.

## Step 3: Deploy to Streamlit Cloud

1. Go to [Streamlit Cloud](https://streamlit.io/cloud)
2. Sign in with GitHub
3. Click 'New app'
4. Select your repository, branch (main), and the path to your app file (app.py)
5. Click 'Deploy'

Your app will be deployed and accessible via a Streamlit Cloud URL.

## Troubleshooting

### Authentication Issues

If you encounter authentication issues when pushing to GitHub, you may need to:

1. Use a Personal Access Token (PAT) instead of password
   - Go to GitHub → Settings → Developer settings → Personal access tokens → Generate new token
   - Select repo scope
   - Use this token instead of your password when prompted

2. Or set up SSH authentication:
   ```bash
   ssh-keygen -t ed25519 -C "your_email@example.com"
   # Add the key to your GitHub account
   git remote set-url origin git@github.com:YOUR-USERNAME/YOUR-REPOSITORY.git
   ```

### Streamlit Deployment Issues

- Ensure your requirements.txt file is up to date
- Check that your app.py file is in the root directory
- Verify that your app runs locally before deploying

## Updating Your Deployed App

After making changes to your code:

```bash
git add .
git commit -m "Your update message"
git push origin main
```

Streamlit Cloud will automatically detect changes and rebuild your app.