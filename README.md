* RESTful-tts-wrapper
* author: @alisharify7
* © under GPL-3.0 license.
* email: alisharifyofficial@gmail.com
* https://github.com/alisharify7/RESTful-tts-wrapper

---
<img src="./docs/media/tts-service.png">

---

# TTS Wrapper

This project is a wrapper around the Sahab Text-to-Speech (TTS) service, designed to improve performance and reduce costs. By caching results in Redis and storing audio files in Amazon S3, the system avoids redundant API calls and speeds up response times.

## Features

- 🔊 Convert text to speech using Sahab TTS
- ☁️ Store audio output in Amazon S3
- ⚡ Cache results in Redis for faster access
- 💸 Save costs by preventing duplicate TTS requests
- 🚀 Simple, fast, and scalable design

## How It Works

1. Receives a request containing text (and optionally voice/language settings)
2. Checks Redis cache:
   - If the audio already exists, it returns the cached result
   - Otherwise, it sends the text to Sahab TTS
3. Stores the generated audio file in S3
4. Saves the S3 URL in Redis for future use
5. Returns the URL to the client



## ⚙️ Configuration

To configure the TTS Wrapper service, follow the steps below:

### 1. Copy the Example Environment File

Start by copying the sample environment file:

```bash
cp .env.sample .env
```

### 2. Fill in Required Values

Open the `.env` file and update the values based on your environment and credentials.

| Variable | Description |
|----------|-------------|
| `APP_DEBUG` | Set to `True` to enable debug mode (useful for development). |
| `APP_SECRET_KEY` | A secure secret key for the app (used for sessions, tokens, etc.). |

---

### 🔊 TTS Service Configuration

| Variable | Description |
|----------|-------------|
| `TTS_SERVICE_API_KEY` | Your API key for authenticating with the Sahab TTS service. |
| `TTS_SERVICE_ENDPOINT` | Endpoint for the Sahab TTS API (e.g., `https://.../speech-synthesys`). |

---

### 🧩 API Info

| Variable | Description |
|----------|-------------|
| `API_NAME` | The name of your API (e.g., `tts_service`). |
| `API_ABSOLUTE_VERSION` | Full version number (e.g., `1.0.0`). |
| `API_SHORT_VERSION` | Short version for URLs (e.g., `1` for `/api/v1`). |
| `API_BASE_URL` | Base path for the API (default: `api/v`). |
| `API_DOCS_PREFIX_URL` | URL prefix for API documentation (e.g., `/docs/`). |
| `HIDE_SWAGGER` | Set to `True` to hide Swagger UI in production. |

---

### ⚡ Caching (Redis)

| Variable | Description |
|----------|-------------|
| `CACHE_ENABLE` | Enable Redis-based caching (`True` or `False`). |
| `REDIS_DEFAULT_URI` | Default Redis connection URI. |
| `REDIS_CACHE_URI` | Redis URI used specifically for audio file caching. |
| `REDIS_API_KEY_URI` | Redis URI used for API key caching. |

---

### ☁️ AWS S3 Configuration

| Variable | Description |
|----------|-------------|
| `AWS_ACCESS_KEY_ID` | Your AWS access key. |
| `AWS_SECRET_ACCESS_KEY` | Your AWS secret access key. |
| `AWS_ENDPOINT_URL` | Endpoint URL for S3 or compatible storage (e.g., MinIO). |

---

### 🌐 Server Settings

| Variable | Description |
|----------|-------------|
| `SERVER_NAME` | Hostname and port the service should bind to (e.g., `localhost:8000`). |

---

### ✅ Example `.env` Setup

```env
APP_DEBUG=True
APP_SECRET_KEY=supersecure

TTS_SERVICE_API_KEY=your_api_key
TTS_SERVICE_ENDPOINT=https://partai.gw.isahab.ir/TextToSpeech/v1/speech-synthesys

API_NAME=tts_service
API_ABSOLUTE_VERSION=1.0.0
API_SHORT_VERSION=1
API_BASE_URL=api/v
API_DOCS_PREFIX_URL=/docs/
HIDE_SWAGGER=True

CACHE_ENABLE=True

AWS_ACCESS_KEY_ID=your_aws_key
AWS_SECRET_ACCESS_KEY=your_aws_secret
AWS_ENDPOINT_URL=https://s3.your-provider.com

REDIS_DEFAULT_URI=redis://localhost:6379/0
REDIS_CACHE_URI=redis://localhost:6379/1
REDIS_API_KEY_URI=redis://localhost:6379/2

SERVER_NAME=localhost:8000
```


