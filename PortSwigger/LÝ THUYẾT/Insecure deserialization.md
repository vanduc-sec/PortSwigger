# Insecure deserialization

Trạng thái: Chưa bắt đầu
subject: Advanced

# Serialization là gì?

---

Tuần tự hóa (serialization) là quá trình chuyển đổi các cấu trúc dữ liệu phức tạp, chẳng hạn như đối tượng và các trường của chúng, sang một định dạng “phẳng” hơn có thể được gửi và nhận như một luồng byte tuần tự. Việc tuần tự hóa dữ liệu giúp đơn giản hóa đáng kể các thao tác:

- Ghi dữ liệu phức tạp vào bộ nhớ liên tiến trình, một tệp hoặc cơ sở dữ liệu
- Gửi dữ liệu phức tạp, ví dụ, qua mạng, giữa các thành phần khác nhau của một ứng dụng, hoặc trong một lời gọi API

Điều quan trọng là khi tuần tự hóa một đối tượng, trạng thái của nó cũng được lưu bền. Nói cách khác, các thuộc tính của đối tượng được bảo toàn cùng với các giá trị đã được gán cho chúng.

---

# **Serialization vs Deserialization**

---

Giải tuần tự hóa (deserialization) là quá trình khôi phục luồng byte này thành một bản sao hoạt động đầy đủ của đối tượng gốc, ở đúng trạng thái như khi nó được tuần tự hóa. Khi đó, logic của website có thể tương tác với đối tượng đã được giải tuần tự này giống như với bất kỳ đối tượng nào khác.

![image.png](Insecure%20deserialization/image.png)

Nhiều ngôn ngữ lập trình cung cấp hỗ trợ gốc cho tuần tự hóa. Cách đối tượng được tuần tự hóa phụ thuộc vào từng ngôn ngữ. Một số ngôn ngữ tuần tự hóa đối tượng sang định dạng nhị phân, trong khi các ngôn ngữ khác dùng các định dạng chuỗi khác nhau với mức độ dễ đọc khác nhau đối với con người. Lưu ý rằng tất cả thuộc tính của đối tượng gốc đều được lưu trong luồng dữ liệu đã tuần tự, bao gồm cả các trường riêng tư (private). Để ngăn một trường bị tuần tự hóa, trường đó phải được đánh dấu rõ ràng là “transient” trong phần khai báo lớp.

Hãy lưu ý rằng khi làm việc với các ngôn ngữ khác nhau, tuần tự hóa có thể được gọi là **marshalling** (Ruby) hoặc **pickling** (Python). Trong ngữ cảnh này, các thuật ngữ này đồng nghĩa với “serialization”.

---

# **Insecure Deserialization là gì?**

---

Giải tuần tự hóa không an toàn (insecure deserialization) là khi dữ liệu do người dùng kiểm soát được website giải tuần tự. Điều này có thể cho phép kẻ tấn công thao túng các đối tượng đã tuần tự hóa để đưa dữ liệu gây hại vào mã ứng dụng.

Thậm chí có thể thay thế một đối tượng đã tuần tự hóa bằng một đối tượng thuộc một lớp hoàn toàn khác. Đáng lo ngại là các đối tượng của bất kỳ lớp nào mà website có thể truy cập đều sẽ được giải tuần tự và khởi tạo, bất kể lớp được mong đợi là gì. Vì lý do này, giải tuần tự hóa không an toàn đôi khi còn được gọi là lỗ hổng “tiêm đối tượng” (object injection).

Một đối tượng thuộc lớp không mong đợi có thể gây ra ngoại lệ. Tuy nhiên, đến lúc đó thiệt hại có thể đã xảy ra. Nhiều cuộc tấn công dựa trên giải tuần tự hóa được hoàn tất trước khi quá trình giải tuần tự kết thúc. Điều này có nghĩa là bản thân quá trình giải tuần tự có thể khởi phát cuộc tấn công, ngay cả khi chức năng của website không trực tiếp tương tác với đối tượng độc hại. Vì lý do này, các website có logic dựa trên ngôn ngữ kiểu tĩnh (strongly typed) cũng có thể dễ bị tổn thương trước các kỹ thuật này.

---

# Phát sinh

---

Giải tuần tự hóa không an toàn thường phát sinh do thiếu hiểu biết chung về mức độ nguy hiểm khi giải tuần tự dữ liệu do người dùng kiểm soát. Lý tưởng nhất là không bao giờ nên giải tuần tự dữ liệu đầu vào từ người dùng.

Tuy nhiên, đôi khi chủ sở hữu website nghĩ rằng họ an toàn vì đã triển khai một số dạng kiểm tra bổ sung trên dữ liệu đã được giải tuần tự. Cách tiếp cận này thường không hiệu quả vì gần như không thể xây dựng cơ chế kiểm tra hoặc làm sạch (validation/sanitization) bao quát mọi tình huống. Các kiểm tra này cũng có lỗi căn bản vì chúng dựa vào việc kiểm tra dữ liệu sau khi đã được giải tuần tự, mà trong nhiều trường hợp là quá muộn để ngăn chặn tấn công.

Lỗ hổng cũng có thể phát sinh vì các đối tượng đã giải tuần tự thường được giả định là đáng tin cậy. Đặc biệt khi dùng các ngôn ngữ có định dạng tuần tự nhị phân, lập trình viên có thể nghĩ rằng người dùng không thể đọc hoặc thao túng dữ liệu một cách hiệu quả. Tuy nhiên, dù có tốn công hơn, kẻ tấn công vẫn có thể khai thác các đối tượng tuần tự nhị phân giống như đối với các định dạng chuỗi.

