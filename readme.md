# LexiBot – AI-Powered Wordle Assistant

**LexiBot** is the next-generation Wordle companion app designed to enhance your gameplay with cutting-edge AI. Built with a React frontend and Django backend, LexiBot uses custom NLP models to provide real-time, intelligent word predictions—boosting user accuracy by up to **40%**.

LexiBot is architected for performance and scalability. From premium analytics dashboards to tiered prediction capabilities, LexiBot offers a powerful and seamless user experience. The application is containerized using Docker and designed for scalable deployment on platforms like AWS.

---

## 🚀 Key Features

* **AI-Powered Word Predictions** – Enhance your gameplay with intelligent suggestions based on custom-built NLP models.
* **Real-Time Assistance** – Immediate in-game help with high responsiveness and minimal latency.
* **Cloud Ready** – Built for deployment on AWS with future plans for CI/CD automation and scalable cloud services.

---

## 🧰 Tech Stack

* **Frontend:** React.js (SPA architecture)
* **Backend:** Django (Python)
* **AI/ML:** Custom NLP models
* **Containerization:** Docker
* **Hosting Ready For:** AWS

---

## 🛠️ Getting Started Locally (Dockerized Setup)

To get LexiBot running locally on your machine using Docker, follow the steps below.

### 📁 Step 1: Build the Frontend Assets

From the root of the project, navigate to the `frontend` directory and run:

```bash
cd frontend
yarn build
```

This command generates a production-ready React build inside the `dist` folder, which will be served by the Django server.

---

### 🐳 Step 2: Build the Docker Image

Return to the root of the project and build the Docker image:

```bash
docker build -t lexibot-official .
```

---

### ▶️ Step 3: Run the Application

Once the image is built, run the container:

```bash
docker run -p 8080:80 lexibot-official
```

Visit [http://localhost:8080](http://localhost:8080) in your browser to use LexiBot locally.

---

## 🔐 Prerequisites

* [Docker Desktop](https://www.docker.com/products/docker-desktop)
* [Node.js](https://nodejs.org/) and [Yarn](https://classic.yarnpkg.com/lang/en/docs/install/) (for building the frontend)
* Optional: Python 3.10+ (for development outside Docker)

---

## 🧠 AI Features

### ✨ Word Correction

Mispelled words are automatically corrected to their intended spelling, enhancing both vocabulary development and gameplay performance. LexiBot uses intelligent NLP heuristics to infer user intent and improve accuracy.


![Alt text](<app_screenshots/mispelling.png> "Mispelled word")


![Alt text](<app_screenshots/word-fix.png> "Word corrected")


### 🧠 Bot Performance Comparison

Curious how your solution compares to an AI model? LexiBot includes a custom-built Wordle AI that solves puzzles with optimal strategies. You can compare your guess efficiency against the bot to see how you stack up.


![Alt text](<app_screenshots/winner.png> "Found word of the day!")


![Alt text](<app_screenshots/lexibot-results.png> "Comparison with LexiBot guess sequence")


---

## 📦 Future Enhancements

* Full CI/CD pipeline integration for seamless deployments
* OAuth and user-specific analytics dashboards
* Enhanced prediction engine with continuous learning
* Mobile-first UI design for better accessibility

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

