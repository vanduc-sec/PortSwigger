# Clickjacking (UI redressing)

Trạng thái: Chưa bắt đầu
subject: Client-side

# Clickjacking là gì?

---

Clickjacking là một dạng tấn công dựa trên giao diện, trong đó người dùng bị đánh lừa để nhấp vào nội dung có thể thao tác trên một website bị ẩn bằng cách nhấp vào một nội dung khác trên một website mồi nhử. Xem ví dụ sau:

Một người dùng web truy cập vào một website mồi nhử (có thể là một liên kết được cung cấp qua email) và nhấp vào một nút để trúng thưởng. Không hề hay biết, họ đã bị kẻ tấn công lừa nhấp vào một nút ẩn khác, dẫn đến việc thanh toán từ một tài khoản trên một trang web khác. Đây là một ví dụ về tấn công clickjacking. Kỹ thuật này phụ thuộc vào việc chèn một trang web (hoặc nhiều trang) vô hình nhưng có thể thao tác, chứa một nút hoặc liên kết ẩn, chẳng hạn nằm trong một iframe. Iframe này được chồng lên trên nội dung trang mồi nhử mà người dùng dự kiến sẽ thấy. Cuộc tấn công này khác với tấn công CSRF ở chỗ nó yêu cầu người dùng thực hiện một hành động như nhấp nút, trong khi tấn công CSRF dựa vào việc giả mạo toàn bộ yêu cầu mà không cần sự biết hay tương tác của người dùng.

![image.png](Clickjacking%20(UI%20redressing)/image.png)

Biện pháp bảo vệ chống tấn công CSRF thường được cung cấp bằng việc sử dụng CSRF token: một số/nonce đặc thù theo phiên và dùng một lần. Các cuộc tấn công clickjacking không được giảm thiểu bởi CSRF token, vì một phiên đích được thiết lập với nội dung được tải từ website hợp lệ và mọi yêu cầu đều diễn ra “cùng miền”. CSRF token được đặt vào các yêu cầu và gửi đến máy chủ như một phần của một phiên hoạt động bình thường. Điểm khác biệt so với một phiên người dùng bình thường là toàn bộ quá trình diễn ra bên trong một iframe ẩn.

---

# Xây dựng cuộc tấn công

---

Các cuộc tấn công clickjacking sử dụng CSS để tạo và thao tác các lớp (layers). Kẻ tấn công nhúng website mục tiêu dưới dạng một lớp iframe chồng lên trên website mồi nhử. Ví dụ sử dụng thẻ `style` và các tham số như sau:

```
<head>
	<style>
		#target_website {
			position:relative;
			width:128px;
			height:128px;
			opacity:0.00001;
			z-index:2;
			}
		#decoy_website {
			position:absolute;
			width:300px;
			height:400px;
			z-index:1;
			}
	</style>
</head>
...
<body>
	<div id="decoy_website">
	...decoy web content here...
	</div>
	<iframe id="target_website" src="https://vulnerable-website.com">
	</iframe>
</body>
```

IFrame của website mục tiêu được định vị trong trình duyệt để có sự chồng khít chính xác giữa hành động mục tiêu và nội dung của website mồi nhử bằng cách dùng các giá trị vị trí, chiều rộng và chiều cao thích hợp. Các giá trị vị trí tuyệt đối (absolute) và tương đối (relative) được sử dụng để bảo đảm website mục tiêu chồng khít website mồi nhử một cách chính xác bất kể kích thước màn hình, loại trình duyệt và nền tảng. Thuộc tính `z-index` xác định thứ tự xếp chồng của các lớp iframe và website. Giá trị `opacity` được đặt là 0.0 (hoặc gần 0.0) để nội dung iframe trong suốt đối với người dùng. Cơ chế bảo vệ clickjacking của trình duyệt có thể áp dụng phát hiện độ trong suốt của iframe dựa trên ngưỡng (ví dụ, Chrome phiên bản 76 có hành vi này còn Firefox thì không). Kẻ tấn công chọn các giá trị `opacity` sao cho đạt được hiệu ứng mong muốn mà không kích hoạt các hành vi bảo vệ.

