# Authentication vulnerabilities

Trạng thái: Chưa bắt đầu
subject: Server-side

# Xác thực là gì?

---

Xác thực (Authentication) là quá trình **xác minh danh tính** của một người dùng hoặc client. Các website có thể bị truy cập bởi bất kỳ ai kết nối Internet. Điều này khiến cho các cơ chế xác thực mạnh mẽ trở thành một phần **thiết yếu trong bảo mật web**.

Có ba loại xác thực chính:

1. **Something you know (thứ bạn biết)**: ví dụ như mật khẩu hoặc câu trả lời cho câu hỏi bảo mật. Đây thường được gọi là **yếu tố tri thức (knowledge factors)**.
2. **Something you have (thứ bạn sở hữu)**: một vật thể vật lý như điện thoại di động hoặc token bảo mật. Đây thường được gọi là **yếu tố sở hữu (possession factors)**.
3. **Something you are or do (thứ bạn là hoặc làm)**: ví dụ như sinh trắc học (vân tay, khuôn mặt) hoặc các mẫu hành vi. Đây thường được gọi là **yếu tố nội tại (inherence factors)**.

Các cơ chế xác thực dựa vào nhiều công nghệ khác nhau để xác minh một hoặc nhiều yếu tố trong số này.

---

# Xác thực - Phân quyền

---

- **Authentication (xác thực)** là quá trình **xác minh rằng một người dùng đúng là người mà họ khai báo**.
- **Authorization (phân quyền/ủy quyền)** là quá trình **xác minh xem người dùng có được phép thực hiện hành động nào đó hay không**.

Ví dụ:

- **Authentication** sẽ xác định xem người đang cố gắng đăng nhập vào website với tên người dùng `Carlos123` có thực sự là chủ tài khoản đó hay không.
- Sau khi `Carlos123` đã được xác thực, **authorization** sẽ xác định các quyền hạn của họ, chẳng hạn như có được phép truy cập thông tin cá nhân của người dùng khác hay xóa tài khoản của người khác hay không.

---

# Nguyên nhân phát sinh

---

Hầu hết các lỗ hổng trong cơ chế xác thực xuất hiện theo **hai cách chính**:

1. **Cơ chế xác thực yếu** vì không bảo vệ đầy đủ trước các cuộc tấn công brute-force.
2. **Lỗi logic hoặc lập trình kém** trong quá trình triển khai cho phép kẻ tấn công **bỏ qua hoàn toàn cơ chế xác thực**. Trường hợp này đôi khi được gọi là **broken authentication (xác thực bị phá vỡ)**.

Trong nhiều khía cạnh của phát triển web, các lỗi logic có thể khiến website hoạt động không như mong đợi — đôi khi không phải là vấn đề bảo mật. Tuy nhiên, vì **xác thực có vai trò tối quan trọng trong bảo mật**, nên các lỗi logic trong xác thực gần như chắc chắn sẽ khiến website **dễ bị khai thác bảo mật**.

---

# Hậu quả

---

Hậu quả của các lỗ hổng xác thực có thể **rất nghiêm trọng**.

- Nếu kẻ tấn công **bỏ qua được bước xác thực** hoặc **brute-force thành công** để truy cập vào tài khoản của người dùng khác, chúng sẽ có toàn quyền với **dữ liệu và chức năng** mà tài khoản bị chiếm đoạt sở hữu.
- Nếu kẻ tấn công chiếm được tài khoản có **đặc quyền cao** (ví dụ: tài khoản quản trị hệ thống), chúng có thể **kiểm soát hoàn toàn ứng dụng** và thậm chí có khả năng truy cập vào **hạ tầng nội bộ**.
- Ngay cả khi chiếm đoạt được một tài khoản **có đặc quyền thấp**, kẻ tấn công vẫn có thể truy cập vào những dữ liệu mà bình thường chúng **không được phép truy cập**, chẳng hạn như các thông tin kinh doanh nhạy cảm.
- Ngay cả khi tài khoản đó **không có quyền truy cập dữ liệu nhạy cảm**, nó vẫn có thể cho phép kẻ tấn công **tiếp cận thêm một số trang khác**, từ đó mở rộng **bề mặt tấn công**.
- Trong nhiều trường hợp, các cuộc tấn công có mức độ nghiêm trọng cao **không thể thực hiện từ những trang công khai**, nhưng lại **có thể khai thác được từ các trang nội bộ**.

---

# Vulnerabilities

---

## **Password-based login**

---

Đối với các website sử dụng cơ chế đăng nhập dựa trên mật khẩu, người dùng sẽ **tự đăng ký tài khoản** hoặc được **quản trị viên cấp tài khoản**. Mỗi tài khoản được gắn với một **tên người dùng (username)** duy nhất và một **mật khẩu bí mật (password)**, mà người dùng sẽ nhập vào form đăng nhập để tiến hành xác thực.

Trong tình huống này, việc người dùng **biết mật khẩu bí mật** được coi là bằng chứng đủ để xác minh danh tính. Điều này đồng nghĩa với việc **bảo mật của website sẽ bị ảnh hưởng** nếu kẻ tấn công có thể **lấy cắp hoặc đoán ra thông tin đăng nhập** của người dùng khác.

Điều này có thể đạt được theo nhiều cách khác nhau. Các phần tiếp theo sẽ trình bày cách kẻ tấn công sử dụng **brute-force attacks** cũng như một số **lỗi trong cơ chế bảo vệ chống brute-force**. Bạn cũng sẽ tìm hiểu về các lỗ hổng trong **HTTP Basic Authentication**.

---

### Brute-force attacks

---

