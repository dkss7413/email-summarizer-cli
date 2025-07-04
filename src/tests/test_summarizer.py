# summarizer 테스트 코드 

import sys
import os
import unittest

# 현재 디렉토리를 Python 경로에 추가
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from email_summarizer.summarizer import TextSummarizer
from email_summarizer.utils import detect_language


class TestTextSummarizer(unittest.TestCase):
    def setUp(self):
        self.summarizer = TextSummarizer()
        
    def test_language_detection(self):
        """언어 감지 기능 테스트"""
        korean_text = "안녕하세요. 이것은 한국어 텍스트입니다."
        english_text = "Hello. This is English text."
        mixed_text = "안녕하세요. This is mixed text."
        
        self.assertEqual(detect_language(korean_text), "Korean")
        self.assertEqual(detect_language(english_text), "English")
        self.assertEqual(detect_language(mixed_text), "Mixed")
    
    def test_summarization(self):
        """요약 기능 테스트"""
        test_text = """
        인공지능(AI)은 컴퓨터 시스템이 인간의 지능을 모방하여 학습하고, 
        추론하고, 문제를 해결할 수 있도록 하는 기술입니다. 
        머신러닝은 AI의 한 분야로, 데이터로부터 패턴을 학습하여 
        예측이나 분류를 수행합니다. 딥러닝은 머신러닝의 하위 분야로, 
        인공신경망을 사용하여 복잡한 패턴을 학습합니다.
        """
        
        summary = self.summarizer.summarize(test_text)
        self.assertIsInstance(summary, str)
        self.assertGreater(len(summary), 0)
        self.assertLess(len(summary), len(test_text))


if __name__ == '__main__':
    unittest.main() 