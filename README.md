# 🚀 Automated Documentation Generator for Capella using AI

## 📌 Project Overview
This project automates the process of **generating documentation from Capella diagrams** using **Python** and **OpenAI API**. It extracts **entities, relationships, and system workflows** directly from Capella models and converts them into structured documentation, reducing **manual effort and time consumption**.

## 🎯 Key Features
- 🔍 **Automated Extraction**: Reads entities and relationships from Capella diagrams.
- 📝 **AI-Powered Documentation**: Uses OpenAI API to generate structured text.
- ⚡ **Time-Saving**: Eliminates the need for manual documentation.
- 🔄 **Scalable & Customizable**: Can be expanded to support different diagram types.
- 📂 **Stored & Shareable**: Generated documentation is saved for easy access.

---

## ⚙️ Technology Stack
- **Capella** (Modeling Tool)
- **Python** (Backend Processing)
- **OpenAI API** (AI-based Text Generation)
- **Hugging Face API** (Alternative AI Testing)
- **Java** (Capella Integrations)

---

## 📑 Project Structure
📂 capella-doc-generator │── 📂 src # Source Code │ │── extract.py # Reads entities & relationships from Capella │ │── generate.py # Calls OpenAI API for documentation generation │ │── store.py # Saves generated documentation │ │── main.py # Main execution file │── 📂 docs # Generated Documentation │── 📂 tests # Testing Scripts │── README.md # Project Documentation (this file) │── requirements.txt # Required Dependencies │── LICENSE # License Information


---

## 🚀 Installation & Setup

### **1️⃣ Prerequisites**
- Install **Python 3.10** (Recommended for compatibility)
- Install **Capella 5.0** (If working with this version)
- Get an **OpenAI API key** (For AI-based documentation generation)

### **2️⃣ Clone the Repository**
```sh
git clone https://github.com/your-username/capella-doc-generator.git
cd capella-doc-generator

```

### 3️⃣ Install Dependencies
```sh
pip install -r requirements.txt
```

### 4️⃣ Set Up OpenAI API Key
Create a .env file and add your API key:
```sh
OPENAI_API_KEY=your-api-key-here

```
### 5️⃣ Run the Script
```sh
python main.py

```

