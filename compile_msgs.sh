#!/bin/bash
# Build python classes for parsing protobuf messages

echo "Starting the protoc compiler!"
protoc -I=msg --python_out=assisipy/msg msg/*.proto
