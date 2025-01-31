# ecw-to-tiff-conversion

Use the easy quick web service [ECW to Tiff Online converter](https://ecw-to-tiff-converter.anotherwebservice.com/).

Or, build and run this locally yourself.

## How to run it

There are two different ways to run the converter

1. As a web application (the default)
2. As a quick docker command without the web application

### Run as a web application:

```bash
cd ecw-to-tiff-conversion
# change UPLOAD_FOLDER_MOUNT_PATH to the right setting
cp .env.example .env
docker-compose up --build
```

## Run as a docker script, without needing the web application

Create a directory to store the file(s) you want to convert (e.g. 'uploads').

Run the command as follows:

- Argument one is the filename (*not* filepath) of the file you want to convert
- Argument two is the full path to the folder where you're storing the image

E.g.

```bash
 ./app/ecw-to-COG.sh my-image-file.ecw $(realpath ./uploads)
```

Don't know what `realpath` does? Or on Windows?


```bash
 ./app/ecw-to-COG.sh my-image-file.ecw C:\Users\Documents\uploads)
```

Your file will be converted into a `GTiff` file format, and placed into the uploads folder
with the filename suffix `_converted.tiff`.

### How to run it using a windows host

Docker Desktop should be changed to use WSL2 mode

1. How to install WSL2 
[https://learn.microsoft.com/en-us/windows/wsl/install-manual](https://learn.microsoft.com/en-us/windows/wsl/install-manual)

2. How to enable WSL2 with docker-desktop
[https://docs.docker.com/desktop/wsl/](https://docs.docker.com/desktop/wsl/)

3. Clone the repo
[https://github.com/KarmaComputing/ecw-to-tiff-conversion.git](https://github.com/KarmaComputing/ecw-to-tiff-conversion.git)

4. Do the "How to run it" section
