## 1. Print non-empty and non-comment lines of a file
```
grep -vE '^\s*#|^\s*$' .env
```

## 2. Check disk size
```
df -h -T
```
