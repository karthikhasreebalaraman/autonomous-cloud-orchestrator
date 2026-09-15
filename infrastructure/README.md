# Member 1 – Cloud Infrastructure & Automatic Execution

## Project

**Autonomous Cloud Infrastructure Orchestrator using Predictive Decision Intelligence**

## Overview

This module handles the **cloud infrastructure and automatic execution** part of the project.

The system uses Docker containers to represent cloud application instances. It monitors the containers, distributes incoming requests, automatically increases or decreases the number of containers based on CPU usage, detects failed containers, and attempts automatic recovery.

The main workflow is:

**Monitor → Predict/Decision → Execute → Verify → Monitor Again**

Member 1 mainly implements the **execution and infrastructure management** part of this workflow.

---

## Technologies Used

- Python
- Docker
- Flask
- Requests

---

## Folder Structure

```text
infrastructure/
│
├── app/
│   ├── app.py
│   ├── Dockerfile
│   └── requirements.txt
│
├── monitor.py
├── autoscaler.py
├── auto_scale.py
├── load_balancer.py
├── load_test.py
├── health_check.py
├── control_api.py
└── README.md