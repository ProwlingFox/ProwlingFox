pkill "queueProcessor.py"
pkill "node index.js"
pkill "uvicorn"

git pull

echo "Starting Queue Processor";
bash -c "cd api;./env/bin/python queueProcessor.py >> ../queue_processor.log 2>&1" &
echo "Starting API";
bash -c "cd api;./env/bin/uvicorn api:app --host 127.0.0.1 --port 8000 >> ../api.log 2>&1" &


echo "Building Svelte App"
bash -c "cd app;npm run build"
echo "Running Frontend App"
bash -c "cd app/build;node index.js >> ../../app.log 2>&1" &



# WINDOWS CREATE SYMLINK
# New-Item -ItemType HardLink -Path "app\.env" -Target ".env"
# New-Item -ItemType HardLink -Path "api\.env" -Target ".env"
# ln -s .env api/.env
# ln -s .env app/.env