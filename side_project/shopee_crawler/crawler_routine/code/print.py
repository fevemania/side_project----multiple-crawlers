#!/bin/bash

import os

print(os.environ.get('POSTGRES_DB'))
print(os.environ.get('POSTGRES_USER'))
