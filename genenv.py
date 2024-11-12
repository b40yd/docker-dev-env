import toml
import os
from typer import Typer
from jinja2 import Environment, FileSystemLoader

app = Typer()
env = Environment(loader=FileSystemLoader('.'))

@app.command(name="gvnc", help="generate vector nginx clickhouse config file.")
def generate_vector_nginx_clickhouse(config: str = './config.toml', template_dir: str = './templates', outputs: str = "outputs"):
    with open(config, 'r') as file:
        config_obj = toml.load(file)
    
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
database = "{clickhouse_database}"
user = "{clickhouse_user}"
password = "{clickhouse_password}"
"""
    with open(f'config.toml', 'w') as file:
        file.write(config)

if __name__ == '__main__':
    app()