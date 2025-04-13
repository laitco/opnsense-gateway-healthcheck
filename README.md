# 🚀 OPNsense Gateway Healthcheck – A Dockerized Monitoring Helper Tool

<p align="center">
  <img src="https://img.shields.io/github/stars/laitco/opnsense-gateway-healthcheck?style=social" alt="GitHub Stars">
  <img src="https://img.shields.io/github/actions/workflow/status/laitco/opnsense-gateway-healthcheck/publish-image.yaml?branch=main" alt="GitHub Workflow Status">
  <img src="https://img.shields.io/badge/python-3.9-blue" alt="Python Version">
  <img src="https://img.shields.io/badge/code%20style-flake8-blue" alt="Code Style">
  <img src="https://img.shields.io/github/last-commit/laitco/opnsense-gateway-healthcheck" alt="Last Commit">
  <img src="https://img.shields.io/github/issues/laitco/opnsense-gateway-healthcheck" alt="Open Issues">
</p>

<p align="center">
  <img src=".github/images/opnsense_gateway_healthcheck_logo.png" alt="OPNsense Gateway Healthcheck Logo" width="630">
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
- [🔑 How to Create an API Key on OPNsense](#-how-to-create-an-api-key-on-opnsense)
- [⚠️ Important Notes](#️-important-notes)
  - [Gateway Monitoring](#gateway-monitoring)
  - [Offline State](#offline-state)
- [🐳 Running with Docker](#-running-with-docker)
  - [Build and Run Locally](#build-and-run-locally)
  - [Run from Docker Hub](#run-from-docker-hub)
- [📡 Integration with Gatus Monitoring System](#-integration-with-gatus-monitoring-system)
- [📜 License](#-license)
- [🤝 Contributing](#-contributing)

## ✨ Description

A Python-based Flask application to monitor the health of gateways in an OPNsense network. The application provides endpoints to check the health status of all gateways, specific gateways by name or address, and lists of healthy or unhealthy gateways. These gateways can include both internet service provider (ISP) and VPN-based gateways.

## 🌟 Features

- **Health Status**: Check the health of all gateways in the OPNsense network.
- **Gateway Lookup**: Query the health of a specific gateway by name or address (case-insensitive).
- **Healthy Gateways**: List all healthy gateways.
- **Unhealthy Gateways**: List all unhealthy gateways.

## 📝 Release Notes

### Version 1.0
- Initial release with basic health check functionality for OPNsense gateways.

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
      "healthy": true,
      "..."
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
  "healthy": true,
  "..."
}
```

### `/health/<address>`
Returns the health status of a specific gateway by address. This endpoint is particularly useful for gateways with static (public) IPs.

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
  "healthy": true,
  "..."
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

## 🔑 How to Create an API Key on OPNsense

API keys are managed in the user manager (`system_usermanager.php`). Follow these steps to create an API key:

1. Navigate to the **User Manager** page in OPNsense.
2. Select a user for whom you want to create the API key.
3. Scroll down to the **API** section for this user.
4. Click on the `+` sign to add a new key.
5. Once the key is created, you will receive a single download containing the credentials in a text file (INI formatted).

The contents of this file will look like this:

```
[API]
key = your-api-key
secret = your-secret-key
```

For more details, refer to the [OPNsense API Documentation](https://docs.opnsense.org/development/how-tos/api.html).

## ⚠️ Important Notes

### Gateway Monitoring

To monitor gateways, **gateway monitoring must be enabled** on the gateways you wish to monitor. This is a critical requirement for the healthcheck application to function correctly.

### Offline State

The offline state of a gateway is determined based on the configured thresholds for **packet loss** and **latency** in the advanced settings of OPNsense. Ensure these thresholds are properly configured to reflect your monitoring needs.

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

## 📡 Integration with Gatus Monitoring System

You can integrate this healthcheck application with the [Gatus](https://github.com/TwiN/gatus) monitoring system to monitor the health of specific devices.

### Example Configuration

```yaml
endpoints:
  - name: tailscale-examplehostname.example.com
    group: tailscale
    url: "http://IP-ADDRESS_OR_HOSTNAME:5000/health/examplegatewayname"
    interval: 5m
    conditions:
      - "[STATUS] == 200"
      - "[BODY].healthy == pat(*true*)"
    alerts:
      - type: email
        failure-threshold: 2
        success-threshold: 3
        description: "healthcheck failed"
        send-on-resolved: true
```

### Explanation

- **`name`**: A descriptive name for the endpoint being monitored.
- **`group`**: A logical grouping for endpoints (e.g., `gateways`).
- **`url`**: The URL of the healthcheck endpoint for a specific gateway.
- **`interval`**: The frequency of the healthcheck (e.g., every 5 minutes).
- **`conditions`**:
  - `[STATUS] == 200`: Ensures the HTTP status code is `200`.
  - `[BODY].healthy == pat(*true*)`: Checks if the `healthy` field in the response body is `true`.
- **`alerts`**:
  - **`type`**: The type of alert (e.g., `email`).
  - **`failure-threshold`**: The number of consecutive failures before triggering an alert.
  - **`success-threshold`**: The number of consecutive successes before resolving an alert.
  - **`description`**: A description of the alert.
  - **`send-on-resolved`**: Whether to send a notification when the issue is resolved.

For more details on configuring Gatus, refer to the [Gatus documentation](https://github.com/TwiN/gatus).

## 📜 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## 🤝 Contributing

Contributions are welcome! Please open an issue or submit a pull request.