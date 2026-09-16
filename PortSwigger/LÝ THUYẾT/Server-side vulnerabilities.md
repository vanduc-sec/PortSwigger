# Server-side vulnerabilities

Trạng thái: Chưa bắt đầu
subject: Advanced

# Path traversal

---

Path traversal còn được gọi là **directory traversal**. Đây là một lỗ hổng cho phép kẻ tấn công đọc các tệp tùy ý trên máy chủ đang chạy ứng dụng. Những tệp này có thể bao gồm:

- **Mã nguồn và dữ liệu của ứng dụng.**
- **Thông tin xác thực (credentials) của các hệ thống back-end.**
- **Các tệp nhạy cảm của hệ điều hành.**

Trong một số trường hợp, kẻ tấn công thậm chí có thể **ghi dữ liệu vào các tệp tùy ý trên máy chủ**, từ đó thay đổi dữ liệu hoặc hành vi của ứng dụng, và cuối cùng có thể **chiếm quyền kiểm soát hoàn toàn máy chủ**.

Hãy tưởng tượng một ứng dụng thương mại điện tử hiển thị hình ảnh các sản phẩm để bán. Ứng dụng này có thể tải ảnh bằng đoạn HTML sau:

```html
<img src="/loadImage?filename=218.png">
```

Tham số `filename` trong URL `/loadImage` được truyền vào và ứng dụng sẽ trả về nội dung của tệp tương ứng. Các tệp ảnh được lưu trữ trên đĩa tại thư mục `/var/www/images/`.

Để trả về một hình ảnh, ứng dụng nối tên tệp được yêu cầu vào thư mục gốc này và sử dụng API của hệ thống tệp để đọc nội dung tệp.

Nói cách khác, ứng dụng đang đọc từ đường dẫn sau:

```
/var/www/images/218.png
```

Ứng dụng này **không triển khai bất kỳ cơ chế phòng vệ nào chống lại path traversal**.

Kết quả là, kẻ tấn công có thể gửi yêu cầu URL sau để lấy tệp `/etc/passwd` từ hệ thống tệp của máy chủ:

```
https://insecure-website.com/loadImage?filename=../../../etc/passwd
```

Điều này buộc ứng dụng đọc từ đường dẫn:

```
/var/www/images/../../../etc/passwd
```

Trong đó chuỗi `../` là hợp lệ trong đường dẫn, có nghĩa là **đi lên một cấp thư mục**. Ba chuỗi `../` liên tiếp sẽ đưa đường dẫn từ `/var/www/images/` lên thư mục gốc của hệ thống, do đó tệp thực tế được đọc là:

```
/etc/passwd
```

Trên hệ điều hành dựa trên Unix, đây là tệp chuẩn chứa thông tin về các user đã đăng ký trên máy chủ. Tuy nhiên, kẻ tấn công cũng có thể dùng kỹ thuật tương tự để truy xuất các tệp tùy ý khác.

Trên Windows, cả `../` và `..\` đều là chuỗi hợp lệ cho **directory traversal**. Ví dụ dưới đây minh họa một cuộc tấn công tương tự trên máy chủ chạy Windows:

```
https://insecure-website.com/loadImage?filename=..\..\..\windows\win.ini
```

---

# Access Control

---

## Khái niệm

---

Access control (kiểm soát truy cập) là việc áp đặt các ràng buộc để xác định **ai hoặc cái gì được phép thực hiện hành động hoặc truy cập tài nguyên**.

Trong bối cảnh ứng dụng web, **access control phụ thuộc vào authentication (xác thực) và session management (quản lý phiên làm việc)**:

- **Authentication (xác thực):** đảm bảo rằng người dùng đúng là người mà họ khai báo.
- **Session management (quản lý phiên):** xác định những HTTP request tiếp theo thuộc về cùng một người dùng đó.
- **Access control (kiểm soát truy cập):** quyết định xem người dùng có được phép thực hiện hành động mà họ đang yêu cầu hay không.

**Broken access control (kiểm soát truy cập bị phá vỡ)** là một trong những lỗ hổng thường gặp và thường mang tính chất nghiêm trọng.

Việc **thiết kế và quản lý access control** là một vấn đề phức tạp và mang tính động, đòi hỏi phải kết hợp nhiều yếu tố: **yêu cầu nghiệp vụ, cấu trúc tổ chức, và ràng buộc pháp lý** để triển khai về mặt kỹ thuật. Vì các quyết định thiết kế access control đều do con người đưa ra, nên khả năng xảy ra lỗi là rất cao.

---

## Leo thang đặc quyền (Vertical)

---

Nếu một người dùng có thể truy cập vào một chức năng mà họ **không được phép sử dụng**, thì đó chính là **vertical privilege escalation**.

Ví dụ: nếu một người dùng **không có quyền quản trị** nhưng vẫn có thể truy cập vào **trang quản trị** (admin page) nơi họ có khả năng **xóa tài khoản của người dùng khác**, thì đây chính là một trường hợp **leo thang đặc quyền theo chiều dọc**.

---

## Chức năng không được bảo vệ

---

Ở mức cơ bản nhất, **vertical privilege escalation** xảy ra khi một ứng dụng **không áp dụng bất kỳ biện pháp bảo vệ nào cho các chức năng nhạy cảm**.

Ví dụ: các chức năng quản trị có thể chỉ được hiển thị trong **trang chào mừng của quản trị viên**, nhưng không xuất hiện trong **trang chào mừng của người dùng thường**. Tuy nhiên, một người dùng vẫn có thể truy cập các chức năng quản trị chỉ bằng cách **truy cập trực tiếp vào URL quản trị liên quan**.

Ví dụ, một website có thể lưu trữ chức năng nhạy cảm tại URL sau:

```
https://insecure-website.com/admin
```

Trong trường hợp này, **mọi người dùng** đều có thể truy cập URL trên, chứ không chỉ riêng các quản trị viên – những người vốn được cung cấp liên kết này trong giao diện của họ.

Trong một số trường hợp, **URL quản trị** có thể bị lộ ở các vị trí khác, chẳng hạn như trong file `robots.txt`:

```
https://insecure-website.com/robots.txt
```

Ngay cả khi URL quản trị không bị tiết lộ trực tiếp, **kẻ tấn công** vẫn có thể sử dụng **wordlist** để brute-force và tìm ra vị trí của chức năng nhạy cảm.

Trong một số trường hợp, chức năng nhạy cảm được **ẩn đi bằng cách gán cho nó một URL khó đoán hơn**. Đây là ví dụ của phương pháp gọi là **“security by obscurity” (bảo mật dựa trên sự che giấu)**.

Tuy nhiên, việc **che giấu chức năng nhạy cảm** không phải là một cơ chế kiểm soát truy cập hiệu quả, bởi vì người dùng vẫn có thể khám phá ra URL bị làm rối (obfuscated URL) bằng nhiều cách khác nhau.

Ví dụ, hãy tưởng tượng một ứng dụng lưu trữ các chức năng quản trị tại URL sau:

```
https://insecure-website.com/administrator-panel-yb556
```

Đây là một URL mà kẻ tấn công **không dễ đoán trực tiếp**. Tuy nhiên, ứng dụng vẫn có thể **vô tình rò rỉ URL này cho người dùng**.

Ví dụ, URL có thể bị tiết lộ trong đoạn **JavaScript** dùng để dựng giao diện dựa trên quyền của người dùng:

```html
<script>
	var isAdmin = false;
	if (isAdmin) {
		...
		var adminPanelTag = document.createElement('a');
		adminPanelTag.setAttribute('href', 'https://insecure-website.com/administrator-panel-yb556');
		adminPanelTag.innerText = 'Admin panel';
		...
	}
