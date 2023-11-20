# docker-live-photos-converter
convert apple live photos downloaded by [icloudpd](https://github.com/boredazfcuk/docker-icloudpd) into google motion photos.

## Usage

Convert all live photos in `./photos`:
```shell
docker run --name live-photos-converter --restart always -d -v "$(pwd)/photos:/photos" lckof/live-photos-converter
```

The cronjob is running every 1 day by default, you can change it by setting `CRON` environment variable.

Change the cronjob to run every 3 hours:
```shell
docker run --name live-photos-converter --restart always -d -v "$(pwd)/photos:/photos" -e CRON="0 */3 * * *" lckof/live-photos-converter
```

And you can specify the exports directory by mount `/exports` volume for uploading to google photos:
```shell
docker run --name live-photos-converter --restart always -d -v "$(pwd)/photos:/photos" -v "$(pwd)/exports:/exports" lckof/live-photos-converter
```

## Develope

### Use buildx
```shell
docker buildx create --name mybuilder
docker buildx use mybuilder
docker buildx inspect --bootstrap
```

### Debug for single platform
```shell
docker buildx build --platform linux/amd64 -t live-photos-converter --load .
docker run --rm --name live-photos-converter -it -v "$(pwd)/photos:/photos" -v "$(pwd)/exports:/exports" --entrypoint bash live-photos-converter
python main.py
```

or use cusomized cronjob
```shell
docker run --rm --name live-photos-converter -it -v "$(pwd)/photos:/photos" -v "$(pwd)/exports:/exports" -e CRON="* * * * *" live-photos-converter
```

### Publish

```shell
docker buildx build --platform linux/amd64 -t lckof/live-photos-converter:latest --push .
```
