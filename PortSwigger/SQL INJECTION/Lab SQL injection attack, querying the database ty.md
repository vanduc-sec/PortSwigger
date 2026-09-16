# Lab: SQL injection attack, querying the database type and version on Oracle

ở đây đầu tiên mình sẽ check xem câu lệnh sql này đang có bao nhiêu cột để mình sẽ dùng UNION cho lệnh tiếp thoe 

![image.png](Lab%20SQL%20injection%20attack,%20querying%20the%20database%20ty/image.png)

ở đây ta sẽ thấy số cột alf 2 vì đến 3 thì đã bị lỗi

![image.png](Lab%20SQL%20injection%20attack,%20querying%20the%20database%20ty/image%201.png)

ở đây sau khi check thì mình thấy cả 2 cột đều strings được giwof mình sẽ khai thác tiếp

sử udngf SELECT banner FROM v$version để check phiên bản của cơ sở dữ liệu

![image.png](Lab%20SQL%20injection%20attack,%20querying%20the%20database%20ty/image%202.png)
