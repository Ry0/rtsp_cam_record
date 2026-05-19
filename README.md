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
