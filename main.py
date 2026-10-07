from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from dotenv import dotenv_values
import yaml
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 1. DEFAULT CONFIGURATION

config = {
    "port": 8000,
    "workers": 1,
    "debug": False,
    "log_level": "info",
    "api_key": "default-secret-000",
}


# 2. LOAD YAML CONFIGURATION

with open("config.development.yaml", "r") as f:
    yaml_config = yaml.safe_load(f)

if yaml_config:
    config.update(yaml_config)


# 3. LOAD .ENV CONFIGURATION

env_config = dotenv_values(".env")

if "NUM_WORKERS" in env_config:
    config["workers"] = env_config["NUM_WORKERS"]

if "APP_LOG_LEVEL" in env_config:
    config["log_level"] = env_config["APP_LOG_LEVEL"]

if "APP_PORT" in env_config:
    config["port"] = env_config["APP_PORT"]

if "APP_DEBUG" in env_config:
    config["debug"] = env_config["APP_DEBUG"]

if "APP_API_KEY" in env_config:
    config["api_key"] = env_config["APP_API_KEY"]


# 4. LOAD OS ENVIRONMENT VARIABLES

env_mapping = {
    "APP_PORT": "port",
    "APP_WORKERS": "workers",
    "APP_DEBUG": "debug",
    "APP_LOG_LEVEL": "log_level",
    "APP_API_KEY": "api_key",
}

for env_name, config_key in env_mapping.items():
    if env_name in os.environ:
        config[config_key] = os.environ[env_name]


# TYPE CONVERSION

def convert_value(key, value):

    if key in ["port", "workers"]:
        return int(value)

    if key == "debug":
        return str(value).lower() in ["true", "1", "yes", "on"]

    return str(value)


@app.get("/effective-config")
async def effective_config(request: Request):

    # Start with configuration from the four layers
    final_config = config.copy()

    # Get all ?set= parameters
    overrides = request.query_params.getlist("set")

    # Apply CLI-style overrides
    for override in overrides:

        if "=" not in override:
            continue

        key, value = override.split("=", 1)

        if key in final_config:
            final_config[key] = convert_value(key, value)


    for key in final_config:
        final_config[key] = convert_value(key, final_config[key])

    # NEVER expose the real API key
    final_config["api_key"] = "****"

    return final_config