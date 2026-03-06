# 💠 Crypto Volatility Visualizer

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28%2B-FF4B4B)
![Plotly](https://img.shields.io/badge/Plotly-Interactive-3f4f75)
![Gemini AI](https://img.shields.io/badge/AI-Google_Gemini-10b981)

**Simulating Market Swings with Mathematics for AI & Python**

The **Crypto Volatility Visualizer** is an interactive, web-based quantitative dashboard designed to analyze and simulate cryptocurrency price movements. [cite_start]Built for the *Mathematics for AI-II* coursework, this project bridges the gap between historical financial data and theoretical mathematical modeling.





## ✨ Key Features

* [cite_start]**📊 Professional Market Charting:** Interactive Plotly Candlestick and Volume charts representing real-world historical Bitcoin data, featuring shaded market phase analysis[cite: 2, 5].
* [cite_start]**🧮 Stochastic Harmonic Simulation:** A custom mathematical engine that generates simulated price swings by combining trigonometric wave-like price swings (sine/cosine), sudden jumps (random noise), and long-term drift (integrals)[cite: 2, 6].
* [cite_start]**🎛️ Dynamic Parameter Controls:** Sidebar sliders allow users to manipulate Amplitude (swing size), Frequency (swing speed), Drift, and Noise in real-time to compare stable vs. volatile market conditions[cite: 2, 6].
* **🤖 AI Quantitative Analyst:** Integrated Google Gemini AI that reads live dashboard metrics and provides context-aware financial analysis via 1-click professional prompts.
* **💎 Glassmorphism UI:** A sleek, high-visibility green-themed interface optimized for a premium user experience.



## 📐 The Mathematics Behind the Simulation

Rather than relying on simple line graphs, this dashboard generates simulated market data using a comprehensive mathematical equation:

$$Price(t) = P_0 + (\mu \cdot t) + (A \cdot \sin(\omega t)) + (\sigma \cdot Z_t)$$

* **$P_0$ (Base Price):** The starting asset value.
* **$\mu \cdot t$ (Macro Drift):** Linear algebra representing the long-term trend (Bull or Bear market)[cite: 2, 6].
* **$A \cdot \sin(\omega t)$ (Harmonic Waves):** Trigonometry simulating repeating economic cycles. Amplitude ($A$) controls swing size; [cite_start]Frequency ($\omega$) controls cycle speed[cite: 2, 6].
* [cite_start]**$\sigma \cdot Z_t$ (Random Noise):** Statistical probability representing sudden, unpredictable daily market shocks[cite: 2, 6].



## 🚀 Installation & Local Setup

To run this dashboard locally on your machine, follow these steps:

### 1. Clone the Repository
```bash
git clone [https://github.com/YOUR_GITHUB_USERNAME/YOUR_REPOSITORY_NAME.git](https://github.com/YOUR_GITHUB_USERNAME/YOUR_REPOSITORY_NAME.git)
cd YOUR_REPOSITORY_NAME
