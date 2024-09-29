# `netbox_query` Documentation

A command-line interface (CLI) tool for querying devices from a NetBox instance. `netbox_query` allows you to fetch device information and integrate it into your automation workflows.

---

## Table of Contents

- [Installation](#installation)
  - [Installing Directly from GitHub](#installing-directly-from-github)
  - [Requirements](#requirements)
- [Configuration](#configuration)
  - [Setting the Encryption Key](#setting-the-encryption-key)
  - [Saving Base URL and API Token](#saving-base-url-and-api-token)
- [Usage](#usage)
  - [Basic Usage](#basic-usage)
  - [Query with Parameters](#query-with-parameters)
- [Examples](#examples)
  - [Automating Loops with Bash](#automating-loops-with-bash)
    - [SSH into Each Device](#ssh-into-each-device)
  - [Automating Loops with PowerShell](#automating-loops-with-powershell)
    - [SSH into Each Device](#ssh-into-each-device-1)
- [Additional Information](#additional-information)
- [License](#license)
- [Contributing](#contributing)
- [Contact](#contact)

---

## Installation

### Installing Directly from GitHub

You can install `netbox_query` directly from the GitHub repository using `pip`.

```bash
pip install git+https://github.com/edwordout/NETBOX_QUERY.git
```
or
```bash
pip install git+ssh://git@github.com/edwordout/NETBOX_QUERY.git
```

### Requirements

- **Python**: 3.6 or higher
- **Dependencies**: Automatically installed via `pip`
  - `httpx`
  - `cryptography`

---

## Configuration

### Setting the Encryption Key

`netbox_query` uses an encryption key to securely store configuration data. Change the `KEY` variable with your encryption key or set it as the environment variable named `NETBOX_QUERY_KEY`.

**Generate an Encryption Key:**

```python
from cryptography.fernet import Fernet
print(Fernet.generate_key().decode())
```

**Set the Environment Variable:**

- **Unix/Linux/macOS (Bash):**

  ```bash
  export NETBOX_QUERY_KEY='your-encryption-key'
  ```

- **Windows (Command Prompt):**

  ```cmd
  set NETBOX_QUERY_KEY=your-encryption-key
  ```

- **Windows (PowerShell):**

  ```powershell
  $env:NETBOX_QUERY_KEY = 'your-encryption-key'
  ```

**Important:** Replace `'your-encryption-key'` with the key generated.

### Saving Base URL and API Token

The first time you run `netbox_query`, provide your NetBox instance's base URL and API token. These will be securely stored for future use.

```bash
netbox-query --base-url https://netbox.example.com --token your_api_token
```

---

## Usage

### Basic Usage

After initial configuration, you can run `netbox_query` without additional parameters to list all devices.

```bash
netbox-query
```

### Query with Parameters

Filter devices using query parameters. Parameters should be in the format `key=value`.

```bash
netbox-query --params status=active role=server
```

---

## Examples

### Automating Loops with Bash

#### SSH into Each Device

Use the output of `netbox_query` to SSH into each device.

```bash
for device in $(netbox-query --params status=active); do
    ssh user@"$device" 'hostname && uptime'
done
```

**Explanation:**

- Loops through each device name returned by `netbox_query`.
- SSHes into the device and runs `hostname` and `uptime`.

**Ensure:**

- SSH keys are set up for passwordless authentication, or be prepared to enter passwords.
- Replace `user` with your actual username.

### Automating Loops with PowerShell

#### SSH into Each Device

In PowerShell, use the pipeline to process each device.

```powershell
netbox-query --params status=active | ForEach-Object {
    ssh user@$_ 'hostname; uptime'
}
```

**Explanation:**

- Pipes the output of `netbox_query` to `ForEach-Object`.
- SSHes into each device and runs `hostname` and `uptime`.

**Ensure:**

- SSH client is installed on your Windows system.
- Replace `user` with your actual username.

---

## Additional Information

- **SSL Verification:** The tool currently disables SSL verification (`verify=False`). For production environments, consider enabling SSL verification for secure connections.
- **Error Handling:** If an error occurs while fetching devices, an error message with the status code will be displayed.

---

## License

This project is licensed under the terms of the [MIT License](LICENSE).

---

## Contributing

Contributions are welcome! Please open an issue or submit a pull request on GitHub.

---

## Contact

For questions or support, please contact [Eduardo Gomes](mailto:e-gomes@live.com).
