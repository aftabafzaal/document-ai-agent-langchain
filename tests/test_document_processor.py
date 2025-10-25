import pytest
import tempfile
import os
from pathlib import Path
from src.core.langchain_loader import LangChainDocumentProcessor

class TestDocumentProcessor:
    def setup_method(self):
        self.processor = LangChainDocumentProcessor()
        self.test_dir = tempfile.mkdtemp()
    
    def test_txt_processing(self):
        """Test TXT file processing"""
        test_content = "This is a test document content."
        test_file = os.path.join(self.test_dir, "test.txt")
        
        with open(test_file, 'w') as f:
            f.write(test_content)
        
        documents = self.processor.load_documents_from_folder(self.test_dir)
        assert len(documents) > 0
        assert test_content in documents[0].page_content
    
    def test_unsupported_format(self):
        """Test handling of unsupported formats"""
        test_file = os.path.join(self.test_dir, "test.unsupported")
        
        with open(test_file, 'w') as f:
            f.write("test content")
        
        documents = self.processor.load_documents_from_folder(self.test_dir)
        assert len(documents) == 0