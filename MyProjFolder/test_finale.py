from unittest.mock import patch, Mock
from io import BytesIO
import requests

from function_app import scarica_pdf 

with patch('requests.get') as mock_get:
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.headers = {'Content-Type': 'application/pdf'}
    mock_response.content = b'%PDF-1.4 binary content here'
    mock_get.return_value = mock_response
    
    pdf_content = scarica_pdf("")
    assert isinstance(pdf_content, BytesIO), "Failed: Expected a BytesIO object for PDF content."
    assert b'%PDF-1.4' in pdf_content.getvalue(), "Failed: PDF content does not match expected content."

print("Test case 1 (Successful PDF download): Passed")


with patch('requests.get') as mock_get:
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.headers = {'Content-Type': 'text/html'}
    mock_response.content = b'<html>Not a PDF</html>'
    mock_get.return_value = mock_response
    
    pdf_content = scarica_pdf("")
    assert pdf_content is None, "Failed: Expected None for non-PDF content type."

print("Test case 2 (Wrong content type): Passed")

with patch('requests.get') as mock_get:
    mock_response = Mock()
    mock_response.status_code = 404
    mock_get.return_value = mock_response
    
    pdf_content = scarica_pdf("")
    assert pdf_content is None, "Failed: Expected None for HTTP error."

print("Test case 3 (HTTP error): Passed")

with patch('requests.get') as mock_get:
    mock_get.side_effect = requests.exceptions.ConnectionError
    
    pdf_content = scarica_pdf("")
    assert pdf_content is None, "Failed: Expected None for network error."

print("Test case 4 (Network error): Passed")
