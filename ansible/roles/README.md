# Web App Role

An Ansible role to deploy a web application using Docker Compose.

## Requirements

- Ansible 2.9+
- Docker
- Docker Compose Plugin

## Role Dependencies

This role depends on:
- geerlingguy.docker (version 7.1.0)

## Role Variables

### Defaults

| Variable     | Default | Description                                                |
| ------------ | ------- | ---------------------------------------------------------- |
| wipe_web_app | false   | When true, removes the application container and directory |
| app_path     | /app    | Application deployment directory                           |

## Example Playbook

```yaml
name: Deploy app to host
hosts: vagrant_hosts
become: yes
roles:
web_app
vars:
app_path: "/custom/path"
wipe_web_app: false
```


## Tags

- `wipe-web-app`: Use this tag to remove the application and its data

## Features

1. **Docker Integration**: Seamless integration with Docker and Docker Compose
2. **File Synchronization**: Uses rsync to efficiently transfer application files
3. **Idempotent Deployment**: Safe to run multiple times
4. **Cleanup Functionality**: Includes ability to wipe application when needed

## Development Setup

This role has been tested using Vagrant with VMware Desktop provider. See the Vagrant configuration in the parent directory for the development environment setup.

## License

MIT

## Author

Demezy