**Brute-force attack** là khi kẻ tấn công sử dụng phương pháp **thử và sai (trial and error)** để đoán thông tin đăng nhập hợp lệ của người dùng. Các cuộc tấn công này thường được **tự động hóa bằng wordlist** chứa danh sách tên người dùng và mật khẩu. Khi được tự động hóa, đặc biệt là bằng các công cụ chuyên dụng, kẻ tấn công có thể thực hiện một lượng **khổng lồ các yêu cầu đăng nhập với tốc độ rất cao**.

Brute-force không phải lúc nào cũng chỉ là việc đoán ngẫu nhiên tên đăng nhập và mật khẩu. Bằng cách sử dụng **logic cơ bản** hoặc các **thông tin công khai sẵn có**, kẻ tấn công có thể **tinh chỉnh brute-force** để đưa ra các phỏng đoán hợp lý hơn, từ đó **tăng đáng kể hiệu quả** của tấn công.

Những website chỉ dựa vào cơ chế đăng nhập bằng mật khẩu như **phương thức xác thực duy nhất**, nhưng lại không triển khai biện pháp chống brute-force đủ mạnh, sẽ trở nên **rất dễ bị tấn công**.

Tên người dùng thường **dễ đoán** nếu chúng tuân theo một **mẫu nhận diện rõ ràng**, chẳng hạn như địa chỉ email. Ví dụ, định dạng đăng nhập doanh nghiệp phổ biến là:

```
firstname.lastname@somecompany.com
```

Tuy nhiên, ngay cả khi không có mẫu hiển nhiên, đôi khi các tài khoản có **đặc quyền cao** cũng được tạo với tên người dùng **dễ đoán**, như `admin` hoặc `administrator`.

Trong quá trình kiểm thử (auditing), cần kiểm tra xem website có **vô tình tiết lộ tên người dùng tiềm năng** hay không. Ví dụ:

- Bạn có thể truy cập profile người dùng mà **không cần đăng nhập** không?
    
    → Ngay cả khi nội dung profile bị ẩn, tên hiển thị trong profile đôi khi lại **trùng với username đăng nhập**.
    
- Kiểm tra phản hồi HTTP để xem có **email bị lộ** hay không. Thỉnh thoảng, phản hồi chứa email của người dùng có đặc quyền cao, như **administrator** hoặc **IT support**.

Mật khẩu cũng có thể bị **brute-force**, với mức độ khó khăn phụ thuộc vào **độ mạnh (strength)** của mật khẩu. Nhiều website áp dụng **chính sách mật khẩu (password policy)** buộc người dùng phải tạo mật khẩu có **entropy cao**, tức là về mặt lý thuyết sẽ khó bị crack chỉ bằng brute-force.

Thông thường, chính sách này yêu cầu mật khẩu phải có:

- **Số ký tự tối thiểu**
- **Kết hợp chữ thường và chữ hoa**
- **Ít nhất một ký tự đặc biệt**

Tuy mật khẩu có entropy cao rất khó để máy tính thuần túy crack, nhưng kẻ tấn công có thể khai thác **hành vi con người** – những điểm yếu mà người dùng vô tình đưa vào hệ thống.

Thay vì tạo ra một mật khẩu mạnh với **chuỗi ký tự ngẫu nhiên**, người dùng thường chọn một mật khẩu **dễ nhớ**, rồi tìm cách **biến tấu nó** để đáp ứng chính sách mật khẩu. Ví dụ: nếu `mypassword` không được chấp nhận, họ có thể thử:

- `Mypassword1!`
- `Myp4$$w0rd`

Trong các trường hợp chính sách yêu cầu người dùng **thường xuyên thay đổi mật khẩu**, họ cũng có xu hướng chỉ thay đổi **nhẹ và dễ đoán** so với mật khẩu cũ. Ví dụ:

- `Mypassword1!` → `Mypassword1?`
- `Mypassword1!` → `Mypassword2!`

Chính nhờ những **mẫu mật khẩu dự đoán được** này, các cuộc tấn công brute-force có thể được **tinh chỉnh tinh vi hơn nhiều**, từ đó trở nên **hiệu quả hơn nhiều so với việc thử toàn bộ mọi tổ hợp ký tự**.

---

### Username enumeration

---

**Username enumeration** xảy ra khi kẻ tấn công có thể quan sát sự **thay đổi trong hành vi của website** để xác định xem một username nào đó có hợp lệ hay không.

Việc liệt kê username thường xảy ra ở:

- **Trang đăng nhập (login page):** ví dụ khi bạn nhập **username hợp lệ** nhưng **mật khẩu sai**, thông báo lỗi sẽ khác so với khi nhập username không tồn tại.
- **Form đăng ký (registration form):** khi bạn nhập vào một username đã được sử dụng, hệ thống sẽ báo là tên đó đã tồn tại.

Điều này giúp kẻ tấn công **giảm đáng kể thời gian và công sức brute-force đăng nhập**, vì chúng có thể nhanh chóng tạo một **danh sách rút gọn các username hợp lệ**.

Khi tiến hành brute-force trên trang đăng nhập, bạn cần chú ý đặc biệt đến **những khác biệt** sau:

