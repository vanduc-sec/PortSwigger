# Blind OS command injection with time delays

Bài này đầu vào sẽ được xử lý bằng 1 lệnh shell và chúng ta phải sử dụng sleep để cho server ngủ trong 10 giây, vẫn như mọi bài giờ mình sẽ mở bằng burp suite

![image.png](Blind%20OS%20command%20injection%20with%20time%20delays/image.png)

Ở đây mình sẽ nôp 1 feedback trước rồi mở nó bằng burp để bắt đầu chỉnh sửa

![image.png](Blind%20OS%20command%20injection%20with%20time%20delays/image%201.png)

ở đây khi mình thử tạo các biến thành payload thì nó có vẻ không đươc thực thi giờ tiếp mình thử tạo bằng số lệnh bình thường có vẻ nó  đã bị cầm hết rồi nên giờ mình sẽ thử lệnh mạnh hơn bằng backtick

![image.png](Blind%20OS%20command%20injection%20with%20time%20delays/image%202.png)

và lệnh đã được thực thi 

![image.png](Blind%20OS%20command%20injection%20with%20time%20delays/image%203.png)
