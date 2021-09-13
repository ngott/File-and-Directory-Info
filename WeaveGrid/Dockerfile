FROM python:3

COPY . .

# $0 will get the first input flag
# $@ will get the rest of the inputs
ENTRYPOINT python3 file_info.py $0 $@
