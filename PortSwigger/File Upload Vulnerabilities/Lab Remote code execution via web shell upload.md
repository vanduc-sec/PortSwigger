# Lab: Remote code execution via web shell upload

![image.png](Lab%20Remote%20code%20execution%20via%20web%20shell%20upload/image.png)

chúng ta được cung cấp 1 trang web có user name và pass của tài khoản mình sẽ tiến hành đăng nhập trước

vào trang thì có phần yêu cầu upload 1 file ảnh lên mình sẽ tải một file ảnh lên 

![image.png](Lab%20Remote%20code%20execution%20via%20web%20shell%20upload/image%201.png)

giờ mình sẽ vào burp suite để thử thay đổi file ảnh thành file mã độc và gửi lên server đối với bước này thì đầu tiên mình sẽ thử câu  lệnh đơn giản với php trước

```python
<?php phpinfo(); ?>
```

![image.png](Lab%20Remote%20code%20execution%20via%20web%20shell%20upload/image%202.png)

![image.png](Lab%20Remote%20code%20execution%20via%20web%20shell%20upload/image%203.png)

sau khi tải lên thì file đã được upload được luôn có vẻ server không kiểm tra gì đối với các file mà sẽ lưu lại hết giờ mình sẽ thử thực thi mã lệnh

![image.png](Lab%20Remote%20code%20execution%20via%20web%20shell%20upload/image%204.png)

Mình đã gửi payload thành công giờ mình sẽ gửi yêu cầu để thực hiện lấy file mã độc mình gửi lên để server thực thi payload của mình

![image.png](Lab%20Remote%20code%20execution%20via%20web%20shell%20upload/image%205.png)

payload của mình đã được thực thi giờ mình chỉ cần đọc file secret

![image.png](Lab%20Remote%20code%20execution%20via%20web%20shell%20upload/image%206.png)

onzjWabQkNwnW3C25J6ofw61LK89kg6K
