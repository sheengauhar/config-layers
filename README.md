# FastAPI Configuration Layer Service

A FastAPI application that merges configuration values from multiple sources using a defined precedence order and supports dynamic runtime overrides through query parameters.

## Live Deployment

**Platform:** Render

**API Endpoint:** [https://config-layers.onrender.com/effective-config](https://config-layers.onrender.com/effective-config)

## Configuration Precedence

Configuration values are merged in the following order (lowest to highest priority):

1. Hardcoded Defaults
2. Environment-specific YAML (`config.development.yaml`)
3. `.env` File
4. OS-level Environment Variables (`APP_` prefix)
5. CLI Overrides (query parameters)

Higher-priority configuration sources override lower-priority values.

## Configuration Layers

### 1. Defaults

| Key       | Value              |
| --------- | ------------------ |
| port      | 8000               |
| workers   | 1                  |
| debug     | false              |
| log_level | info               |
| api_key   | default-secret-000 |

### 2. YAML Configuration

File: `config.development.yaml`

```yaml
workers: 16
```

### 3. Environment File

File: `.env`

```env
APP_PORT=8589
NUM_WORKERS=1
APP_API_KEY=key-tpqgvdtyx2
```

### 4. OS Environment Variables

```env
APP_WORKERS=7
APP_DEBUG=false
```

## API Usage

### GET `/effective-config`

Returns the effective configuration after merging all configuration layers.

**Example request:**

```http
GET /effective-config
```

**Example response:**

```json
{
  "port": 8589,
  "workers": 7,
  "debug": false,
  "log_level": "info",
  "api_key": "****"
}
```

## CLI Overrides

The API accepts multiple `set` query parameters to override configuration values dynamically.

**Example request:**

```http
GET /effective-config?set=port=9000&set=debug=true&set=workers=2
```

**Example response:**

```json
{
  "port": 9000,
  "workers": 2,
  "debug": true,
  "log_level": "info",
  "api_key": "****"
}
```

CLI overrides have the highest precedence and are applied on every request.

## Type Conversion

Configuration values are converted according to their expected types:

- `port`, `workers`: Integer
- `debug`: Boolean (`true`, `1`, `yes`, `on` are interpreted as true, case-insensitive).
- `log_level` and other configuration keys: String.

## Special Handling

- **Alias Mapping:** `NUM_WORKERS` in the `.env` file maps to `workers`.
- **Secret Masking:** The actual API key is never exposed. The response always returns `"****"` for `api_key`.
- **CORS:** Cross-origin requests are enabled to allow browser-based grading.

## Technologies Used

- Python
- FastAPI
- Uvicorn
- PyYAML
- python-dotenv

## Running Locally

Install dependencies:

```bash
pip install -r requirements.txt
```

Start the application:

```bash
uvicorn main:app --reload
```

The API will be available at:

```text
http://localhost:8000
```

Test the endpoint:

```text
http://localhost:8000/effective-config
```

## Deployment

The application is deployed on Render.

**Live URL:**

[https://config-layers.onrender.com/effective-config](https://config-layers.onrender.com/effective-config)

The endpoint supports dynamic configuration overrides through query parameters and returns the effective configuration as JSON.
