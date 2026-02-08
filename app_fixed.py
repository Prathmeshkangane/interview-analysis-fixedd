"""
AI Mock Interview System - Complete Fixed Version
5 personalized resume-based questions
"""

from flask import Flask, render_template, request, jsonify, send_file, redirect, url_for
from flask_cors import CORS
import os
from datetime import datetime
from werkzeug.utils import secure_filename
import uuid
import traceback

# Import modules
from document_parser import DocumentParser
from question_generator import QuestionGenerator
from answer_analyzer import AnswerAnalyzer
from report_generator import ReportGenerator

app = Flask(__name__)
app.secret_key = os.urandom(24)
CORS(app)

# Config
UPLOAD_FOLDER = 'uploads'
REPORTS_FOLDER = 'reports'
ALLOWED_EXTENSIONS = {'pdf', 'docx', 'txt'}

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(REPORTS_FOLDER, exist_ok=True)
os.makedirs('templates', exist_ok=True)
os.makedirs('static/css', exist_ok=True)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['REPORTS_FOLDER'] = REPORTS_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

# Initialize
doc_parser = DocumentParser()
question_generator = QuestionGenerator()
answer_analyzer = AnswerAnalyzer()
report_generator = ReportGenerator()

# Sessions storage
interview_sessions = {}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def index():
    """Upload page"""
    print("\n🏠 Homepage accessed")
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload_documents():
    """Handle file upload and question generation"""
    try:
        print("\n📤 Upload request received")
        
        # Validate files
        if 'resume' not in request.files or 'job_description' not in request.files:
            print("❌ Missing files in request")
            return jsonify({'success': False, 'error': 'Both files required'}), 400
        
        resume_file = request.files['resume']
        jd_file = request.files['job_description']
        
        print(f"📄 Resume: {resume_file.filename}")
        print(f"📄 JD: {jd_file.filename}")
        
        if resume_file.filename == '' or jd_file.filename == '':
            return jsonify({'success': False, 'error': 'No file selected'}), 400
        
        if not (allowed_file(resume_file.filename) and allowed_file(jd_file.filename)):
            return jsonify({'success': False, 'error': 'Invalid format'}), 400
        
        # Save files
        resume_path = os.path.join(app.config['UPLOAD_FOLDER'], 
                                   secure_filename(resume_file.filename))
        jd_path = os.path.join(app.config['UPLOAD_FOLDER'], 
                              secure_filename(jd_file.filename))
        
        resume_file.save(resume_path)
        jd_file.save(jd_path)
        print("✅ Files saved")
        
        # Parse
        print("📖 Parsing documents...")
        resume_text = doc_parser.parse_document(resume_path)
        jd_text = doc_parser.parse_document(jd_path)
        
        if not resume_text or not jd_text:
            return jsonify({'success': False, 'error': 'Failed to parse documents'}), 400
        
        print(f"✅ Resume: {len(resume_text)} chars")
        print(f"✅ JD: {len(jd_text)} chars")
        
        # Generate session
        session_id = str(uuid.uuid4())
        print(f"🆔 Session: {session_id}")
        
        # Generate questions
        print("🎯 Generating 5 resume-based questions...")
        all_questions = question_generator.generate_resume_specific_questions(
            resume_text, jd_text, 5
        )
        
        print(f"✅ Generated {len(all_questions)} questions:")
        for i, q in enumerate(all_questions, 1):
            print(f"   {i}. {q['question'][:60]}...")
        
        # Store session
        interview_sessions[session_id] = {
            'resume_text': resume_text,
            'jd_text': jd_text,
            'questions': all_questions,
            'answers': [],
            'current_question': 0,
            'created_at': datetime.now().isoformat()
        }
        
        print(f"💾 Session stored. Total sessions: {len(interview_sessions)}")
        print(f"   Session keys: {list(interview_sessions.keys())}")
        
        return jsonify({
            'success': True,
            'session_id': session_id,
            'total_questions': len(all_questions)
        })
        
    except Exception as e:
        print(f"\n❌ Upload error: {e}")
        traceback.print_exc()
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/interview/<session_id>')
def interview_page(session_id):
    """Interview page with video"""
    print(f"\n🎥 Interview page requested: {session_id}")
    print(f"   Available sessions: {list(interview_sessions.keys())}")
    
    if session_id not in interview_sessions:
        print(f"❌ Invalid session: {session_id}")
        return redirect(url_for('index'))
    
    print(f"✅ Session found. Questions: {len(interview_sessions[session_id]['questions'])}")
    return render_template('interview.html', session_id=session_id)


