# AI Mock Interview System - Quick Start Guide

## 🚀 Get Started in 5 Minutes

### Step 1: Install Python (if not installed)
Download from: https://www.python.org/downloads/
- Minimum version: Python 3.8
- Make sure to check "Add Python to PATH" during installation

### Step 2: Install Dependencies
```bash
# Open terminal/command prompt in project folder
pip install -r requirements.txt
```

### Step 3: Get Groq API Key (FREE & FAST!)

**Using Groq (Recommended - FREE and FASTER):**
1. Go to https://console.groq.com/
2. Create a free account
3. Go to API Keys section
4. Click "Create API Key"
5. Copy the key (starts with `gsk_`)

**Why Groq?**
- ✅ **Completely FREE** - No credit card required
- ✅ **Super FAST** - Fastest LLM inference available
- ✅ **No usage limits** for developers
- ✅ Uses powerful Llama 3 model

### Step 4: Configure API Key
1. Create a file named `.env` in the project folder
2. Add this line (paste your actual key):
   ```
   OPENAI_API_KEY=gsk_your_groq_key_here
   ```
   
   **Note:** Even though we're using Groq, we still use the variable name `OPENAI_API_KEY` because the code is compatible with both providers.

### Step 5: Run the Application!
```bash
python app.py
```

Then open your browser and go to: **http://localhost:5000**

## ✨ What's New in This Version

### Key Features:
- 📋 **10 Personalized Questions** - All questions are based on YOUR resume and the job description
- 🎤 **Real-time Speech Recognition** - Your voice is converted to text as you speak
- 📹 **Video Interview Interface** - Practice with your webcam like a real interview
- 📊 **Detailed Analysis** - Get comprehensive feedback on every answer
- 📄 **PDF Report** - Download a professional interview report

### How It Works:
1. **Upload** your resume and job description (PDF, DOCX, or TXT)
2. **Answer 10 questions** tailored specifically to your profile
3. **Record** your answers using the microphone
4. **Get instant feedback** on each answer
5. **Download** a detailed PDF report with recommendations

## 🎯 Interview Process

### Questions Generated:
- **10 Resume-Based Questions** - Focused on:
  - Your specific projects and experience
  - Technologies you've worked with
  - Achievements mentioned in your resume
  - Match with job requirements

### What's Being Analyzed:
- **Content Quality (40%)** - Examples, specifics, achievements
- **Clarity (25%)** - Clear communication, reduced filler words
- **Confidence (20%)** - Positive tone, conviction
- **Professionalism (15%)** - Professional language and tone

## 💡 Tips for Best Results

### Before Starting:
✅ Close other apps using camera/microphone  
✅ Find a quiet room with good lighting  
✅ Position camera at eye level  
✅ Test your microphone volume  
✅ Prepare your resume and job description files  

### During Interview:
✅ Look at the camera when speaking  
✅ Speak clearly and at moderate pace  
✅ Use the STAR method (Situation, Task, Action, Result)  
✅ Provide specific examples with numbers  
✅ Keep answers 30-90 seconds long  

### Answer Structure (STAR Method):
1. **Situation**: Set the context
2. **Task**: Explain your responsibility
3. **Action**: Describe what you did
4. **Result**: Share the outcome (with numbers!)

## 🎓 Sample Answer Example

**Question**: "Tell me about a challenging project you worked on."

**Poor Answer** (Score: 45/100):
"Um, I worked on a project that was hard. It was challenging and I had to work with my team. We finished it eventually."

**Good Answer** (Score: 85/100):
"In my previous role as a software engineer, our team faced a critical performance issue where page load times exceeded 8 seconds, impacting 10,000+ daily users. I took the lead on investigating the root cause, identified inefficient database queries, and implemented caching mechanisms. Within two weeks, we reduced load times by 75% to under 2 seconds, which increased user engagement by 30% and received positive feedback from management."

### Why the Good Answer Scores Higher:
✅ Specific role and context  
✅ Quantified problem (8 seconds, 10,000 users)  
✅ Clear action taken (investigation, implementation)  
✅ Measurable results (75% improvement, 30% engagement)  
✅ Professional language  
✅ Well-structured narrative  

## 🔧 Common Issues & Quick Fixes

### "No module named 'xxx'"
```bash
pip install -r requirements.txt --upgrade
```

### "Microphone not detected"
1. Check System Settings → Privacy → Microphone
2. Allow Python/Terminal to access microphone
3. Try unplugging and replugging microphone

### "Camera not found"
1. Check System Settings → Privacy → Camera
2. Close other apps using camera (Zoom, Teams, etc.)
3. Restart your browser

