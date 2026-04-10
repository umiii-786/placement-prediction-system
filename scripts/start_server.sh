
# Fetch secret securely
DAGSHUB_PAT=$(aws ssm get-parameter \
    --name "/placement-app/DAGSHUB_PAT" \
    --with-decryption \
    --query "Parameter.Value" \
    --output text)

docker stop placement-app || true
docker rm placement-app || true

docker run -d -p 80:8000 \
            --restart unless-stopped \
            -e DAGSHUB_PAT=$DAGSHUB_PAT \
            --name placement-app \
           umiii908/placement-prediction:v1

docker logs placement-app --tail 50