- **Mã trạng thái (Status codes):** Trong quá trình brute-force, hầu hết các thử sai sẽ trả về cùng một HTTP status code. Nếu một lần thử trả về mã trạng thái khác, đây là **dấu hiệu mạnh** cho thấy username đó đúng. Best practice là website nên luôn trả về cùng một status code bất kể kết quả, nhưng thực tế điều này không phải lúc nào cũng được tuân thủ.
- **Thông báo lỗi (Error messages):** Đôi khi thông báo lỗi khác nhau tùy thuộc vào việc **cả username và password đều sai**, hay chỉ **password sai**. Best practice là website nên hiển thị thông báo **giống nhau, dạng chung chung** cho cả hai trường hợp, nhưng lỗi gõ (typo) nhỏ có thể xuất hiện. Chỉ cần một ký tự khác biệt, dù không hiển thị rõ trên trang, cũng khiến hai thông báo trở nên khác nhau.
- **Thời gian phản hồi (Response times):** Nếu hầu hết các request có thời gian xử lý tương tự, bất kỳ request nào lệch đáng kể đều gợi ý rằng có điều gì khác đang diễn ra phía backend. Đây là một dấu hiệu khác cho thấy username được đoán có thể đúng. Ví dụ: một website có thể chỉ kiểm tra password nếu username hợp lệ. Bước kiểm tra thêm này có thể khiến thời gian phản hồi tăng lên một chút. Mặc dù khác biệt này thường rất nhỏ, nhưng kẻ tấn công có thể **làm rõ độ trễ** bằng cách nhập một mật khẩu quá dài khiến website mất nhiều thời gian xử lý hơn.

Một cuộc tấn công brute-force gần như chắc chắn sẽ bao gồm **rất nhiều lần thử sai** trước khi kẻ tấn công chiếm đoạt được tài khoản. Về mặt logic, cơ chế bảo vệ brute-force tập trung vào việc **làm cho quá trình tự động hóa trở nên khó khăn** và **làm chậm tốc độ thử đăng nhập** của kẻ tấn công.

Hai cách phổ biến nhất để ngăn chặn brute-force là:

1. **Khóa tài khoản** mà người dùng từ xa đang cố gắng truy cập nếu họ nhập sai quá nhiều lần.
2. **Chặn địa chỉ IP** của người dùng từ xa nếu họ thực hiện quá nhiều lần thử đăng nhập trong thời gian ngắn.

Cả hai cách tiếp cận đều mang lại mức độ bảo vệ nhất định, nhưng **không cách nào hoàn hảo**, đặc biệt nếu được triển khai với logic sai.

---

### IP locking

---

Ví dụ:

- Trong một số hệ thống, IP của bạn có thể bị chặn nếu đăng nhập sai quá nhiều lần.
- Tuy nhiên, bộ đếm số lần đăng nhập sai có thể **được reset nếu IP đó đăng nhập thành công**.

Điều này đồng nghĩa với việc kẻ tấn công chỉ cần **thỉnh thoảng đăng nhập vào tài khoản của chính chúng** trong quá trình brute-force để tránh chạm đến giới hạn.

Trong trường hợp này, chỉ cần **chèn thông tin đăng nhập hợp lệ của bản thân vào wordlist theo chu kỳ**, kẻ tấn công đã có thể **vô hiệu hóa gần như hoàn toàn biện pháp phòng thủ này**.

---

### Account locking

---

Một cách mà website thường sử dụng để ngăn chặn brute-force là **khóa tài khoản** nếu phát hiện các tiêu chí nghi ngờ, thường là khi có một số lần đăng nhập sai vượt quá giới hạn cho phép.

Tuy nhiên, cũng giống như lỗi đăng nhập thông thường, các phản hồi từ server báo rằng một tài khoản đã bị khóa có thể giúp kẻ tấn công **liệt kê (enumerate) username hợp lệ**.

Việc khóa tài khoản mang lại một mức độ bảo vệ nhất định đối với các cuộc brute-force **nhắm mục tiêu vào một tài khoản cụ thể**. Nhưng phương pháp này lại **không hiệu quả** trong việc ngăn chặn các cuộc brute-force mà kẻ tấn công chỉ đơn giản là muốn chiếm quyền truy cập vào **bất kỳ tài khoản nào**.

Ví dụ, kẻ tấn công có thể sử dụng phương pháp sau để **vượt qua biện pháp bảo vệ này**:

1. **Xây dựng danh sách username tiềm năng** có khả năng hợp lệ. Điều này có thể thực hiện bằng cách **username enumeration** hoặc đơn giản là dựa vào danh sách các username phổ biến.
2. **Chọn một danh sách mật khẩu rút gọn** (rất ít) mà bạn cho rằng ít nhất một người dùng sẽ sử dụng. Quan trọng là **số lượng mật khẩu chọn không được vượt quá số lần thử đăng nhập tối đa cho phép**. Ví dụ: nếu giới hạn là **3 lần thử**, bạn chỉ được chọn tối đa **3 mật khẩu**.
3. Sử dụng công cụ như **Burp Intruder**, thử lần lượt từng mật khẩu đã chọn với từng username trong danh sách.

Bằng cách này, bạn có thể **brute-force trên toàn bộ danh sách tài khoản** mà **không kích hoạt khóa tài khoản**. Bạn chỉ cần **một người dùng** sử dụng một trong ba mật khẩu đã chọn là đã có thể **chiếm đoạt được tài khoản**.

Khóa tài khoản cũng **không thể bảo vệ** trước các cuộc tấn công **credential stuffing**.

- **Credential stuffing** là hình thức sử dụng một **dictionary khổng lồ chứa các cặp username:password thật**, vốn bị đánh cắp trong các vụ rò rỉ dữ liệu.
- Kiểu tấn công này dựa vào thực tế rằng nhiều người có thói quen **tái sử dụng cùng một username và mật khẩu trên nhiều website khác nhau**. Do đó, luôn có khả năng một số thông tin đăng nhập trong dictionary sẽ hợp lệ trên website mục tiêu.

Cơ chế khóa tài khoản không ngăn chặn được credential stuffing, vì mỗi username trong dictionary chỉ bị thử **một lần duy nhất**.

Credential stuffing đặc biệt nguy hiểm vì đôi khi nó có thể giúp kẻ tấn công **chiếm đoạt nhiều tài khoản khác nhau chỉ bằng một cuộc tấn công tự động duy nhất**.

