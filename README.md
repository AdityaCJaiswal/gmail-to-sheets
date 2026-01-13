# Gmail to Sheets Automation

**Author:** [YOUR FULL NAME]  
**Internship Track:** Full Stack Development

## 🎥 Project Demo
**Watch the full execution and code walkthrough here:** [![Watch the video](https://img.youtube.com/vi/aOiBKP7eMKk/0.jpg)](https://youtu.be/aOiBKP7eMKk)  
[Click to Watch on YouTube](https://youtu.be/aOiBKP7eMKk)

---

## 📋 Project Overview
This tool automates the workflow of tracking specific email notifications. It connects to the **Gmail API** to fetch unread emails, parses relevant data (Sender, Subject, Date, Body), and logs them into a **Google Sheet**.

**Key Use Case:**
In this implementation, the system is configured to track **"LeetCode Weekly Digest"** emails, allowing a developer to automatically archive their coding progress while ignoring other inbox noise.

---

## 🏗 Architecture
![Architecture Diagram](proof/architecture_diagram.png)
*(Note: Please find the hand-drawn architecture diagram in the `proof/` folder as requested.)*

**Flow:**
1.  **Auth:** User authenticates via OAuth 2.0 (Google Cloud).
2.  **Fetch:** Python script queries Gmail for `is:unread` + `subject:"LeetCode Weekly Digest"`.
3.  **Parse:** Script decodes the payload and strips HTML tags to plain text.
4.  **Store:** Data is appended to Google Sheets.
5.  **State:** Processed Email IDs are saved locally to `state.json` to prevent duplicates.

---

## ⚙️ Setup Instructions

### 1. Prerequisites
* Python 3.x installed.
* A Google Cloud Project with **Gmail API** and **Google Sheets API** enabled.

### 2. Installation
```bash
# Clone the repository
git clone <your-repo-link>
cd gmail-to-sheets

# Install dependencies
pip install -r requirements.txt