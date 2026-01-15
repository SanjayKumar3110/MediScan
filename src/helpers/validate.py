# Utility functions
import os
from llama_cpp import Llama

def load_config():
    pass

# --- Global Model Loader ---
_local_llm = None

DRUG_INTERACTIONS_KB = {
    "aspirin": ["warfarin", "ibuprofen", "blood thinners"],
    "amoxicillin": ["methotrexate", "birth control"],
    "metformin": ["alcohol", "contrast dye"],
    "ibuprofen": ["aspirin", "naproxen"]
}

def local_model():
    global _local_llm
    # Path to downloaded GGUF file
    model_path = "./models/Meditron3-Gemma2-2B.Q4_K_M.gguf"
    
    if _local_llm is None:
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Model file missing: {model_path}. Run download script first.")
            
        print("Loading Meditron3 model to GPU...")
        _local_llm = Llama(
            model_path=model_path,
            n_gpu_layers=-1,  # -1 = Offload everything to your RTX 2050
            n_ctx=4096,       # Context window size
            verbose=False     # Turn off technical logs
        )
    return _local_llm

def safety_check(extracted_text, response_text):
    """
    1. Checks for dangerous keywords.
    2. Adds mandatory medical disclaimer.
    3. Cross-checks with Knowledge Base for interactions.
    """
    
    # 1. Knowledge Base Check (Simple String Matching)
    warnings = []
    text_lower = extracted_text.lower()
    
    for drug, bad_mixes in DRUG_INTERACTIONS_KB.items():
        if drug in text_lower:
            for bad_mix in bad_mixes:
                # If the user asks about a bad mix, or if the bad mix is also in the prescription
                if bad_mix in text_lower:
                    warnings.append(f"⚠️ **INTERACTION WARNING:** {drug.title()} may interact with {bad_mix.title()}.")

    # 2. Disclaimer Injection
    disclaimer = "\n\n---\n*Disclaimer: I am an AI assistant, not a doctor. This information is for educational purposes only. Always verify with a certified medical professional.*"
    
    # Combine everything
    final_output = response_text + disclaimer
    
    if warnings:
        # Prepend warnings to the top
        final_output = "\n".join(warnings) + "\n\n" + final_output
        
    return final_output
