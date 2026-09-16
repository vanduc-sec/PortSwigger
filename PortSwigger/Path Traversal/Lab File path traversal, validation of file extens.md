# Lab: File path traversal, validation of file extension with null byte bypass

bài này thì nó sẽ kiểm tra xem chúng ta có cung cấp tên tệp với phần mở rộng đúng khong ở đay cso vẻ jpg là được cho phép

giờ để chúng ta có thể vượt qua lớp bảo về của web thì chắc chắn phải có dduois file là .jpg nhưng làm sao để có thể để hệ điều hành thực hiện được nếu có .jpg , ở hệ điều hành có ksy tự là \0 đối với hệ điều hành thì khi gặp được kí tự này ở bất cứ đâu nó sẽ coi như hết lệnh và sẽ không duyệt đằng sau nên chúng ta sẽ chenf kí tự NULL trước .jpg thì khi dso hệ điều hành sẽ khong đọc đên đuôi jpg nữa

![image.png](Lab%20File%20path%20traversal,%20validation%20of%20file%20extens/image.png)
