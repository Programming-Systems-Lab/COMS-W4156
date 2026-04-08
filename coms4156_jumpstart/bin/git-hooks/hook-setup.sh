#!/bin/sh
#
# Script to set pre-commit git-hook as a synlink to the actual hook script which
# is maintained within the repo proper.

GITHOOKS_DIR=$(git rev-parse --show-toplevel)/.git/hooks
# Rename REPOHOOKS_DIR if changing where the actual hook scripts live
REPOHOOKS_DIR=$(git rev-parse --show-toplevel)/bin/git-hooks

# If something exists, back it up
if [ -e "$GITHOOKS_DIR/pre-commit" ]
then
    mv $GITHOOKS_DIR/pre-commit $GITHOOKS_DIR/pre-commit.old
fi

ln -s -f $REPOHOOKS_DIR/pre-commit $GITHOOKS_DIR/pre-commit