[Lab: Basic clickjacking with CSRF token protection | Web Security Academy](https://portswigger.net/web-security/clickjacking/lab-basic-csrf-protected)

---

## Clickbandit

---

Mặc dù bạn có thể tự tạo một bằng chứng khái niệm (proof of concept) cho clickjacking như mô tả ở trên, nhưng trên thực tế điều này khá tẻ nhạt và tốn thời gian. Khi kiểm thử clickjacking ngoài thực tế, chúng tôi khuyến nghị thay vào đó sử dụng công cụ Clickbandit của Burp. Công cụ này cho phép bạn dùng trình duyệt để thực hiện các thao tác mong muốn trên trang có thể đóng khung (frameable), rồi tạo ra một tệp HTML chứa lớp phủ clickjacking phù hợp. Bạn có thể dùng nó để tạo một PoC tương tác chỉ trong vài giây mà không cần viết bất kỳ dòng HTML hay CSS nào.

---

# **Clickjacking with prefilled form input**

---

Một số website yêu cầu hoàn thành và gửi biểu mẫu cho phép điền sẵn (prepopulate) các trường nhập bằng tham số GET trước khi gửi. Các website khác có thể yêu cầu phải có văn bản trước khi gửi biểu mẫu. Vì các giá trị GET là một phần của URL nên URL mục tiêu có thể được sửa đổi để đưa vào các giá trị do kẻ tấn công lựa chọn, và nút “submit” trong suốt được chồng lên (overlay) trang mồi nhử như trong ví dụ clickjacking cơ bản.

[Lab: Clickjacking with form input data prefilled from a URL parameter | Web Security Academy](https://portswigger.net/web-security/clickjacking/lab-prefilled-form-input)

---

# **Frame busting scripts**

---

Các cuộc tấn công clickjacking có thể xảy ra bất cứ khi nào website có thể bị đóng khung (framed). Do đó, các kỹ thuật phòng ngừa dựa trên việc hạn chế khả năng đóng khung của website. Một biện pháp bảo vệ phía client phổ biến được thực thi qua trình duyệt là sử dụng các script “frame busting” hoặc “frame breaking”. Những script này có thể được triển khai thông qua các tiện ích bổ sung hoặc phần mở rộng JavaScript của trình duyệt như NoScript. Các script thường được thiết kế để thực hiện một phần hoặc toàn bộ các hành vi sau:

- kiểm tra và cưỡng chế rằng cửa sổ ứng dụng hiện tại là cửa sổ chính (main) hoặc cửa sổ trên cùng (top),
- làm cho tất cả các frame hiển thị,
- ngăn việc nhấp chuột vào các frame vô hình,
- chặn và cảnh báo cho người dùng về các cuộc tấn công clickjacking tiềm ẩn.

Các kỹ thuật frame busting thường phụ thuộc vào trình duyệt và nền tảng, và do tính linh hoạt của HTML nên chúng thường có thể bị kẻ tấn công vượt qua. Vì frame buster là JavaScript nên các thiết lập bảo mật của trình duyệt có thể ngăn chúng hoạt động, hoặc thậm chí trình duyệt có thể không hỗ trợ JavaScript. Một cách lách hiệu quả của kẻ tấn công đối với frame busters là sử dụng thuộc tính `sandbox` của iframe trong HTML5. Khi thuộc tính này được đặt với các giá trị `allow-forms` hoặc `allow-scripts` và bỏ giá trị `allow-top-navigation`, script frame buster có thể bị vô hiệu hóa vì iframe không thể kiểm tra liệu nó có phải là cửa sổ top hay không:

```
<iframe id="victim_website" src="https://victim-website.com" sandbox="allow-forms"></iframe>
```

Cả `allow-forms` và `allow-scripts` đều cho phép các hành động được chỉ định bên trong iframe nhưng điều hướng cấp cao nhất (top-level navigation) bị vô hiệu. Điều này ức chế các hành vi frame busting đồng thời vẫn cho phép chức năng bên trong website mục tiêu.

[Lab: Clickjacking with a frame buster script | Web Security Academy](https://portswigger.net/web-security/clickjacking/lab-frame-buster-script)

---

# **Combining clickjacking with a DOM XSS attack**

---

Cho đến giờ, chúng ta đã xem clickjacking như một cuộc tấn công độc lập. Trong lịch sử, clickjacking từng được dùng để thực hiện các hành vi như tăng “lượt thích” trên một trang Facebook. Tuy nhiên, mức độ nguy hiểm thực sự của clickjacking bộc lộ khi nó được dùng như kênh mang tải cho một cuộc tấn công khác, chẳng hạn DOM XSS. Việc triển khai cuộc tấn công kết hợp này tương đối đơn giản, giả định rằng kẻ tấn công đã xác định được lỗ hổng XSS trước đó. Khai thác XSS sau đó được kết hợp vào URL mục tiêu của iframe, để khi người dùng nhấp vào nút hoặc liên kết thì sẽ dẫn đến việc thực thi tấn công DOM XSS.

[Lab: Exploiting clickjacking vulnerability to trigger DOM-based XSS | Web Security Academy](https://portswigger.net/web-security/clickjacking/lab-exploiting-to-trigger-dom-based-xss)

---

# **Multistep clickjacking**

---

Việc kẻ tấn công thao túng các đầu vào của website mục tiêu có thể đòi hỏi nhiều thao tác. Ví dụ, kẻ tấn công có thể muốn lừa người dùng mua hàng trên một website bán lẻ, vì vậy cần phải thêm sản phẩm vào giỏ trước khi đặt hàng. Những thao tác này có thể được triển khai bằng cách sử dụng nhiều thẻ `div` hoặc `iframe`. Các cuộc tấn công như vậy đòi hỏi mức độ chính xác và sự cẩn trọng đáng kể từ phía kẻ tấn công nếu muốn vừa hiệu quả vừa khó bị phát hiện.

[Lab: Multistep clickjacking | Web Security Academy](https://portswigger.net/web-security/clickjacking/lab-multistep)

---

# Bảo mật

---

Chúng ta đã bàn về một cơ chế phòng ngừa phổ biến ở phía trình duyệt, cụ thể là các script phá khung (frame busting). Tuy nhiên, chúng ta cũng thấy rằng kẻ tấn công thường có thể dễ dàng lách các biện pháp bảo vệ này. Do đó, các giao thức do máy chủ chi phối đã được đưa ra nhằm hạn chế việc sử dụng iframe của trình duyệt và giảm thiểu clickjacking.

Clickjacking là một hành vi xảy ra ở phía trình duyệt và mức độ thành công của nó phụ thuộc vào chức năng của trình duyệt cũng như mức độ tuân thủ các tiêu chuẩn web hiện hành và thực tiễn tốt. Bảo vệ phía máy chủ đối với clickjacking được thực hiện bằng cách xác định và truyền đạt các ràng buộc về việc sử dụng các thành phần như iframe. Tuy nhiên, việc triển khai bảo vệ phụ thuộc vào việc trình duyệt tuân thủ và thực thi các ràng buộc này. Hai cơ chế bảo vệ clickjacking phía máy chủ là X-Frame-Options và Content Security Policy.

---

## **X-Frame-Options**

---

X-Frame-Options ban đầu được giới thiệu như một HTTP response header không chính thức trong Internet Explorer 8 và nhanh chóng được các trình duyệt khác áp dụng. Header này cho phép chủ sở hữu website kiểm soát việc sử dụng iframe hoặc object, nhờ đó có thể cấm đưa một trang web vào trong khung bằng chỉ thị `deny`:

```
X-Frame-Options: deny
```

Ngoài ra, có thể hạn chế việc đóng khung về cùng origin với website bằng chỉ thị `sameorigin`:

```
X-Frame-Options: sameorigin
```

hoặc về một website được nêu đích danh bằng chỉ thị `allow-from`:

```
X-Frame-Options: allow-from https://normal-website.com
```

X-Frame-Options không được triển khai thống nhất giữa các trình duyệt (ví dụ, chỉ thị `allow-from` không được hỗ trợ trong Chrome phiên bản 76 hoặc Safari 12). Tuy nhiên, khi được áp dụng đúng cách cùng với Content Security Policy như một phần của chiến lược phòng thủ nhiều lớp, nó có thể cung cấp sự bảo vệ hiệu quả.

---

## **Content Security Policy (CSP)**

---

**Content Security Policy (CSP)** là một cơ chế phát hiện và phòng ngừa, cung cấp biện pháp giảm thiểu đối với các cuộc tấn công như XSS và clickjacking. CSP thường được triển khai trên máy chủ web dưới dạng một header phản hồi có cấu trúc:

```
Content-Security-Policy: policy
```

trong đó *policy* là một chuỗi các chỉ thị chính sách (policy directives) được phân tách bằng dấu chấm phẩy. CSP cung cấp cho trình duyệt khách thông tin về các nguồn tài nguyên web được phép, để trình duyệt có thể áp dụng vào việc phát hiện và chặn các hành vi độc hại.

Biện pháp bảo vệ clickjacking được khuyến nghị là đưa chỉ thị `frame-ancestors` vào Content Security Policy của ứng dụng. Chỉ thị `frame-ancestors 'none'` có hành vi tương tự với chỉ thị `deny` của X-Frame-Options. Chỉ thị `frame-ancestors 'self'` về tổng thể tương đương với chỉ thị `sameorigin` của X-Frame-Options. CSP sau đây chỉ cho phép frame từ cùng miền:

```
Content-Security-Policy: frame-ancestors 'self';
```

Ngoài ra, việc đóng khung có thể bị giới hạn cho các site được nêu đích danh:

```
Content-Security-Policy: frame-ancestors normal-website.com;
```

Để hiệu quả trước clickjacking và XSS, CSP cần được xây dựng, triển khai và kiểm thử cẩn trọng, và nên được sử dụng như một phần của chiến lược phòng thủ nhiều lớp.
