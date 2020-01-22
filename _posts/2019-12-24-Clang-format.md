

brew install clang-format

clang-format -style=google -dump-config > .clang-format

clang-format -i *.cpp
find . -regex '.*\.\(cpp\|hpp\|cu\|c\|h\)' -exec clang-format -style=file -i {} \;

https://www.codepool.biz/vscode-format-c-code-windows-linux.html
```
    "editor.formatOnSave": true,
    "clang-format.assumeFilename": ".clang-format",
    "clang-format.fallbackStyle": "none",
    "clang-format.language.c.fallbackStyle": "none",
```