Các cuộc tấn công dựa trên giải tuần tự cũng trở nên khả thi do số lượng phụ thuộc (dependency) trong các website hiện đại. Một trang điển hình có thể sử dụng nhiều thư viện khác nhau, và mỗi thư viện lại có các phụ thuộc riêng. Điều này tạo ra một “bể” lớp và phương thức khổng lồ, rất khó quản lý an toàn. Vì kẻ tấn công có thể tạo thể hiện của bất kỳ lớp nào trong số này, thật khó để dự đoán những phương thức nào có thể được gọi trên dữ liệu độc hại. Điều này đặc biệt đúng nếu kẻ tấn công có thể xâu chuỗi một loạt lời gọi phương thức ngoài dự kiến, đưa dữ liệu vào một sink hoàn toàn không liên quan đến nguồn ban đầu. Do đó, gần như không thể tiên liệu luồng dữ liệu độc hại và bịt kín mọi lỗ hổng tiềm ẩn.

Tóm lại, có thể cho rằng không thể giải tuần tự một cách an toàn đối với dữ liệu không đáng tin cậy.

---

# Hậu quả

---

Tác động của giải tuần tự hóa không an toàn có thể rất nghiêm trọng vì nó mở ra một điểm vào làm tăng mạnh bề mặt tấn công. Nó cho phép kẻ tấn công tái sử dụng mã ứng dụng hiện có theo cách gây hại, dẫn đến nhiều lỗ hổng khác, thường là thực thi mã từ xa (RCE).

Ngay cả trong các trường hợp không thể thực thi mã từ xa, giải tuần tự hóa không an toàn vẫn có thể dẫn đến leo thang đặc quyền, truy cập tệp tùy ý và tấn công từ chối dịch vụ (DoS).

---

# Kiểm thử

---

Việc nhận diện giải tuần tự hóa không an toàn tương đối đơn giản, bất kể bạn đang kiểm thử whitebox hay blackbox.

Trong quá trình audit, bạn nên xem xét mọi dữ liệu được truyền vào website và cố gắng xác định bất cứ thứ gì trông giống dữ liệu đã tuần tự hóa. Dữ liệu đã tuần tự hóa có thể được nhận diện tương đối dễ dàng nếu bạn biết định dạng mà các ngôn ngữ khác nhau sử dụng. Trong phần này, chúng tôi sẽ đưa ra ví dụ từ cả tuần tự hóa PHP và Java. Sau khi xác định được dữ liệu đã tuần tự hóa, bạn có thể kiểm tra liệu mình có khả năng kiểm soát nó hay không.

> **Mẹo**
Đối với người dùng Burp Suite Professional, Burp Scanner sẽ tự động gắn cờ mọi thông điệp HTTP có vẻ chứa các đối tượng đã tuần tự hóa.
> 

---

## PHP

---

PHP dùng định dạng chuỗi phần lớn có thể đọc được bằng mắt, trong đó chữ cái biểu thị kiểu dữ liệu và chữ số biểu thị độ dài của từng mục. Ví dụ, xét một đối tượng User với các thuộc tính:

```
$user->name = "carlos";
$user->isLoggedIn = true;
```

Khi được tuần tự hóa, đối tượng này có thể trông như sau:

```
O:4:"User":2:{s:4:"name":s:6:"carlos";s:10:"isLoggedIn":b:1;}
```

Có thể diễn giải như sau:

- `O:4:"User"` – Một đối tượng có tên lớp dài 4 ký tự là "User"
- `2` – đối tượng có 2 thuộc tính
- `s:4:"name"` – khóa của thuộc tính thứ nhất là chuỗi dài 4 ký tự "name"
- `s:6:"carlos"` – giá trị của thuộc tính thứ nhất là chuỗi dài 6 ký tự "carlos"
- `s:10:"isLoggedIn"` – khóa của thuộc tính thứ hai là chuỗi dài 10 ký tự "isLoggedIn"
- `b:1` – giá trị của thuộc tính thứ hai là kiểu boolean true

Các phương thức gốc để tuần tự hóa trong PHP là `serialize()` và `unserialize()`. Nếu có quyền truy cập mã nguồn, bạn nên bắt đầu bằng cách tìm bất kỳ nơi nào gọi `unserialize()` trong code và điều tra thêm.

---

## Java

---

Một số ngôn ngữ, như Java, sử dụng định dạng tuần tự nhị phân. Điều này khó đọc hơn, nhưng bạn vẫn có thể nhận diện dữ liệu đã tuần tự nếu biết một vài dấu hiệu đặc trưng. Ví dụ, các đối tượng Java đã tuần tự luôn bắt đầu bằng cùng một dãy byte, được mã hóa là `ac ed` ở dạng thập lục phân và `rO0` ở dạng Base64.

Bất kỳ lớp nào triển khai interface `java.io.Serializable` đều có thể được tuần tự hóa và giải tuần tự. Nếu có quyền truy cập mã nguồn, hãy lưu ý mọi đoạn code sử dụng phương thức `readObject()`, phương thức này được dùng để đọc và giải tuần tự dữ liệu từ một `InputStream`.

---

# Xâm nhập

---

## Thao túng S**erialized objects**

---

Khai thác một số lỗ hổng giải tuần tự hóa có thể đơn giản như việc thay đổi một thuộc tính trong đối tượng đã tuần tự. Vì trạng thái của đối tượng được lưu bền, bạn có thể xem xét dữ liệu đã tuần tự để nhận diện và chỉnh sửa các giá trị thuộc tính thú vị. Sau đó, bạn có thể đưa đối tượng độc hại này vào website thông qua quy trình giải tuần tự của nó. Đây là bước khởi đầu cho một khai thác giải tuần tự cơ bản.

