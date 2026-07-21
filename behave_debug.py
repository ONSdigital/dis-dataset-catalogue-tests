import sys
from behave.__main__ import run_behave
from behave.configuration import Configuration

if __name__ == "__main__":
    args = [
        # Feature file path:
        "features/dataset_api.feature",
        # Two lines below used to specify a single scenario within the feature file
        # Comment out to debug all scenarios in the given feature file
        "-n",
        "Get editions for a dataset",
    ]
    configuration = Configuration(args)
    sys.exit(run_behave(configuration))
