# 🚀 Streamlit Deployment Guide

Deploy your Misinformation Detection System as a pure Streamlit application.

## 🎯 Streamlit Cloud (FREE & EASIEST)

### Step-by-Step Deployment:

1. **Prepare your repository:**
   ```bash
   git add .
   git commit -m "Deploy to Streamlit Cloud"
   git push origin main
   ```

2. **Deploy on Streamlit Cloud:**
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Sign in with GitHub
   - Click "New app"
   - Select your repository
   - Set main file: `streamlitui.py`
   - Add secrets in "Advanced settings":
     ```
     GEMINI_API_KEY = "your-api-key-here"
     ```
   - Click "Deploy"

3. **Your app will be live at:** `https://your-app-name.streamlit.app`

### 🔑 Required Environment Variables:
- `GEMINI_API_KEY`: Your Google Gemini API key (required)

## 🚂 Alternative Platforms

### Railway (FREE TIER)
1. Go to [railway.app](https://railway.app)
2. Deploy from GitHub repo
3. Add `GEMINI_API_KEY` environment variable
4. **Live at:** `https://your-app-name.railway.app`

### Render (FREE TIER)
1. Go to [render.com](https://render.com)
2. Create Web Service from repo
3. Add `GEMINI_API_KEY` environment variable
4. **Live at:** `https://your-app-name.onrender.com`

### Heroku (PAID)
1. Go to [heroku.com](https://heroku.com)
2. Create new app from GitHub
3. Add `GEMINI_API_KEY` config var
4. **Live at:** `https://your-app-name.herokuapp.com`

## 🐳 Docker Deployment

### Local Docker Testing
```bash
# Build the image
docker build -t misinformation-detector .

# Run Streamlit UI
docker run -p 8080:8080 -e GEMINI_API_KEY=your-key misinformation-detector

# Run API only
docker run -p 8080:8080 -e APP_MODE=api -e GEMINI_API_KEY=your-key misinformation-detector
```

### Google Cloud Run
```bash
# Build and push to Google Container Registry
gcloud builds submit --tag gcr.io/PROJECT_ID/misinformation-detector

# Deploy to Cloud Run
gcloud run deploy misinformation-detector \
  --image gcr.io/PROJECT_ID/misinformation-detector \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars GEMINI_API_KEY=your-key
```

### AWS ECS/Fargate
```bash
# Build and push to ECR
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin your-account.dkr.ecr.us-east-1.amazonaws.com
docker build -t misinformation-detector .
docker tag misinformation-detector:latest your-account.dkr.ecr.us-east-1.amazonaws.com/misinformation-detector:latest
docker push your-account.dkr.ecr.us-east-1.amazonaws.com/misinformation-detector:latest
```

## 🔧 Environment Variables

All deployment platforms need these environment variables:

| Variable | Value | Required |
|----------|-------|----------|
| `GEMINI_API_KEY` | Your Google Gemini API key | ✅ Yes |
| `GEMINI_MODEL` | `gemini-2.0-flash` | No (has default) |
| `DATABASE_URL` | `sqlite:///./misinformation_detector.db` | No (has default) |
| `APP_MODE` | `streamlit` or `api` | No (defaults to streamlit) |

## 🎯 Recommended Deployment Strategy

**For Personal Use:** Streamlit Cloud (free, easy)
**For Team Use:** Railway or Render (free tiers available)
**For Production:** Google Cloud Run or AWS (scalable, reliable)

## 🔍 Testing Your Deployment

After deployment, test your app:

1. **Visit your live URL**
2. **Enter sample text:** "The Earth is flat and NASA is hiding the truth"
3. **Click "Analyze for Misinformation"**
4. **Verify you get analysis results**

## 🚨 Troubleshooting

**Common Issues:**

1. **"Backend Offline" in Streamlit:**
   - Check if `GEMINI_API_KEY` is set correctly
   - Verify the API key has quota remaining

2. **Build Failures:**
   - Ensure `requirements.txt` is up to date
   - Check Python version compatibility

3. **Database Errors:**
   - SQLite works for most deployments
   - For high traffic, consider PostgreSQL

4. **Timeout Errors:**
   - Increase timeout settings in cloud platform
   - Optimize analysis parameters

## 📞 Support

If you encounter issues:
1. Check the platform's logs/console
2. Verify environment variables are set
3. Test locally with Docker first
4. Check API key validity and quota

---

**🎉 Once deployed, you'll have a live misinformation detection system accessible from anywhere!**