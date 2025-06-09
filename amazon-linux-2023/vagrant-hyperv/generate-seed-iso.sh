#!/bin/bash

cd "$(dirname "$0")" || exit 1
genisoimage -output seed.iso -volid cidata -joliet -rock user-data meta-data