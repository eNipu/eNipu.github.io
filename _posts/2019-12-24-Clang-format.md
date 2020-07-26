
### Installation in Mac
```brew install clang-format```

### Dumping with pre-define coding style (Here Google's coding guideline)

```clang-format -style=google -dump-config > .clang-format```

### Running on all file with .cpp extension
```clang-format -i *.cpp```

### Running on specific format
find . -regex '.*\.\(cpp\|hpp\|cu\|c\|h\)' -exec clang-format -style=file -i {} \;

### Configuring VS Code
https://www.codepool.biz/vscode-format-c-code-windows-linux.html
```
    "editor.formatOnSave": true,
    "clang-format.assumeFilename": ".clang-format",
    "clang-format.fallbackStyle": "none",
    "clang-format.language.c.fallbackStyle": "none",
```