---

### Rate limiting

---

Một cách khác mà website áp dụng để ngăn chặn brute-force là **giới hạn tốc độ (rate limiting)**. Trong cơ chế này, nếu có quá nhiều yêu cầu đăng nhập được gửi trong một khoảng thời gian ngắn, địa chỉ IP của bạn sẽ bị **chặn**.

Thông thường, IP bị chặn chỉ có thể được mở khóa bằng một trong các cách sau:

- **Tự động** sau một khoảng thời gian nhất định.
- **Thủ công bởi quản trị viên**.
- **Thủ công bởi chính người dùng**, ví dụ sau khi vượt qua một CAPTCHA thành công.

Cơ chế rate limiting đôi khi được **ưu tiên hơn so với khóa tài khoản**, vì nó ít bị lợi dụng để **username enumeration** hoặc **tấn công từ chối dịch vụ (DoS)**. Tuy nhiên, nó **không hoàn toàn an toàn**. Như đã thấy trong một lab trước, có nhiều cách để kẻ tấn công **giả mạo hoặc thay đổi IP** nhằm vượt qua hạn chế này.

Ngoài ra, vì giới hạn dựa trên **tốc độ request HTTP gửi từ một IP**, kẻ tấn công đôi khi có thể **bỏ qua cơ chế phòng thủ này** nếu tìm ra cách thử nhiều mật khẩu trong **một request duy nhất**.

---

### HTTP Basic Authentication

---

Mặc dù khá cũ, nhưng do có **tính đơn giản** và **dễ triển khai**, nên đôi khi bạn vẫn có thể bắt gặp cơ chế **HTTP Basic Authentication** được sử dụng.

Trong HTTP Basic Authentication:

- Client nhận một **authentication token** từ server.
- Token này được tạo bằng cách **nối (concatenate) username và password**, sau đó **mã hóa bằng Base64**.
- Token được trình duyệt lưu trữ và quản lý, rồi **tự động thêm vào header `Authorization` của mọi request tiếp theo**, theo định dạng sau:

```
Authorization: Basic base64(username:password)
```

Vì nhiều lý do, **HTTP Basic Authentication thường không được coi là phương thức xác thực an toàn**:

1. **Gửi lặp lại thông tin đăng nhập:** Cơ chế này liên tục gửi **thông tin đăng nhập (username và password)** trong mỗi request. Nếu website không triển khai **HSTS**, thông tin này có thể bị đánh cắp qua tấn công **Man-in-the-Middle (MitM)**.
2. **Không hỗ trợ chống brute-force:** Nhiều triển khai của HTTP Basic Authentication **không có cơ chế bảo vệ brute-force**. Do token chỉ bao gồm **giá trị tĩnh** (username:password mã hóa Base64), nó có thể dễ dàng trở thành mục tiêu brute-force.
3. **Dễ bị tấn công liên quan đến session:** HTTP Basic Authentication **đặc biệt dễ bị khai thác** bởi các tấn công liên quan đến session, điển hình là **CSRF**, và bản thân nó **không có cơ chế bảo vệ** chống lại kiểu tấn công này.

Trong một số trường hợp, việc khai thác lỗ hổng trong HTTP Basic Authentication có thể chỉ giúp kẻ tấn công truy cập một trang có vẻ **không quan trọng**. Tuy nhiên:

- Trang này vẫn có thể mở rộng **bề mặt tấn công**.
- Quan trọng hơn, **thông tin đăng nhập bị lộ** có thể được **tái sử dụng** trong các ngữ cảnh khác, nhạy cảm hơn nhiều.

---

## **Multi-factor authentication**

---

Trong phần này, chúng ta sẽ tìm hiểu một số lỗ hổng có thể xuất hiện trong các cơ chế **xác thực đa yếu tố (Multi-Factor Authentication – MFA).**

Nhiều website chỉ dựa vào **xác thực một yếu tố (single-factor authentication)** bằng mật khẩu để xác minh người dùng. Tuy nhiên, một số website yêu cầu người dùng phải chứng minh danh tính của mình bằng **nhiều yếu tố xác thực**.

Việc xác minh yếu tố **sinh trắc học (biometric)** là **khó khả thi** đối với hầu hết website. Tuy nhiên, hiện nay ngày càng phổ biến cả **bắt buộc** lẫn **tùy chọn** hình thức **xác thực hai yếu tố (2FA)** dựa trên:

- **Something you know (thứ bạn biết):** ví dụ mật khẩu.
- **Something you have (thứ bạn sở hữu):** ví dụ mã xác minh tạm thời từ thiết bị vật lý ngoài băng (out-of-band device).

Trong đó, người dùng thường phải nhập cả **mật khẩu truyền thống** và **mã xác minh tạm thời** từ thiết bị họ sở hữu.

Mặc dù kẻ tấn công đôi khi có thể lấy được một yếu tố dựa trên tri thức (chẳng hạn mật khẩu), nhưng khả năng đồng thời lấy được **yếu tố từ nguồn ngoài băng** là **khó hơn rất nhiều**. Vì vậy, 2FA **chứng minh được là an toàn hơn nhiều** so với xác thực một yếu tố.

Tuy nhiên, cũng giống như bất kỳ biện pháp bảo mật nào, 2FA chỉ **an toàn đúng bằng mức độ triển khai của nó**. Nếu được triển khai kém, 2FA hoàn toàn có thể bị **đánh bại** hoặc thậm chí **bị bypass hoàn toàn**, giống như xác thực một yếu tố.

Một điểm đáng chú ý khác là: **lợi ích thực sự của xác thực đa yếu tố chỉ đạt được khi xác minh nhiều loại yếu tố khác nhau**. Nếu chỉ xác minh **cùng một yếu tố theo hai cách**, thì đó **không phải là 2FA thực sự**.

