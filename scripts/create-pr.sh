#!/bin/bash

# Create Pull Request Script
# Usage: ./create-pr.sh "PR Title" "PR Description"

set -e

if [ -z "$1" ]; then
    echo "❌ Error: Please provide a PR title"
    echo "Usage: ./create-pr.sh \"PR Title\" \"PR Description\""
    exit 1
fi

TITLE=$1
DESCRIPTION=${2:-"Please review these changes"}
CURRENT_BRANCH=$(git branch --show-current)

echo "📝 Creating pull request for branch: $CURRENT_BRANCH"

# Check if we're on a feature branch
if [[ $CURRENT_BRANCH != feature/* ]]; then
    echo "⚠️  Warning: You're not on a feature branch"
    read -p "Continue anyway? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Push current branch
echo "📤 Pushing current branch..."
git push origin $CURRENT_BRANCH

# Create PR
echo "🔄 Creating pull request..."
gh pr create --base develop --head $CURRENT_BRANCH \
    --title "$TITLE" \
    --body "$DESCRIPTION"

echo "✅ Pull request created successfully!"
echo "🔗 View it on GitHub or use 'gh pr view' to see details"
