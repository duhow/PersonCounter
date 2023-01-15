# Run

```sh
docker run --rm -d -p 6379:6379 -v $PWD/redis:/data --name redis eqalpha/keydb
python3 -m flask run --host 0.0.0.0
```
