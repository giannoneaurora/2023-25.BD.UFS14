from unittest.mock import patch, Mock
from io import BytesIO


from function_app import scarica_pdf 
from jsonschema import validate

pdf_schema = {
    "type": "object",
    "properties": {
        "content_type": {"type": "string"},
        "binary_content": {"type": "string"}
    },
    "required": ["content_type", "binary_content"]
}


# Wrapper function for schema validation
def validate_pdf_content(instance):
    schema_instance = {
        "content_type": "application/pdf",
        "binary_content": isinstance(instance, BytesIO)
    }
    try:
        validate(instance=schema_instance, schema=pdf_schema)
        return True
    except Exception as e:
        print(f"Schema validation error: {e}")
        return False


def test_scarica_pdf_success():
    url = ""
    pdf_content = scarica_pdf(url)
    
    assert pdf_content is not None, "Expected a valid PDF content."
    assert validate_pdf_content(pdf_content), "Downloaded content does not match PDF schema."

def test_scarica_pdf_non_pdf():
    url = ""
    pdf_content = scarica_pdf(url)

    assert pdf_content is None, "Expected None for non-PDF content."


def test_scarica_pdf_http_error():
    url = ""
    pdf_content = scarica_pdf(url)

    assert pdf_content is None, "Expected None for HTTP error."


def test_scarica_pdf_network_error():
    url = "http://10.255.255.1"  
    pdf_content = scarica_pdf(url)

    assert pdf_content is None, "Expected None for network error."


# Run all tests
if __name__ == "__main__":
    test_scarica_pdf_success()
    print("Test case 1 (Successful PDF download): Passed")
    
    test_scarica_pdf_non_pdf()
    print("Test case 2 (Non-PDF content type): Passed")
    
    test_scarica_pdf_http_error()
    print("Test case 3 (HTTP error): Passed")
    
    test_scarica_pdf_network_error()
    print("Test case 4 (Network error): Passed")