Nói chung, có hai cách tiếp cận khi thao túng các đối tượng đã tuần tự hóa. Bạn có thể chỉnh sửa trực tiếp đối tượng ở dạng luồng byte của nó, hoặc bạn có thể viết một đoạn script ngắn bằng ngôn ngữ tương ứng để tự tạo và tuần tự hóa đối tượng mới. Cách tiếp cận thứ hai thường dễ hơn khi làm việc với các định dạng tuần tự nhị phân.

---

### Chỉnh sửa Object

---

Khi can thiệp vào dữ liệu, miễn là kẻ tấn công vẫn giữ cho đối tượng đã tuần tự hợp lệ, quá trình giải tuần tự sẽ tạo ra một đối tượng phía server với các giá trị thuộc tính đã bị sửa đổi.

Ví dụ đơn giản, xét một website dùng một đối tượng `User` đã tuần tự để lưu dữ liệu phiên của người dùng trong cookie. Nếu kẻ tấn công phát hiện đối tượng đã tuần tự này trong một yêu cầu HTTP, họ có thể giải mã để thấy luồng byte sau:

```
O:4:"User":2:{s:8:"username";s:6:"carlos";s:7:"isAdmin";b:0;}
```

Thuộc tính `isAdmin` là một điểm quan tâm hiển nhiên. Kẻ tấn công có thể đơn giản đổi giá trị boolean của thuộc tính này thành `1` (true), mã hóa lại đối tượng, rồi ghi đè cookie hiện tại của họ bằng giá trị đã chỉnh sửa. Xét riêng lẻ thì điều này không có tác dụng gì. Tuy nhiên, giả sử website dùng cookie này để kiểm tra liệu người dùng hiện tại có quyền truy cập một số chức năng quản trị hay không:

```php
$user = unserialize($_COOKIE);
if ($user->isAdmin === true) {
    // allow access to admin interface
}
```

Đoạn mã dễ bị tấn công này sẽ khởi tạo một đối tượng `User` dựa trên dữ liệu từ cookie, bao gồm cả thuộc tính `isAdmin` đã bị kẻ tấn công sửa đổi. Không có bước nào kiểm tra tính xác thực của đối tượng đã tuần tự. Dữ liệu này sau đó được đưa vào câu lệnh điều kiện và, trong trường hợp này, sẽ cho phép leo thang đặc quyền một cách dễ dàng.

Kịch bản đơn giản này không phổ biến ngoài thực tế. Tuy nhiên, việc sửa một giá trị thuộc tính theo cách này minh họa bước đầu tiên hướng tới việc tiếp cận lượng bề mặt tấn công khổng lồ mà giải tuần tự hóa không an toàn phơi bày.

