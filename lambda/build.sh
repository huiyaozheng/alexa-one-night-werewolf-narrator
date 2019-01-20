pip install ask-sdk-core -t ./skill_env
cp ./lambda_function.py ./skill_env/lambda_function.py
cd ./skill_env
zip -r * .