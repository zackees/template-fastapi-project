
# If $DATA_ROOT is unset
if [ -z "$DATA_ROOT" ]; then
    DATA_ROOT="/app/var/data"
fi
export DATA_ROOT
set -e
mkdir -p $DATA_ROOT
# First launch the uvicorn server
pm2 start ./unicorn.sh
echo DATA_ROOT is $DATA_ROOT