[Lab: Modifying serialized objects | Web Security Academy](https://portswigger.net/web-security/deserialization/exploiting/lab-deserialization-modifying-serialized-objects)

---

### Chỉnh sửa Data

---

Chúng ta đã thấy cách bạn có thể sửa giá trị thuộc tính trong các đối tượng đã tuần tự hóa, nhưng cũng có thể cung cấp các **kiểu dữ liệu** ngoài dự kiến.

Logic dựa trên PHP đặc biệt dễ bị thao túng dạng này do hành vi của **toán tử so sánh lỏng** (`==`) khi so sánh các kiểu dữ liệu khác nhau. Ví dụ, nếu bạn so sánh lỏng giữa một số nguyên và một chuỗi, PHP sẽ cố gắng chuyển chuỗi sang số nguyên, nghĩa là `5 == "5"` cho kết quả `true`.

Bất thường là điều này cũng đúng với **mọi chuỗi chữ-số** bắt đầu bằng một chữ số. Trong trường hợp này, PHP thực chất sẽ chuyển cả chuỗi thành giá trị số nguyên dựa trên con số ở đầu; phần còn lại của chuỗi bị bỏ qua hoàn toàn. Do đó, `5 == "5 of something"` trên thực tế được coi như `5 == 5`.

Tương tự, trên PHP 7.x và cũ hơn, phép so sánh `0 == "Example string"` cho kết quả `true` vì PHP coi toàn bộ chuỗi là số nguyên 0.

Hãy xét một tình huống trong đó toán tử so sánh lỏng này được dùng cùng với dữ liệu do người dùng kiểm soát đến từ một đối tượng đã giải tuần tự. Điều này có thể dẫn tới các lỗi logic nguy hiểm.

```php
$login = unserialize($_COOKIE)
if ($login['password'] == $password) {
  // log in successfully
}
```

Giả sử kẻ tấn công sửa thuộc tính `password` để nó chứa **số nguyên 0** thay vì chuỗi như mong đợi. Miễn là mật khẩu lưu trữ **không bắt đầu bằng chữ số**, điều kiện sẽ luôn trả về `true`, cho phép **vượt qua xác thực**. Lưu ý rằng điều này chỉ khả thi vì quá trình giải tuần tự **giữ nguyên kiểu dữ liệu**. Nếu mã lấy mật khẩu trực tiếp từ request, giá trị `0` sẽ được chuyển thành chuỗi và điều kiện sẽ cho kết quả `false`.

> **Lưu ý**
> 
> 
> Trên PHP 8 trở lên, phép so sánh `0 == "Example string"` cho kết quả `false` vì chuỗi **không còn** bị ngầm chuyển thành `0` trong so sánh. Do đó, khai thác này **không khả thi** trên các phiên bản PHP này.
> 
> Hành vi khi so sánh một chuỗi chữ-số bắt đầu bằng chữ số vẫn **giữ nguyên** trên PHP 8. Vì vậy, `5 == "5 of something"` vẫn được coi như `5 == 5`.
> 

Hãy lưu ý rằng khi sửa đổi **kiểu dữ liệu** trong bất kỳ định dạng đối tượng đã tuần tự nào, điều quan trọng là phải nhớ **cập nhật cả nhãn kiểu dữ liệu và chỉ báo độ dài** trong dữ liệu đã tuần tự. Nếu không, đối tượng đã tuần tự sẽ bị hỏng và không thể giải tuần tự.

Khi làm việc trực tiếp với các định dạng nhị phân, chúng tôi khuyến nghị dùng **tiện ích mở rộng Hackvertor**, có sẵn trên **BApp Store**. Với Hackvertor, bạn có thể chỉnh sửa dữ liệu đã tuần tự ở dạng chuỗi và tiện ích sẽ **tự động cập nhật dữ liệu nhị phân**, điều chỉnh các **offset** tương ứng. Điều này có thể giúp bạn tiết kiệm rất nhiều công sức thủ công.

[Lab: Modifying serialized data types | Web Security Academy](https://portswigger.net/web-security/deserialization/exploiting/lab-deserialization-modifying-serialized-data-types)

---

## **Using application functionality**

---

Bên cạnh việc chỉ kiểm tra các giá trị thuộc tính, chức năng của một website cũng có thể thực hiện các thao tác nguy hiểm trên dữ liệu đến từ một đối tượng đã giải tuần tự. Trong trường hợp này, bạn có thể lợi dụng giải tuần tự hóa không an toàn để truyền vào dữ liệu ngoài dự kiến và tận dụng chức năng liên quan để gây hại.

Ví dụ, như một phần của chức năng “Xóa người dùng” trên website, ảnh đại diện của người dùng sẽ bị xóa bằng cách truy cập đường dẫn tệp trong thuộc tính `$user->image_location`. Nếu `$user` được tạo ra từ một đối tượng đã tuần tự, kẻ tấn công có thể khai thác điều này bằng cách truyền vào một đối tượng đã chỉnh sửa với `image_location` được đặt thành một đường dẫn tệp tùy ý. Khi xóa tài khoản của chính mình, kẻ tấn công khi đó cũng sẽ xóa luôn tệp tùy ý này.

Ví dụ này dựa trên việc kẻ tấn công tự tay gọi phương thức nguy hiểm thông qua chức năng mà người dùng có thể truy cập. Tuy nhiên, giải tuần tự hóa không an toàn trở nên thú vị hơn nhiều khi bạn tạo các khai thác truyền dữ liệu vào những phương thức nguy hiểm một cách tự động. Điều này khả thi nhờ việc sử dụng các “magic method”.

[Lab: Using application functionality to exploit insecure deserialization | Web Security Academy](https://portswigger.net/web-security/deserialization/exploiting/lab-deserialization-using-application-functionality-to-exploit-insecure-deserialization)

---

## Magic Methods

---

Magic methods là một tập con đặc biệt của các phương thức mà bạn không cần gọi tường minh. Thay vào đó, chúng được tự động gọi mỗi khi xảy ra một sự kiện hoặc kịch bản cụ thể. Magic methods là tính năng phổ biến của lập trình hướng đối tượng trong nhiều ngôn ngữ. Đôi khi chúng được nhận diện bằng cách thêm tiền tố hoặc bao quanh tên phương thức bằng hai dấu gạch dưới.

Lập trình viên có thể thêm magic methods vào một lớp để xác định trước đoạn mã sẽ được thực thi khi sự kiện hoặc kịch bản tương ứng xảy ra. Thời điểm và lý do một magic method được gọi khác nhau tùy từng phương thức. Một ví dụ phổ biến trong PHP là `__construct()`, được gọi mỗi khi một đối tượng của lớp được khởi tạo, tương tự như `__init__` của Python. Thông thường, các phương thức khởi dựng (constructor) như vậy chứa mã để khởi tạo các thuộc tính của thể hiện. Tuy nhiên, magic methods có thể được tùy biến bởi lập trình viên để thực thi bất kỳ đoạn mã nào họ muốn.

Magic methods được dùng rộng rãi và tự bản thân chúng không phải là một lỗ hổng. Nhưng chúng có thể trở nên nguy hiểm khi đoạn mã chúng thực thi xử lý dữ liệu do kẻ tấn công kiểm soát, ví dụ như dữ liệu đến từ một đối tượng đã giải tuần tự. Kẻ tấn công có thể lợi dụng điều này để tự động gọi các phương thức trên dữ liệu đã giải tuần tự khi các điều kiện tương ứng được thỏa mãn.

Điều quan trọng nhất trong ngữ cảnh này là một số ngôn ngữ có các magic methods được gọi tự động trong quá trình giải tuần tự. Ví dụ, phương thức `unserialize()` của PHP sẽ tìm và gọi magic method `__wakeup()` của đối tượng.

Trong giải tuần tự Java, điều tương tự áp dụng cho `ObjectInputStream.readObject()`, vốn được dùng để đọc dữ liệu từ luồng byte ban đầu và về bản chất hoạt động như một constructor để “tái khởi tạo” một đối tượng đã tuần tự. Tuy nhiên, các lớp `Serializable` cũng có thể tự khai báo phương thức `readObject()` như sau:

```java
private void readObject(ObjectInputStream in) throws IOException, ClassNotFoundException
{
    // implementation
}
```

Một phương thức `readObject()` được khai báo chính xác theo cách này sẽ đóng vai trò như một magic method được gọi trong quá trình giải tuần tự. Điều này cho phép lớp kiểm soát chặt chẽ hơn việc giải tuần tự các trường của chính nó.

Bạn nên đặc biệt chú ý đến bất kỳ lớp nào chứa các loại magic methods này. Chúng cho phép bạn đưa dữ liệu từ một đối tượng đã tuần tự vào mã của website trước khi đối tượng được giải tuần tự hoàn toàn. Đây là điểm khởi đầu để tạo ra các khai thác nâng cao hơn.

---

## **Injecting arbitrary objects**

---

Như chúng ta đã thấy, đôi khi có thể khai thác giải tuần tự hóa không an toàn chỉ bằng cách chỉnh sửa đối tượng do website cung cấp. Tuy nhiên, việc tiêm các kiểu đối tượng tùy ý có thể mở ra nhiều khả năng hơn nữa.

Trong lập trình hướng đối tượng, các phương thức mà một đối tượng có thể sử dụng được xác định bởi lớp (class) của nó. Do đó, nếu kẻ tấn công có thể thao túng lớp của đối tượng được truyền vào dưới dạng dữ liệu đã tuần tự, họ có thể ảnh hưởng tới đoạn mã được thực thi sau khi giải tuần tự, thậm chí ngay trong quá trình giải tuần tự.

Các phương thức giải tuần tự thường không kiểm tra xem chúng đang giải tuần tự cái gì. Điều này có nghĩa là bạn có thể truyền vào các đối tượng thuộc bất kỳ lớp nào có thể tuần tự hóa và sẵn có đối với website, và đối tượng đó sẽ được giải tuần tự. Về thực chất, điều này cho phép kẻ tấn công tạo thể hiện của các lớp tùy ý. Việc đối tượng này không thuộc lớp như mong đợi không thành vấn đề. Kiểu đối tượng ngoài dự kiến có thể gây ra ngoại lệ trong logic ứng dụng, nhưng đến lúc đó đối tượng độc hại đã được khởi tạo rồi.

Nếu kẻ tấn công có quyền truy cập mã nguồn, họ có thể nghiên cứu chi tiết tất cả các lớp sẵn có. Để xây dựng một khai thác đơn giản, họ sẽ tìm các lớp chứa các magic method liên quan đến giải tuần tự, rồi kiểm tra xem có lớp nào thực hiện các thao tác nguy hiểm trên dữ liệu có thể kiểm soát hay không. Kẻ tấn công sau đó có thể truyền vào một đối tượng đã tuần tự của lớp này để sử dụng magic method của nó cho mục đích khai thác.
Các lớp chứa những magic method giải tuần tự này cũng có thể được dùng để khởi phát các cuộc tấn công phức tạp hơn, liên quan đến một chuỗi dài các lời gọi phương thức, được gọi là “gadget chain”.

[Lab: Arbitrary object injection in PHP | Web Security Academy](https://portswigger.net/web-security/deserialization/exploiting/lab-deserialization-arbitrary-object-injection-in-php)

---

## Gadget chains

---

“Gadget” là một đoạn mã sẵn có trong ứng dụng có thể giúp kẻ tấn công đạt được một mục tiêu nhất định. Một gadget đơn lẻ có thể không trực tiếp làm điều gì nguy hại với dữ liệu người dùng. Tuy nhiên, mục tiêu của kẻ tấn công có thể chỉ là gọi một phương thức sẽ truyền dữ liệu đầu vào của họ sang một gadget khác. Bằng cách xâu chuỗi nhiều gadget theo cách này, kẻ tấn công có thể truyền dữ liệu vào một “sink gadget” nguy hiểm, nơi nó có thể gây thiệt hại tối đa.

Điều quan trọng cần hiểu là, không giống một số kiểu khai thác khác, một chuỗi gadget **không phải** là payload gồm các phương thức được kẻ tấn công tự ghép lại. Toàn bộ mã đã tồn tại sẵn trên website. Thứ duy nhất kẻ tấn công kiểm soát là **dữ liệu** được truyền vào chuỗi gadget. Việc này thường được thực hiện thông qua một **magic method** được gọi trong quá trình giải tuần tự, đôi khi được gọi là “kick-off gadget”.

Ngoài thực tế, nhiều lỗ hổng giải tuần tự hóa không an toàn chỉ có thể khai thác được thông qua việc sử dụng **gadget chain**. Đôi khi đó có thể là một chuỗi đơn giản một hoặc hai bước, nhưng để xây dựng các cuộc tấn công mức độ nghiêm trọng cao thường sẽ cần một trình tự phức tạp hơn gồm khởi tạo đối tượng và gọi phương thức. Vì vậy, khả năng xây dựng **gadget chain** là một trong những yếu tố then chốt để khai thác thành công lỗ hổng giải tuần tự hóa không an toàn.

---

### **Pre-built gadget chains**

---

Việc tự tay xác định các chuỗi gadget có thể khá vất vả và gần như không thể nếu không có quyền truy cập mã nguồn. May mắn là có một vài lựa chọn để làm việc với các chuỗi gadget dựng sẵn mà bạn có thể thử trước.

Có một số công cụ cung cấp nhiều chuỗi đã được phát hiện trước đó và đã được khai thác thành công trên các website khác. Ngay cả khi bạn không có quyền truy cập mã nguồn, bạn vẫn có thể dùng các công cụ này để vừa nhận diện vừa khai thác các lỗ hổng giải tuần tự hóa không an toàn với tương đối ít công sức. Cách tiếp cận này khả thi nhờ việc các thư viện chứa các chuỗi gadget có thể khai thác được sử dụng rộng rãi. Ví dụ, nếu một chuỗi gadget trong thư viện Apache Commons Collections của Java có thể bị khai thác trên một website, thì bất kỳ website nào khác triển khai thư viện này cũng có thể bị khai thác bằng cùng chuỗi đó.

> **ysoserial**
> 

Một công cụ như vậy cho việc giải tuần tự Java là **“ysoserial”**. Công cụ này cho phép bạn chọn một trong các **gadget chain** được cung cấp cho thư viện mà bạn cho rằng ứng dụng mục tiêu đang sử dụng, sau đó truyền vào **lệnh** bạn muốn thực thi. Nó sẽ tạo ra một **đối tượng đã tuần tự** phù hợp dựa trên chuỗi đã chọn. Cách làm này vẫn cần một mức độ thử - sai nhất định, nhưng ít tốn công hơn đáng kể so với tự xây dựng các gadget chain thủ công.

> **Lưu ý**
> 
> 
> Trên các phiên bản Java từ **16** trở lên, bạn cần đặt một loạt tham số dòng lệnh để Java có thể chạy **ysoserial**. Ví dụ:
> 
> ```bash
> java -jar ysoserial-all.jar \
>    --add-opens=java.xml/com.sun.org.apache.xalan.internal.xsltc.trax=ALL-UNNAMED \
>    --add-opens=java.xml/com.sun.org.apache.xalan.internal.xsltc.runtime=ALL-UNNAMED \
>    --add-opens=java.base/java.net=ALL-UNNAMED \
>    --add-opens=java.base/java.util=ALL-UNNAMED \
>    [payload] '[command]'
> ```
> 

[Lab: Exploiting Java deserialization with Apache Commons | Web Security Academy](https://portswigger.net/web-security/deserialization/exploiting/lab-deserialization-exploiting-java-deserialization-with-apache-commons)

Không phải tất cả các chuỗi gadget trong **ysoserial** đều cho phép bạn chạy mã tùy ý. Thay vào đó, chúng có thể hữu ích cho các mục đích khác. Ví dụ, bạn có thể dùng các chuỗi sau để giúp nhanh chóng phát hiện giải tuần tự hóa không an toàn trên hầu như mọi máy chủ:

- **URLDNS** kích hoạt một truy vấn DNS tới URL được cung cấp. Quan trọng nhất, nó **không phụ thuộc** vào việc ứng dụng mục tiêu sử dụng một thư viện dễ tổn thương cụ thể nào và hoạt động trên **mọi** phiên bản Java đã biết. Điều này khiến nó trở thành chuỗi gadget **phổ quát nhất** cho mục đích **phát hiện**. Nếu bạn phát hiện một đối tượng đã tuần tự trong lưu lượng, bạn có thể thử dùng chuỗi gadget này để tạo ra một đối tượng kích hoạt **tương tác DNS** với máy chủ **Burp Collaborator**. Nếu có tương tác, bạn có thể chắc chắn rằng quá trình **giải tuần tự** đã xảy ra trên mục tiêu.
- **JRMPClient** là một chuỗi phổ quát khác có thể dùng cho bước phát hiện ban đầu. Nó khiến máy chủ cố gắng **thiết lập kết nối TCP** tới địa chỉ IP được cung cấp. Lưu ý rằng bạn cần cung cấp **địa chỉ IP thô** thay vì hostname. Chuỗi này có thể hữu ích trong môi trường mà **mọi lưu lượng outbound đều bị firewall chặn**, bao gồm cả truy vấn DNS. Bạn có thể thử tạo payload với **hai địa chỉ IP khác nhau**: một **cục bộ (local)** và một **bên ngoài bị firewall chặn**. Nếu ứng dụng **phản hồi ngay** với payload dùng địa chỉ cục bộ nhưng **treo/delay** với payload dùng địa chỉ bên ngoài (do máy chủ cố gắng kết nối tới địa chỉ bị firewall chặn), điều này cho thấy chuỗi gadget đã hoạt động. Trong trường hợp này, **sự khác biệt thời gian phản hồi** tinh tế có thể giúp bạn phát hiện liệu việc **giải tuần tự** có diễn ra trên máy chủ hay không, ngay cả trong các tình huống **mù (blind)**.

---

### **PHP Generic Gadget Chains**

---

Hầu hết các ngôn ngữ thường xuyên gặp lỗ hổng giải tuần tự hóa không an toàn đều có các công cụ proof-of-concept tương đương. Ví dụ, với các website dùng PHP, bạn có thể sử dụng **“PHP Generic Gadget Chains” (PHPGGC)**.

[Lab: Exploiting PHP deserialization with a pre-built gadget chain | Web Security Academy](https://portswigger.net/web-security/deserialization/exploiting/lab-deserialization-exploiting-php-deserialization-with-a-pre-built-gadget-chain)

> **Lưu ý**
> 
> 
> Điều quan trọng cần lưu ý là lỗ hổng nằm ở việc **giải tuần tự dữ liệu do người dùng kiểm soát**, chứ không phải chỉ vì sự hiện diện của một **gadget chain** trong mã của website hoặc trong bất kỳ thư viện nào của nó. Gadget chain chỉ là phương tiện để thao túng luồng dữ liệu gây hại **sau khi** nó đã được tiêm vào. Điều này cũng áp dụng cho nhiều lỗ hổng **hỏng bộ nhớ (memory corruption)** dựa vào việc giải tuần tự dữ liệu không đáng tin cậy. Nói cách khác, một website vẫn có thể dễ bị tấn công ngay cả khi nó bằng cách nào đó đã bịt kín **mọi** gadget chain có thể có.
> 

---

## **Documented gadget chains**

---

Không phải lúc nào cũng có sẵn một công cụ chuyên dụng để khai thác các chuỗi gadget đã biết trong framework mà ứng dụng mục tiêu sử dụng. Trong trường hợp này, luôn đáng để tìm kiếm trực tuyến xem có khai thác nào đã được ghi chép mà bạn có thể tự điều chỉnh hay không. Việc tinh chỉnh mã có thể đòi hỏi một số hiểu biết cơ bản về ngôn ngữ và framework, và đôi khi bạn có thể cần tự tuần tự hóa đối tượng, nhưng cách tiếp cận này vẫn tốn ít công sức hơn đáng kể so với việc xây dựng một khai thác từ đầu.

[Lab: Exploiting Ruby deserialization using a documented gadget chain | Web Security Academy](https://portswigger.net/web-security/deserialization/exploiting/lab-deserialization-exploiting-ruby-deserialization-using-a-documented-gadget-chain)

Ngay cả khi bạn không tìm được một chuỗi gadget sẵn dùng, bạn vẫn có thể thu được những kiến thức giá trị giúp bạn tự tạo một khai thác (exploit) tùy chỉnh.

---

## Tự tạo cuộc tấn công

---

Khi các chuỗi gadget đóng gói sẵn và các khai thác đã được ghi chép không thành công, bạn sẽ cần tự tạo khai thác của mình.

Để xây dựng thành công một chuỗi gadget riêng, gần như chắc chắn bạn sẽ cần quyền truy cập mã nguồn. Bước đầu tiên là nghiên cứu mã nguồn này để xác định một lớp chứa một magic method được gọi trong quá trình giải tuần tự. Đánh giá đoạn mã mà magic method này thực thi để xem liệu nó có trực tiếp làm điều gì nguy hiểm với các thuộc tính do người dùng kiểm soát hay không. Luôn đáng để kiểm tra điều này phòng trường hợp có thể khai thác trực tiếp.

Nếu bản thân magic method không thể khai thác, nó có thể đóng vai trò “kick-off gadget” cho một chuỗi gadget. Hãy nghiên cứu bất kỳ phương thức nào mà kick-off gadget gọi tới. Có phương thức nào trong số này làm điều gì nguy hiểm với dữ liệu bạn kiểm soát không? Nếu không, hãy xem kỹ hơn từng phương thức mà chúng gọi tiếp theo, và cứ như vậy.

Lặp lại quy trình này, ghi lại những giá trị mà bạn có quyền truy cập, cho đến khi bạn đi vào ngõ cụt hoặc xác định được một “sink gadget” nguy hiểm mà vào đó dữ liệu có thể kiểm soát của bạn được truyền.

Khi bạn đã tìm ra cách xây dựng thành công một chuỗi gadget trong mã ứng dụng, bước tiếp theo là tạo một đối tượng đã tuần tự chứa payload của bạn. Việc này đơn giản là nghiên cứu phần khai báo lớp trong mã nguồn và tạo một đối tượng đã tuần tự hợp lệ với các giá trị phù hợp cần cho khai thác của bạn. Như chúng ta đã thấy trong các lab trước, điều này tương đối đơn giản khi làm việc với các định dạng tuần tự hóa dạng chuỗi.

Làm việc với các định dạng nhị phân, chẳng hạn khi xây dựng một khai thác giải tuần tự Java, có thể đặc biệt cồng kềnh. Khi chỉ thay đổi nhỏ trên một đối tượng hiện có, bạn có thể thoải mái làm việc trực tiếp với các byte. Tuy nhiên, khi thực hiện những thay đổi lớn hơn, như truyền vào một đối tượng hoàn toàn mới, điều này nhanh chóng trở nên bất khả thi. Thường sẽ đơn giản hơn nhiều nếu bạn tự viết mã bằng ngôn ngữ mục tiêu để tự tạo và tuần tự hóa dữ liệu.

Khi tạo chuỗi gadget của riêng bạn, hãy chú ý tìm cơ hội tận dụng phần bề mặt tấn công bổ sung này để kích hoạt các lỗ hổng thứ cấp.

[Lab: Developing a custom gadget chain for Java deserialization | Web Security Academy](https://portswigger.net/web-security/deserialization/exploiting/lab-deserialization-developing-a-custom-gadget-chain-for-java-deserialization)

Bằng cách nghiên cứu kỹ mã nguồn, bạn có thể phát hiện các chuỗi gadget dài hơn, có khả năng cho phép bạn xây dựng các cuộc tấn công mức độ nghiêm trọng cao, thường bao gồm cả thực thi mã từ xa.

[Lab: Developing a custom gadget chain for PHP deserialization | Web Security Academy](https://portswigger.net/web-security/deserialization/exploiting/lab-deserialization-developing-a-custom-gadget-chain-for-php-deserialization)

---

## **PHAR deserialization**

---

Cho đến nay, chúng ta chủ yếu xem xét việc khai thác các lỗ hổng giải tuần tự hóa khi website **rõ ràng** giải tuần tự đầu vào do người dùng cung cấp. Tuy nhiên, trong PHP đôi khi vẫn có thể khai thác giải tuần tự hóa ngay cả khi **không có** dấu hiệu sử dụng phương thức `unserialize()`.

PHP cung cấp một số wrapper kiểu URL mà bạn có thể dùng để xử lý các giao thức khác nhau khi truy cập đường dẫn tệp. Một trong số đó là wrapper `phar://`, cung cấp giao diện stream để truy cập các tệp PHP Archive (`.phar`).

Tài liệu PHP cho biết các tệp manifest của PHAR chứa **metadata đã tuần tự hóa**. Điều quan trọng là nếu bạn thực hiện **bất kỳ thao tác hệ thống tệp** nào trên một stream `phar://`, metadata này sẽ được **giải tuần tự ngầm**. Điều này có nghĩa là một stream `phar://` **có thể** trở thành vector khai thác giải tuần tự hóa không an toàn, miễn là bạn có thể truyền stream này vào một phương thức thao tác hệ thống tệp.

Với các phương thức hệ thống tệp rõ ràng nguy hiểm, như `include()` hoặc `fopen()`, các website thường đã triển khai biện pháp đối phó để giảm khả năng bị lạm dụng. Tuy nhiên, các phương thức như `file_exists()`, vốn **không** quá hiển nhiên là nguy hiểm, có thể **không** được bảo vệ chặt chẽ như vậy.

Kỹ thuật này cũng yêu cầu bạn **tải lên** PHAR lên máy chủ bằng cách nào đó. Một cách tiếp cận là tận dụng chức năng **upload ảnh**, chẳng hạn. Nếu bạn có thể tạo một **polyglot file**, trong đó một PHAR **giả dạng** như một tệp JPG đơn giản, bạn đôi khi có thể **vượt qua** các kiểm tra hợp lệ của website. Nếu sau đó bạn buộc website **nạp** “JPG” đa ngữ này thông qua stream `phar://`, bất kỳ dữ liệu độc hại nào bạn tiêm qua **PHAR metadata** sẽ được **giải tuần tự**. Do PHP **không kiểm tra** phần mở rộng tệp khi đọc một stream, việc tệp dùng đuôi ảnh **không quan trọng**.

Miễn là lớp (class) của đối tượng được website hỗ trợ, cả hai magic method `__wakeup()` và `__destruct()` đều có thể được gọi theo cách này, cho phép bạn **khởi phát một gadget chain** bằng kỹ thuật nói trên.

[Lab: Using PHAR deserialization to deploy a custom gadget chain | Web Security Academy](https://portswigger.net/web-security/deserialization/exploiting/lab-deserialization-using-phar-deserialization-to-deploy-a-custom-gadget-chain)

---

## Memory corruption

---

Ngay cả khi không dùng gadget chain, vẫn có thể khai thác giải tuần tự hóa không an toàn. Nếu mọi cách khác đều thất bại, thường có các lỗ hổng hỏng bộ nhớ đã được công bố công khai có thể khai thác thông qua giải tuần tự hóa không an toàn. Những lỗ hổng này thường dẫn đến thực thi mã từ xa (RCE).

Các phương thức giải tuần tự, như `unserialize()` của PHP, hiếm khi được gia cố chống lại dạng tấn công này và phơi bày một lượng lớn bề mặt tấn công. Điều này không phải lúc nào cũng được coi là một lỗ hổng tự thân vì ngay từ đầu các phương thức này không được thiết kế để xử lý dữ liệu do người dùng kiểm soát.

---

# Bảo mật

---

Nói chung, nên tránh giải tuần tự dữ liệu đầu vào từ người dùng trừ khi thực sự cần thiết. Mức độ nghiêm trọng mà các khai thác có thể gây ra và độ khó trong việc bảo vệ chống lại chúng thường lớn hơn lợi ích trong nhiều trường hợp.

Nếu bạn buộc phải giải tuần tự dữ liệu từ nguồn không tin cậy, hãy tích hợp các biện pháp mạnh để bảo đảm dữ liệu không bị giả mạo. Ví dụ, bạn có thể triển khai chữ ký số để kiểm tra tính toàn vẹn của dữ liệu. Tuy nhiên, hãy nhớ rằng mọi kiểm tra phải diễn ra **trước khi** bắt đầu quá trình giải tuần tự. Nếu không, chúng hầu như không có tác dụng.

Nếu có thể, bạn nên tránh hoàn toàn việc sử dụng các cơ chế giải tuần tự tổng quát. Dữ liệu đã tuần tự từ các cơ chế này chứa **mọi** thuộc tính của đối tượng gốc, bao gồm cả các trường riêng tư có thể chứa thông tin nhạy cảm. Thay vào đó, bạn có thể tự xây dựng các phương thức tuần tự hóa theo từng lớp (class-specific) để ít nhất có thể kiểm soát trường nào được lộ ra.

Cuối cùng, hãy nhớ rằng lỗ hổng nằm ở **việc giải tuần tự dữ liệu từ người dùng**, chứ không phải ở sự hiện diện của các gadget chain xử lý dữ liệu về sau. Đừng dựa vào việc cố gắng loại bỏ các gadget chain mà bạn phát hiện trong quá trình kiểm thử. Việc bịt kín tất cả chúng là bất khả thi do mạng lưới phụ thuộc giữa các thư viện gần như chắc chắn tồn tại trên website của bạn. Tại bất kỳ thời điểm nào, các khai thác hỏng bộ nhớ đã được công bố công khai cũng là một yếu tố, nghĩa là ứng dụng của bạn vẫn có thể dễ bị tổn thương dù sao đi nữa.
