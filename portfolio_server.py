# 🚀 Interactive Portfolio & Resume AI Agent

An interactive portfolio and resume website powered by a custom multi-threaded Python server and an integrated AI Agent backend.

---

## 🌟 Key Features

* **AI Agent Chatbot:** Integrated conversational backend (`/api/chat`) designed to answer questions about projects, experience, and skills.
* **Multi-Threaded Server:** Built with Python's `ThreadingHTTPServer` for concurrent request handling and non-blocking asset delivery.
* **Instant Rebind Support:** Configured with `allow_reuse_address = True` to eliminate port-blocking delays on restart.
* **Responsive Portfolio Showcase:** Clean UI highlighting projects, technical stack, and interactive elements.
* **Developer First DX:** Includes ANSI-colored CLI status dashboard and automatic browser launching.

---

## 🛠️ Tech Stack

* **Backend:** Python 3 (`http.server`, `threading`, `json`, `webbrowser`)
* **Frontend:** HTML5, CSS3, JavaScript (ES6+)
* **Architecture:** RESTful endpoint (`/api/chat`) communicating with a conversational agent pipeline

---

## 🚀 Quick Start

### 1. Clone the Repository
```bash
git clone https://github.com/rishthik2007-commits/Resume.git
cd Resume
python server.py