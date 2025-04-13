# 🚀 OPNsense Gateway Healthcheck – A Dockerized Monitoring Helper Tool

<p align="center">
  <img src="https://img.shields.io/github/stars/laitco/opnsense-gateway-healthcheck?style=social" alt="GitHub Stars">
  <img src="https://img.shields.io/github/actions/workflow/status/laitco/opnsense-gateway-healthcheck/publish-image.yaml?branch=main" alt="GitHub Workflow Status">
  <img src="https://img.shields.io/docker/pulls/laitco/opnsense-gateway-healthcheck" alt="Docker Pulls">
  <img src="https://img.shields.io/github/license/laitco/opnsense-gateway-healthcheck" alt="License">
  <img src="https://img.shields.io/badge/python-3.9-blue" alt="Python Version">
  <img src="https://img.shields.io/badge/code%20style-flake8-blue" alt="Code Style">
  <img src="https://img.shields.io/github/last-commit/laitco/opnsense-gateway-healthcheck" alt="Last Commit">
  <img src="https://img.shields.io/github/issues/laitco/opnsense-gateway-healthcheck" alt="Open Issues">
</p>

## 📖 Table of Contents
- [✨ Description](#-description)
- [🌟 Features](#-features)
- [📡 Endpoints](#-endpoints)
  - [`/health`](#health)
  - [`/health/<name>`](#healthname)
  - [`/health/<address>`](#healthaddress)
  - [`/health/healthy`](#healthhealthy)
  - [`/health/unhealthy`](#healthunhealthy)
- [⚙️ Configuration](#️-configuration)
- [🐳 Running with Docker](#-running-with-docker)
  - [Build and Run Locally](#build-and-run-locally)
  - [Run from Docker Hub](#run-from-docker-hub)
- [📜 License](#-license)
- [🤝 Contributing](#-contributing)

## ✨ Description

A Python-based Flask application to monitor the health of gateways in an OPNsense network. The application provides endpoints to check the health status of all gateways, specific gateways by name or address, and lists of healthy or unhealthy gateways.

## 🌟 Features

- **Health Status**: Check the health of all gateways in the OPNsense network.
- **Gateway Lookup**: Query the health of a specific gateway by name or address (case-insensitive).
- **Healthy Gateways**: List all healthy gateways.
- **Unhealthy Gateways**: List all unhealthy gateways.

## 📡 Endpoints

### `/health`
Returns the health status of all gateways.

**Example Response**:
```json
{
  "items": [
    {
      "address": "12.34.56.789",
      "name": "WAN",
      "status_translated": "Online",
      "healthy": true
    }
  ]
}
```

### `/health/<name>`
Returns the health status of a specific gateway by name (case-insensitive).

**Example**:
```
GET /health/WAN
```

**Example Response**:
```json
{
  "address": "12.34.56.789",
  "name": "WAN",
  "status_translated": "Online",
  "healthy": true
}
```

### `/health/<address>`
Returns the health status of a specific gateway by address. This endpoint is particularly useful for gateways with static public IPs.

**Example**:
```
GET /health/12.34.56.789
```

**Example Response**:
```json
{
  "address": "12.34.56.789",
  "name": "WAN",
  "status_translated": "Online",
  "healthy": true
}
```

### `/health/healthy`
Returns a list of all healthy gateways.

### `/health/unhealthy`
Returns a list of all unhealthy gateways.

## ⚙️ Configuration

The application is configured using environment variables:

| Variable         | Default Value              | Description                                      |
|------------------|----------------------------|--------------------------------------------------|
| `API_KEY`        | None                       | The API key for OPNsense authentication.         |
| `API_SECRET`     | None                       | The API secret for OPNsense authentication.      |
| `OPNSENSE_PORT`    | `443`                      | The port used to connect to the OPNsense instance. |
| `OPNSENSE_BASE_URL` | `https://opnsense.example.com` | The base URL of the OPNsense instance.          |
| `PORT`           | `5000`                     | The port the application runs on.               |

## 🐳 Running with Docker

### Build and Run Locally

1. **Build the Docker Image**:
   ```bash
   docker build -t laitco/opnsense-gateway-healthcheck .
   ```

2. **Run the Docker Container**:
   ```bash
   docker run -d -p 5000:5000 \
       -e API_KEY="your-api-key" \
       -e API_SECRET="your-api-secret" \
       -e OPNSENSE_BASE_URL="https://opnsense.example.com" \
       -e OPNSENSE_PORT="443" \
       --name opnsense-gateway-healthcheck laitco/opnsense-gateway-healthcheck
   ```

3. **Access the Application**:
   Open your browser and navigate to:
   ```
   http://IP-ADDRESS_OR_HOSTNAME:5000/health
   ```

### Run from Docker Hub

1. **Pull the Docker Image**:
   ```bash
   docker pull laitco/opnsense-gateway-healthcheck:latest
   ```

2. **Run the Docker Container**:
   ```bash
   docker run -d -p 5000:5000 \
       -e API_KEY="your-api-key" \
       -e API_SECRET="your-api-secret" \
       -e OPNSENSE_BASE_URL="https://opnsense.example.com" \
       -e OPNSENSE_PORT="443" \
       --name opnsense-gateway-healthcheck laitco/opnsense-gateway-healthcheck:latest
   ```

3. **Access the Application**:
   Open your browser and navigate to:
   ```
   http://IP-ADDRESS_OR_HOSTNAME:5000/health
   ```

## 📜 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## 🤝 Contributing

Contributions are welcome! Please open an issue or submit a pull request.