#!/bin/bash

set -e

IMAGE_TAG="$1"

if [ -z "$IMAGE_TAG" ]; then
    echo "Usage: ./deploy.sh <image-tag>"
    exit 1
fi

CURRENT_IMAGE=$(docker inspect --format '{{.Config.Image}}' cloud-dashboard 2>/dev/null || true)

if [ -n "$CURRENT_IMAGE" ]; then
    echo "Current image: $CURRENT_IMAGE"
else
    echo "Current image: none"
fi

PREVIOUS_IMAGE="$CURRENT_IMAGE"

PREVIOUS_TAG=""

if [ -n "$PREVIOUS_IMAGE" ]; then
	PREVIOUS_TAG="${PREVIOUS_IMAGE##*:}"
fi

rollback() {
    if [ -z "$PREVIOUS_TAG" ]; then
        echo "No previous image available for rollback."
        exit 1
    fi

    echo "Rolling back to: $PREVIOUS_TAG"

    IMAGE_TAG="$PREVIOUS_TAG" docker compose -f docker-compose.deploy.yml pull
    IMAGE_TAG="$PREVIOUS_TAG" docker compose -f docker-compose.deploy.yml up -d

    echo "Waiting for rollback health..."

    for i in {1..30}; do
        if curl -fs http://localhost:5000/health > /dev/null; then
            EXPECTED_ROLLBACK_IMAGE="ghcr.io/jagsdd/cloud-homelab-dashboard:$PREVIOUS_TAG"
            ACTUAL_ROLLBACK_IMAGE=$(docker inspect --format '{{.Config.Image}}' cloud-dashboard)

            echo "Expected rollback image: $EXPECTED_ROLLBACK_IMAGE"
            echo "Actual rollback image:   $ACTUAL_ROLLBACK_IMAGE"

            if [ "$ACTUAL_ROLLBACK_IMAGE" != "$EXPECTED_ROLLBACK_IMAGE" ]; then
                echo "ERROR: Rollback image does not match previous image."
                exit 1
            fi

            echo "Rollback application is healthy."
            echo "Checking Prometheus after rollback..."

            ROLLBACK_PROMETHEUS_UP=$(curl -fs 'http://localhost:9090/api/v1/query?query=up%7Bjob%3D%22cloud-dashboard%22%7D' | grep -o '"value":\[[^]]*,"1"' || true)

            if [ -z "$ROLLBACK_PROMETHEUS_UP" ]; then
                echo "ERROR: Prometheus is not reporting the rolled-back dashboard as up."
                exit 1
            fi

            echo "Prometheus is reporting the rolled-back dashboard as up."
            echo "Rollback verified successfully."
            return 0
        fi

        echo "Waiting..."
        sleep 2
    done

    echo "ERROR: Rollback failed."
    exit 1
}

echo "Deploying image: $IMAGE_TAG"

IMAGE_TAG="$IMAGE_TAG" docker compose -f docker-compose.deploy.yml pull

IMAGE_TAG="$IMAGE_TAG" docker compose -f docker-compose.deploy.yml up -d

echo "Waiting for application health..."

HEALTHY=false

for i in {1..30}; do
    if curl -fs http://localhost:5000/health > /dev/null; then
        echo "Application is healthy."
        HEALTHY=true
        break
    fi

    echo "Waiting..."
    sleep 2
done

if [ "$HEALTHY" != "true" ]; then
    echo "ERROR: Application failed health check."
    rollback
fi

EXPECTED_IMAGE="ghcr.io/jagsdd/cloud-homelab-dashboard:$IMAGE_TAG"
ACTUAL_IMAGE=$(docker inspect --format '{{.Config.Image}}' cloud-dashboard)

echo "Expected image: $EXPECTED_IMAGE"
echo "Actual image:   $ACTUAL_IMAGE"

if [ "$ACTUAL_IMAGE" != "$EXPECTED_IMAGE" ]; then
    echo "ERROR: Running image does not match requested image."
    rollback
fi

echo "Checking Prometheus..."

PROMETHEUS_UP=$(curl -fs 'http://localhost:9090/api/v1/query?query=up%7Bjob%3D%22cloud-dashboard%22%7D' | grep -o '"value":\[[^]]*,"1"' || true)

if [ -z "$PROMETHEUS_UP" ]; then
    echo "ERROR: Prometheus is not reporting the dashboard as up."
    rollback
fi

echo "Prometheus is reporting the dashboard as up."
echo "Deployment verified successfully."