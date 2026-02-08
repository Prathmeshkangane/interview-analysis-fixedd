# Troubleshooting Guide - AI Mock Interview System

## Common Issues and Solutions

### 1. Installation Issues

#### "Python is not recognized as an internal or external command"
**Problem**: Python is not in your system PATH  
**Solution**:
- Windows: Reinstall Python and check "Add Python to PATH" during installation
- Mac/Linux: Install Python using package manager (brew, apt-get)
- Verify: Run `python --version` in terminal

#### "pip is not recognized"
**Problem**: pip is not installed or not in PATH  
**Solution**:
```bash
# Windows
python -m ensurepip --upgrade

# Mac/Linux
python3 -m ensurepip --upgrade
```

#### "No module named 'xxx'" errors
**Problem**: Dependencies not installed  
**Solution**:
```bash
pip install -r requirements.txt --upgrade

# If that fails, install individually:
pip install flask flask-cors openai anthropic
pip install PyPDF2 python-docx nltk textblob vaderSentiment
pip install fpdf2
```

### 2. API Key Issues

#### "Invalid API key" or "Authentication failed"
**Problem**: API key is incorrect or not properly configured  
**Solutions**:
1. Check your .env file exists in the project root
2. Verify no extra spaces around the API key
3. For Groq: Key should start with `gsk_`
4. For OpenAI: Key should start with `sk-`
5. Make sure the .env file format is:
   ```
   OPENAI_API_KEY=your_key_here
   ```
   (No quotes, no spaces around =)

#### "Rate limit exceeded"
**Problem**: Too many API requests  
**Solutions**:
- For Groq: Should not happen (very high limits)
- For OpenAI: Wait a few minutes or upgrade your plan
- Check if you have multiple instances running

### 3. Camera/Microphone Issues

#### "Camera not detected" or "Permission denied"
**Windows**:
1. Settings → Privacy → Camera → Allow apps to access camera
2. Enable for Python/Terminal
3. Close other apps using camera (Zoom, Teams, Skype)

**Mac**:
1. System Preferences → Security & Privacy → Camera
2. Check the box for Terminal/Python
3. May need to restart the app

**Linux**:
1. Check camera: `ls /dev/video*`
2. Add user to video group: `sudo usermod -a -G video $USER`
3. Logout and login again

#### "Microphone not working" or "Speech not recognized"
**Solutions**:
1. Check browser permissions (Chrome/Edge recommended)
2. Click the microphone icon in address bar to allow access
3. Test microphone in system settings
4. Speak clearly and louder
5. Reduce background noise
6. Use headset microphone for better quality

#### "Speech recognition not supported"
**Problem**: Browser doesn't support Web Speech API  
**Solution**:
- Use Google Chrome (best support)
- Use Microsoft Edge (good support)
- Firefox/Safari have limited support - not recommended

### 4. Application Errors

#### "Address already in use" or "Port 5000 is already allocated"
**Problem**: Port 5000 is being used by another application  
**Solutions**:
1. Find and stop the process using port 5000:
   ```bash
   # Windows
   netstat -ano | findstr :5000
   taskkill /PID <PID_NUMBER> /F
   
   # Mac/Linux
   lsof -i :5000
   kill <PID>
   ```
2. Or change the port in app.py (last line):
   ```python
   app.run(debug=True, host='0.0.0.0', port=5001)  # Use 5001 instead
   ```

#### "TemplateNotFound" error
**Problem**: Templates folder not found  
**Solution**:
1. Make sure templates/ folder exists in project root
2. Check that index.html, interview.html, results.html are in templates/
3. Folder structure should be:
   ```
   project_root/
   ├── app.py
   ├── templates/
   │   ├── index.html
   │   ├── interview.html
   │   └── results.html
   └── static/
       └── css/
           └── style.css
   ```

#### "No such file or directory" for static files
**Problem**: Static files folder missing  
**Solution**:
1. Create the folders:
   ```bash
   mkdir -p static/css
   ```
2. Make sure style.css is in static/css/

### 5. Question Generation Issues

#### "Failed to generate questions" or empty questions
**Problem**: API issue or document parsing failed  
**Solutions**:
1. Check API key is valid and has credits (for OpenAI)
2. Verify resume and JD files are not corrupted
3. Check console/terminal for error messages
4. Try with simpler PDF files (some PDFs are image-based)
5. Convert image PDFs to text-based PDFs

#### "Questions not personalized"
**Problem**: Fallback questions being used  
**Solutions**:
1. API may not be responding - check your internet connection
2. Verify API key is working
3. Check console for "Using Groq provider" or "Using OpenAI provider" message
4. Make sure resume and JD have enough content (100+ words each)

### 6. Interview Page Issues

#### "No speech detected" message keeps appearing
**Solutions**:
1. Click "Start Recording" before speaking
2. Speak louder and clearer
3. Check microphone is not muted
4. Allow microphone access in browser
5. Test microphone in system settings first

