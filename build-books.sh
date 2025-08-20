#!/bin/bash

# Build script for GitBook-style documentation using mdBook
# Usage: ./build-books.sh [serve]

echo "🔧 Building books..."

# Check if mdbook is installed
if ! command -v mdbook &> /dev/null; then
    echo "❌ mdBook is not installed. Please install it first:"
    echo "cargo install mdbook"
    exit 1
fi

# Create books-build directory if it doesn't exist
mkdir -p books-build

# Build each book
for book_dir in books/*/; do
    if [ -d "$book_dir" ]; then
        book_name=$(basename "$book_dir")
        echo "📖 Building book: $book_name"
        
        cd "$book_dir"
        mdbook build --dest-dir "../../books-build/$book_name"
        cd "../.."
        
        if [ $? -eq 0 ]; then
            echo "✅ Successfully built $book_name"
        else
            echo "❌ Failed to build $book_name"
        fi
    fi
done

echo "🎉 All books built successfully!"
echo "📚 Books are available in the books-build/ directory"

# If 'serve' argument is provided, start the development server
if [ "$1" = "serve" ]; then
    echo "🚀 Starting development server..."
    
    # Check if live-server is installed
    if command -v live-server &> /dev/null; then
        echo "📡 Using live-server on http://localhost:8080"
        live-server --port=8080 --open=/ --ignore=books,books-build --wait=500
    elif command -v python3 &> /dev/null; then
        echo "🐍 Using Python HTTP server on http://localhost:8000"
        echo "📝 Note: Live reload not available with Python server"
        python3 -m http.server 8000
    elif command -v python &> /dev/null; then
        echo "🐍 Using Python HTTP server on http://localhost:8000"
        echo "📝 Note: Live reload not available with Python server"
        python -m SimpleHTTPServer 8000
    else
        echo "❌ No suitable web server found. Please install live-server or Python"
        exit 1
    fi
fi