Ví dụ: **2FA dựa trên email**. Người dùng cần cung cấp cả mật khẩu và mã xác minh gửi qua email. Tuy nhiên, việc truy cập mã này chỉ phụ thuộc vào việc người dùng biết **thông tin đăng nhập email** của mình. Nghĩa là yếu tố tri thức (knowledge factor) đã bị **xác minh hai lần**, chứ không phải hai yếu tố riêng biệt.

---

### **Two-factor authentication tokens**

---

Mã xác minh thường được người dùng đọc từ **một thiết bị vật lý** nào đó. Nhiều website có yêu cầu bảo mật cao hiện nay cung cấp cho người dùng **thiết bị chuyên dụng** cho mục đích này, ví dụ như **RSA token** hoặc **thiết bị bàn phím (keypad device)** dùng để truy cập vào dịch vụ ngân hàng trực tuyến hoặc máy tính công việc.

Ngoài việc được thiết kế chuyên biệt cho bảo mật, các thiết bị này còn có ưu điểm là **tự tạo mã xác minh trực tiếp**. Bên cạnh đó, nhiều website cũng sử dụng **ứng dụng di động chuyên dụng**, như **Google Authenticator**, vì lý do tương tự.

Ngược lại, một số website gửi mã xác minh đến **điện thoại di động của người dùng qua SMS**. Về mặt kỹ thuật, đây vẫn là xác minh yếu tố **“something you have” (thứ bạn sở hữu)**, nhưng lại dễ bị lạm dụng:

1. **Mã được truyền qua SMS** thay vì được sinh ra trực tiếp trên thiết bị, tạo khả năng bị **chặn và đánh cắp trong quá trình truyền**.
2. Nguy cơ **SIM swapping**: kẻ tấn công có thể gian lận để chiếm đoạt một SIM card có cùng số điện thoại với nạn nhân. Khi đó, chúng sẽ nhận được toàn bộ tin nhắn SMS gửi cho nạn nhân, bao gồm cả mã xác minh.

Trong một số trường hợp, việc triển khai **xác thực hai yếu tố (2FA)** có thể bị lỗi đến mức cho phép **bỏ qua hoàn toàn**.

Ví dụ: nếu người dùng được yêu cầu nhập **mật khẩu trước**, sau đó được yêu cầu nhập **mã xác minh trên một trang riêng biệt**, thì thực chất người dùng đã ở trong trạng thái **“đã đăng nhập”** trước khi nhập mã xác minh.

Trong tình huống này, bạn nên thử kiểm tra xem có thể **truy cập trực tiếp các trang chỉ dành cho người đã đăng nhập** sau khi hoàn thành bước xác thực đầu tiên hay không. Thỉnh thoảng, bạn sẽ phát hiện website **không hề kiểm tra** việc người dùng có thực hiện bước thứ hai hay không trước khi tải trang.

---

### Flawed two-factor verification logic

---

Đôi khi, do **lỗi logic trong cơ chế xác thực hai yếu tố (2FA)**, sau khi người dùng hoàn thành bước đăng nhập đầu tiên, website lại **không xác minh đầy đủ** rằng cùng một người dùng đang thực hiện bước thứ hai.

Ví dụ:

- Người dùng đăng nhập bằng thông tin bình thường ở bước đầu tiên:

```
POST /login-steps/first HTTP/1.1
Host: vulnerable-website.com
...
username=carlos&password=qwerty
```

- Sau đó, server gán cho họ một cookie liên quan đến tài khoản:

```
HTTP/1.1 200 OK
Set-Cookie: account=carlos
```

- Người dùng được chuyển sang bước thứ hai:

```
GET /login-steps/second HTTP/1.1
Cookie: account=carlos
```

- Khi gửi mã xác minh, request sẽ sử dụng cookie này để xác định tài khoản mà người dùng muốn truy cập:

```
POST /login-steps/second HTTP/1.1
Host: vulnerable-website.com
Cookie: account=carlos
...
verification-code=123456
```

👉 Trong trường hợp này, kẻ tấn công có thể:

- Đăng nhập bằng **thông tin của chính mình**.
- Sau đó **thay đổi giá trị cookie `account`** thành bất kỳ username nào khi gửi mã xác minh:

```
POST /login-steps/second HTTP/1.1
Host: vulnerable-website.com
Cookie: account=victim-user
...
verification-code=123456
```

Điều này **cực kỳ nguy hiểm** nếu kẻ tấn công có thể brute-force mã xác minh, vì nó cho phép chúng **đăng nhập vào tài khoản của bất kỳ người dùng nào chỉ dựa trên username**, mà **không bao giờ cần biết mật khẩu của họ**.

---

### **Brute-forcing 2FA verification codes**

---

Cũng giống như mật khẩu, các website cần triển khai biện pháp để **ngăn chặn brute-force mã xác minh 2FA**. Điều này đặc biệt quan trọng vì mã 2FA thường chỉ là một số **4 hoặc 6 chữ số**. Nếu không có cơ chế bảo vệ brute-force thích hợp, việc crack mã này trở nên **quá đơn giản**.

Một số website cố gắng ngăn brute-force bằng cách **tự động đăng xuất người dùng** nếu họ nhập sai quá nhiều mã xác minh. Tuy nhiên, biện pháp này **không hiệu quả trên thực tế**, bởi vì một kẻ tấn công tinh vi có thể **tự động hóa toàn bộ quy trình nhiều bước** này bằng cách sử dụng **macro cho Burp Intruder**. Ngoài ra, extension **Turbo Intruder** cũng có thể được dùng cho mục đích này.

---

## **Other authentication mechanisms**

---

