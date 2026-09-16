# note

```
# OS Command Injection / Shell Injection

OS command injection (còn gọi là shell injection) là lỗi khi ứng dụng lấy input của người dùng rồi ghép trực tiếp vào một lệnh hệ điều hành để chạy trên server.
Bản chất của lỗi là: app nghĩ input chỉ là dữ liệu, nhưng shell lại hiểu một phần input đó là cú pháp lệnh. Khi đó dữ liệu đầu vào biến thành code điều khiển lệnh.

---

## 1. Khái niệm cần nhớ
- **OS command injection / Shell injection** = chèn lệnh hệ điều hành / chèn lệnh shell
- **Shell** = trình thông dịch lệnh
- **Command execution** = thực thi lệnh
- **User input** = dữ liệu người dùng nhập
- **Shell metacharacters** = ký tự đặc biệt của shell

Lỗi thường xuất hiện khi code làm kiểu:
```python
cmd = "stockreport.pl " + productID + " " + storeID
system(cmd)
```

Nguy hiểm vì shell không chỉ đọc dữ liệu, mà còn đọc cả cú pháp như:

- dấu tách lệnh
- pipe
- redirection
- variable expansion
- command substitution
- dấu nháy

---

## 2. Vì sao lỗi này nguy hiểm?

Nếu khai thác được OS command injection, attacker có thể:

- chạy lệnh trên server
- xem user đang chạy ứng dụng
- đọc thông tin hệ điều hành
- dò cấu hình mạng
- xem tiến trình đang chạy
- đọc/ghi file
- lấy dữ liệu nhạy cảm
- pivot sang hệ thống khác

Thuật ngữ:

- **Compromise** = chiếm quyền / xâm phạm thành công
- **Pivot** = xoay trục tấn công sang máy khác
- **Trust relationship** = quan hệ tin cậy giữa các hệ thống
- **Data exfiltration** = rút dữ liệu ra ngoài

---

## 3. Shell hiểu chuỗi lệnh như thế nào?

Khi shell nhận một chuỗi, nó sẽ:

1. tách token
2. phân tích cú pháp
3. xử lý biến, substitution, quote, operator
4. thực thi lệnh

Đây là lý do command injection là lỗi **data becomes code**:

- dữ liệu đầu vào bị shell hiểu thành cú pháp lệnh

Thuật ngữ:

- **Tokenize** = tách token
- **Parse** = phân tích cú pháp
- **Expansion** = mở rộng / thay thế
- **Operator** = toán tử / ký hiệu điều khiển

---

## 4. Các dấu quan trọng trong OS command injection

### `&`

- Tên: **ampersand**
- Ý nghĩa: trong nhiều ngữ cảnh injection, nó làm tách lệnh; trên Unix còn có nghĩa chạy nền
- Ví dụ:

```
echo one &echo two
```

- Ý tưởng: shell không còn hiểu đây là một chuỗi dữ liệu liền nữa, mà tách thành nhiều phần lệnh

### `;`

- Tên: **semicolon**
- Ý nghĩa: chạy lệnh bên trái xong rồi chạy tiếp lệnh bên phải, bất kể thành công hay thất bại
- Ví dụ:

```
echo one;echo two
```

### `&&`

- Tên: **AND operator**
- Ý nghĩa: chỉ chạy lệnh bên phải nếu lệnh bên trái thành công
- Ví dụ:

```
echo ok &&echo next
```

### `||`

- Tên: **OR operator**
- Ý nghĩa: chỉ chạy lệnh bên phải nếu lệnh bên trái thất bại
- Ví dụ:

```
false ||echo fallback
```

### `|`

- Tên: **pipe**
- Ý nghĩa: đưa output của lệnh bên trái thành input của lệnh bên phải
- Ví dụ:

```
echo hello |wc-c
```

- Phân biệt:
    - `;` = chỉ chạy nối tiếp
    - `|` = truyền dữ liệu giữa hai lệnh

### Newline

- Tên: **newline / line break**
- Ý nghĩa: trên Unix, xuống dòng cũng có thể kết thúc một lệnh
- Ví dụ:

```
echo one
echo two
```

### ``...``

- Tên: **backtick**
- Ý nghĩa: command substitution kiểu cũ; shell chạy lệnh trong backticks rồi thay output vào chỗ đó
- Ví dụ:

```
echo `whoami`
```

### `$(...)`

- Tên: **command substitution**
- Ý nghĩa: giống backticks nhưng hiện đại hơn, dễ đọc hơn
- Ví dụ:

```
echo $(whoami)
```

### `$VAR`

- Tên: **variable expansion / environment variable expansion**
- Ý nghĩa: lấy giá trị biến môi trường
- Ví dụ:

```
echo$HOME
```

- Phân biệt:
    - `$HOME` = lấy giá trị biến
    - `$(whoami)` = chạy lệnh rồi lấy output

### `>`

- Tên: **output redirection**
- Ý nghĩa: ghi output vào file, thường là ghi đè
- Ví dụ:

```
echo hello > out.txt
```

### `>>`

- Tên: **append redirection**
- Ý nghĩa: ghi thêm output vào cuối file
- Ví dụ:

```
echo hello >> out.txt
```

### `<`

- Tên: **input redirection**
- Ý nghĩa: lấy nội dung file làm input cho lệnh
- Ví dụ:

```
wc-l < notes.txt
```

### `2>`

- Tên: **stderr redirection**
- Ý nghĩa: chuyển hướng luồng lỗi vào file
- Ví dụ:

```
ls no_such_file2> err.txt
```

### `2>&1`

- Tên: **redirect stderr to stdout**
- Ý nghĩa: gộp lỗi chuẩn vào cùng nơi với đầu ra chuẩn
- Ví dụ:

```
command > all.txt2>&1
```

### `'...'`

- Tên: **single quotes**
- Ý nghĩa: trên Unix, giữ nguyên gần như mọi thứ bên trong
- Ví dụ:

```
echo'$HOME'
```

- Kết quả: in ra đúng `$HOME`

### `"..."`

- Tên: **double quotes**
- Ý nghĩa: vẫn giữ chuỗi lại, nhưng cho phép một số expansion như biến môi trường
- Ví dụ:

```
echo"$HOME"
```

### `\`

- Tên: **backslash / escape character**
- Ý nghĩa: làm mất ý nghĩa đặc biệt của ký tự phía sau
- Ví dụ:

```
echo \$HOME
```

### 

- Tên: **wildcard / glob**
- Ý nghĩa: khớp nhiều tên file
- Ví dụ:

```
ls *.txt
```

### `?`

- Tên: **single-character wildcard**
- Ý nghĩa: khớp đúng 1 ký tự
- Ví dụ:

```
ls file?.txt
```

### `#`

