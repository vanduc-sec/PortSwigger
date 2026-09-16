# note

# File Upload Vulnerabilities

## Khái niệm

Là lỗi khi web cho upload file nhưng kiểm tra không chặt về:

- tên file
- extension / MIME type
- nội dung file
- kích thước file

Kết quả: attacker có thể upload file nguy hiểm thay vì file hợp lệ.

## Hậu quả

- Upload web shell => RCE
- Ghi đè file quan trọng
- Kết hợp path traversal để lưu file sai chỗ
- Stored XSS nếu upload HTML/SVG
- XXE / parser bug nếu server xử lý file
- DoS nếu upload file quá lớn

## Các cách bypass hay gặp

- Fake `Content-Type`
- Đổi extension hoặc dùng extension lạ (`.php5`, `.phtml`)
- Double extension: `shell.php.jpg`
- Viết hoa/thường: `shell.pHp`
- Trailing dot: `shell.php.`
- URL encode / double encode
- Null byte / semicolon
- Polyglot file (ví dụ JPEG + code)
- Upload `.htaccess` / `web.config`
- Path traversal khi upload
- Race condition
- HTTP PUT

## Ý chính cần nhớ

Server thường xử lý file dựa trên extension và config:

- file tĩnh => trả nội dung
- file script + được execute => chạy code
- file script nhưng không execute => có thể lộ source

Nguy hiểm nhất là upload được file script vào thư mục server cho thực thi.

## Phòng thủ

- Dùng whitelist extension, không dùng blacklist
- Kiểm tra cả filename, content, size
- Đổi tên file khi lưu
- Không lưu thẳng vào thư mục chính trước khi validate xong
- Không cho execute trong thư mục upload
- Dùng framework chuẩn thay vì tự viết logic upload

## Checklist khi gặp chức năng upload

- Kiểm tra extension kiểu gì?
- Có tin `Content-Type` từ client không?
- File được lưu ở đâu?
- Có truy cập lại file được không?
- Khi truy cập lại thì server render, download hay execute?
- Có thử được các bypass ở trên không?