</script>
```

---

## Parameter-based

---

Một số ứng dụng xác định **quyền truy cập hoặc vai trò (role) của người dùng** tại thời điểm đăng nhập, rồi **lưu trữ thông tin này ở vị trí mà người dùng có thể kiểm soát**. Các vị trí này có thể là:

- Trường ẩn (**hidden field**) trong form.
- **Cookie**.
- Tham số truy vấn (**query string parameter**) được gán sẵn.

Ứng dụng sau đó đưa ra quyết định **kiểm soát truy cập** dựa trên giá trị được gửi lên. Ví dụ:

```
https://insecure-website.com/login/home.jsp?admin=true
https://insecure-website.com/login/home.jsp?role=1
```

Cách tiếp cận này **không an toàn**, bởi vì người dùng hoàn toàn có thể **tự chỉnh sửa giá trị** và truy cập vào các chức năng mà họ **không được phép**, chẳng hạn như **chức năng quản trị (admin functions)**.

---

## Leo thang đặc quyền (Horizon)

---

**Horizontal privilege escalation** xảy ra khi một người dùng có thể truy cập vào **tài nguyên của người dùng khác**, thay vì chỉ tài nguyên của chính họ thuộc cùng loại.

Ví dụ: nếu một nhân viên có thể xem được **hồ sơ của các nhân viên khác** ngoài hồ sơ của chính mình, thì đây là **horizontal privilege escalation**.

Các cuộc tấn công leo thang đặc quyền ngang hàng có thể sử dụng các phương pháp khai thác tương tự như **vertical privilege escalation**.

Ví dụ: một người dùng truy cập trang tài khoản của mình bằng URL:

```
https://insecure-website.com/myaccount?id=123
```

Nếu kẻ tấn công thay đổi giá trị của tham số `id` sang ID của người dùng khác, họ có thể **truy cập vào trang tài khoản của người dùng đó**, bao gồm **dữ liệu và chức năng liên quan**.

> **NOTE**
> 
> 
> Đây là ví dụ của một lỗ hổng **Insecure Direct Object Reference (IDOR)**.
> 
> Loại lỗ hổng này xảy ra khi **giá trị tham số do người dùng kiểm soát** được sử dụng trực tiếp để truy cập tài nguyên hoặc chức năng.
> 

Trong một số ứng dụng, tham số khai thác được không mang giá trị dễ đoán.

Ví dụ: thay vì sử dụng số tăng dần, ứng dụng có thể sử dụng **Globally Unique Identifiers (GUIDs)** để định danh người dùng. Điều này có thể ngăn kẻ tấn công đoán hoặc dự đoán định danh của người khác.

Tuy nhiên, **GUID của người dùng khác có thể bị lộ** ở những vị trí khác trong ứng dụng – chẳng hạn như trong **tin nhắn** hoặc **bình luận/review** – nơi mà người dùng được tham chiếu.

Thường thì một cuộc tấn công **horizontal privilege escalation** có thể được **chuyển thành vertical privilege escalation** bằng cách chiếm đoạt tài khoản của một người dùng có đặc quyền cao hơn.

Ví dụ: **horizontal escalation** có thể cho phép kẻ tấn công **đặt lại hoặc chiếm đoạt mật khẩu** của người dùng khác. Nếu kẻ tấn công nhắm đến một tài khoản **quản trị viên (administrator)** và chiếm được tài khoản đó, thì họ sẽ có quyền quản trị và có thể thực hiện **vertical privilege escalation**.

Kẻ tấn công có thể khai thác kỹ thuật **parameter tampering** (sửa đổi tham số) đã mô tả ở phần horizontal privilege escalation để truy cập vào trang tài khoản của người dùng khác:

```
https://insecure-website.com/myaccount?id=456
```

Nếu người dùng mục tiêu là **administrator**, thì kẻ tấn công sẽ truy cập được vào **trang tài khoản quản trị**. Trang này có thể:

- **Tiết lộ mật khẩu của quản trị viên**, hoặc
- **Cung cấp cơ chế để thay đổi mật khẩu**, hoặc
- **Cung cấp quyền truy cập trực tiếp đến các chức năng đặc quyền**.

---

# **Authentication vulnerabilities**

---

## Khái niệm

---

Về mặt khái niệm, các lỗ hổng xác thực khá dễ hiểu. Tuy nhiên, chúng thường mang tính **nghiêm trọng** vì có mối liên hệ trực tiếp giữa **authentication (xác thực)** và **security (bảo mật)**.

**Authentication vulnerabilities** có thể cho phép kẻ tấn công:

- Truy cập vào **dữ liệu và chức năng nhạy cảm**.
- Mở rộng **bề mặt tấn công (attack surface)** cho các khai thác tiếp theo.

Chính vì vậy, việc **nhận diện, khai thác và bypass các cơ chế bảo vệ xác thực phổ biến** là vô cùng quan trọng.

Trong phần này, chúng ta sẽ tìm hiểu:

1. **Các cơ chế xác thực phổ biến nhất** mà website thường sử dụng.
2. **Những lỗ hổng tiềm ẩn** trong các cơ chế đó.
3. **Lỗ hổng vốn có (inherent vulnerabilities)** trong từng loại cơ chế xác thực.
4. **Những lỗ hổng phát sinh** từ việc triển khai không đúng cách.
5. Cách để **xây dựng cơ chế xác thực an toàn và vững chắc nhất có thể**.

---

## **Authentication v/s Authorization**

---

- **Authentication (xác thực)** là quá trình kiểm tra để đảm bảo rằng một người dùng đúng là người mà họ khai báo.
- **Authorization (ủy quyền / phân quyền)** là quá trình kiểm tra xem người dùng đó có được phép thực hiện một hành động nào đó hay không.

Ví dụ: **Authentication** xác định liệu một người đang cố gắng truy cập website với tên đăng nhập `Carlos123` có thực sự là chủ tài khoản đã tạo ra username này hay không.

Sau khi `Carlos123` **đã được xác thực**, quyền hạn (**permissions**) của tài khoản sẽ xác định những gì anh ta được **ủy quyền** để thực hiện.

Ví dụ: anh ta có thể được ủy quyền để:

- Truy cập thông tin cá nhân của những người dùng khác, hoặc
- Thực hiện các hành động như **xóa tài khoản của người dùng khác**.

---

## Brute-force

---

Một cuộc tấn công **brute-force** xảy ra khi kẻ tấn công sử dụng phương pháp **thử – sai (trial and error)** để đoán ra **thông tin xác thực hợp lệ của người dùng**.

Các cuộc tấn công này thường được **tự động hóa** bằng cách sử dụng **wordlist** chứa danh sách username và password. Việc tự động hóa, đặc biệt khi sử dụng các công cụ chuyên dụng, cho phép kẻ tấn công thực hiện **một lượng lớn yêu cầu đăng nhập trong thời gian rất ngắn**.

Brute-force **không chỉ đơn thuần** là việc đưa ra các phỏng đoán ngẫu nhiên về username và password. Bằng cách sử dụng **logic cơ bản** hoặc **thông tin công khai sẵn có**, kẻ tấn công có thể **tinh chỉnh** brute-force để đưa ra những phỏng đoán hợp lý hơn, từ đó **tăng đáng kể hiệu quả** của cuộc tấn công.

Các website **chỉ dựa vào cơ chế đăng nhập bằng mật khẩu** như phương thức xác thực duy nhất sẽ đặc biệt dễ bị tổn thương nếu **không triển khai đủ biện pháp bảo vệ chống brute-force** (ví dụ: lockout, rate limiting, captcha).

Tên đăng nhập (**username**) thường rất dễ đoán nếu chúng tuân theo một mẫu định dạng quen thuộc, chẳng hạn như **địa chỉ email**.

Ví dụ: trong môi trường doanh nghiệp, định dạng đăng nhập phổ biến thường là:

```
firstname.lastname@somecompany.com
```

Tuy nhiên, ngay cả khi không có mẫu rõ ràng, vẫn thường thấy các tài khoản có đặc quyền cao (**high-privileged accounts**) được tạo với tên đăng nhập **dễ đoán** như:

```
admin
administrator
```

Trong quá trình **auditing (kiểm thử, đánh giá bảo mật)**, bạn cần kiểm tra xem **website có vô tình tiết lộ username tiềm năng** ra công khai hay không.

Ví dụ:

- Người dùng có thể **truy cập hồ sơ (profile) của người khác mà không cần đăng nhập** hay không?
    
    → Dù nội dung hồ sơ bị ẩn, nhưng **tên hiển thị trong profile** đôi khi chính là **username đăng nhập**.
    
- Kiểm tra **HTTP responses** để xem liệu có bị lộ **địa chỉ email** hay không.
    
    → Thỉnh thoảng, trong response có thể chứa email của người dùng có đặc quyền cao, chẳng hạn như **administrator** hoặc **IT support**.
    

Mật khẩu (**passwords**) cũng có thể bị brute-force, với mức độ khó dễ tùy thuộc vào **độ mạnh (strength)** của mật khẩu.

Nhiều website áp dụng một dạng **chính sách mật khẩu (password policy)**, nhằm **bắt buộc người dùng tạo mật khẩu có độ ngẫu nhiên cao (high-entropy)**. Về lý thuyết, điều này khiến việc brute-force mật khẩu trở nên khó khăn hơn.

Thông thường, chính sách này bao gồm các yêu cầu như:

- Độ dài tối thiểu của mật khẩu (**minimum number of characters**)
- Sự kết hợp giữa **chữ thường và chữ hoa**
- Ít nhất một **ký tự đặc biệt (special character)**

Tuy mật khẩu có **độ ngẫu nhiên cao (high-entropy passwords)** rất khó bị máy tính brute-force thuần túy, nhưng **attacker** có thể khai thác **hành vi con người** để tận dụng các lỗ hổng mà chính người dùng vô tình tạo ra.

Thay vì đặt mật khẩu mạnh với chuỗi ký tự hoàn toàn ngẫu nhiên, người dùng thường chọn một mật khẩu dễ nhớ rồi **chỉnh sửa để đáp ứng chính sách mật khẩu (password policy)**.

Ví dụ: nếu mật khẩu `mypassword` không được chấp nhận, thì người dùng có thể đổi thành:

- `Mypassword1!`
- `Myp4$$w0rd`

Trong các trường hợp chính sách yêu cầu người dùng **thường xuyên thay đổi mật khẩu (password rotation policy)**, họ cũng có xu hướng chỉ thực hiện những thay đổi nhỏ, dễ đoán.

Ví dụ:

- `Mypassword1!` → `Mypassword1?`
- `Mypassword1!` → `Mypassword2!`

Chính kiến thức này về **mật khẩu tiềm năng (likely credentials)** và **mẫu lặp dự đoán được (predictable patterns)** cho phép **attacker** thực hiện brute-force theo cách **tinh vi và hiệu quả hơn nhiều** so với việc chỉ đơn thuần thử mọi tổ hợp ký tự có thể.

Username enumeration xảy ra khi attacker có thể quan sát **sự thay đổi hành vi của website** để xác định xem một username có tồn tại hợp lệ hay không.

**Ví dụ điển hình:**

- **Login page (trang đăng nhập):**
    - Khi nhập **username hợp lệ** + **password sai** → website trả về lỗi: *"Password incorrect"*.
    - Khi nhập **username không hợp lệ** → website trả về lỗi: *"Username does not exist"*.
        
        → Attacker dựa vào sự khác biệt này để phân biệt username nào tồn tại.
        
- **Registration form (form đăng ký):**
    - Khi nhập một username → website báo *"This username is already taken"*.
    - Nghĩa là attacker có thể nhanh chóng xây dựng **danh sách username hợp lệ** chỉ bằng cách thử đăng ký.

**Nguy cơ bảo mật:**

Kỹ thuật này **rút ngắn thời gian brute-force** vì attacker không cần thử mật khẩu với mọi username có thể, mà chỉ tập trung vào **shortlist username hợp lệ** đã thu thập được.

Vượt qua cơ chế xác thực hai yếu tố (2FA)

Trong một số trường hợp, việc triển khai cơ chế xác thực hai yếu tố tồn tại lỗ hổng đến mức có thể bị **bỏ qua hoàn toàn**.

Ví dụ, nếu người dùng trước tiên được yêu cầu nhập mật khẩu, sau đó được yêu cầu nhập mã xác minh ở một trang khác, thì thực chất họ đã ở trong trạng thái **“đã đăng nhập”** trước cả khi nhập mã xác minh. Trong tình huống này, kẻ tấn công có thể thử truy cập trực tiếp vào các trang chỉ dành cho người đã đăng nhập, sau khi hoàn thành bước xác thực đầu tiên. Đôi khi, bạn sẽ phát hiện rằng website thực tế **không kiểm tra** việc người dùng có hoàn tất bước thứ hai hay không trước khi tải trang.

---

# SSRF

---

**Server-Side Request Forgery (SSRF)** là một lỗ hổng bảo mật web cho phép kẻ tấn công ép ứng dụng phía máy chủ (server-side application) gửi các yêu cầu (requests) đến những vị trí ngoài ý muốn.

Trong một cuộc tấn công SSRF điển hình, kẻ tấn công có thể khiến máy chủ kết nối đến các dịch vụ **chỉ dành cho nội bộ** bên trong hạ tầng của tổ chức. Trong những trường hợp khác, chúng có thể ép máy chủ kết nối đến các hệ thống bên ngoài tùy ý. Điều này có thể dẫn đến **rò rỉ dữ liệu nhạy cảm**, chẳng hạn như thông tin xác thực (authorization credentials).

Trong một cuộc tấn công **SSRF nhắm vào máy chủ**, kẻ tấn công khiến ứng dụng gửi một HTTP request ngược lại chính máy chủ đang chạy ứng dụng, thông qua **loopback network interface**. Việc này thường được thực hiện bằng cách cung cấp một URL có hostname như `127.0.0.1` (địa chỉ IP dự trữ trỏ về loopback adapter) hoặc `localhost` (tên thường dùng cho cùng adapter đó).

Ví dụ, giả sử một ứng dụng mua sắm cho phép người dùng xem tình trạng còn hàng của một sản phẩm tại một cửa hàng cụ thể. Để cung cấp thông tin này, ứng dụng phải truy vấn đến nhiều REST API ở back-end. Nó làm việc này bằng cách truyền URL của API endpoint tương ứng qua một HTTP request từ front-end. Khi người dùng kiểm tra trạng thái hàng tồn, trình duyệt sẽ gửi request như sau:

```
POST /product/stock HTTP/1.0
Content-Type: application/x-www-form-urlencoded
Content-Length: 118

