# Lab: Web shell upload via obfuscated file extension

Ở bài này chúng tiếp tục được biết đến ky thuật làm mờ phần mở rộng vẫn giống như các lab trước giờ mình sẽ bắt đầu upload ảnh lên và tiến hành làm mờ extension

![image.png](Lab%20Web%20shell%20upload%20via%20obfuscated%20file%20extension/image.png)

ở đây mình thử thêm 1 .php đằng sau nhưng mà vẫn không vượt qua được bộ lọc của web server giờ thì ưu tiên thứ 2 là chúng sẽ dùng NULL byte %00

![image.png](Lab%20Web%20shell%20upload%20via%20obfuscated%20file%20extension/image%201.png)

Ok file đã được upload thành công rồi giờ check xem nó chạy được chưa

![image.png](Lab%20Web%20shell%20upload%20via%20obfuscated%20file%20extension/image%202.png)

file đã được thực thi giờ mình thay đổi payload và lấy flag

![image.png](Lab%20Web%20shell%20upload%20via%20obfuscated%20file%20extension/image%203.png)

gYIy375CjS38GE4MuoZ5wJeFu9ccWnTl
