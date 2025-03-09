# Streamlit Cloud Setup Guide

## Setting Up Your OpenAI API Key in Streamlit Cloud

When deploying your chatbot to Streamlit Cloud, you need to configure your OpenAI API key as a secret. This guide will walk you through the process.

### Steps to Configure Secrets in Streamlit Cloud

1. **Deploy your app to Streamlit Cloud**
   - Follow the instructions in the GITHUB_DEPLOYMENT_GUIDE.md file to deploy your app to Streamlit Cloud

2. **Access the Streamlit Cloud Dashboard**
   - Go to [Streamlit Cloud](https://streamlit.io/cloud)
   - Sign in with your account
   - Find and select your deployed app

3. **Configure Secrets**
   - In your app's dashboard, click on the **⋮** (three dots) menu in the top-right corner
   - Select **Settings**
   - Navigate to the **Secrets** section
   - Add your OpenAI API key in the following format:

   ```toml
   [openai]
   api_key = "your-api-key-here"
   ```

4. **Save and Reboot**
   - Click **Save** to store your secrets
   - Reboot your app by clicking on the **⋮** menu again and selecting **Reboot app**

### Verifying Your Setup

After configuring your API key in Streamlit Cloud:

1. Your app should automatically use the API key from Streamlit Cloud secrets
2. You should see a success message in the sidebar: "Using API key from Streamlit secrets"
3. Users will no longer need to enter an API key manually

### Troubleshooting

If your API key isn't working in Streamlit Cloud:

1. **Check the API key format**
   - Ensure there are no extra spaces or characters in your API key
   - Make sure the key is entered exactly as provided by OpenAI

2. **Verify the secrets format**
   - The secrets must be in the exact format shown above
   - The section must be named `[openai]` and the key must be `api_key`

3. **Reboot your app**
   - After making changes to secrets, always reboot your app

4. **Check API key validity**
   - Verify that your OpenAI API key is valid and has not expired
   - Test the key locally before deploying

### Security Note

Never commit your `.streamlit/secrets.toml` file to your GitHub repository. This file is only for local development. For production, always use Streamlit Cloud's secrets management system.