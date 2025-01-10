# LangChain Server

## Overview

This project sets up a simple API server using LangChain's Runnable interfaces. It leverages FastAPI for the web framework, SQLModel for database interactions, and various other libraries for specific functionalities like image generation and embeddings.

## Setup

### Prerequisites

- Python 3.11
- Docker
- Poetry

### Installation

1. **Clone the repository:**

	```sh
	git clone <repository-url>
	cd <repository-directory>
	```

2. **Install dependencies:**

	```sh
	poetry install
	```

3. **Set up environment variables:**

	Create a `.env` file in the root directory and add the following:

	```env
	OPENAI_API_KEY=your_openai_api_key
	TAVILY_API_KEY=your_tavily_api_key
	LANGFUSE_PUBLIC_KEY=your_langfuse_public_key
	LANGFUSE_SECRET_KEY=your_langfuse_secret_key
	LANGFUSE_HOST=https://cloud.langfuse.com
	```

### Running the Server

1. **Using Docker:**

	```sh
	docker-compose up --build
	```

2. **Locally:**

	```sh
	uvicorn app.server:app --host 0.0.0.0 --port 8080
	```

## Endpoints

### Conversations

- **Create a new conversation:**

	```http
	POST /{user_id}/conversations
	```

- **Get conversations based on user_id:**

	```http
	GET /{user_id}/conversations
	```

- **Get a specific conversation:**

	```http
	GET /{user_id}/conversations/{conversation_id}
	```

### File Upload

- **Upload a file:**

	```http
	POST /files/upload
	```

### Image Generation

- **Generate an image:**

	```http
	POST /generate_image
	```

## Key Components

- **Server:** [app/server.py](app/server.py)
- **Agent:** [app/agent.py](app/agent.py)
- **Database:** [app/database.py](app/database.py)
- **Embeddings:** [app/embeddings.py](app/embeddings.py)
- **Image Generation:** [app/image_gen.py](app/image_gen.py)
- **Models:** [app/models.py](app/models.py)
- **SQL History:** [app/sql_history.py](app/sql_history.py)

## Configuration

Configuration settings are managed in [app/config.py](app/config.py).

## Database

Database setup and table creation are handled in [app/database.py](app/database.py). The database engine is initialized and tables are created on server startup.