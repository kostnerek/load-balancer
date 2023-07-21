import subprocess
from jinja2 import Template
import sys

def generate_nginx_conf(num_replicas):
    # Generate the upstream block template for Jinja2
    upstream_template = Template("""
# nginx.conf

events {
  worker_connections  1024;  # Adjust this number based on your requirements
}

http {
  upstream backend_servers {
        {% for i in range(num_replicas) %}
        server backend{{ i }}:3000;
        {% endfor %}
    }

  server {
    listen 80;

    location / {
      proxy_pass http://backend_servers;
      proxy_set_header Host $host;
      proxy_set_header X-Real-IP $remote_addr;
    }
  }
}
""")

    # Render the template with the specified number of replicas
    upstream_block = upstream_template.render(num_replicas=num_replicas)

    # Write the generated upstream block to nginx.conf
    with open('nginx.conf', 'w') as f:
        f.write(upstream_block)

def generate_docker_compose(num_replicas):
    # Generate the Docker Compose YAML template for Jinja2
    docker_compose_template = Template("""
version: "3.8"

services:
  nginx:
    container_name: nginx
    build:
      context: .
      dockerfile: Dockerfile.nginx
    ports:
      - "80:80" # Expose the load balancer on port 80
    networks:
      - my-network
    depends_on:
      {% for i in range(num_replicas) %}
      - backend{{ i }}
      {% endfor %}

{% for i in range(num_replicas) %}
  backend{{ i }}:
    container_name: backend{{ i }}
    build:
      context: .
      dockerfile: Dockerfile
    volumes:
      - .:/app
    ports:
      - "3000" # Expose the backend service on port 3000 for the load balancer
    networks:
      - my-network
{% endfor %}
networks:
  my-network: # Create a custom network to allow communication between containers
    driver: bridge
""")

    # Render the template with the specified number of replicas
    docker_compose_yaml = docker_compose_template.render(num_replicas=num_replicas)

    # Write the generated Docker Compose YAML to docker-compose.yml
    with open('docker-compose.yml', 'w') as f:
        f.write(docker_compose_yaml)

if __name__ == "__main__":
    # Define the desired number of replicas
    num_replicas = 1
    try:
        num_replicas = int(sys.argv[1])  # Set this to the desired number of replicas
    except: pass

    # Generate the nginx.conf file
    generate_nginx_conf(num_replicas)

    # Generate the Docker Compose YAML file
    generate_docker_compose(num_replicas)
