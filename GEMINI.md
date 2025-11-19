# RL Swarm - Google Drive Mode

## Project Overview

This project is a fork of the [Gensyn RL Swarm](https://github.com/gensyn-ai/rl-swarm) that has been modified to use Google Drive for coordination, removing the need for blockchain, Docker, and other complex dependencies. The project implements the **SAPO (Swarm sAmpling Policy Optimization)** algorithm for decentralized reinforcement learning.

The core idea is to enable collaborative training of language models where nodes share their experiences (rollouts) through Google Drive, allowing them to learn from each other without the need for a centralized server or a complex P2P network.

The project is written in Python and uses the `torch`, `transformers`, and `accelerate` libraries for deep learning. The `genrl` library, which is included as a vendor dependency, provides the basic building blocks for reinforcement learning.

## Building and Running

The project is designed to be run on Google Colab, but it can also be run locally. All configuration is done through environment variables.

### Prerequisites

- Python 3.8+
- The dependencies listed in `requirements.txt`.

### Installation

```bash
pip install -r requirements.txt
```

### Running the Swarm

The swarm consists of a **coordinator** and one or more **workers**.

**1. Start the Coordinator**

The coordinator is responsible for managing the global state of the swarm, such as the current round number. It does not perform any training.

```bash
export GDRIVE_PATH="/path/to/your/gdrive/rl-swarm"
export EXPERIMENT_NAME="my_sapo_experiment"
export NODE_ROLE="coordinator"
export NODE_ID="coordinator-0"
export MODEL_NAME="openai-community/gpt2" # Or any other Hugging Face model

python -m rgym_exp.runner.swarm_launcher
```

**2. Start one or more Workers**

Workers are responsible for training the model and sharing their experiences with the swarm.

```bash
export GDRIVE_PATH="/path/to/your/gdrive/rl-swarm"
export EXPERIMENT_NAME="my_sapo_experiment"
export NODE_ROLE="worker"
export NODE_ID="worker-1" # Use a unique ID for each worker
export MODEL_NAME="openai-community/gpt2"

python -m rgym_exp.runner.swarm_launcher
```

## Development Conventions

- **Configuration**: All configuration is done through environment variables. There are no YAML or JSON configuration files.
- **Simplicity**: The codebase has been simplified by removing complex dependencies like blockchain, Docker, and Hydra.
- **Modularity**: The code is organized into modules with clear responsibilities. The `rgym_exp` directory contains the main application logic, while the `genrl` directory contains the core reinforcement learning framework.
- **Logging**: The project uses the standard Python `logging` module. Logs are streamed to the console and also saved to Google Drive for persistence.
- **Testing**: The `README.md` file provides instructions for running a series of tests to verify the functionality of the system.
