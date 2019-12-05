<h1>Managing Artifacts from Jobs</h1>

When running a job, sometimes you may want to save files to analyze indepth later, or to track data. Foundations can help store and track any artifacts generated by your job for later retrival and supports files of any type (.parquet, .hdf5, .pkl, .csv, etc). Users can specify a directory which Foundations will track during job execution, then save files to that path, providing maximum flexibility and organization of generated files.

## Create Artifact Storage Structure

Foundations gives users the ability to define the folder structure on how they want to store files. Since the project whole folder is bundled when a Foundations job is deployed, users can create their own folder structures in their project directory for Foundations to track.

For example, lets say you want to store different types of files (models and data) in your job. You can define an `artifacts` folder with two subdirectories: `models` and `data` in your project:

```
project_name
├── config
│   └── local.config.yaml
├── data
├── post_processing
│   └── results.py
├── project_code
│   ├── artifacts
│   │   └── models
│   │   └── data
│   ├── driver.py
│   └── model.py
└── README.txt
```

Then, in your code, you can write artifacts to those paths for easy organization of files:

```python
df.to_pickle("artifacts/data/variables.pkl")
model.save('artifacts/models/my_model.h5')
```

## Define Artifact Path in Environment Configuration

To specify to Foundations where your generated files are saved to, you can define a relative directory in your environment configuration file for Foundations to track. From the example above, since we are writing all our files to the `artifact` folder, we specify the relative path here:

```yaml
job_deployment_env: local

results_config: 
    artifact_path: artifacts

cache_config: {}
log_level: DEBUG
```

Foundations will then save all files from the `artifact_path` for post-job retrieval. This parameter supports any relative path, so if you wanted to only save files in the `data` folder, you could put: `artifacts/data` as the `artifact_path`. For more information on setting up configurations, please refer to the documentation [here](../configs/#results-configurations)

## Retrieving Artifacts from Completed Jobs

Users can download the files from a completed job with the Foundations CLI command. If the job failed during execution, users will still be able to retrieve any saved artifacts from the job up until the failure. Additional information on the CLI command can be found [here](../project_creation/#retrieve-stored-artifacts)

```shellscript
$ foundations retrieve artifacts --job_id=<deployed job_id> --env=<env_name> [options]
```
<h3>Options</h3>
|   Option &nbsp;&nbsp;&nbsp;&nbsp;   | Description  |
|----|----|
| save_dir| The directory on the machine where to download all artifacts to. Can be both relative or absolute paths. By default, Foundations will download artifacts to the present working directory|
| source_dir| The subdirectory of artifacts from the user-defined `artifact_path` to download. By default foundations will download all stored artifacts from the root directory for a job|