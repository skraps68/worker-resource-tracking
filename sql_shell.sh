#!/bin/bash
# Interactive SQL shell for the test database
# Usage: ./sql_shell.sh

source .env
#psql "$TEST_DATABASE_URL"
psql "$DATABASE_URL"