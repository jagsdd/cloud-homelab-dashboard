## Architecture

The application is split into three layers:

### Routes
Responsible for handling HTTP requests and responses.

### Services
Responsible for business logic and validation.

### Repositories
Responsible for database communication.

### Deployment
The application is deployed using the Docker image published to GitHub Container Registry.
To deploy a specific image version:

```bash
IMAGE_TAG=<version> docker compose -f docker-compose.prod.yml up -d