Ngoài chức năng đăng nhập cơ bản, hầu hết các website còn cung cấp các chức năng bổ sung để người dùng **quản lý tài khoản** của mình. Ví dụ, người dùng thường có thể:

- **Thay đổi mật khẩu.**
- **Đặt lại mật khẩu khi quên**.

Tuy nhiên, chính những cơ chế này cũng có thể tạo ra **lỗ hổng** mà kẻ tấn công có thể khai thác.

Thông thường, các website sẽ cẩn trọng trong việc tránh những lỗ hổng đã biết trên trang đăng nhập. Nhưng lại dễ **bỏ qua việc áp dụng các biện pháp bảo mật tương tự** cho những chức năng liên quan. Điều này đặc biệt nguy hiểm trong trường hợp kẻ tấn công có thể **tự tạo tài khoản** và từ đó dễ dàng tiếp cận, nghiên cứu các trang bổ sung này.

---

### Keeping users logged in

---

Một tính năng phổ biến là tùy chọn cho phép người dùng **duy trì trạng thái đăng nhập ngay cả sau khi đóng trình duyệt**. Thường được hiển thị dưới dạng một checkbox với nhãn như **“Remember me”** hoặc **“Keep me logged in”**.

Chức năng này thường được triển khai bằng cách tạo ra một loại **token “remember me”**, sau đó lưu trong **persistent cookie**. Vì việc sở hữu cookie này đồng nghĩa với việc **bỏ qua toàn bộ quá trình đăng nhập**, nên best practice là cookie này phải **không thể đoán được**.

Tuy nhiên, một số website lại tạo cookie dựa trên **chuỗi nối (concatenation) có thể đoán trước** của các giá trị tĩnh, chẳng hạn như:

- **Username + timestamp**, hoặc thậm chí
- **Sử dụng password** như một phần của cookie.

Cách triển khai này **đặc biệt nguy hiểm** nếu kẻ tấn công có thể **tự tạo tài khoản**:

- Họ sẽ phân tích cookie của chính mình để tìm ra cách nó được sinh ra.
- Sau đó, khi đã xác định được công thức, họ có thể **brute-force cookie của người dùng khác** để chiếm quyền truy cập vào tài khoản.

Một số website cho rằng nếu cookie được **mã hóa theo một cách nào đó**, thì nó sẽ không thể đoán được, ngay cả khi sử dụng các giá trị tĩnh. Điều này chỉ đúng khi việc mã hóa được thực hiện đúng cách.

- Nếu chỉ “mã hóa” cookie bằng các phương pháp **mã hóa hai chiều đơn giản** như **Base64**, thì hoàn toàn **không có giá trị bảo mật**.
- Ngay cả khi sử dụng **hàm băm một chiều (hash function)** hợp lệ, nó vẫn không hoàn toàn an toàn. Nếu kẻ tấn công dễ dàng xác định được thuật toán băm và cookie không sử dụng **salt**, chúng có thể brute-force cookie bằng cách đơn giản là **băm wordlist** của mình.

Cách này thậm chí có thể được sử dụng để **vượt qua giới hạn số lần đăng nhập** nếu hệ thống **không áp dụng giới hạn tương tự cho việc thử cookie**.

Ngay cả khi kẻ tấn công **không thể tự tạo tài khoản**, lỗ hổng này vẫn có thể bị khai thác. Ví dụ:

- Bằng các kỹ thuật thường thấy như **XSS**, kẻ tấn công có thể đánh cắp cookie “remember me” của người dùng khác và từ đó phân tích cách cookie được sinh ra.
- Nếu website được xây dựng bằng **framework mã nguồn mở**, thì **chi tiết về cơ chế sinh cookie** có thể đã được **công khai trong tài liệu**, giúp kẻ tấn công dễ dàng hơn trong việc khai thác.

Trong một số trường hợp hiếm gặp, kẻ tấn công thậm chí có thể lấy được **mật khẩu gốc (cleartext password)** của người dùng trực tiếp từ cookie, ngay cả khi mật khẩu đó đã được băm.

Nguyên nhân là do:

- Các phiên bản băm của **các danh sách mật khẩu phổ biến** đã được công khai rộng rãi trên Internet.
- Nếu mật khẩu của người dùng nằm trong những danh sách này, việc "giải mã" hash đôi khi **đơn giản như việc dán hash đó vào công cụ tìm kiếm**.

Điều này cho thấy **tầm quan trọng của việc sử dụng salt trong quá trình mã hóa/băm** để đảm bảo an toàn cho mật khẩu.

---

### **Resetting user passwords**

---

Trong thực tế, một số người dùng sẽ quên mật khẩu, vì vậy hầu hết các website đều cung cấp **chức năng đặt lại mật khẩu**. Do trong tình huống này **không thể áp dụng cơ chế xác thực bằng mật khẩu thông thường**, website buộc phải dựa vào **các phương pháp thay thế** để đảm bảo rằng **chính chủ tài khoản** là người đang thực hiện việc đặt lại mật khẩu.

Chính vì lý do này, chức năng đặt lại mật khẩu vốn dĩ đã **tiềm ẩn nguy hiểm** và cần phải được triển khai một cách **an toàn tuyệt đối**.

Có một số cách triển khai tính năng này khá phổ biến, nhưng mỗi cách lại tồn tại những **mức độ lỗ hổng khác nhau**.

> **Qua Email**
> 

Hiển nhiên rằng, nếu một website xử lý mật khẩu một cách an toàn ngay từ đầu thì việc **gửi mật khẩu hiện tại của người dùng qua email** là điều **tuyệt đối không bao giờ được phép xảy ra**.

Thay vào đó, một số website chọn cách **tạo mật khẩu mới** và gửi mật khẩu này cho người dùng qua email.

