from src.agents.medic_agent import MedicalAgent
from src.agents.locate_agent import LocationAgent

class Orchestrator:
    """
    The Main Controller.
    Routes user requests to the appropriate specialist agent.
    """
    
    def __init__(self):
        print("--- System: Initializing Agents ---")
        self.medical_agent = MedicalAgent()
        self.location_agent = LocationAgent()
        
    def route_request(self, user_input, image=None, context=None):
        """
        Decides whether to perform OCR, Medical Chat, or Location Search.
        
        Args:
            user_input (str): Text from the user.
            image (file): Uploaded image (optional).
            context (str): Previous extracted text (optional).
        """
        
        # PRIORITY 1: Image Analysis
        # If an image is provided, it ALWAYS goes to the Medical Agent.
        if image:
            print("Orchestrator: Routing to >> MedicalAgent (Vision Task)")
            return self.medical_agent.process_prescription(image)

        # PRIORITY 2: Contextual Chat
        # If we have previous prescription context and the user is NOT asking for location,
        # assume they are asking about the medicine.
        intent = self._classify_intent(user_input)
        
        if context and intent == "medical_chat":
            print("Orchestrator: Routing to >> MedicalAgent (Chat Task)")
            return self.medical_agent.chat(user_input, context)

        # PRIORITY 3: Location Search
        if intent == "location_search":
            print("Orchestrator: Routing to >> LocationAgent")
            return self.location_agent.find_doctors(user_input)
            
        # Fallback
        return "I can help you analyze prescriptions or find nearby doctors. Please upload an image or ask 'Where is a hospital?'"

    def _classify_intent(self, text):
        """
        Simple keyword-based intent classifier.
        """
        text = text.lower()
        
        # Keywords that strongly suggest a Location intent
        location_keywords = [
            "find", "where", "location", "near", "nearby", "hospital", 
            "clinic", "doctor", "cardiologist", "neurologist", "map"
        ]
        
        if any(word in text for word in location_keywords):
            return "location_search"
            
        return "medical_chat"