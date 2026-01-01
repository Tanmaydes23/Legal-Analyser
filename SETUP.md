# Legal Analyzer - Quick Setup Guide

## 🎯 Get Started in 5 Minutes

### Step 1: Get Google Gemini API Key (FREE)
1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Click "Create API Key"
3. Copy your API key

### Step 2: Configure Backend
```bash
cd backend
copy .env.example .env
```

Open `.env` file and paste your API key:
```
GOOGLE_API_KEY=your_api_key_here
```

### Step 3: Install Backend Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Install Frontend Dependencies
```bash
cd ../frontend
npm install
```

### Step 5: Start the Application

**Terminal 1 - Backend:**
```bash
cd backend
python main.py
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
```

### Step 6: Open Browser
Navigate to: **http://localhost:3000**

---

## ✅ Test It Out

1. Click "Analyze Document"
2. Upload a sample contract(PDF/DOCX/TXT)
3. Wait 20-30 seconds
4. Review the AI analysis!

---

## 🐛 Troubleshooting

### Backend won't start
- Make sure Python 3.10+ is installed: `python --version`
- Install dependencies: `pip install -r requirements.txt`
- Check `.env` file has your Google API key

### Frontend won't start
- Make sure Node.js 18+ is installed: `node --version`
- Delete `node_modules` and reinstall: `npm install`

### "API Key Error"
- Verify your Google API key is correct in `backend/.env`
- Make sure it's Gemini API key (not other Google APIs)

### Can't upload files
- Make sure backend is running on port 8000
- Check browser console for errors
- Verify file is PDF, DOCX, or TXT

---

## 📞 Need Help?

Check the full [README.md](README.md) for detailed documentation.
