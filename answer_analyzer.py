"""
Enhanced Answer Analyzer Module
Analyzes interview answers, facial expressions, and speech features
"""

import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from textblob import TextBlob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from typing import Dict, List
import re

# Download required NLTK data
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt', quiet=True)

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords', quiet=True)


class AnswerAnalyzer:
    """Analyze interview answers with speech and facial features"""
    
    def __init__(self):
        """Initialize answer analyzer"""
        self.sentiment_analyzer = SentimentIntensityAnalyzer()
        self.stop_words = set(stopwords.words('english'))
        
        # Filler words to detect
        self.filler_words = [
            'um', 'uh', 'like', 'you know', 'sort of', 'kind of',
            'i mean', 'actually', 'basically', 'literally', 'seriously',
            'honestly', 'right', 'okay', 'so', 'well', 'yeah'
        ]
    
    def analyze_answer(self, answer: str, question: str, 
                       video_data: Dict = None,
                       audio_duration: float = 0) -> Dict:
        """
        Comprehensive analysis of interview answer with A/V features
        
        Args:
            answer: Candidate's answer text
            question: Interview question
            video_data: Optional facial expression data
            audio_duration: Duration of answer in seconds
            
        Returns:
            Dictionary with comprehensive analysis
        """
        if not answer or not answer.strip():
            return self._get_empty_analysis()
        
        # Text analysis
        text_analysis = {
            'text_metrics': self._analyze_text_metrics(answer),
            'content_quality': self._analyze_content_quality(answer, question),
            'sentiment': self._analyze_sentiment(answer),
            'relevance': self._analyze_relevance(answer, question),
            'clarity': self._analyze_clarity(answer),
            'professionalism': self._analyze_professionalism(answer)
        }
        
        # Speech analysis
        speech_analysis = self._analyze_speech_features(answer, audio_duration)
        
        # Facial expression analysis
        facial_analysis = self._analyze_facial_expressions(video_data) if video_data else {}
        
        # Combine all analyses
        analysis = {
            **text_analysis,
            'speech_features': speech_analysis,
            'facial_expressions': facial_analysis,
            'overall_score': 0
        }
        
        # Calculate overall score
        analysis['overall_score'] = self._calculate_overall_score(analysis)
        
        return analysis
    
    def _analyze_speech_features(self, text: str, duration: float) -> Dict:
        """Analyze speech patterns and features"""
        words = word_tokenize(text.lower())
        text_lower = text.lower()
        
        # Detect filler words
        filler_count = sum(text_lower.count(filler) for filler in self.filler_words)
        
        # Calculate speaking rate (words per minute)
        speaking_rate = 0
        if duration > 0:
            speaking_rate = (len(words) / duration) * 60
        
        # Detect repetitions
        word_freq = {}
        for word in words:
            if word.isalpha() and len(word) > 3:
                word_freq[word] = word_freq.get(word, 0) + 1
        repetitions = sum(1 for count in word_freq.values() if count > 2)
        
        # Detect long pauses (indicated by multiple punctuation)
        pause_indicators = text.count('...') + text.count('..') 
        
        # Estimate stuttering (repeated characters or words)
        stutter_pattern = r'\b(\w+)\s+\1\b'
        stutters = len(re.findall(stutter_pattern, text_lower))
        
        # Calculate fluency score
        fluency_score = 100
        fluency_score -= min(filler_count * 5, 30)  # -5 per filler word, max -30
        fluency_score -= min(stutters * 10, 20)     # -10 per stutter, max -20
        fluency_score -= min(pause_indicators * 5, 15)  # -5 per pause, max -15
        
        # Adjust for speaking rate
        if speaking_rate > 0:
            if speaking_rate < 100:  # Too slow
                fluency_score -= 10
            elif speaking_rate > 200:  # Too fast
                fluency_score -= 10
        
        fluency_score = max(0, min(100, fluency_score))
        
        return {
            'filler_word_count': filler_count,
            'speaking_rate': round(speaking_rate, 1),
            'repetitions': repetitions,
            'stuttering_instances': stutters,
            'pause_indicators': pause_indicators,
            'fluency_score': fluency_score,
            'speaking_pace': self._get_speaking_pace(speaking_rate)
        }
    
    def _get_speaking_pace(self, rate: float) -> str:
        """Categorize speaking pace"""
        if rate == 0:
            return 'unknown'
        elif rate < 100:
            return 'too slow'
        elif rate < 130:
            return 'slow'
        elif rate < 160:
            return 'optimal'
        elif rate < 190:
            return 'fast'
        else:
            return 'too fast'
    
    def _analyze_facial_expressions(self, video_data: Dict) -> Dict:
        """Analyze facial expressions from video data"""
        if not video_data:
            return {
                'confidence_level': 70,
                'nervousness': 'moderate',
                'eye_contact': 'good',
                'expressions': 'neutral'
            }
        
        # Extract metrics from video_data
        eye_contact_pct = video_data.get('eye_contact_percentage', 60)
        dominant_emotion = video_data.get('dominant_emotion', 'neutral')
        engagement = video_data.get('engagement_score', 70)
        
        # Determine nervousness level
        nervousness = 'low'
        if engagement < 50:
            nervousness = 'high'
        elif engagement < 70:
            nervousness = 'moderate'
        
        # Determine confidence from engagement and emotion
        confidence = engagement
        if dominant_emotion in ['happy', 'focused']:
            confidence += 10
        elif dominant_emotion in ['sad', 'worried']:
            confidence -= 10
        confidence = max(0, min(100, confidence))
        
        # Eye contact quality
        eye_contact_quality = 'excellent' if eye_contact_pct > 70 else \
                             'good' if eye_contact_pct > 50 else \
                             'needs improvement'
        
        return {
            'confidence_level': round(confidence, 1),
            'nervousness': nervousness,
            'eye_contact': eye_contact_quality,
            'eye_contact_percentage': round(eye_contact_pct, 1),
            'dominant_emotion': dominant_emotion,
            'engagement_score': round(engagement, 1)
        }
    
    def _analyze_text_metrics(self, text: str) -> Dict:
        """Analyze basic text metrics"""
        words = word_tokenize(text.lower())
        sentences = sent_tokenize(text)
        content_words = [w for w in words if w.isalpha() and w not in self.stop_words]
        
        avg_word_length = sum(len(w) for w in content_words) / len(content_words) if content_words else 0
        avg_sentence_length = len(words) / len(sentences) if sentences else 0
        
        return {
            'word_count': len(words),
            'sentence_count': len(sentences),
            'content_word_count': len(content_words),
            'avg_word_length': round(avg_word_length, 2),
            'avg_sentence_length': round(avg_sentence_length, 2),
            'unique_words': len(set(content_words)),
            'vocabulary_richness': round(len(set(content_words)) / len(content_words), 3) if content_words else 0
        }
    
    def _analyze_content_quality(self, text: str, question: str) -> Dict:
        """Analyze content quality and specificity"""
        text_lower = text.lower()
        
        # Check for examples and specificity
        has_numbers = bool(re.search(r'\d+', text))
        has_examples = any(phrase in text_lower for phrase in 
                          ['for example', 'for instance', 'such as', 'like when', 'specifically'])
        has_quantification = any(word in text_lower for word in 
                                ['increased', 'decreased', 'improved', 'reduced', 'achieved', 
                                 'percent', '%', 'times', 'doubled', 'tripled'])
        
        # Check for STAR method indicators
        has_situation = any(word in text_lower for word in ['situation', 'context', 'background'])
        has_task = any(word in text_lower for word in ['task', 'goal', 'objective', 'challenge'])
        has_action = any(word in text_lower for word in ['action', 'did', 'implemented', 'developed'])
        has_result = any(word in text_lower for word in ['result', 'outcome', 'impact', 'achievement'])
        
        # Calculate quality score
        quality_score = 50  # Base score
        if has_numbers: quality_score += 10
        if has_examples: quality_score += 15
        if has_quantification: quality_score += 15
        if has_situation: quality_score += 5
        if has_task: quality_score += 5
        if has_action: quality_score += 5
        if has_result: quality_score += 10
        
        quality_score = min(100, quality_score)
        
        return {
            'quality_score': quality_score,
            'has_specific_examples': has_examples,
            'has_quantifiable_results': has_quantification,
            'has_numbers': has_numbers,
            'uses_star_method': has_situation and has_task and has_action and has_result
        }
    
    def _analyze_sentiment(self, text: str) -> Dict:
        """Analyze sentiment and confidence"""
        scores = self.sentiment_analyzer.polarity_scores(text)
        blob = TextBlob(text)
        
        # Calculate confidence level based on sentiment
        confidence = 50 + (scores['pos'] * 50) - (scores['neg'] * 30)
        confidence = max(0, min(100, confidence))
        
        return {
            'polarity': round(blob.sentiment.polarity, 3),
            'subjectivity': round(blob.sentiment.subjectivity, 3),
            'positive_score': round(scores['pos'], 3),
            'negative_score': round(scores['neg'], 3),
            'neutral_score': round(scores['neu'], 3),
            'confidence_level': round(confidence, 1),
            'enthusiasm_score': round(scores['pos'] * 100, 1)
        }
    
    def _analyze_relevance(self, answer: str, question: str) -> Dict:
        """Analyze answer relevance to question"""
        answer_words = set(word_tokenize(answer.lower()))
        question_words = set(word_tokenize(question.lower()))
        
        # Remove stop words
        answer_words = {w for w in answer_words if w.isalpha() and w not in self.stop_words}
        question_words = {w for w in question_words if w.isalpha() and w not in self.stop_words}
        
        # Calculate overlap
        overlap = answer_words.intersection(question_words)
        relevance = (len(overlap) / len(question_words)) * 100 if question_words else 50
        relevance = min(100, relevance * 1.5)  # Boost the score slightly
        
        return {
            'relevance_score': round(relevance, 1),
            'keyword_overlap': len(overlap),
            'directly_addresses_question': len(overlap) >= len(question_words) * 0.3
        }
    
    def _analyze_clarity(self, text: str) -> Dict:
        """Analyze clarity and structure"""
        text_lower = text.lower()
        
        # Check for transition words
        transitions = ['first', 'second', 'then', 'next', 'finally', 'additionally', 
                      'moreover', 'however', 'therefore', 'consequently']
        transition_count = sum(1 for t in transitions if t in text_lower)
        
        # Calculate clarity score
        clarity_score = 60  # Base score
        clarity_score += min(transition_count * 8, 24)  # Up to +24 for transitions
        
        # Penalize if too many short sentences or too few
        sentences = sent_tokenize(text)
        avg_sentence_length = len(word_tokenize(text)) / len(sentences) if sentences else 0
        if 10 < avg_sentence_length < 25:
            clarity_score += 16
        elif avg_sentence_length < 5:
            clarity_score -= 10
        
        clarity_score = max(0, min(100, clarity_score))
        
        return {
            'clarity_score': clarity_score,
            'has_structure': transition_count > 0,
            'transition_words': transition_count
        }
    
    def _analyze_professionalism(self, text: str) -> Dict:
        """Analyze professionalism"""
        text_lower = text.lower()
        
        # Professional phrases
        professional_phrases = [
            'experience', 'responsible for', 'achieved', 'developed', 
            'implemented', 'collaborated', 'managed', 'led', 'initiated'
        ]
        professional_count = sum(1 for phrase in professional_phrases if phrase in text_lower)
        
        # Casual words
        casual_words = ['gonna', 'wanna', 'kinda', 'sorta', 'yeah', 'stuff', 'things', 'like']
        casual_count = sum(1 for word in casual_words if word in text_lower)
        
        # Calculate score
        prof_score = 70  # Base
        prof_score += professional_count * 5
        prof_score -= casual_count * 10
        prof_score = max(0, min(100, prof_score))
        
        return {
            'professionalism_score': prof_score,
            'professional_language': professional_count,
            'casual_language': casual_count
        }
    
    def _calculate_overall_score(self, analysis: Dict) -> float:
        """Calculate weighted overall score"""
        weights = {
            'content_quality': 0.25,
            'relevance': 0.20,
            'clarity': 0.15,
            'sentiment': 0.10,
            'professionalism': 0.10,
            'speech': 0.15,
            'facial': 0.05
        }
        
        scores = {
            'content_quality': analysis['content_quality']['quality_score'],
            'relevance': analysis['relevance']['relevance_score'],
            'clarity': analysis['clarity']['clarity_score'],
            'sentiment': analysis['sentiment']['confidence_level'],
            'professionalism': analysis['professionalism']['professionalism_score'],
            'speech': analysis.get('speech_features', {}).get('fluency_score', 70),
            'facial': analysis.get('facial_expressions', {}).get('confidence_level', 70)
        }
        
        overall = sum(scores[key] * weights[key] for key in weights.keys())
        return round(overall, 1)
    
    def get_feedback(self, analysis: Dict) -> List[str]:
        """Generate specific, actionable feedback"""
        feedback = []
        
        # Content feedback
        content = analysis['content_quality']
        if not content.get('has_specific_examples'):
            feedback.append("Add specific examples from your experience to illustrate your points")
        if not content.get('has_quantifiable_results'):
            feedback.append("Include measurable results (percentages, numbers, metrics) to demonstrate impact")
        if content['quality_score'] < 60:
            feedback.append("Provide more detailed responses with concrete details and outcomes")
        
        # Speech feedback
        if 'speech_features' in analysis:
            speech = analysis['speech_features']
            if speech['filler_word_count'] > 3:
                feedback.append(f"Reduce filler words (found {speech['filler_word_count']} instances of 'um', 'uh', 'like')")
            if speech['stuttering_instances'] > 0:
                feedback.append("Practice your answers to reduce stuttering and improve fluency")
            if speech['speaking_pace'] in ['too slow', 'too fast']:
                feedback.append(f"Adjust your speaking pace (currently {speech['speaking_pace']}) to 130-160 words/minute")
        
        # Facial expression feedback
        if 'facial_expressions' in analysis:
            facial = analysis['facial_expressions']
            if facial.get('eye_contact_percentage', 100) < 50:
                feedback.append("Maintain better eye contact with the camera (look directly at it)")
            if facial.get('nervousness') == 'high':
                feedback.append("Try to relax and appear more confident - take deep breaths before answering")
            if facial.get('engagement_score', 100) < 60:
                feedback.append("Show more enthusiasm and engagement through your facial expressions")
        
        # Relevance feedback
        if analysis['relevance']['relevance_score'] < 60:
            feedback.append("Ensure your answer directly addresses what was asked in the question")
        
        # Clarity feedback
        if analysis['clarity']['clarity_score'] < 60:
            feedback.append("Structure your answer better using transitions (first, then, finally)")
        
        # Professionalism feedback
        if analysis['professionalism']['professionalism_score'] < 60:
            feedback.append("Use more professional language and avoid casual expressions")
        
        # Length feedback
        word_count = analysis['text_metrics']['word_count']
        if word_count < 30:
            feedback.append("Provide longer, more detailed answers (aim for 50-150 words)")
        elif word_count > 200:
            feedback.append("Keep answers more concise and focused on key points")
        
        # If no issues, give encouragement
        if not feedback:
            feedback.append("Excellent answer! Keep up the great work!")
        
        return feedback[:5]  # Return top 5 feedback points
    
    def _get_empty_analysis(self) -> Dict:
        """Return empty analysis"""
        return {
            'text_metrics': {'word_count': 0},
            'content_quality': {'quality_score': 0},
            'sentiment': {'confidence_level': 0},
            'relevance': {'relevance_score': 0},
            'clarity': {'clarity_score': 0},
            'professionalism': {'professionalism_score': 0},
            'speech_features': {'fluency_score': 0},
            'facial_expressions': {'confidence_level': 0},
            'overall_score': 0
        }