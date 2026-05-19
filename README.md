# Anker監視カメラ録画スクリプト
## 概要
`Eufy Indoor Cam 2K Pan & Tilt`では、SDカードに指定した時間帯の録画ができるが、保存されたデータは、専用のアプリでないと閲覧できないもので取り回しが悪い。
一方、RTSP機能を有効にすることで、外部のPCからカメラのデータをストリームすることができるので、この機能を使ってサーバのほうでストリームしてデータを保存するようにした。
Raspberry PIなどでの運用可。

## install 

```
pip install -r requirements.txt
```

```
sudo cp rtsp_cam_record.service /etc/systemd/system/rtsp_cam_record.service
sudo systemctl enable rtsp_cam_record.service
sudo systemctl start rtsp_cam_record.service
sudo systemctl status rtsp_cam_record.service
```
