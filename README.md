# Data2textDemo
 Data2textDemo for CKIP

## Run
```
source /share/home/timchen0618/data2text-zh/pure_mt5/data2text-zh/bin/activate

python data2text.py
or
gunicorn -w 1 -t 300 -b 0.0.0.0:5555 data2text:app
```

http://deep:5555/