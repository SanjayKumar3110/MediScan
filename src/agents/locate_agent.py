import src.helpers.doc_locate as location_tool # Assuming you renamed location_service.py to doc_locate.py per your screenshot

class LocationAgent:
    """
    Agent responsible for finding medical services.
    """
    def find_doctors(self, user_query):
        """
        Parses user query and finds nearby doctors.
        Input: "Find a Cardiologist in Coimbatore"
        Output: Formatted string with map links.
        """
        print(f"LocationAgent: Analyzing query '{user_query}'...")
        
        # 1. Simple Entity Extraction (Rule-Based for now)
        # In a real app, you might use a small NLP model here.
        city = "Coimbatore" # Default fallback
        specialty = None
        
        # basic parsing logic
        words = user_query.split()
        if "in" in words:
            try:
                # "Cardiologist in Chennai" -> Grab "Chennai"
                idx = words.index("in")
                if idx + 1 < len(words):
                    city = words[idx + 1]
            except:
                pass
                
        # Check for specialties
        common_specialties = ["cardiologist", "neurologist", "dentist", "dermatologist", "hospital", "pharmacy"]
        for s in common_specialties:
            if s in user_query.lower():
                specialty = s.capitalize()
                break
        
        # 2. Call the Helper Tool
        print(f"LocationAgent: Searching for {specialty} in {city}...")
        results = location_tool.nearby_medic(city, specialty)
        
        return results