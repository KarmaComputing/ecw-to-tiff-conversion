# ecw-to-tiff-conversion

## How to run it
```
cd ecw-to-tiff-conversion
# change UPLOAD_FOLDER_MOUNT_PATH to the right setting
cp .env.example .env
docker-compose up --build
```
### How to run it using a windows host 
Docker Desktop should be changed to use WSL2 mode

1. How to install WSL2 
https://learn.microsoft.com/en-us/windows/wsl/install-manual

2. How to enable WSL2 with docker-desktop
https://docs.docker.com/desktop/wsl/

3. Clone the repo
https://github.com/KarmaComputing/ecw-to-tiff-conversion.git

4. Do the "How to run it" section
