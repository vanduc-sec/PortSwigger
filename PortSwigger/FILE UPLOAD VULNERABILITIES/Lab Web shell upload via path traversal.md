# Lab: Web shell upload via path traversal

![image.png](Lab%20Web%20shell%20upload%20via%20path%20traversal/image.png)

ở đây mọi người vẫn sẽ thực hiện các bược upload file ảnh lên như bình thường sau đó sẽ chuyển thành file php để thực, ở đây thì mình đã up file thành công rồi 

![image.png](Lab%20Web%20shell%20upload%20via%20path%20traversal/image%201.png)

nhưng mà đến khi mình gọi đến file đấy nhưng mà nó lại in ra nội dung file mình gửi lên thôi chứ nó không thực thi kết hợp với đề bài đã nói cho chúng ta biết có vẻ như là thư mục mà máy chủ dùng để lưu file chúng ta tải lên đã bị chặn không cho thực thi nữa rồi, vậy giờ mình sẽ phải thoát khỏi thư mục này, vậy thoát khỏi kiểu gì như chúng ta biết thì ‘..’ là đại diện cho thư mục cha giờ để chúng ta có thể thoát khỏi thư mục này thì chỉ cần đặt teen file là  ../filename thì khi server truy cập đến file này nó sẽ quay lại thư mục trước và lưu fiel vào thư mục đó

![image.png](Lab%20Web%20shell%20upload%20via%20path%20traversal/image%202.png)

ở đây khi mình tải lên thì file vẫn được lưu trong thư mục avatar và ../ của chúng ta đã biến mất có vẻ như đã bị cắt bỏ rồi giờ tiếp đến chúng ta sẽ thử mã hóa để vượt qua xem được khong

<?php phpinfo() ?>

![image.png](Lab%20Web%20shell%20upload%20via%20path%20traversal/image%203.png)

sau khi mã url encode file của mình đã được upload thành công rồi giờ mình sẽ thay đổi payload và truy cập vào file

![image.png](Lab%20Web%20shell%20upload%20via%20path%20traversal/image%204.png)

![image.png](Lab%20Web%20shell%20upload%20via%20path%20traversal/image%205.png)

vAelVp1BuKsc95CaYwRVR1q1bLNKiZyH
