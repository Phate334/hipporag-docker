# Running HippoRAG in Containers

This project provides a containerized environment for running HippoRAG, leveraging LiteLLM and llama.cpp server to offer a local, OpenAI API-compatible interface. By using Docker containers, you can easily deploy and manage HippoRAG alongside a local LLM backend, enabling efficient and flexible experimentation or development without relying on external APIs.

## Container Images

Container images are automatically built and published to GitHub Container Registry (ghcr.io) via GitHub Actions.

### Available Images

- `ghcr.io/phate334/hipporag-docker:2.0.0a3` - Image tagged with hipporag package version
- `ghcr.io/phate334/hipporag-docker:latest` - Latest build from main branch
- `ghcr.io/phate334/hipporag-docker:main` - Main branch builds
- `ghcr.io/phate334/hipporag-docker:v*` - Tagged releases

### Using Pre-built Images

Instead of building the image locally, you can use the pre-built images:

```bash
# Pull the image tagged with hipporag version
docker pull ghcr.io/phate334/hipporag-docker:2.0.0a3

# Or pull the latest image
docker pull ghcr.io/phate334/hipporag-docker:latest

# Update compose.yaml to use the pre-built image
# Replace the build context with:
# image: ghcr.io/phate334/hipporag-docker:2.0.0a3
```

## Usage

- build the Docker image

```bash
docker build -t hipporag:2.0.0a3 .
```

this will build the Docker image for the HippoRAG. after the build is complete, run the following command to start all containers:

```bash
$ docker images
REPOSITORY                   TAG              IMAGE ID       CREATED         SIZE
hipporag                     2.0.0a3          69748a2d016e   6 minutes ago   11GB
ghcr.io/ggml-org/llama.cpp   server-b5517     707db50b2e0d   37 hours ago    149MB
ghcr.io/berriai/litellm      v1.71.1-stable   317211c421e9   3 days ago      5.55GB
$ docker compose up -d
```

when first time run it, llm and embed containers will download models from huggingface.

## GPU Support

For example to run with NVIDIA GPU, you need to install the NVIDIA Container Toolkit and replace llama.cpp image tag to cuda version in [`compose.yaml`](./compose.yaml). check the latest [llama.cpp package](https://github.com/ggml-org/llama.cpp/pkgs/container/llama.cpp) and choose `server-cuda-<version>` tag, and enable gpu access in `compose.yaml`:

```yaml
services:
  llm:
    image: ghcr.io/ggml-org/llama.cpp:server-cuda-b5517
    ...
    environment:
        ...
        - LLAMA_ARG_N_GPU_LAYERS=99
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: 1
              capabilities: [gpu]
```

more llama-server arguments can be found in the [here](https://github.com/ggml-org/llama.cpp/tree/master/tools/server)
