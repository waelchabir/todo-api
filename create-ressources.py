import os
import uuid
import json
import argparse
import base64

import boto3


AUTH_KEY_PARAM_NAME = '/todo-api/auth-key'
TABLES = {
    'app': {
        'prefix': 'todo-api',
        'env_var': 'APP_TABLE_NAME',
        'hash_key': 'username',
        'range_key': 'uid'
    }
}