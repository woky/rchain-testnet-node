import grpc
import logging
import sys
from rchain.client import RClient
from rchain.client import RClientException

root = logging.getLogger()
root.setLevel(logging.DEBUG)

ret=0
with grpc.insecure_channel('localhost:40401') as channel:
    client = RClient(channel)
    try:
        client.propose()
    except RClientException as e:
        # NoNewDeploys case should not exit with an error \
        # so autopropose script can deploy again before next propose
        if "NoNewDeploys" not in str(e):
            ret=1
sys.exit(ret)