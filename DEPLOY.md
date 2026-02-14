# Deployment Guide (Free Tier)

This guide will help you deploy your AI SQL Agent for free using **Neon** (Database) and **Render** (App Hosting).

## Prerequisites
- GitHub Account (to host your code)
- [Neon Account](https://neon.tech) (Free PostgreSQL)
- [Render Account](https://render.com) (Free Web Hosting)

## Step 1: Database Setup (Neon)
1. Log in to **Neon Console**.
2. Create a new project (e.g., `ai-sql-rag`).
3. Copy the **Connection String** (Postgres URL). It looks like:
   `postgres://user:pass@ep-xyz.region.aws.neon.tech/neondb?sslmode=require`
4. Store this string; you will need it for the `DB_HOST`, `DB_USER`, `DB_PASS`, etc.

## Step 2: Push Code to GitHub
1. Create a **New Repository** on GitHub.
2. Push your local code to this repository:
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git branch -M main
   git remote add origin https://github.com/YOUR_USER/YOUR_REPO.git
   git push -u origin main
   ```

## Step 3: Deploy App (Render)
1. Log in to **Render Dashboard**.
2. Click **New +** -> **Web Service**.
3. Connect your **GitHub Repository**.
4. Configure the service:
   - **Name**: `ai-rag-agent`
   - **Runtime**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
5. **Environment Variables** (Click "Advanced"):
   Add the following variables using your Neon DB details and Gemini Key:
   - `GEMINI_API_KEY`: `your_gemini_key_here`
   - `DB_HOST`: `ep-xyz.region.aws.neon.tech` (from Neon URL)
   - `DB_NAME`: `neondb`
   - `DB_USER`: `your_user`
   - `DB_PASS`: `your_password`
   - `DB_PORT`: `5432`

6. Click **Create Web Service**.

## Step 4: Initialize the Database
Since the free tier doesn't allow shell access easily, you can populate the database by connecting from your local machine (since Neon allows external connections).

1. Update your local `.env` file with the **Neon Connection Details**.
2. Run the data generator locally:
   ```bash
   python data_generator.py
   ```
   *This will connect to your remote Neon DB and create the tables/data.*

## Step 5: Access Your App
Render will provide a URL (e.g., `https://ai-rag-agent.onrender.com`).
Visit it to see your vibrant, responsive AI Agent live!
