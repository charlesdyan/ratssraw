# ratssraw
Simple server for vh

# Instructions

Running the server:
```
$ docker build -t ratssraw .
$ docker run -p 8080:8080 --rm ratssraw
```

Running the tests:
```
$ pip install .
$ pytest
```