# threesixtyeye

Sam Hume's public sandbox repo for 360i hacking. 

This project consists of basic example programs aimed at demonstrating the steps in a 360i pipeline. They will be 
iteratively improved and extended. Some will be replaced by preferred alternatives. They're intended to provide initial 
steps towards a 360i pipeline that will be made available via the CDISC 360i GitHub repo.

## Introduction

These programs are designed to function as command-line applications that can run as standalone applications or can 
be chained together to function as a pipeline of sorts. Everything in this repo should be considered sandbox 
development work in support of the 360i program.

Eventually, these programs will work together to generate the LZZT SDTM datasets and conformance report.

Currently, this pipeline retrieves a raw dataset from a GitHub repository, converts the dataset to Dataset-JSON NDJSON
v1.1, validates the dataset, and posts the dataset to the draft Dataset-JSON API.

## Overview of Programs in the Pipeline

- github2dsj: this program retrieves an LZZT raw dataset file as Dataset-JSON v1.0 from GitHub and saves it to a local directory.
- dsjupversion: this program converts the retrieved dataset to Dataset-JSON NDJSON v1.1
- dsjvalidate: this program validates the Dataset-JSON NDJOSN v1.1 dataset using the LinkML model
- dsj2api: this program posts the upversioned and valid Dataset-JSON v1.1 dataset to a POC Dataset-JSON API

This pipeline will be extended and improved in future iterations. New programs and examples will be added every
couple of weeks.

## Prerequisites

These programs were developed using Python 3.12 and have not been tested using other versions.

Ensure that the config.ini is present. You will need to rename config-template.ini to config.ini. You will need
to update the config.ini to use your GitHub token and the path to your threesixtyeye repository. 

Ensure the config.ini includes a RawDataSource section with values for 
* gh_token: your GitHub token
* gh_user_name: the username for the repository to retrieve the raw LZZT dataset from
* gh_repo_name: the name of the repository to retrieve the dataset from
* gh_repo_path: the path to the dataset to retrieve

Ensure the config.ini includes the following sections and keys:
* Section Study with key study_oid: this should be set to 360i-lzzt
* Section Data with key data_path: path to your data folder
* Section LinkML with key ndjson_linkml_yamlL path and filename for the dataset-ndjson.yaml LinkML model
* Section Commands with key python: set this to the name of your Python executable (e.g., python3)

For now, most will be unable to post the dataset to the Dataset-JSON API as access to the API Key is limited because 
the POC API is running on a very small server. Read access to the API does not require an API Key. If interested 
in testing the POC Dataset-JSON CRUD functions, please post a question to this repo with your request. To use the 
dsj2api.py script, make sure the config.ini includes a DSJAPI section with values for:
* api_key: the API key is necessary to perform operations other than read
* base_url: base URL for the Dataset-JSON API

## Example Using the Programs Together from the Command-line
The following Linux command-line example retrieves a raw dataset, converts it to Dataset-JSON v1.1 NDJSON, validates the
dataset, and then posts it to the Dataset-JSON API:

```
python3 github2dsj/github2dsj.py ie.json --path ./data | dsjupversion/dsjupversion.py | 
dsjvalidate/dsjvalidate.py | dsj2api/dsj2api.py
```

This command-line uses 4 small Python command-line applications to:
1. Retrieves the IE dataset as Dataset-JSON v1.0 from GitHub
2. Pipes the filename and path into an application that updates it to Dataset-JSON NDJSON v1.1
3. Pipes the filename and path into a program that validates the dataset against the Dataset-JSON v1.1 model, 
4. Uploads the dataset to the Dataset-JSON API (API Key required)

If you clone the repo, you can run this yourself except for posting the dataset to the Dataset-JSON
API. Write access to the API is limited to keep hosting costs to a minimum.

In addition to running on Linux, this command-line approach should work on MacOS.

Next steps include generating ODM metadata and data to serve as a raw data source for the LZZT study in the 360i
program.

## Example Using the Programs Together from a Script 
If you're don't have access to a Linux command-line (or maybe MacOS), you can still chain the applications 
together to run on Windows, but that will require some additional configuring. That configuring has not been completed
or tested at this time, though you're welcome to make the needed tweaks.

The easiest way to try this on Windows today is to run the `360i.py` script that simulates chaining these programs
together on the command-line. You run 360i like you would any other Python program:
```
python3 360i.py
```
or, if you'd like to run it in verbose mode:
```
python 360i.py -v
```
## Running the Programs Individually
Instead of running the applications at one time, you can run them from the command-line independently. The next several
sections provide examples highlighting how to run each of the applications independently.

These programs assume you are running the program from the threesixtyeye folder and save the dataset in the 
threesixtyeye/data folder.

### github2dsj
This application retrieves a Dataset-JSON dataset from GitHub and stores it on your hard drive as a file. 
```
python3 github2dsj/github2dsj.py ie.json --path ./data
```

### dsjupversion
This application converts the dataset retrieved from GitHub to Dataset-JSON NDJSON v1.1.
```
python3 dsjupversion/dsjupversion.py -f /home/sam/src/threesixtyeye/data/ie.json
```

### dsjvalidate
This application validates the upversioned Dataset-JSON NDJSON v1.1 dataset using the LinkML model.
```
python3 dsjvalidate/dsjvalidate.py -f /home/sam/src/threesixtyeye/data/ie.ndjson
```

### dsj2api
This program posts the newly upversioned and valideated dataset to the Dataset-JSON API. This API is a proof-of-concept
application and requires an API key to post or modify data. The -f option provides the dataset file to upload, and the
-u option provides the base URL for the API.
```
python3 dsj2api/dsj2api.py -f /home/sam/src/threesixtyeye/data/ie.ndjson -u http://127.0.0.1:8000/ 
```
