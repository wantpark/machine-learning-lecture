# 개발 환경 설정

## 도커 설치

- 다운로드 설치

```shell
https://www.docker.com
```

### 캐시 삭제 (option)

```shell
sudo docker builder prune --all
```

### 에러 발생  (option)

- ERROR [internal] load metadata for

```shell
rm ~/.docker/config.json
```

## 도커 이미지 만들기

- CPU=amd64
- CPU=arm64v8

```shell
sudo docker build -t machine-learning --build-arg CPU=amd64 .
```

## 도커 이미지 실행

```shell
sudo docker images --format="{{.Repository}} {{.ID}}" | grep "^machine-learning" | cut -d' ' -f2 | xargs sudo docker run -it -d -p 8000:8000 -p 2222:22 --name machine-learning
```

## 도커 이미지 실행 완료 후 도커 이미지 저장

```shell
sudo docker commit -m "complete" machine-learning
sudo docker images
sudo docker tag <IMAGE ID> machine-learning
```

## 실행 중인 도커 컨테이너 접속

```shell
sudo docker exec -it machine-learning /bin/bash
```

### 오픈소스 라이선스

[object_detector](https://raw.githubusercontent.com/AndreyGermanov/yolov8_onnx_go/main/LICENSE)
[image caption](https://www.apache.org/licenses/LICENSE-2.0)

## path

Open "/usr/local/lib/python3.12/dist-packages/imgaug/imgaug.py" file, change line 2120 to:
fig.canvas.manager.set_window_title("imgaug.imshow(%s)" % (image.shape,))

sed -i 's/fig\.canvas\.set_window_title("imgaug\.imshow(%s)" % (image\.shape,))/fig\.canvas\.manager\.set_window_title("imgaug\.imshow(%s)" % (image\.shape,))/g' /usr/local/lib/python3.12/dist-packages/imgaug/imgaug.py
