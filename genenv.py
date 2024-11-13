import toml
import os
from typer import Typer
from jinja2 import Environment, FileSystemLoader, Template
from pydantic import BaseModel, Field
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

def generate_nginx_server():
    server = '''
server {
    listen 80;

    location / {
        root /usr/share/nginx/html;
        index index.html;
    }
}
'''
    return Template(server)

@app.command(name="gvnc", help="generate vector nginx clickhouse config file.")
def generate_vector_nginx_clickhouse(config: str = './config.toml', template_dir: str = './templates', outputs: str = "outputs/vector-nginx-clickhouse"):
    with open(config, 'r') as file:
        config_obj = Config(**toml.load(file))

    template_dir = template_dir.rstrip('/')
    
    templates = {
        'docker/nginx_vector/Dockerfile': env.get_template(f'{template_dir}/docker/nginx_vector/Dockerfile.j2'),
        'docker/nginx_vector/entrypoint.sh': env.get_template(f'{template_dir}/docker/nginx_vector/entrypoint.sh.j2'),
        'docker/repos/debian.list': env.get_template(f'{template_dir}/docker/repos/debian.list.j2'),
        'docker-compose.yaml': env.get_template(f'{template_dir}/vector-nginx-clickhouse/docker-compose.yaml.j2'),
        'nginx.conf': env.get_template(f'{template_dir}/vector-nginx-clickhouse/nginx.conf.j2'),
        'nginx_conf.d/default.conf': generate_nginx_server(),
        'vector.toml': env.get_template(f'{template_dir}/vector-nginx-clickhouse/vector.toml.j2')
    }
    
    for name, template in templates.items():
        output = template.render(config_obj)
        file = f"{outputs}/{name}"
        file_dir = os.path.dirname(file)
        if not os.path.isdir(file_dir):
            os.makedirs(file_dir, exist_ok=True)

        with open(file, 'w') as file:
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