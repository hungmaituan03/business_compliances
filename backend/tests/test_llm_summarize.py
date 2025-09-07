import unittest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from LLM_summarize import summarize_with_llm

class TestLLMSummarize(unittest.TestCase):
    def test_summarize_with_llm(self):
        # This test only checks if the function returns a non-empty string for a valid IRS URL
        url = "https://www.irs.gov/businesses/small-businesses-self-employed/self-employed-individuals-tax-center"
        result = summarize_with_llm(url)
        self.assertIsInstance(result, str)
        self.assertTrue(len(result) > 0)

if __name__ == "__main__":
    unittest.main()
