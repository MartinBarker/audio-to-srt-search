# How to create python virtual env
python -m venv venv_name
# How to setup/use virt env
Windows: `venv_name\Scripts\activate`
Mac/Linux: `source venv_name/bin/activate`
Leave: `deactivate`
`pip freeze > requirements.txt`
`pip install -r requirements.txt`

# Run script to upload every .srt file to my ec2 elasticsearch instance (linux)
`$ unbuffer python3 upload.py "/mnt/y/Jerma985 Streams Audio/allSrt/" > output.log 2>&1`