# quick and dirty lambda deployer

set -euxo pipefail

FUNCTION_NAME=SurfDiary

rm -rf deployment_package
pip install -t deployment_package -r requirements/lambda_runtime.txt
cp -r surf_data deployment_package

(cd deployment_package && zip -r9 ../deployment.zip .)



aws lambda update-function-code \
        --function-name ${FUNCTION_NAME} \
        --zip-file fileb://`pwd`/deployment.zip\
        --no-cli-pager \
        --region us-west-1

# clean up
rm deployment.zip
rm -rf deployment_package