Tuy nhiên, về nguyên tắc, việc **gửi mật khẩu có giá trị lâu dài qua các kênh không an toàn** là điều cần tránh. Trong trường hợp này, độ an toàn phụ thuộc vào việc:

- Mật khẩu được sinh ra **hết hạn sau một khoảng thời gian rất ngắn**, hoặc
- Người dùng **ngay lập tức thay đổi lại mật khẩu** của mình.

Nếu không, phương pháp này sẽ **rất dễ bị tấn công Man-in-the-Middle (MitM)**.

Ngoài ra, **email nhìn chung không được coi là kênh an toàn**, bởi vì:

- Hộp thư đến thường là **lưu trữ lâu dài** và không được thiết kế để bảo mật thông tin nhạy cảm.
- Nhiều người dùng còn **đồng bộ hóa hộp thư giữa nhiều thiết bị** thông qua các kênh tiềm ẩn rủi ro.

> **Qua URL**
> 

Một phương pháp **an toàn hơn** để đặt lại mật khẩu là gửi cho người dùng một **URL duy nhất** dẫn đến trang reset mật khẩu.

Tuy nhiên, những triển khai kém an toàn của phương pháp này lại sử dụng **URL với tham số dễ đoán** để xác định tài khoản cần đặt lại. Ví dụ:

```
http://vulnerable-website.com/reset-password?user=victim-user
```

Trong trường hợp này, kẻ tấn công có thể thay đổi giá trị của tham số `user` để tham chiếu đến bất kỳ username nào mà chúng đã xác định được. Từ đó, chúng có thể được đưa thẳng đến trang cho phép **đặt lại mật khẩu mới cho tài khoản bất kỳ**.

Một cách triển khai **an toàn hơn** là sinh ra một **token có entropy cao, khó đoán** và xây dựng URL reset dựa trên token đó. Trong kịch bản tốt nhất, URL này **không tiết lộ bất kỳ thông tin nào về người dùng** đang được đặt lại mật khẩu.

Ví dụ:

```
http://vulnerable-website.com/reset-password?token=a0ba0d1cb3b63d13822572fcff1a241895d893f659164d4cc550b421ebdd48a8
```

Khi người dùng truy cập URL này, hệ thống sẽ kiểm tra token ở backend để xác định:

- Token có tồn tại hay không.
- Nếu có, token đó gắn với tài khoản nào để tiến hành reset mật khẩu.

Token này cần phải:

- **Hết hạn sau một khoảng thời gian ngắn**, và
- **Bị hủy ngay lập tức** sau khi mật khẩu đã được đặt lại.

Tuy nhiên, một số website lại **không kiểm tra lại token khi form reset được submit**. Trong tình huống này, kẻ tấn công có thể:

1. Truy cập form reset mật khẩu từ chính tài khoản của chúng.
2. Xóa token khỏi request.
3. Lợi dụng trang này để **đặt lại mật khẩu cho tài khoản bất kỳ**.

Nếu URL trong email reset được sinh ra **một cách động (dynamically)**, thì cơ chế này cũng có thể dễ dàng bị tấn công theo kiểu **password reset poisoning**.

Trong tình huống này, kẻ tấn công có thể **đánh cắp token reset của người dùng khác** và sử dụng nó để **thay đổi mật khẩu** của họ.

---

### Changing user passwords

---

Thông thường, việc thay đổi mật khẩu yêu cầu người dùng nhập:

1. **Mật khẩu hiện tại**
2. **Mật khẩu mới** (nhập hai lần để xác nhận)

Các trang này về cơ bản dựa vào cùng một quy trình như **trang đăng nhập thông thường** để kiểm tra sự khớp giữa **username** và **mật khẩu hiện tại**. Do đó, chúng cũng có thể bị khai thác bằng **các kỹ thuật tấn công tương tự**.

Chức năng đổi mật khẩu đặc biệt **nguy hiểm** nếu cho phép kẻ tấn công **truy cập trực tiếp** mà **không cần đăng nhập bằng tài khoản nạn nhân**.

Ví dụ: nếu **username** được truyền trong một **trường ẩn (hidden field)**, kẻ tấn công có thể chỉnh sửa giá trị này trong request để nhắm đến tài khoản tùy ý. Điều này có thể bị khai thác để:

- **Liệt kê username (username enumeration)**
- **Brute-force mật khẩu**

---

# Ngăn chặn

---

Chúng ta đã xem qua nhiều cách mà các website có thể trở nên **dễ bị tấn công** do cách triển khai cơ chế xác thực.

Để giảm thiểu rủi ro các cuộc tấn công như vậy trên website của bạn, có một số **nguyên tắc quan trọng** mà bạn nên luôn tuân theo.

---

## User credentials

---

Ngay cả những cơ chế xác thực mạnh mẽ nhất cũng sẽ trở nên **vô dụng** nếu bạn vô tình làm lộ **thông tin đăng nhập hợp lệ** cho kẻ tấn công.

- Hiển nhiên, bạn **không bao giờ được gửi dữ liệu đăng nhập qua các kết nối không mã hóa**.
- Ngay cả khi bạn đã triển khai **HTTPS cho các request đăng nhập**, hãy đảm bảo rằng bạn **ép buộc sử dụng HTTPS** bằng cách **chuyển hướng toàn bộ HTTP request sang HTTPS**.

Ngoài ra, bạn cũng nên **kiểm tra (audit)** website để đảm bảo rằng:

- Không có **username** hoặc **địa chỉ email** nào bị lộ qua các **profile công khai**.
- Không bị phản hồi trong **HTTP response** theo bất kỳ cách nào.

---

## Don’t count on users

---