@app.route('/api/get-question/<session_id>', methods=['GET'])
def get_question(session_id):
    """Get current question"""
    try:
        print(f"\n📝 Question request for session: {session_id}")
        print(f"   Available sessions: {list(interview_sessions.keys())}")
        
        if not session_id or session_id == '':
            print("❌ Empty session ID")
            return jsonify({'error': 'No session ID provided'}), 400
        
        if session_id not in interview_sessions:
            print(f"❌ Invalid session: {session_id}")
            print(f"   Session not found in: {list(interview_sessions.keys())}")
            return jsonify({'error': 'Invalid session. Please upload files again.'}), 404
        
        session_data = interview_sessions[session_id]
        current_idx = session_data['current_question']
        questions = session_data['questions']
        
        print(f"   Current: {current_idx + 1}/{len(questions)}")
        
        if current_idx >= len(questions):
            print("✅ Interview complete")
            return jsonify({
                'completed': True,
                'message': 'Interview completed'
            })
        
        question = questions[current_idx]
        
        print(f"   Question: {question['question'][:50]}...")
        
        response_data = {
            'completed': False,
            'question_number': current_idx + 1,
            'total_questions': len(questions),
            'question': question['question'],
            'category': question.get('category', 'Resume-Based'),
            'difficulty': question.get('difficulty', 'intermediate'),
            'focus_area': question.get('focus_area', '')
        }
        
        print(f"   Sending response: {response_data}")
        return jsonify(response_data)
        
    except Exception as e:
        print(f"❌ Get question error: {e}")
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500


@app.route('/api/submit-answer/<session_id>', methods=['POST'])
def submit_answer(session_id):
    """Submit answer and get feedback"""
    try:
        print(f"\n📝 Answer submission for session: {session_id}")
        
        if session_id not in interview_sessions:
            print(f"❌ Invalid session")
            return jsonify({'success': False, 'error': 'Invalid session'}), 404
        
        data = request.get_json()
        answer_text = data.get('answer', '')
        duration = data.get('duration', 0)
        
        print(f"   Answer length: {len(answer_text)} chars")
        print(f"   Duration: {duration}s")
        
        session_data = interview_sessions[session_id]
        current_idx = session_data['current_question']
        question = session_data['questions'][current_idx]
        
        # Analyze answer
        print("🔍 Analyzing answer...")
        analysis = answer_analyzer.analyze_answer(
            answer_text,
            question['question']
        )
        
        # Generate feedback
        feedback = answer_analyzer.get_feedback(analysis)
        
        print(f"   Score: {analysis['overall_score']}")
        
        # Store answer
        session_data['answers'].append({
            'question': question['question'],
            'answer': answer_text,
            'duration': duration,
            'analysis': analysis,
            'feedback': feedback,
            'timestamp': datetime.now().isoformat()
        })
        
        # Move to next question
        session_data['current_question'] += 1
        is_complete = session_data['current_question'] >= len(session_data['questions'])
        
        print(f"   Progress: {session_data['current_question']}/{len(session_data['questions'])}")
        print(f"   Complete: {is_complete}")
        
        return jsonify({
            'success': True,
            'score': analysis['overall_score'],
            'feedback': feedback[:3],  # Return top 3 feedback points
            'is_complete': is_complete
        })
        
    except Exception as e:
        print(f"❌ Submit answer error: {e}")
        traceback.print_exc()
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/results/<session_id>')
def results_page(session_id):
    """Results page"""
    print(f"\n📊 Results page requested: {session_id}")
    
    if session_id not in interview_sessions:
        print(f"❌ Invalid session")
        return redirect(url_for('index'))
    
    print(f"✅ Session found")
    return render_template('results.html', session_id=session_id)


