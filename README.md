# Linux Black Box

Linux Black Box is a Linux observability and incident-replay platform designed to reconstruct system activity before crashes, slowdowns, and abnormal behavior.

## Current Features

- Process collection
- PID / PPID tracking
- CPU usage
- RAM usage
- Swap statistics
- Disk I/O statistics
- Timestamped telemetry
- JSONL historical storage
- Basic automated tests

## Architecture

```text
Linux Host
   ↓
Collector Agent
   ↓
Process + CPU + RAM + Disk Metrics
   ↓
Telemetry Storage
   ↓
Future Incident Detection
   ↓
Future Incident Replay Dashboard