stockApi=http://stock.weliketoshop.net:8080/product/stock/check%3FproductId%3D6%26storeId%3D1
```

Request này khiến máy chủ gửi yêu cầu đến URL được chỉ định, lấy thông tin hàng tồn và trả về cho người dùng.

Trong ví dụ trên, kẻ tấn công có thể sửa đổi request để chỉ định một URL cục bộ trên máy chủ:

```
POST /product/stock HTTP/1.0
Content-Type: application/x-www-form-urlencoded
Content-Length: 118

stockApi=http://localhost/admin
```

Khi đó, máy chủ sẽ fetch nội dung của `/admin` và trả lại cho người dùng.

Nếu kẻ tấn công tự truy cập trực tiếp `/admin`, họ sẽ không thấy gì vì chức năng quản trị thường chỉ khả dụng với người dùng đã xác thực. Tuy nhiên, nếu request đến `/admin` xuất phát từ **máy local** (chính máy chủ), thì cơ chế kiểm soát truy cập thông thường sẽ bị **bỏ qua**. Ứng dụng sẽ cấp **toàn quyền truy cập chức năng quản trị**, bởi vì request này trông như được gửi từ một nguồn **đáng tin cậy (trusted location)**.

**Tại sao các ứng dụng lại hoạt động theo cách này và ngầm tin tưởng các request xuất phát từ máy local?**

Điều này có thể xảy ra vì nhiều lý do khác nhau:

- **Kiểm soát truy cập được triển khai ở một thành phần khác** nằm phía trước application server. Khi một kết nối được gửi ngược lại về máy chủ, cơ chế kiểm soát này sẽ bị bỏ qua.
- **Phục hồi thảm họa (Disaster Recovery):** ứng dụng có thể cho phép quyền truy cập quản trị mà không cần đăng nhập đối với bất kỳ người dùng nào đến từ local machine. Cách này cho phép quản trị viên có thể khôi phục hệ thống nếu họ bị mất thông tin xác thực (credentials). Giả định ở đây là chỉ có người dùng hoàn toàn đáng tin cậy mới có thể truy cập trực tiếp từ máy chủ.
- **Giao diện quản trị chạy trên một port khác** so với ứng dụng chính, và người dùng bên ngoài thường không thể truy cập trực tiếp đến port này.

Những **mối quan hệ tin cậy (trust relationships)** kiểu này – khi request xuất phát từ local machine được xử lý khác biệt so với request thông thường – thường khiến **SSRF trở thành một lỗ hổng nghiêm trọng (critical vulnerability)**.

Trong một số tình huống, **application server** có khả năng tương tác với các hệ thống back-end mà người dùng bên ngoài **không thể truy cập trực tiếp**. Các hệ thống này thường sử dụng **địa chỉ IP private (không định tuyến được ra Internet)**. Bình thường, các hệ thống back-end này được bảo vệ nhờ **cấu trúc mạng (network topology)**, vì vậy chúng thường có **tư thế bảo mật yếu hơn (weaker security posture)**.

Trong nhiều trường hợp, hệ thống back-end nội bộ chứa các chức năng nhạy cảm có thể truy cập **mà không cần xác thực**, miễn là kẻ tấn công có thể tương tác được với hệ thống đó.

Ví dụ từ tình huống trước, giả sử tồn tại một giao diện quản trị (administrative interface) tại back-end URL:

```
https://192.168.0.68/admin
```

Kẻ tấn công có thể gửi request sau để khai thác lỗ hổng SSRF và truy cập giao diện quản trị này:

```
POST /product/stock HTTP/1.0
Content-Type: application/x-www-form-urlencoded
Content-Length: 118

