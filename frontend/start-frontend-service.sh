#!/bin/bash
set -e

exec npm run dev -- --host 0.0.0.0 --port 3000
