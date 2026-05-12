# Smart Medical Assistant using Multi-Agent LLM 

## 📌 Project Overview
Medical prescriptions are often difficult for patients to understand due to handwritten text, medical abbreviations, complex drug names, and dosage instructions. This can lead to confusion, medication errors, and poor treatment adherence.

The **Smart Medical Assistant** is an AI-powered healthcare support system that helps users interpret medical prescriptions in a clear and patient-friendly manner. The system allows users to upload prescription images and generates simplified explanations, safety guidance, and structured medical information using a **multi-agent Large Language Model (LLM) architecture**.

This project integrates **computer vision, natural language processing, pretrained LLMs, and safety validation mechanisms** to deliver an end-to-end intelligent healthcare assistant.

---

## 🎯 Objectives
- Extract text from prescription images using OCR
- Identify key medical entities such as medicines, dosage, and frequency
- Generate patient-friendly explanations using LLMs
- Validate outputs for safety and ethical compliance
- Provide assistive guidance without replacing professional medical advice
- Locate nearby doctors and hospitals based on user queries

---

## 🧠 System Architecture (Multi-Agent Design)
The system follows a **multi-agent orchestration approach**, where each agent is responsible for a specialized task.

### 🔹 Agents Overview
1. **Orchestrator (`src/orchestrate.py`)**
   - The central controller that manages the workflow.
   - Routes user requests (images or text) to the appropriate specialist agent.
   - Classifies user intent (Medical Chat vs. Location Search).

2. **Medical Agent (`src/agents/medic_agent.py`)**
   - **Vision Task**: Handles OCR to extract text from prescription images.
   - **Chat Task**: Uses an LLM to explain medicines, side effects, and usage instructions in simple language.

3. **Location Agent (`src/agents/locate_agent.py`)**
   - Handles requests for finding doctors, clinics, or hospitals.
   - Uses geolocation tools to provide nearby medical recommendations.

4. **Helpers (`src/helpers/`)**
   - `ocr_model.py`: Handles the optical character recognition logic.
   - `chat_llm.py`: Interfaces with the Large Language Model for generating responses.
   - `doc_locate.py`: Logic for searching medical facilities.
   - `validate.py`: Ensures safety and adds disclaimers to the output.

### 📂 Project Structure
```text
MediScan/
├── data/                     # Data storage (images, dataset, etc.)
├── src/
│   ├── agents/               # Specialist Agents
│   │   ├── medic_agent.py    # Handles OCR & Medical Chat
│   │   └── locate_agent.py   # Handles Doctor/Hospital Search
│   ├── helpers/              # Utility Scripts
│   │   ├── chat_llm.py       # LLM Interface
│   │   ├── doc_locate.py     # Geolocation Logic
│   │   ├── ocr_model.py      # OCR Logic
│   │   └── validate.py       # Safety Validation
│   └── orchestrate.py        # Main Controller
├── test/
│   ├── chat.ipynb            # Notebook for downloading the model
│   ├── ocr.ipynb             # Notebook for testing the OCR model
│   └── location.ipynb        # Notebook for testing the location agent
├── app.py                    # Streamlit Frontend
├── requirements.txt          # Project Dependencies
└── README.md                 # Project Documentation
```

---

## 🔄 Complete Workflow
1. **Image Upload**: User uploads a prescription image via the Streamlit UI.
2. **Routing**: `app.py` sends the image to the **Orchestrator**.
3. **Processing**: The Orchestrator routes the image to the **Medical Agent**, which uses `ocr_model.py` to extract text.
4. **Interaction**: User asks a question (e.g., "What is this medicine?" or "Find a cardiologist nearby").
5. **Intent Classification**: The Orchestrator determines if the query is **Medical** or **Location-based**.
6. **Response Generation**:
   - **Medical Queries**: Handled by **Medical Agent** (using `chat_llm.py`).
   - **Location Queries**: Handled by **Location Agent** (using `doc_locate.py`).
7. **Validation**: Responses are checked by `validate.py` for safety.
8. **Display**: The final answer is shown to the user in the UI.

![Multi agent LLM Architecture](data/detail_diagram.png)
---



## 🛠️ Installation & Usage

### Prerequisites

* **Python 3.10+** (Recommended)
* **Git** installed.
* **Jupyter Notebook** (to run the setup script).
* *(Optional)* NVIDIA GPU with CUDA drivers (for faster local AI performance).

### Installation Steps

1. **Clone the Repository**
```bash
git clone https://github.com/SanjayKumar3110/MediScan.git
cd Mediscan/
```

2. **Create a Virtual Environment**
```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
# Mac/Linux:
source .venv/bin/activate
```