stockApi=http://192.168.0.68/admin
```

👉 Điều này cho thấy **SSRF có thể trở thành cầu nối để vượt qua các lớp bảo mật mạng**, mở đường cho việc khai thác các hệ thống nội bộ vốn được coi là an toàn.

---

# **File upload vulnerabilities**

---

**Lỗ hổng tải tệp** xảy ra khi một web server cho phép người dùng tải tệp lên hệ thống file (filesystem) **mà không thực hiện kiểm tra chặt chẽ** các yếu tố như: tên tệp, loại tệp, nội dung, hoặc kích thước.

Nếu việc áp đặt các ràng buộc này không được thực hiện đúng cách, thì ngay cả một chức năng tải ảnh đơn giản cũng có thể bị lợi dụng để tải lên **tệp tùy ý và nguy hiểm**, bao gồm cả **tệp script phía server (server-side script)** có khả năng dẫn đến **Remote Code Execution (RCE)**.

Trong một số trường hợp, chỉ riêng hành động tải tệp lên đã đủ gây ra thiệt hại. Ở những tấn công khác, kẻ tấn công cần thực hiện một HTTP request tiếp theo đến tệp vừa tải lên, thường nhằm **kích hoạt việc thực thi của nó trên máy chủ**.

Mặc dù mối nguy hiểm từ việc tải tệp là khá rõ ràng, nhưng hiếm có website nào ngoài thực tế lại **không áp dụng bất kỳ hạn chế nào** đối với tệp mà người dùng được phép tải lên. Thay vào đó, các lập trình viên thường triển khai những cơ chế kiểm tra tưởng như “chặt chẽ”, nhưng trên thực tế lại tồn tại **lỗ hổng tiềm ẩn** hoặc có thể bị **bypass dễ dàng**.

Ví dụ:

- Website có thể áp dụng **blacklist** để chặn các loại tệp nguy hiểm, nhưng lại bỏ sót sự khác biệt trong cách **parser** xử lý phần mở rộng tệp (file extension). Giống như mọi blacklist khác, rất dễ vô tình bỏ qua những loại tệp ít phổ biến nhưng vẫn nguy hiểm.
- Một số website kiểm tra loại tệp (file type) bằng cách xác minh các thuộc tính có thể bị **giả mạo** bởi kẻ tấn công, sử dụng các công cụ như **Burp Proxy** hoặc **Repeater**.
- Ngay cả khi có cơ chế kiểm tra mạnh mẽ, chúng thường được áp dụng **không nhất quán** trên toàn bộ hệ thống (nhiều host, nhiều thư mục). Sự thiếu nhất quán này có thể bị lợi dụng để khai thác.

👉 Tóm lại, **sai sót trong cách xác thực (validation) hoặc áp dụng validation không đồng nhất** chính là nguyên nhân chủ yếu tạo điều kiện cho **File Upload Vulnerabilities**.

Từ góc độ bảo mật, **kịch bản tồi tệ nhất** là khi một website cho phép tải lên các **server-side script** như PHP, Java, hoặc Python, và đồng thời máy chủ được cấu hình để **thực thi** các tệp đó như code. Khi đó, việc tạo một **web shell** trên server trở nên cực kỳ đơn giản.

> **Web Shell**
> 
> 
> **Web shell** là một đoạn script độc hại cho phép kẻ tấn công thực thi **các lệnh tùy ý (arbitrary commands)** trên máy chủ web từ xa, chỉ bằng cách gửi các HTTP request đến đúng endpoint.
> 

Nếu tải lên thành công một web shell, kẻ tấn công gần như có **toàn quyền kiểm soát server**:

- Đọc và ghi tệp tùy ý trên filesystem.
- Rò rỉ (exfiltrate) dữ liệu nhạy cảm.
- Sử dụng máy chủ làm bàn đạp (pivot) để tấn công vào **hạ tầng nội bộ** hoặc các server khác bên ngoài mạng.

**Ví dụ web shell cơ bản (PHP one-liner)**

```php
<?php echo file_get_contents('/path/to/target/file'); ?>
```

Sau khi tệp này được upload, chỉ cần gửi request đến file đó là có thể nhận lại **nội dung của tệp mục tiêu** trong response.

**Ví dụ web shell linh hoạt hơn**

```php
<?php echo system($_GET['command']); ?>
```

Script này cho phép truyền vào một lệnh hệ thống tùy ý thông qua query parameter, ví dụ:

```
GET /example/exploit.php?command=id HTTP/1.1
```

→ Máy chủ sẽ thực thi lệnh `id` và trả về kết quả trong HTTP response.

👉 Đây chính là lý do **File Upload Vulnerabilities** thường bị đánh giá ở mức **Critical**, vì chúng có thể dẫn tới **Remote Code Execution (RCE)** và toàn quyền kiểm soát hệ thống.

Trong thực tế, rất hiếm khi bạn gặp một website **không có bất kỳ cơ chế bảo vệ nào** chống lại tấn công tải tệp (như ví dụ trong lab trước). Tuy nhiên, việc tồn tại các lớp phòng thủ **không đồng nghĩa với việc chúng đủ mạnh**.

Trong nhiều trường hợp, kẻ tấn công vẫn có thể **khai thác lỗ hổng trong cơ chế kiểm tra (validation flaws)** để **tải lên web shell**, từ đó đạt được **Remote Code Execution (RCE)** trên máy chủ.

👉 Nói cách khác, **các biện pháp kiểm soát tải tệp thường dễ bị bypass** nếu chỉ dựa vào những kỹ thuật kiểm tra không chắc chắn (ví dụ: chỉ dựa vào phần mở rộng tệp, MIME type, hoặc lọc blacklist).

---

## **Flawed file type validation**

---

Khi gửi form HTML, trình duyệt thường gửi dữ liệu trong một **POST request** với `Content-Type: application/x-www-form-urlencoded`.

Cách này phù hợp để truyền dữ liệu văn bản đơn giản, chẳng hạn như tên hoặc địa chỉ.

Tuy nhiên, kiểu content type này **không thích hợp** khi truyền một lượng lớn dữ liệu nhị phân (binary data), chẳng hạn như toàn bộ file ảnh hoặc tài liệu PDF.

Trong các trường hợp này, **`Content-Type: multipart/form-data`** sẽ được sử dụng thay thế.

👉 Đây chính là nền tảng để nhiều website áp dụng kiểm tra loại tệp (file type validation). Nhưng nếu validation này bị triển khai sai hoặc có thể bị giả mạo (MIME spoofing), thì kẻ tấn công có thể **lách qua kiểm tra** và tải lên file độc hại.

Giả sử có một form gồm các trường: tải lên một hình ảnh, nhập mô tả cho nó, và nhập username. Khi submit form này, request có thể trông như sau:

```sql
POST /images HTTP/1.1
    Host: normal-website.com
    Content-Length: 12345
    Content-Type: multipart/form-data; boundary=---------------------------012345678901234567890123456

    ---------------------------012345678901234567890123456
    Content-Disposition: form-data; name="image"; filename="example.jpg"
    Content-Type: image/jpeg

    [...binary content of example.jpg...]

    ---------------------------012345678901234567890123456
    Content-Disposition: form-data; name="description"

    This is an interesting description of my image.

    ---------------------------012345678901234567890123456
    Content-Disposition: form-data; name="username"

    wiener
    ---------------------------012345678901234567890123456--
