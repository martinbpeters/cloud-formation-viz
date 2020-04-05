TEST_CASE_FOLDER=tests/fixtures/templates
TEST_CASE_OUTPUT=tests/output

echo 'codebuild'
cfviz --unique-edges --no-pseudo --icons-path ./icons/ $TEST_CASE_FOLDER/codebuild.yaml - | dot -Tpng -o$TEST_CASE_OUTPUT/codebuild.png

echo 'codepipeline'
cfviz --unique-edges --no-pseudo --icons-path icons/ $TEST_CASE_FOLDER/codepipeline.yaml - | dot -Tpng -o$TEST_CASE_OUTPUT/codepipeline.png

echo 'iotanalytics'
cfviz --unique-edges --no-pseudo --icons-path icons/ $TEST_CASE_FOLDER/iotanalytics.yaml - | dot -Tpng -o$TEST_CASE_OUTPUT/iotanalytics.png

echo 'iotanalytics-monitoring'
cfviz --unique-edges --no-pseudo --icons-path icons/ $TEST_CASE_FOLDER/iotanalytics-monitoring.yaml - | dot -Tpng -o$TEST_CASE_OUTPUT/iotanalytics-monitoring.png

echo 'iotanalytics-topicrule'
cfviz --unique-edges --no-pseudo --icons-path icons/ $TEST_CASE_FOLDER/iotanalytics-topicrule.yaml - | dot -Tpng -o$TEST_CASE_OUTPUT/iotanalytics-topicrule.png

echo 'sls-sam-backend-app-template'
cfviz --unique-edges --no-pseudo --icons-path icons/ $TEST_CASE_FOLDER/sls-sam-backend-app-template.yaml - | dot -Tpng -o$TEST_CASE_OUTPUT/sls-sam-backend-app-template.png

echo 'sls-sam-backend-app-api'
cfviz --unique-edges --no-pseudo --icons-path icons/ $TEST_CASE_FOLDER/sls-sam-backend-app-api.yaml - | dot -Tpng -o$TEST_CASE_OUTPUT/sls-sam-backend-app-api.png

echo 'sls-sam-backend-app-database'
cfviz --unique-edges --no-pseudo --icons-path icons/ $TEST_CASE_FOLDER/sls-sam-backend-app-database.yaml - | dot -Tpng -o$TEST_CASE_OUTPUT/sls-sam-backend-app-database.png

echo 'sls-sam-analytics-app-template'
cfviz --unique-edges --no-pseudo --icons-path ./icons/ $TEST_CASE_FOLDER/sls-sam-analytics-app-template.yaml - | dot -Tpng -o$TEST_CASE_OUTPUT/sls-sam-analytics-app-template.png

echo 'sls-sam-ops-app-template'
cfviz --unique-edges --no-pseudo --icons-path icons/ $TEST_CASE_FOLDER/sls-sam-ops-app-template.yaml - | dot -Tpng -o$TEST_CASE_OUTPUT/sls-sam-ops-app-template.png

echo 'sls-sam-ops-app-dashboard'
cfviz --unique-edges --no-pseudo --icons-path icons/ $TEST_CASE_FOLDER/sls-sam-ops-app-dashboard.yaml - | dot -Tpng -o$TEST_CASE_OUTPUT/sls-sam-ops-app-dashboard.png

echo 'sls-sam-ops-app-alarm'
cfviz --unique-edges --no-pseudo --icons-path icons/ $TEST_CASE_FOLDER/sls-sam-ops-app-alarm.yaml - | dot -Tpng -o$TEST_CASE_OUTPUT/sls-sam-ops-app-alarm.png

echo 'sls-sam-ops-cicd'
cfviz --unique-edges --no-pseudo --icons-path icons/ $TEST_CASE_FOLDER/sls-sam-ops-cicd.yaml - | dot -Tpng -o$TEST_CASE_OUTPUT/sls-sam-ops-cicd.png

echo 'sls-sam-static-website-template'
cfviz --unique-edges --no-pseudo --icons-path icons/ $TEST_CASE_FOLDER/sls-sam-static-website-template.yaml - | dot -Tpng -o$TEST_CASE_OUTPUT/sls-sam-static-website-template.png

echo 'VPC'
cfviz --unique-edges --no-pseudo --icons-path icons/ $TEST_CASE_FOLDER/vpc.json - | dot -Tpng -o$TEST_CASE_OUTPUT/vpc.png

echo 'Aurora + VPC'
cfviz --unique-edges --no-pseudo --icons-path icons/ $TEST_CASE_FOLDER/aurora-serverless.json - | dot -Tpng -o$TEST_CASE_OUTPUT/aurora-serverless.png
