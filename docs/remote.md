# SSH Remote Setup

## 1. Install SSH Server (Target Linux)

```bash
sudo apt install -y openssh-server
sudo systemctl enable --now ssh
```

If UFW is enabled:

```bash
sudo ufw allow OpenSSH
```

## 2. Install SSH Client (Agent)

Linux:

```bash
sudo apt install -y openssh-client
```

Android Termux:

```bash
pkg install openssh python
```

## 3. Generate SSH Key (Agent)

```bash
ssh-keygen -t ed25519
```

## 4. Copy Public Key (Agent → Target)

```bash
ssh-copy-id user@192.168.1.100
```

For localhost testing:

```bash
ssh-copy-id "$USER@localhost"
```

## 5. Verify Connection

```bash
ssh -o BatchMode=yes user@192.168.1.100 hostname
```

Verify the server fingerprint when connecting for the first time.

## 6. Execute Remote Recipe

```bash
agent remote-check --host user@192.168.1.100 --run
```

Localhost testing:

```bash
agent remote-check --host localhost --run
```

**Notes:**
- SSH key authentication is required for non-interactive execution.
- Agent automatically transfers referenced scripts and snippets.
- Python 3 is required on the target only for Python-based recipes.
- Never share your private SSH key.