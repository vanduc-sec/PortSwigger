# OS command injection, simple case

Bài này theo mô tả thì có lỗ hổng trong việc kiểm tra kho sản phẩm sẽ có một lệnh shell thực thi với đầu vào là id và tên cửa hàng do người dùng cung cấp, đến đây chúng ta biết là mình sẽ có thể điều khiển được tên cửa hàng này 

![image.png](OS%20command%20injection%2C%20simple%20case/image.png)

ở đây mình sẽ check đại 1 cái là london sau đó sẽ vào burpsuite

![image.png](OS%20command%20injection%2C%20simple%20case/image%201.png)

Mình thêm 1 lệnh whoami ngay sau store là đã được rồi bài này khá đơn giản

ở đây hiểu là khi mình thêm dấu ; thì khi mà server thực hiện xong 2 lệnh id kia thì sẽ sang tiếp lệnh whoami của mình vì dau ; là thực hiện lần lượt các lệnh