```

**Phân tích**

- **Message body** của request được chia thành **nhiều phần (multipart)**, mỗi phần tương ứng với một input trong form.
- Mỗi phần đều có một **`Content-Disposition` header** mô tả thông tin cơ bản về input liên quan (ví dụ: tên trường, tên file).
- Với các input kiểu tệp (file upload), từng phần cũng có thể chứa thêm **`Content-Type` header**, cho biết **MIME type** của dữ liệu được submit.

👉 Đây chính là điểm quan trọng: **nhiều server dựa vào `Content-Type` trong từng phần để xác định loại file**. Nếu validation chỉ dựa vào thông tin này, kẻ tấn công có thể **giả mạo (MIME spoofing)** bằng cách chỉnh sửa request qua công cụ như **Burp Proxy/Repeater**, khiến server tin rằng tệp độc hại là file hợp lệ (ví dụ: PHP script nhưng được gắn `Content-Type: image/jpeg`).

**Xác thực file upload dựa vào MIME type (MIME type validation)**

Một cách mà các website thường áp dụng để kiểm tra tệp tải lên là **so sánh `Content-Type` của từng input** với MIME type được mong đợi.

Ví dụ: nếu server chỉ cho phép tải lên ảnh, thì nó sẽ chấp nhận các loại MIME như:

- `image/jpeg`
- `image/png`

**Vấn đề**

Rủi ro xuất hiện khi server **tin tưởng tuyệt đối** vào giá trị của header `Content-Type`.

- Nếu **không có bước kiểm tra bổ sung** để xác nhận rằng **nội dung thực sự** của file đúng với MIME type khai báo, thì cơ chế phòng thủ này có thể bị **bypass rất dễ dàng**.
- Kẻ tấn công chỉ cần dùng công cụ như **Burp Repeater** để thay đổi giá trị `Content-Type` sang một loại hợp lệ (ví dụ: `image/jpeg`), trong khi thực tế file lại là **PHP script hoặc payload độc hại**.

👉 Điều này dẫn đến việc **cơ chế xác thực loại tệp trở nên vô hiệu**, và file nguy hiểm vẫn có thể được tải lên thành công.

---

# OS Command Injection

---

**OS Command Injection** (còn gọi là **Shell Injection**) là một lỗ hổng bảo mật cho phép kẻ tấn công **thực thi các lệnh của hệ điều hành (OS commands)** trên máy chủ đang chạy ứng dụng. Điều này thường dẫn đến việc **toàn bộ ứng dụng và dữ liệu bị kiểm soát**.

Trong nhiều trường hợp, kẻ tấn công có thể lợi dụng lỗ hổng **OS Command Injection** để:

- **Xâm phạm các thành phần khác** trong hạ tầng máy chủ.
- Khai thác **các mối quan hệ tin cậy (trust relationships)** giữa các hệ thống.
- **Mở rộng tấn công (pivot)** sang những hệ thống nội bộ khác trong tổ chức.

👉 Đây là một trong những loại lỗ hổng **nguy hiểm nhất**, thường dẫn đến **toàn quyền kiểm soát hệ thống (full system compromise)**.

Sau khi bạn xác định được lỗ hổng OS command injection (chèn lệnh hệ điều hành), việc thực thi một số lệnh ban đầu để thu thập thông tin về hệ thống là rất hữu ích. Dưới đây là tóm tắt một số lệnh hữu ích trên nền tảng Linux và Windows:

| **Purpose of command** | **Linux** | **Windows** |
| --- | --- | --- |
| Name of current user | `whoami` | `whoami` |
| Operating system | `uname -a` | `ver` |
| Network configuration | `ifconfig` | `ipconfig /all` |
| Network connections | `netstat -an` | `netstat -an` |
| Running processes | `ps -ef` | `tasklist` |

👉 Những lệnh này giúp kẻ tấn công **dò quét môi trường**, xác định **quyền hạn hiện có**, và từ đó tìm cách leo thang đặc quyền (privilege escalation) hoặc pivot sang các hệ thống khác.

Ví dụ sau mô tả một ứng dụng mua sắm cho phép người dùng kiểm tra tình trạng hàng tồn của một sản phẩm tại một cửa hàng cụ thể. Thông tin này được truy cập thông qua URL:

```
https://insecure-website.com/stockStatus?productID=381&storeID=29
```

Để lấy dữ liệu về hàng tồn kho, ứng dụng cần truy vấn đến nhiều hệ thống **legacy**. Vì lý do lịch sử, chức năng này được triển khai bằng cách gọi ra một **shell command**, trong đó `productID` và `storeID` được truyền làm tham số:

```
stockreport.pl 381 29
```

Lệnh trên sẽ xuất ra tình trạng hàng tồn của sản phẩm được chỉ định, và kết quả này sẽ được trả về cho người dùng.

👉 Chính vì cơ chế này, nếu dữ liệu đầu vào (productID hoặc storeID) không được **kiểm tra / lọc kỹ lưỡng**, kẻ tấn công có thể **chèn thêm OS command** để thực thi lệnh tùy ý trên server.

Ứng dụng trong ví dụ **không triển khai bất kỳ cơ chế phòng thủ nào** chống lại OS Command Injection, nên kẻ tấn công có thể gửi payload sau để thực thi lệnh tùy ý:

```
& echo aiwefwlguh &
```

Nếu payload này được chèn vào tham số `productID`, lệnh thực thi trên server sẽ trở thành:

```
stockreport.pl & echo aiwefwlguh & 29
```

Trong đó:

- Lệnh `echo` sẽ in ra chuỗi `aiwefwlguh`. Đây là cách phổ biến để **kiểm tra nhanh lỗ hổng Command Injection**.
- Ký tự `&` trong shell là **command separator**, cho phép tách nhiều lệnh để chạy liên tiếp.

**Kết quả trả về cho người dùng:**

```
Error - productID was not provided
aiwefwlguh
29: command not found
```

**Phân tích kết quả**

1. **Lệnh gốc `stockreport.pl`** được thực thi nhưng thiếu tham số hợp lệ ⇒ báo lỗi.
2. **Lệnh chèn `echo aiwefwlguh`** được thực thi thành công ⇒ chuỗi được in ra.
3. **Tham số gốc `29`** bị shell coi như một lệnh ⇒ báo lỗi `"command not found"`.

Việc đặt một command separator `&` **sau lệnh chèn** giúp **tách payload ra khỏi phần còn lại** của lệnh gốc. Điều này làm giảm nguy cơ các tham số hoặc câu lệnh tiếp theo **ngăn không cho lệnh chèn chạy thành công**.

👉 Đây là một kỹ thuật cơ bản nhưng rất hiệu quả để xác nhận và khai thác **OS Command Injection**.

---

# SQLi

---

SQL injection (SQLi) là một lỗ hổng bảo mật web cho phép kẻ tấn công can thiệp vào các truy vấn mà một ứng dụng gửi tới cơ sở dữ liệu. Điều này có thể cho phép kẻ tấn công xem những dữ liệu mà bình thường họ không thể lấy được. Dữ liệu này có thể bao gồm dữ liệu thuộc về người dùng khác, hoặc bất kỳ dữ liệu nào mà ứng dụng có quyền truy cập.

Trong nhiều trường hợp, kẻ tấn công có thể sửa đổi hoặc xóa dữ liệu này, gây ra những thay đổi lâu dài đối với nội dung hoặc hành vi của ứng dụng.

Trong một số tình huống, kẻ tấn công có thể leo thang tấn công SQL injection để chiếm quyền điều khiển máy chủ nền tảng hoặc các hạ tầng back-end khác. Nó cũng có thể cho phép họ thực hiện các cuộc tấn công từ chối dịch vụ (DoS).

Bạn có thể phát hiện SQL injection thủ công bằng cách sử dụng một tập hợp các bài kiểm thử có hệ thống trên mọi điểm nhập liệu (entry point) trong ứng dụng. Để làm điều này, bạn thường sẽ gửi:

- Ký tự dấu nháy đơn `'` và quan sát các lỗi hoặc các bất thường khác.
- Một số cú pháp SQL đặc thù có thể đánh giá về giá trị gốc (original value) của điểm nhập liệu, và một giá trị khác biệt, rồi quan sát sự khác nhau có hệ thống trong phản hồi của ứng dụng.
- Các điều kiện Boolean như `OR 1=1` và `OR 1=2`, và quan sát sự khác biệt trong phản hồi của ứng dụng.
- Các payload được thiết kế để kích hoạt độ trễ thời gian (time delay) khi được thực thi trong một truy vấn SQL, rồi so sánh sự khác nhau về thời gian phản hồi.
- Các payload **OAST** (Out-of-band Application Security Testing) được thiết kế để kích hoạt một tương tác mạng ngoài băng (out-of-band network interaction) khi được thực thi trong truy vấn SQL, và giám sát các tương tác phát sinh.