- Tên: **comment marker**
- Ý nghĩa: trong nhiều shell, phần sau `#` bị coi là comment
- Ví dụ:

```
echo hello# comment
```

---

## 5. Những nhóm dấu cần nhớ

### Nhóm tách hoặc nối lệnh

- `&`
- `;`
- `&&`
- `||`
- newline

### Nhóm truyền hoặc chuyển hướng dữ liệu

- `|`
- `>`
- `>>`
- `<`
- `2>`
- `2>&1`

### Nhóm thay thế / mở rộng

- ``...``
- `$(...)`
- `$VAR`

### Nhóm kiểm soát ngữ cảnh

- `'...'`
- `"..."`
- `\`

### Nhóm khớp mẫu / cắt phần sau

- 
- `?`
- `#`

---

## 6. `$` hoạt động như thế nào?

Dấu `$` rất quan trọng vì nó có nhiều vai trò:

### `$VAR`

Lấy giá trị biến:

```
echo$HOME
```

### `${VAR}`

Cũng là lấy biến nhưng viết rõ hơn:

```
echo${HOME}
```

### `$(command)`

Chạy một lệnh rồi thay output của lệnh vào:

```
echo $(whoami)
```

Chốt:

- `$HOME` = biến môi trường
- `$(whoami)` = command substitution

---

## 7. `;` hoạt động như thế nào?

Dấu `;` chỉ đơn giản là:

- kết thúc lệnh này
- rồi bắt đầu lệnh khác

Ví dụ:

```
echo one;echo two
```

Khác với pipe:

```
echo one |wc-c
```

- `;` = chạy nối tiếp
- `|` = truyền output sang lệnh khác

---

## 8. Pipe `|` hoạt động như thế nào?

Pipe nối:

- **stdout** của lệnh trái
- vào **stdin** của lệnh phải

Ví dụ:

```
echo hello |wc-c
```

Giải thích:

- `echo hello` sinh output
- output đó đi qua pipe
- `wc -c` nhận làm input và đếm số ký tự

Thuật ngữ:

- **stdout (standard output)** = đầu ra chuẩn
- **stdin (standard input)** = đầu vào chuẩn
- **Pipeline** = chuỗi lệnh nối bằng pipe

---

## 9. Backtick và `$(...)`

Cả hai đều là **command substitution**.

### Backtick

```
echo `whoami`
```

### Dollar-parentheses

```
echo $(whoami)
```

Khác nhau:

- backtick là cú pháp cũ
- `$(...)` dễ đọc hơn
- `$(...)` dễ lồng nhau hơn
- hiện nay thường ưu tiên `$(...)`

---

## 10. Dấu nháy ảnh hưởng thế nào?

### Không có dấu nháy

Shell tự do tách token và expand.

### Single quote `'...'`

Giữ nguyên gần như toàn bộ:

```
echo'$HOME'
```

### Double quote `"..."`

Vẫn cho phép expansion như biến:

```
echo"$HOME"
```

Ý nghĩa trong injection:

payload có chạy hay không còn phụ thuộc input đang nằm:

- ngoài quote
- trong single quote
- hay trong double quote

Thuật ngữ:

- **Context** = ngữ cảnh
- **Quoted context** = ngữ cảnh có dấu nháy
- **Break out of quotes** = thoát khỏi vùng bị nháy

---

## 11. In-band và Blind command injection

### In-band command injection

Là trường hợp output của lệnh xuất hiện ngay trong HTTP response.

Ví dụ tư duy kiểm tra:

```
echo hello
```

Nếu response có `hello` thì rất đáng nghi.

### Blind command injection

Là trường hợp lệnh có thể chạy nhưng output không hiện trực tiếp.

Khi đó thường nghĩ tới:

- **Time delay** = gây chậm phản hồi
- **Output redirection** = ghi output ra file
- **Out-of-band / OAST** = tạo tương tác ra ngoài

Thuật ngữ:

- **Blind command injection** = chèn lệnh mù
- **Time delay** = trì hoãn thời gian phản hồi
- **Output redirection** = chuyển hướng đầu ra
- **Out-of-band** = ngoài kênh chính
- **OAST (Out-of-band Application Security Testing)** = kiểm thử bảo mật ứng dụng bằng tương tác ngoài kênh
