#!/bin/bash
# Complete Download Script for Employee Attendance System

echo "================================================"
echo "  Employee Attendance System - Download All"
echo "================================================"
echo ""

TARGET_DIR="${1:-./employee-attendance-system}"

echo "Creating directory structure in: $TARGET_DIR"
mkdir -p "$TARGET_DIR"
mkdir -p "$TARGET_DIR/backend"
mkdir -p "$TARGET_DIR/frontend/src/pages"
mkdir -p "$TARGET_DIR/frontend/src/components/ui"
mkdir -p "$TARGET_DIR/frontend/src/hooks"
mkdir -p "$TARGET_DIR/frontend/src/lib"
mkdir -p "$TARGET_DIR/frontend/public"

echo ""
echo "Files to copy:"
echo "=============="

# List all files
find /app -type f \
  \( -name "*.md" -o -name "*.py" -o -name "*.js" -o -name "*.jsx" \
  -o -name "*.txt" -o -name "*.json" -o -name "*.css" \
  -o -name "*.sh" -o -name "*.bat" -o -name "*.html" \
  -o -name ".gitignore" \) \
  ! -path "*/node_modules/*" \
  ! -path "*/venv/*" \
  ! -path "*/.git/*" \
  ! -path "*/build/*" \
  ! -path "*/test_reports/*" \
  ! -path "*/memory/*" \
  ! -path "*/tests/*" \
  -exec echo "  ✓ {}" \;

echo ""
echo "Total files found:"
find /app -type f \
  \( -name "*.md" -o -name "*.py" -o -name "*.js" -o -name "*.jsx" \
  -o -name "*.txt" -o -name "*.json" -o -name "*.css" \
  -o -name "*.sh" -o -name "*.bat" -o -name "*.html" \
  -o -name ".gitignore" \) \
  ! -path "*/node_modules/*" \
  ! -path "*/venv/*" \
  ! -path "*/.git/*" \
  ! -path "*/build/*" \
  ! -path "*/test_reports/*" \
  ! -path "*/memory/*" \
  ! -path "*/tests/*" | wc -l

echo ""
echo "To copy files, run:"
echo "  cp -r /app/backend/* $TARGET_DIR/backend/"
echo "  cp -r /app/frontend/src/* $TARGET_DIR/frontend/src/"
echo "  cp -r /app/frontend/public/* $TARGET_DIR/frontend/public/"
echo "  cp /app/frontend/*.json $TARGET_DIR/frontend/"
echo "  cp /app/frontend/*.js $TARGET_DIR/frontend/"
echo "  cp /app/*.md $TARGET_DIR/"
echo "  cp /app/*.sh $TARGET_DIR/"
echo "  cp /app/*.bat $TARGET_DIR/"
echo "  cp /app/.gitignore $TARGET_DIR/"
echo ""
echo "Done!"
