import toml
import os
from typer import Typer
from jinja2 import Environment, FileSystemLoader
from pydantic import BaseModel, Field, field_validator
from typing import Optional

app = Typer()
env = Environment(loader=FileSystemLoader('.'))

class NginxConfig(BaseModel):
    port: int = Field(..., ge=1, le=65535, description="Port number must be between 1 and 65535")
    path: str = Field(..., min_length=1, max_length=255, description="Path must be between 1 and 255 characters")
    config_path: str = Field(..., min_length=1, max_length=255, description="Config path must be between 1 and 255 characters")
    log_path: str = Field(..., min_length=1, max_length=255, description="Log path must be between 1 and 255 characters")
    worker_connections: int = Field(..., ge=1, le=100000, description="Worker connections must be between 1 and 100000")


class ClickhouseConfig(BaseModel):
    port: int = Field(..., ge=1, le=65535, description="Port number must be between 1 and 65535")
    database: str = Field(..., min_length=1, max_length=50, description="Database name must be between 1 and 50 characters")
    user: str = Field(..., min_length=1, max_length=50, description="User name must be between 1 and 50 characters")
    password: Optional[str] = Field(default="", min_length=0, max_length=50, description="Password must be between 0 and 50 characters")


class Config(BaseModel):
    nginx: NginxConfig
    clickhouse: ClickhouseConfig

@app.command(name="gvnc", help="generate vector nginx clickhouse config file.")
def generate_vector_nginx_clickhouse(config: str = './config.toml', template_dir: str = './templates', outputs: str = "outputs"):
    with open(config, 'r') as file:
        config_obj = Config(**toml.load(file))
    
    templates = {
        'docker-compose.yaml': env.get_template(f'{template_dir}/docker-compose.yaml.j2'),
        'nginx.conf': env.get_template(f'{template_dir}/nginx.conf.j2'),
        'vector.toml': env.get_template(f'{template_dir}/vector.toml.j2')
    }
    
    for name, template in templates.items():
        output = template.render(config_obj)
        if not os.path.exists(outputs):
            os.mkdir(outputs)

        with open(f'{outputs}/{name}', 'w') as file:
            file.write(output)

@app.command(name="gc", help="generate config.")
def generate_config(nginx_port=8888, 
                    nginx_path="/etc/nginx", 
                    nginx_config_path="/etc/nginx/conf.d", 
                    nginx_log_path="/var/log/nginx", 
                    nginx_worker_connections=1024,
                    clickhouse_port=8123,
                    clickhouse_database="default", 
                    clickhouse_user="default", 
                    clickhouse_password=""):
    config = f"""[nginx]
port = "{nginx_port}"
path = "{nginx_path}"
config_path = "{nginx_config_path}"
log_path = "{nginx_log_path}"
worker_connections = "{nginx_worker_connections}"

[clickhouse]
port = "{clickhouse_port}"
database = "{clickhouse_database}"
user = "{clickhouse_user}"
password = "{clickhouse_password}"
"""
    with open(f'config.toml', 'w') as file:
        file.write(config)

if __name__ == '__main__':
    app()