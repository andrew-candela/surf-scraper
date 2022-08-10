
# Package Installation

Only install the packages you need for the environment you're using!
The lambda deployment package size can't be more than something like 50MB or so.
Only install the packages you need by keeping your requirement files tidy!

## lambda_runtime.txt

The lambda runtime comes with boto3 and botocore installed.
Those are big packages, so we save a lot of space by not including them.

## production.txt

Installs the lambda runtime requirements plus boto3.
This will give your env everything it needs to run locally.

## dev.txt

Installs production requirements plus anything we need for active development.
This installs linters, mypy, stubs etc.
