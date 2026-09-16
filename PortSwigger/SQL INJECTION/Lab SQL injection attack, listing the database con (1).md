# Lab: SQL injection attack, listing the database contents on Oracle

![image.png](Lab%20SQL%20injection%20attack,%20listing%20the%20database%20con%203514-6a92/image.png)

ở đây khi chúng ta check về tên các bảng ta sẽ thấy có bảng là user giờ chúng ta sẽ khai thác vào bảng này

GET /filter?category=Accessories'+UNION+SELECT+table_name,NULL+FROM+all_tables-- HTTP/2

![image.png](Lab%20SQL%20injection%20attack,%20listing%20the%20database%20con%203514-6a92/image%201.png)

trong bảng này chúng ta có biết được 2 cột có trong bảng này giờ mình sẽ truy cập vào 2 bảng này để lấy thông tin người dùng

![image.png](Lab%20SQL%20injection%20attack,%20listing%20the%20database%20con%203514-6a92/image%202.png)

đã lấy được thông tin lab đã được giải
