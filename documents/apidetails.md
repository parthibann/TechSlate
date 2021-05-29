## API Details:

All the apis are open endpoints and requires no authentication.

#### LIST IMAGES
`GET: /v1/images`

Sample Response:

``` 
{
	"images": [
		"python",
		"nodejs",
		"go"
	],
	"image_details": {
		"python": {
			"version": "3",
			"image_tag": "techslate/python:v1",
			"image_id": "9e25367b8f1f"
		},
		"nodejs": {
			"version": "12",
			"image_tag": "techslate/nodejs12:v1",
			"image_id": "49cce91238ad"
		},
		"go": {
			"version": "1.16",
			"image_tag": "techslate/go:v1",
			"image_id": "6efff097a868"
		}
	}
}
```

#### START CONTAINER

`POST: /v1/docker/start`

Sample Request:

```
{
	"image_tag": "techslate/python:v1",
	"port": "2245",
	"label": "hello"
}
```

Sample Response:

```
{
	"message": "Request taken for processing. Please wait for 10 - 30 seconds for the contatiner to come to ready state."
}
```

#### LIST CONTAINERS

`GET: /v1/containers`

Sample Response:

```
[
	{
		"name": "laughing_wescoff",
		"id": "ebb0000477ee",
		"port": "27439: 3331/tcp",
		"web_terminal_port": "26654",
		"label": "techslate"
	}
]
```

#### STOP CONTAINERS

`GET: /v1/docker/stop/:containerID`

Sample Response:

```
{
	"message": "Request taken for processing."
}
```