@app.route('/api/generate-report/<session_id>', methods=['POST'])
def generate_report(session_id):
    """Generate final report"""
    try:
        print(f"\n📄 Report generation for session: {session_id}")
        
        if session_id not in interview_sessions:
            return jsonify({'success': False, 'error': 'Invalid session'}), 404
        
        session_data = interview_sessions[session_id]
        
        print("📊 Generating comprehensive report...")
        
        # Prepare interview data for report
        interview_data = {
            'answers': session_data['answers'],
            'resume_text': session_data['resume_text'],
            'jd_text': session_data['jd_text'],
            'timestamp': session_data['created_at']
        }
        
        # Generate report path
        report_filename = f'interview_report_{session_id}.pdf'
        report_path = os.path.join(app.config['REPORTS_FOLDER'], report_filename)
        
        # Generate the report
        success = report_generator.generate_report(interview_data, report_path)
        
        if not success:
            return jsonify({'success': False, 'error': 'Failed to generate report'}), 500
        
        print(f"✅ Report generated: {report_path}")
        
        # Calculate metrics
        scores = [ans['analysis']['overall_score'] for ans in session_data['answers']]
        overall_score = sum(scores) / len(scores) if scores else 0
        
        # Extract individual metric scores
        content_scores = [ans['analysis']['content_quality']['quality_score'] for ans in session_data['answers']]
        clarity_scores = [ans['analysis']['clarity']['clarity_score'] for ans in session_data['answers']]
        confidence_scores = [ans['analysis']['sentiment']['confidence_level'] for ans in session_data['answers']]
        professional_scores = [ans['analysis']['professionalism']['professionalism_score'] for ans in session_data['answers']]
        
        metrics = {
            'content_score': sum(content_scores) / len(content_scores) if content_scores else 70,
            'clarity_score': sum(clarity_scores) / len(clarity_scores) if clarity_scores else 70,
            'confidence_score': sum(confidence_scores) / len(confidence_scores) if confidence_scores else 70,
            'professionalism_score': sum(professional_scores) / len(professional_scores) if professional_scores else 70
        }
        
        print(f"   Overall: {overall_score}")
        print(f"   Metrics: {metrics}")
        
        return jsonify({
            'success': True,
            'overall_score': overall_score,
            'metrics': metrics,
            'report_url': f'/download-report/{session_id}'
        })
        
    except Exception as e:
        print(f"❌ Report generation error: {e}")
        traceback.print_exc()
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/download-report/<session_id>')
def download_report(session_id):
    """Download PDF report"""
    try:
        report_path = os.path.join(app.config['REPORTS_FOLDER'], f'interview_report_{session_id}.pdf')
        
        if not os.path.exists(report_path):
            return "Report not found", 404
        
        return send_file(
            report_path,
            as_attachment=True,
            download_name=f'interview_report_{datetime.now().strftime("%Y%m%d")}.pdf'
        )
    except Exception as e:
        print(f"❌ Download error: {e}")
        return str(e), 500


# Debug route to check sessions
@app.route('/api/debug/sessions')
def debug_sessions():
    """Debug endpoint to check active sessions"""
    return jsonify({
        'total_sessions': len(interview_sessions),
        'session_ids': list(interview_sessions.keys()),
        'sessions': {
            sid: {
                'questions': len(data['questions']),
                'answers': len(data['answers']),
                'current': data['current_question'],
                'created': data['created_at']
            }
            for sid, data in interview_sessions.items()
        }
    })


if __name__ == '__main__':
    print("\n" + "="*50)
    print("🚀 AI Mock Interview System Starting...")
    print("="*50)
    print(f"📁 Upload folder: {UPLOAD_FOLDER}")
    print(f"📁 Reports folder: {REPORTS_FOLDER}")
    print(f"🌐 Access at: http://localhost:5000")
    print("="*50 + "\n")
    
    app.run(debug=True, host='0.0.0.0', port=5000)