Ngoài ra, bạn cũng có thể phát hiện phần lớn lỗ hổng SQL injection một cách nhanh chóng và đáng tin cậy bằng cách sử dụng **Burp Scanner**.

Ứng dụng không triển khai bất kỳ cơ chế phòng thủ nào chống lại SQL injection. Điều này có nghĩa là kẻ tấn công có thể tạo ra cuộc tấn công như sau, ví dụ:

```
https://insecure-website.com/products?category=Gifts'--
```

Điều này dẫn đến truy vấn SQL:

```sql
SELECT * FROM products WHERE category = 'Gifts'--' AND released = 1
```

Điểm mấu chốt: hãy chú ý rằng `--` là ký hiệu chú thích trong SQL. Điều này có nghĩa là phần còn lại của câu truy vấn sẽ bị coi như là comment, và thực chất bị loại bỏ. Trong ví dụ này, điều đó đồng nghĩa với việc truy vấn không còn bao gồm điều kiện `AND released = 1`. Kết quả là tất cả các sản phẩm đều được hiển thị, kể cả những sản phẩm chưa phát hành.

Bạn có thể sử dụng một cuộc tấn công tương tự để khiến ứng dụng hiển thị toàn bộ sản phẩm trong bất kỳ danh mục nào, kể cả những danh mục mà người dùng không biết:

```
https://insecure-website.com/products?category=Gifts'+OR+1=1--
```

Điều này dẫn đến truy vấn SQL:

```sql
SELECT * FROM products WHERE category = 'Gifts' OR 1=1--' AND released = 1
```

Câu truy vấn đã bị chỉnh sửa để trả về tất cả các mặt hàng mà **hoặc** category là `Gifts`, **hoặc** điều kiện `1=1`. Vì `1=1` luôn đúng, nên truy vấn trả về toàn bộ mặt hàng.

> ⚠️ **Cảnh báo**
> 
> 
> Hãy cẩn thận khi chèn điều kiện `OR 1=1` vào một truy vấn SQL. Ngay cả khi nó có vẻ vô hại trong ngữ cảnh bạn đang chèn, thì cũng rất thường gặp trường hợp ứng dụng sử dụng dữ liệu từ một request trong nhiều truy vấn khác nhau. Nếu điều kiện này đi vào một câu lệnh `UPDATE` hoặc `DELETE` chẳng hạn, nó có thể dẫn đến việc mất dữ liệu ngoài ý muốn.
> 

Hãy tưởng tượng một ứng dụng cho phép người dùng đăng nhập bằng **tên người dùng (username)** và **mật khẩu (password)**.

Nếu một người dùng nhập username là `wiener` và password là `bluecheese`, thì ứng dụng sẽ kiểm tra thông tin xác thực bằng cách thực thi câu truy vấn SQL sau:

```sql
SELECT * FROM users WHERE username = 'wiener' AND password = 'bluecheese'
```

Nếu truy vấn trả về thông tin của một người dùng, thì quá trình đăng nhập thành công. Ngược lại, nếu không có kết quả, việc đăng nhập sẽ bị từ chối.

Trong trường hợp này, kẻ tấn công có thể đăng nhập với tư cách bất kỳ người dùng nào **mà không cần biết mật khẩu**.

Họ có thể làm điều này bằng cách sử dụng chuỗi comment trong SQL (`--`) để loại bỏ phần kiểm tra mật khẩu khỏi mệnh đề `WHERE` của truy vấn.

Ví dụ: kẻ tấn công gửi username là:

```
administrator'--
```

và password để trống. Khi đó, câu truy vấn SQL được thực thi sẽ là:

```sql
SELECT * FROM users WHERE username = 'administrator'--' AND password = ''
```

Do `--` biến phần còn lại của câu lệnh thành comment, nên điều kiện kiểm tra password (`AND password = ''`) bị bỏ qua.

Kết quả là truy vấn chỉ cần thỏa mãn `username = 'administrator'`, và ứng dụng sẽ trả về thông tin của user `administrator`.

Từ đó, kẻ tấn công đăng nhập thành công với quyền của tài khoản **administrator** mà không cần biết mật khẩu.