### "API key not working"
1. Make sure you're using a Groq API key (starts with `gsk_`)
2. Check for extra spaces in .env file
3. Verify key is active on https://console.groq.com/

### "Speech not recognized"
1. Speak louder and clearer
2. Reduce background noise
3. Make sure you're using Chrome or Edge browser
4. Try speaking in shorter sentences

## 📊 Understanding Your Scores

| Score Range | Rating | Meaning |
|-------------|--------|---------|
| 85-100 | Excellent | Ready for real interviews! |
| 70-84 | Good | Minor improvements needed |
| 50-69 | Average | Practice specific areas |
| Below 50 | Needs Work | Review feedback carefully |

### Score Components:
- **Content** (40%): Specific examples, achievements, quantification
- **Clarity** (25%): Clear communication, minimal fillers
- **Confidence** (20%): Positive tone, conviction
- **Professionalism** (15%): Professional language

## 🗂️ Project Structure

```
ai_interview_fixed/
├── app.py                      # Main Flask application
├── templates/
│   ├── index.html             # Upload page
│   ├── interview.html         # Interview page
│   └── results.html           # Results page
├── static/
│   └── css/
│       └── style.css          # Styling
├── document_parser.py         # Parse PDF/DOCX files
├── question_generator.py      # Generate questions using Groq
├── answer_analyzer.py         # Analyze answers
├── report_generator.py        # Create PDF reports
├── requirements.txt           # Python dependencies
└── .env                       # API key (create this)
```

## 🌟 Features Breakdown

### 1. Document Processing
- Supports PDF, DOCX, and TXT files
- Extracts text from resumes and job descriptions
- Identifies key skills and experiences

### 2. Question Generation
- Uses Groq's Llama 3 model
- Generates personalized questions
- Focuses on resume-JD alignment

### 3. Speech Recognition
- Real-time transcription
- Word count tracking
- Web Speech API integration

### 4. Answer Analysis
- NLP-based content analysis
- Sentiment analysis
- Professionalism scoring
- Clarity measurement

### 5. Report Generation
- Professional PDF reports
- Visual score charts
- Detailed recommendations
- Question-by-question feedback

## ❓ FAQ

**Q: How many practice interviews should I do?**  
A: At least 3-5 before your real interview. More for important roles.

**Q: Can I pause during the interview?**  
A: No, it runs continuously like a real interview. But you can take brief pauses between thoughts.

**Q: Do I need a job description?**  
A: Yes, it's required. The questions are tailored to match your resume with the JD.

**Q: Is my data saved?**  
A: Only the final PDF report is saved. Video/audio are processed in real-time only.

**Q: Can I review questions before starting?**  
A: Questions are generated after upload but shown one at a time during the interview.

**Q: What browsers are supported?**  
A: Chrome and Edge work best. Safari and Firefox have limited speech recognition support.

**Q: Is Groq really free?**  
A: Yes! Groq offers free API access with generous rate limits for developers.

**Q: Why is it asking for OPENAI_API_KEY if I'm using Groq?**  
A: The code is compatible with both OpenAI and Groq. It automatically detects Groq keys (starting with `gsk_`) and uses the appropriate endpoint.

## 🎯 Next Steps After Your Mock Interview

1. **Review PDF Report** - Read all sections carefully
2. **Watch Score Trends** - Which areas need most work?
3. **Address Weak Points** - Practice those specific areas
4. **Repeat Weekly** - Track improvement over time
5. **Real Interview** - You're ready when scoring 75+!

## 📚 Additional Resources

**Interview Skills:**
- Glassdoor Interview Questions
- Cracking the Coding Interview (book)
- YouTube: Mock interview channels

**Technical Practice:**
- LeetCode (coding)
- System Design Primer
- Behavioral Interview Guide

**Communication:**
- Toastmasters (public speaking)
- Dale Carnegie courses
- Record & review yourself

## 🔐 Privacy & Security

- All processing happens locally on your machine
- No data is sent to external servers except the Groq API for question generation
- Resume and JD are processed in memory only
- Videos are not recorded or saved
- Only the final PDF report is saved locally

## 🆘 Support

If you encounter issues:
1. Check this README for common solutions
2. Make sure all dependencies are installed
3. Verify your API key is correct
4. Check browser console for errors (F12)

## 📝 License

This is an educational project. Use it to practice and improve your interview skills!

---

## 🚀 Ready to Start?

Run this command:
```bash
python app.py
```

Then open: **http://localhost:5000**

**Remember**: This is PRACTICE. Don't stress about perfect scores.  
Focus on IMPROVEMENT with each attempt!

Good luck! 🎯✨
