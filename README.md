# File and Directory Info

File and Directory Info is a REST API run using docker. Running this API successfully will yield information on your directories and files given starting from a root you provide. This API supports hidden files, read-only files, and complex directories. You can optionally print this information in a pretty format or as a JSON blob.

## Installation

1) Ensure Docker is supported from your machine -> [download docker](https://www.docker.com/products/docker-desktop)

2) Clone the git repository to the file system you wish to test

```bash
git clone https://github.com/ngott/File-and-Directory-Info.git
```

3) Navigate to the right directory

```bash
cd File-and-Directory-Info/WeaveGrid/
```

4) Build the docker container!

```bash
docker build -t <Name_The_Container> .
```

## Usage

Arguement Flags
- --root: provide a root directory (full path or releative path)
- (optional) --print-pretty: pretty print instead of a json blob

Run the container

```bash
docker run -it <Name_The_Container> [Flags]
```
Output

1) JSON blob to stdout organized to show the directories and files in a tree format with file name, owner, size, permissions, and contents.
2) Same as number (1.) but printed linearly in an easier to read format.

## Testing

A testing file is provided in the WeaveGrid directory called "test_file_info.py". To run these unittests execute:

```bash
python3 -m unittest test_file_info
```
