import requests

def nearby_medic(city, specialty=None):
    """
    Searches for medical services using the Free OpenStreetMap (Nominatim) API.
    
    Features:
    - Auto-Fallback: Searches for 'Cardiologist', if none found, searches 'Hospitals'.
    - Contact Info: Aggressively hunts for phone numbers and websites in metadata.
    - Privacy Safe: No API Key required.
    """
    
    # 1. Configuration
    base_url = "https://nominatim.openstreetmap.org/search"
    # User-Agent is REQUIRED by OpenStreetMap policy
    headers = { 'User-Agent': 'SmartMedicalAssistant_StudentProject/1.0' }
    
    # Helper to clean up "Not Listed" data
    def _get_tag(tags, keys):
        if not tags: return None
        for key in keys:
            if tags.get(key):
                return tags.get(key)
        return "Not Listed"

    # Helper function to run the API request
    def _run_search(query_text):
        params = {
            'q': query_text,
            'format': 'json',
            'addressdetails': 1,
            'limit': 5,         # Top 5 results
            'extratags': 1      # CRITICAL: Asks for Phone/Website data
        }
        try:
            r = requests.get(base_url, params=params, headers=headers)
            if r.status_code == 200:
                return r.json()
            return []
        except:
            return []

    # 2. Strategy A: Specific Specialist Search
    # If specialty is provided, try that first (e.g., "Cardiologist in Coimbatore")
    search_query = f"{specialty} in {city}" if specialty else f"Hospitals in {city}"
    print(f"🔎 Connecting to OpenStreetMap... Searching: '{search_query}'")
    
    results = _run_search(search_query)

    # 3. Strategy B: Fallback Logic
    # If specific search failed (empty list), try general "Hospitals"
    if not results and specialty:
        print(f"⚠️ No '{specialty}' found specifically. Switching to general Hospital search...")
        fallback_query = f"Hospitals in {city}"
        results = _run_search(fallback_query)

    if not results:
        return f"❌ No medical services found in {city}. Please check the city name."

    # 4. Format the Output
    output_text = f"### 🏥 Recommended Medical Services in {city}\n"
    if specialty:
        output_text += f"*(Showing results for {specialty} or General Hospitals)*\n"
        
    for place in results:
        # Get Name
        name = place.get('display_name', 'Unknown').split(',')[0]
        
        # Get Coordinates for Google Maps Link
        lat = place.get('lat')
        lon = place.get('lon')
        map_link = f"https://www.google.com/maps/search/?api=1&query={lat},{lon}"

        # Build the String
        output_text += f"\n**{name}**"
        output_text += f"\n📍 [Click to Navigate]({map_link})\n"
        output_text += "---"

    return output_text