Các biện pháp xác thực nghiêm ngặt thường yêu cầu người dùng phải bỏ ra thêm một chút nỗ lực. Tuy nhiên, **bản chất con người** gần như chắc chắn sẽ khiến một số người tìm cách **lách luật để tiết kiệm công sức**. Vì vậy, bạn cần **cưỡng chế hành vi an toàn** ở bất cứ nơi nào có thể.

Ví dụ rõ ràng nhất là việc triển khai **chính sách mật khẩu hiệu quả**.

- Nhiều chính sách truyền thống thất bại vì người dùng cố gắng **“biến tấu” mật khẩu dễ đoán** của mình để khớp với yêu cầu chính sách.
- Thay vào đó, một giải pháp hiệu quả hơn là sử dụng **trình kiểm tra độ mạnh mật khẩu (password checker)**, cho phép người dùng thử nghiệm mật khẩu và nhận được phản hồi về độ mạnh **theo thời gian thực**.

Một ví dụ phổ biến là **thư viện JavaScript zxcvbn** do **Dropbox** phát triển. Bằng cách chỉ cho phép người dùng sử dụng các mật khẩu được trình kiểm tra đánh giá ở mức cao, bạn có thể **ép buộc sử dụng mật khẩu an toàn hiệu quả hơn** so với các chính sách truyền thống.

---

## **Prevent username enumeration**

---

Việc phá vỡ cơ chế xác thực của bạn sẽ trở nên **dễ dàng hơn nhiều** nếu bạn vô tình tiết lộ rằng một người dùng nào đó **tồn tại trong hệ thống**. Trong một số trường hợp, chỉ riêng việc biết rằng một cá nhân có tài khoản trên website cũng đã là **thông tin nhạy cảm**.

Để phòng tránh:

- Bất kể username thử có hợp lệ hay không, hãy sử dụng **các thông báo lỗi giống hệt nhau, dạng chung chung**, và đảm bảo rằng chúng **thực sự giống nhau**.
- Luôn trả về **cùng một HTTP status code** cho mọi request đăng nhập.
- Đảm bảo **thời gian phản hồi (response time)** trong các kịch bản khác nhau càng khó phân biệt càng tốt.

---

## **Implement robust brute-force protection**

---

Vì việc xây dựng một cuộc tấn công brute-force là **tương đối đơn giản**, nên việc triển khai các biện pháp để **ngăn chặn hoặc ít nhất là làm gián đoạn** các nỗ lực brute-force đăng nhập là điều **cực kỳ quan trọng**.

Một trong những phương pháp hiệu quả hơn là:

- **Triển khai cơ chế giới hạn tốc độ (rate limiting) nghiêm ngặt dựa trên IP**.
- Bao gồm các biện pháp để ngăn kẻ tấn công **giả mạo hoặc thao túng địa chỉ IP**.
- Lý tưởng nhất, sau khi đạt đến một giới hạn nhất định, người dùng cần phải **hoàn thành bài kiểm tra CAPTCHA** cho mỗi lần đăng nhập tiếp theo.

Lưu ý rằng những biện pháp này **không đảm bảo loại bỏ hoàn toàn mối đe dọa brute-force**. Tuy nhiên, việc khiến quy trình trở nên **thủ công và rườm rà** sẽ làm tăng khả năng kẻ tấn công **từ bỏ và chuyển sang mục tiêu dễ khai thác hơn**.

---

## **Triple-check your verification logic**

---

Các lỗi logic đơn giản rất dễ len lỏi vào mã và, trong trường hợp xác thực, chúng có thể dẫn đến việc xâm phạm hoàn toàn website và người dùng của bạn. Việc audit kỹ lưỡng mọi logic xác minh/kiểm tra hợp lệ để loại bỏ lỗi là yếu tố then chốt của một cơ chế xác thực vững chắc. Một bước kiểm tra có thể bị bỏ qua rốt cuộc cũng không tốt hơn nhiều so với việc không kiểm tra.

---

## **Don't forget supplementary functionality**

---

Hãy bảo đảm bạn không chỉ tập trung vào các trang đăng nhập trung tâm mà bỏ qua những chức năng bổ sung liên quan đến xác thực. Điều này đặc biệt quan trọng trong các trường hợp kẻ tấn công có thể tự do đăng ký tài khoản của riêng mình và khám phá các chức năng này. Hãy nhớ rằng việc đặt lại hoặc thay đổi mật khẩu cũng là một **bề mặt tấn công** hợp lệ như cơ chế đăng nhập chính và, do đó, phải vững chắc tương đương.

---

## **Implement proper multi-factor authentication**

---

Mặc dù xác thực đa yếu tố (MFA) có thể không thực tế với mọi website, nhưng khi được triển khai đúng cách, nó an toàn hơn nhiều so với chỉ đăng nhập dựa trên mật khẩu. Hãy nhớ rằng việc xác minh nhiều lần của **cùng một yếu tố** không phải là xác thực đa yếu tố thực sự. Gửi mã xác minh qua email về bản chất chỉ là một dạng kéo dài hơn của xác thực **một yếu tố**.

Về mặt kỹ thuật, 2FA dựa trên SMS xác minh hai yếu tố (thứ bạn biết và thứ bạn sở hữu). Tuy nhiên, khả năng bị lạm dụng qua **SIM swapping**, chẳng hạn, khiến hệ thống này có thể **không đáng tin cậy**.

Lý tưởng nhất, 2FA nên được triển khai bằng **thiết bị hoặc ứng dụng chuyên dụng** tạo mã xác minh trực tiếp. Do được thiết kế chuyên biệt cho bảo mật, chúng thường **an toàn hơn**.

Cuối cùng, cũng như với **logic xác thực** chính, hãy bảo đảm **logic kiểm tra 2FA** của bạn chặt chẽ để không thể dễ dàng bị **bỏ qua (bypass)**.
