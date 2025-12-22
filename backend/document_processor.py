"""
Document Processor Module
Handles PDF, DOCX, and TXT document parsing
Adapted from legal_document_analysis repository
"""
import os
import io
from typing import Optional
from pathlib import Path
import PyPDF2
from docx import Document
from PIL import Image
import pytesseract

class DocumentProcessor:
    """Process various document formats and extract text"""
    
    def __init__(self):
        self.supported_formats = ['.pdf', '.docx', '.doc', '.txt']
    
    def process_document(self, file_path: str) -> dict:
        """
        Process a document and extract text
        
        Args:
            file_path: Path to the document file
            
        Returns:
            dict with 'text', 'pages', and 'metadata'
        """
        file_path = Path(file_path)
        extension = file_path.suffix.lower()
        
        if extension == '.pdf':
            return self._process_pdf(file_path)
        elif extension in ['.docx', '.doc']:
            return self._process_docx(file_path)
        elif extension == '.txt':
            return self._process_txt(file_path)
        else:
            raise ValueError(f"Unsupported file format: {extension}")
    
    def _process_pdf(self, file_path: Path) -> dict:
        """Extract text from PDF files"""
        text = ""
        pages = []
        metadata = {}
        
        try:
            with open(file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                metadata = {
                    'num_pages': len(pdf_reader.pages),
                    'author': pdf_reader.metadata.get('/Author', '') if pdf_reader.metadata else '',
                    'title': pdf_reader.metadata.get('/Title', '') if pdf_reader.metadata else '',
                }
                
                for page_num, page in enumerate(pdf_reader.pages, 1):
                    page_text = page.extract_text()
                    pages.append({
                        'page_number': page_num,
                        'text': page_text
                    })
                    text += page_text + "\n\n"
        
        except Exception as e:
            raise Exception(f"Error processing PDF: {str(e)}")
        
        return {
            'text': text.strip(),
            'pages': pages,
            'metadata': metadata
        }
    
    def _process_docx(self, file_path: Path) -> dict:
        """Extract text from DOCX files"""
        try:
            doc = Document(file_path)
            paragraphs = [para.text for para in doc.paragraphs if para.text.strip()]
            text = "\n\n".join(paragraphs)
            
            metadata = {
                'num_paragraphs': len(paragraphs),
                'author': doc.core_properties.author,
                'title': doc.core_properties.title,
            }
            
            return {
                'text': text,
                'pages': [{'page_number': 1, 'text': text}],  # DOCX doesn't have pages
                'metadata': metadata
            }
        except Exception as e:
            raise Exception(f"Error processing DOCX: {str(e)}")
    
    def _process_txt(self, file_path: Path) -> dict:
        """Extract text from TXT files"""
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                text = file.read()
            
            return {
                'text': text,
                'pages': [{'page_number': 1, 'text': text}],
                'metadata': {'format': 'txt'}
            }
        except Exception as e:
            raise Exception(f"Error processing TXT: {str(e)}")
    
    def extract_text_from_image(self, image_path: str) -> str:
        """
        Extract text from image using OCR (for scanned documents)
        Requires tesseract to be installed
        """
        try:
            image = Image.open(image_path)
            text = pytesseract.image_to_string(image)
            return text
        except Exception as e:
            raise Exception(f"Error in OCR: {str(e)}")