3. **Install Dependencies**
```bash
pip install -r requirements.txt
```

*Note: If you have an NVIDIA GPU, ensure `llama-cpp-python` is installed with CUDA support for better performance.*
4. **Set Up Environment Variables**
* Create a file named `.env` in the root directory.
* Add your Google Gemini API key (for OCR):

```env
API_KEY_EXTRACTION=your_gemini_api_key_here
```

5. **📥 Download Local Meditron Model**
* Before running the app, you must download the local LLM weights.
1. Navigate to the `test/` folder.
2. Open **`chat.ipynb`** in Jupyter Notebook or VS Code.
3. **Run the first cell** (labeled "Download Model").
4. Wait for the download to complete. This will verify your setup and save the model file (`Meditron3-Gemma2-2B.Q4_K_M.gguf`) into the `models/` directory.

6. **🚀 Run the Application**
```bash
streamlit run app.py
```
---

## 📖 How to Use

### Mode 1: Prescription Analysis (The "Eyes")

1. **Select Mode:** Choose **"Prescription Analysis"** from the sidebar (or let the Orchestrator decide).
2. **Upload:** Drop an image of a medical prescription (JPG/PNG).
3. **Analyze:** Click the **"Analyse Prescription"** button.
* The **OCR Agent** will extract text (Patient Name, Medicines, Dosages).
* The **Safety Agent** will scan for potential drug interactions.


4. **Chat:** Ask questions like *"What is Metformin used for?"* or *"Are there side effects?"*. The local **Medical Agent** will answer privately.

### Mode 2: Find a Doctor (The "Location")

1. **Ask Directly:** You don't need to change menus. Just type in the chat:
* *"Find a cardiologist in Coimbatore"*
* *"Where is the nearest hospital?"*


2. **View Results:** The **Location Agent** will return a list of nearby clinics with Clickable Google Maps Links

---

## 🧩 Technologies & Tools Used

### 🔹 Programming Language

* **Python 3.10+**

### 🔹 Architecture

* **Multi-Agent System**: Custom Orchestrator design with specialized agents (`MedicalAgent`, `LocationAgent`).

### 🔹 Frontend / UI
* **Streamlit**: Used for the interactive web interface and session state management.

### 🔹 AI & Machine Learning

* **Vision & OCR**: **Google Gemini 2.5 Flash** (via `google-generativeai`).
 *Used for*: Handwriting recognition and entity extraction from prescription images.


* **Local LLM (Chat)**: **Meditron3-Gemma2-2B** (GGUF Quantized).
 *Runtime*: **llama.cpp** (via `llama-cpp-python`) for efficient local inference on consumer hardware.
* *Used for*: Private, medically-aware conversation and explanation.



### 🔹 Geolocation Services

* **OpenStreetMap (Nominatim)**: Used for finding nearby hospitals and specialists without requiring an API key.

### 🔹 Key Libraries

* `streamlit`: Web UI.
* `google-generativeai`: Google AI Studio SDK.
* `llama-cpp-python`: To run the GGUF model locally with GPU acceleration.
* `huggingface_hub`: To download the quantized Meditron model.
* `python-dotenv`: For secure environment variable management.
* `requests`: For connecting to the Location API.
* `Pillow` (PIL): For image processing.
* `transformers`: For running the GGUF model locally with GPU acceleration.

## ⚠️ Ethical Considerations & Safety
- The system is designed strictly as an **assistive tool**
- Does **not provide diagnosis or treatment recommendations**
- Explicit medical disclaimers are included
- Encourages users to consult qualified healthcare professionals

---

## 🚀 Expected Outcomes
- Improved patient understanding of prescriptions
- Reduced confusion in medication usage
- Demonstration of LLM-driven multi-agent systems in healthcare
- A scalable architecture for future medical AI applications

---

## 🔮 Future Enhancements
- Multilingual support
- Voice-based interaction
- Doctor and hospital recommendations using geolocation
- Integration with electronic health records (EHR)
- Mobile application deployment

---

## 📚 Academic Relevance
This project demonstrates:
- Practical application of AI in healthcare
- Multi-agent system design using pretrained models
- Ethical and responsible use of Large Language Models
- End-to-end system integration under real-world constraints

---
## Dataset
The dataset used for training is publicly available on **Kaggle**:
- The project uses the [Doctors Handwritten Prescription BD Dataset](https://www.kaggle.com/datasets/mamun1113/doctors-handwritten-prescription-bd-dataset)

---

## 📄 Disclaimer
This application is intended for educational and assistive purposes only.  
It does not replace professional medical consultation, diagnosis, or treatment.
## License
This project is licensed under the Apache License 2.0.
