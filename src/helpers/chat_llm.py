from src.helpers.validate import local_model, safety_check

# --- Chat (Updated to Local Meditron) ---
def medical_chat(user_query, prescription_context):
    """
    Uses Local Meditron model.
    Arguments:
      user_query: The question from the user.
      prescription_context: The text extracted from the image.
    """
    try:
        llm = local_model()
        
        # Minimal Prompt Structure for Gemma-2 based models
        # We strictly pass Context + Question without extra "personality" instructions.
        prompt = f"""<start_of_turn>user
                        Context:
                        {prescription_context}

                        Question:
                        {user_query}<end_of_turn>
                        <start_of_turn>model
                    """

        # Generate response
        output = llm(
            prompt,
            max_tokens=512,
            stop=["<end_of_turn>"], # Critical: stops model from talking to itself
            temperature=0.7,
            echo=False
        )

        raw_response = output['choices'][0]['text'].strip()
        validate_response = safety_check(prescription_context, raw_response)
        
        return validate_response

    except Exception as e:
        return f"Error during local chat: {e}"