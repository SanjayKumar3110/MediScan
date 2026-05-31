import src.helpers.ocr_model as ocr_tool
import src.helpers.chat_llm as chat_tool
# import src.helpers.utils as utils  # Uncomment if you have validation utils later

class MedicalAgent:
    """
    Agent responsible for all medical interpretation tasks.
    It manages the OCR extraction and the Meditron-based conversation.
    """

    def __init__(self):
        pass

    def process_prescription(self, image_file):
        print("--- MedicalAgent: Received image for processing ---")

        try:
            print("MedicalAgent: Delegating task to OCR Helper...")
            extracted_text = ocr_tool.ocr_extraction(image_file)
            
            if not extracted_text:
                return "Error: No text could be extracted. The image might be too blurry."
                
            return extracted_text

        except Exception as e:
            return f"MedicalAgent Error (OCR): {str(e)}"

    def chat(self, user_query, prescription_context):
        # 1. Validation
        if not prescription_context:
            return "I need to analyze a prescription first before I can answer questions about it."

        # 2. Delegate to Chat Tool (Meditron)
        try:
            print(f"MedicalAgent: Processing query: '{user_query}'")
            response = chat_tool.medical_chat(user_query, prescription_context)
            
            return response

        except Exception as e:
            return f"MedicalAgent Error (Chat): {str(e)}"