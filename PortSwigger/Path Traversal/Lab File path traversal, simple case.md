# Lab: File path traversal, simple case

Bài này chúng ta sẽ phải đọc nội dung trông etc/passwd

![image.png](Lab%20File%20path%20traversal%2C%20simple%20case/image.png)

ở đây khi truy cập vào 1 mặt hàng chúng ta thấy sẽ có 1 biến product nhận input đầu vào để thực thi có thể đây chính là 1 lỗ hổng 

![image.png](Lab%20File%20path%20traversal%2C%20simple%20case/image%201.png)

tuy nhiên ở đây khi mình thử payload và thì bị sai có vẻ như nó chỉ nhận input được định săn rồi giờ mình sẽ tìm đến 1 đường dẫn khác

![image.png](Lab%20File%20path%20traversal%2C%20simple%20case/image%202.png)

ở đây chúng ta có thể thấy ngoài biến productid ra thì còn 1 biến file name nữa giờ mình sẽ thử chèn vào đường dẫn này

![image.png](Lab%20File%20path%20traversal%2C%20simple%20case/image%203.png)

lệnh của mình đã được thực thi