#### "Video shows black screen"
**Solutions**:
1. Allow camera access when browser prompts
2. Check camera is not being used by another app
3. Try refreshing the page
4. Check camera works in system settings

#### "Transcript not appearing while speaking"
**Solutions**:
1. Must use Chrome or Edge browser
2. Internet connection required for speech recognition
3. Speak in shorter sentences (pause briefly)
4. Reduce background noise
5. Check browser console (F12) for errors

#### "Submit button not appearing"
**Problem**: No speech recognized  
**Solutions**:
1. Make sure you clicked "Start Recording"
2. Speak clearly for at least 5-10 seconds
3. Click "Stop Recording" when done
4. If still no transcript, try recording again

### 7. Report Generation Issues

#### "Failed to generate report" error
**Solutions**:
1. Make sure you answered at least one question
2. Check reports/ folder exists and is writable
3. Try answering more questions (at least 5 recommended)
4. Check console for specific error messages

#### "Report download not working"
**Solutions**:
1. Check browser's download folder
2. Allow downloads in browser settings
3. Report file should be in reports/ folder
4. Try right-click → Save As on the download link

### 8. Performance Issues

#### "Application running slow"
**Solutions**:
1. Close unnecessary browser tabs
2. Close other resource-heavy applications
3. For Groq API: Should be very fast (1-2 seconds)
4. For OpenAI: May take 5-10 seconds per request

#### "Browser becomes unresponsive"
**Solutions**:
1. Use Chrome or Edge (better performance)
2. Close other tabs and applications
3. Clear browser cache
4. Reduce video quality by commenting out in interview.html:
   ```javascript
   // this.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
   ```

### 9. File Upload Issues

#### "Invalid file format" error
**Supported formats**: PDF, DOCX, TXT  
**Solutions**:
1. Convert other formats to PDF
2. For image-based PDFs, use OCR software first
3. Make sure file is not corrupted
4. Try a different file

#### "Failed to parse documents" error
**Solutions**:
1. File may be corrupted - try another file
2. PDF may be password-protected - remove password first
3. DOCX may have unsupported formatting - try converting to PDF
4. File may be too large - try compressing

### 10. NLTK/TextBlob Errors

#### "Resource punkt not found" or similar NLTK errors
**Solution**:
```python
import nltk
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('averaged_perceptron_tagger')
```

Or run this Python script once:
```python
import nltk
nltk.download('all')  # Downloads all NLTK data
```

### 11. Video Analyzer Issues

#### "MediaPipe errors" or "TensorFlow conflicts"
**Solution**:
The video_analyzer.py has been updated to avoid TensorFlow conflicts.
If still having issues:
```bash
pip uninstall tensorflow
pip install mediapipe --upgrade
```

### 12. Browser-Specific Issues

#### Chrome
- Usually works best
- Make sure version is up to date
- Clear cache if having issues

#### Edge
- Second best option
- Based on Chromium, similar to Chrome
- Good compatibility

#### Firefox
- Limited Web Speech API support
- May not work for speech recognition
- Not recommended

#### Safari
- Very limited support
- Speech recognition may not work
- Not recommended

## Getting Help

If none of these solutions work:

1. **Check the console**: Press F12 in browser, look at Console tab for errors
2. **Check terminal output**: Look for error messages in the terminal where you ran `python app.py`
3. **Verify setup**:
   ```bash
   python --version  # Should be 3.8+
   pip list | grep -i flask  # Check Flask is installed
   ls templates/  # Should show HTML files
   ls static/css/  # Should show style.css
   cat .env  # Should show your API key
   ```

4. **Test components individually**:
   ```bash
   # Test document parser
   python document_parser.py
   
   # Test question generator
   python question_generator.py
   
   # Test answer analyzer
   python answer_analyzer.py
   ```

## Still Having Issues?

Make sure you have:
- [ ] Python 3.8 or higher installed
- [ ] All dependencies installed (`pip install -r requirements.txt`)
- [ ] Valid API key in .env file
- [ ] Chrome or Edge browser
- [ ] Working camera and microphone
- [ ] Internet connection
- [ ] Proper folder structure (templates/, static/)
- [ ] Valid resume and job description files

## Quick Reset

If everything is broken, try a fresh start:

```bash
# 1. Delete these folders
rm -rf uploads/ reports/

# 2. Recreate them
mkdir uploads reports

# 3. Reinstall dependencies
pip install -r requirements.txt --upgrade --force-reinstall

# 4. Run setup again
python setup.py

# 5. Start the app
python app.py
```

## Emergency Fallback

If the app won't start at all:

1. Check Python version: `python --version`
2. Create minimal .env with just:
   ```
   OPENAI_API_KEY=gsk_your_key
   ```
3. Install only essential packages:
   ```bash
   pip install flask openai PyPDF2 python-docx fpdf2
   ```
4. Try running: `python app.py`

This should at least get the basic app running, even if some features don't work perfectly.
