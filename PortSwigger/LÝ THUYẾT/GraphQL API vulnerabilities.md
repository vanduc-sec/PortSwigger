# GraphQL API vulnerabilities

Trạng thái: Chưa bắt đầu
subject: Advanced

# Lỗ hổng GraphQL

---

Các lỗ hổng GraphQL thường phát sinh do sai sót trong triển khai và thiết kế. Ví dụ, tính năng *introspection* có thể bị để mở, cho phép kẻ tấn công truy vấn API để thu thập thông tin về *schema* (lược đồ).

Các cuộc tấn công GraphQL thường xuất hiện dưới dạng những yêu cầu độc hại, có thể cho phép kẻ tấn công lấy dữ liệu hoặc thực hiện các hành động trái phép. Những cuộc tấn công này có thể gây tác động nghiêm trọng, đặc biệt nếu kẻ tấn công có thể giành quyền quản trị bằng cách thao túng truy vấn hoặc khai thác CSRF. Các API GraphQL dễ tổn thương cũng có thể dẫn đến các vấn đề rò rỉ thông tin.

Trong phần này, chúng ta sẽ tìm hiểu cách kiểm thử các API GraphQL. Đừng lo nếu bạn chưa quen với GraphQL - chúng tôi sẽ trình bày các chi tiết liên quan trong quá trình tìm hiểu. Chúng tôi cũng cung cấp một số phòng lab để bạn thực hành những gì đã học.

![image.png](GraphQL%20API%20vulnerabilities/image.png)

---

# GraphQL

---

## Khái niệm

---

GraphQL là một ngôn ngữ truy vấn cho API, được thiết kế để hỗ trợ giao tiếp hiệu quả giữa client và server. Nó cho phép người dùng chỉ định chính xác dữ liệu họ muốn trong phản hồi, giúp tránh các đối tượng phản hồi cồng kềnh và việc phải gọi nhiều lần như đôi khi xảy ra với REST API.

Các dịch vụ GraphQL định nghĩa một “hợp đồng” (contract) thông qua đó client có thể giao tiếp với server. Client không cần biết dữ liệu nằm ở đâu. Thay vào đó, client gửi các truy vấn (query) tới máy chủ GraphQL, máy chủ sẽ lấy dữ liệu từ các nguồn liên quan. Vì GraphQL độc lập nền tảng (platform-agnostic), nó có thể được triển khai bằng nhiều ngôn ngữ lập trình khác nhau và có thể dùng để giao tiếp với hầu như bất kỳ kho dữ liệu (data store) nào.

---

## Hoạt động

---

Các **schema** của GraphQL định nghĩa cấu trúc dữ liệu của dịch vụ, liệt kê các đối tượng sẵn có (gọi là **types**), **fields** (trường), và các **mối quan hệ**.

Dữ liệu được mô tả bởi một schema GraphQL có thể được thao tác bằng ba loại **operation**:

- **Queries**: lấy (fetch) dữ liệu.
- **Mutations**: thêm, thay đổi, hoặc xóa dữ liệu.
- **Subscriptions**: tương tự query nhưng thiết lập một kết nối lâu dài để máy chủ chủ động đẩy dữ liệu tới client theo định dạng chỉ định.

Tất cả các operation của GraphQL dùng **cùng một endpoint**, và thường được gửi dưới dạng **yêu cầu POST**. Điều này khác biệt rõ rệt so với REST API, vốn sử dụng các endpoint riêng theo từng thao tác và nhiều phương thức HTTP khác nhau. Với GraphQL, **loại và tên của operation** quyết định cách truy vấn được xử lý, thay vì endpoint hay phương thức HTTP được dùng.

Các dịch vụ GraphQL thường phản hồi các operation bằng một **đối tượng JSON** đúng theo cấu trúc đã được yêu cầu.

---

## Lược đồ (Schema)

---

Trong GraphQL, **schema** đại diện cho một *hợp đồng* (contract) giữa frontend và backend của dịch vụ. Nó định nghĩa dữ liệu có sẵn dưới dạng một tập hợp **types**, sử dụng một ngôn ngữ định nghĩa schema có thể đọc được bởi con người. Các type này sau đó sẽ được dịch vụ triển khai.

Phần lớn các type được định nghĩa là **object types**, mô tả các đối tượng sẵn có cùng với **fields** (trường) và **arguments** (tham số) mà chúng có. Mỗi field có một type riêng, có thể là một object khác hoặc các loại khác như: **scalar, enum, union, interface, hoặc custom type**.

Ví dụ dưới đây thể hiện một định nghĩa schema đơn giản cho một `Product` type. Dấu `!` biểu thị rằng field là **non-nullable** (không thể null) khi được gọi (tức là bắt buộc):

```graphql
# Example schema definition

type Product {
    id: ID!
    name: String!
    description: String!
    price: Int
}
```

Schema cũng bắt buộc phải có ít nhất **một query khả dụng**. Thông thường, schema cũng sẽ bao gồm chi tiết về các **mutation** có sẵn.

---

## Queries

---

GraphQL **queries** được dùng để truy xuất dữ liệu từ **data store**. Chúng tương đương với các **GET request** trong REST API.

Một query thường có các thành phần chính sau:

- **Query operation type**: loại thao tác truy vấn. Đây là tùy chọn, nhưng khuyến khích dùng để nói rõ với server rằng request gửi đến là một query.
- **Query name**: tên truy vấn, có thể đặt tùy ý. Cũng là tùy chọn, nhưng khuyến khích dùng để dễ dàng debug.
- **Data structure**: cấu trúc dữ liệu mà query sẽ trả về.
- **Arguments (tham số)** *(tùy chọn)*: dùng để xây dựng các query trả về chi tiết của một đối tượng cụ thể (ví dụ: “lấy name và description của product có ID = 123”).

Ví dụ dưới đây minh họa một query tên là `myGetProductQuery` để lấy các trường `name` và `description` của product có `id = 123`:

```graphql
# Example query

query myGetProductQuery {
    getProduct(id: 123) {
        name
        description
    }
}
```

> **Lưu ý** 
**Product type** có thể chứa nhiều field hơn so với những gì được yêu cầu ở đây. Chính khả năng chỉ định và lấy **chính xác dữ liệu cần thiết** là một điểm mạnh nổi bật của GraphQL.
> 

---

## Mutations

---

Mutations trong GraphQL được dùng để thay đổi dữ liệu theo một cách nào đó, bao gồm thêm mới, xóa hoặc chỉnh sửa. Chúng tương đương với các phương thức POST, PUT, DELETE trong REST API.

Giống như queries, một mutation có:

- **Operation type:** loại thao tác (mutation).
- **Name:** tên mutation.
- **Structure** for returned data: cấu trúc dữ liệu trả về.

Tuy nhiên, điểm khác biệt là **mutation luôn cần input** ở một dạng nào đó. Input này có thể là một giá trị inline, nhưng trong thực tế thường được truyền vào dưới dạng **biến**.

Ví dụ dưới đây là một mutation để **tạo sản phẩm mới** và phản hồi từ server. Trong trường hợp này, dịch vụ được cấu hình để **tự động gán ID** cho sản phẩm mới, và ID đó được trả về trong kết quả:

```graphql
# Example mutation request

mutation {
    createProduct(name: "Flamin' Cocktail Glasses", listed: "yes") {
        id
        name
        listed
    }
}
```

```json
# Example mutation response

{
    "data": {
        "createProduct": {
            "id": 123,
            "name": "Flamin' Cocktail Glasses",
            "listed": "yes"
        }
    }
}
```

---

## Thành phần Queries - Mutations

---

Cú pháp GraphQL có một số thành phần thường gặp khi làm việc với queries và mutations.

---

### Overview

---

- **Fields** → chọn dữ liệu nào cần trả về.
- **Arguments** → tham số lọc dữ liệu.
- **Variables** → truyền tham số động.
- **Aliases** → gọi nhiều instance cùng loại dữ liệu trong một request.
- **Fragments** → tái sử dụng cấu trúc query.

---

### Fields

---

Mọi **type** trong GraphQL đều chứa các phần dữ liệu có thể truy vấn gọi là **fields**. Khi gửi query hoặc mutation, bạn chỉ định rõ những field muốn API trả về. Kết quả phản hồi sẽ phản chiếu đúng cấu trúc mà bạn đã yêu cầu.

**Ví dụ**: query lấy ID và tên của tất cả nhân viên:

```graphql
# Request
query myGetEmployeeQuery {
    getEmployees {
        id
        name {
            firstname
            lastname
        }
    }
}
```

```json
# Response
{
    "data": {
        "getEmployees": [
            {
                "id": 1,
                "name": {
                    "firstname": "Carlos",
                    "lastname": "Montoya"
                }
            },
            {
                "id": 2,
                "name": {
                    "firstname": "Peter",
                    "lastname": "Wiener"
                }
            }
        ]
    }
}
```

---

### Arguments

---

**Arguments** là các giá trị được truyền cho một field cụ thể. Các argument hợp lệ được định nghĩa sẵn trong **schema**.

Ví dụ: query chỉ lấy thông tin nhân viên có `id = 1`:

```graphql
# Example query with arguments
query myGetEmployeeQuery {
    getEmployees(id:1) {
        name {
            firstname
            lastname
        }
    }
}
```

```json
# Response
{
    "data": {
        "getEmployees": [
            {
                "name": {
                    "firstname": "Carlos",
                    "lastname": "Montoya"
                }
            }
        ]
    }
}
```

> ⚠️ **Lưu ý bảo mật** 
Nếu arguments do người dùng nhập vào được dùng để truy cập trực tiếp đối tượng, API GraphQL có thể bị dính lỗi **IDOR (Insecure Direct Object Reference)**.
> 

---

### Variables

---

**Variables** cho phép truyền tham số động thay vì viết trực tiếp trong query. Điều này giúp tái sử dụng query nhiều lần với các giá trị khác nhau.

Khi dùng variables, cần:

1. Khai báo biến và kiểu dữ liệu.
2. Thay thế argument trong query bằng tên biến.
3. Truyền giá trị biến qua **JSON dictionary**.

**Ví dụ**:

```graphql
# Query with variable
query getEmployeeWithVariable($id: ID!) {
    getEmployees(id:$id) {
        name {
            firstname
            lastname
        }
    }
}

# Variables
{
    "id": 1
}
```

Ở đây, `$id: ID!` nghĩa là biến `id` là bắt buộc (`!`).

---

### Alias

---

GraphQL **không cho phép trả về nhiều property trùng tên**. Ví dụ dưới đây là **invalid** vì gọi `getProduct` hai lần:

```graphql
# Invalid query
query getProductDetails {
    getProduct(id: 1) {
        id
        name
    }
    getProduct(id: 2) {
        id
        name
    }
}
```

Để khắc phục, dùng **alias** để đặt tên khác cho từng instance:

```graphql
# Valid query with aliases
query getProductDetails {
    product1: getProduct(id: "1") {
        id
        name
    }
    product2: getProduct(id: "2") {
        id
        name
    }
}
```

```json
# Response
{
    "data": {
        "product1": {
            "id": 1,
            "name": "Juice Extractor"
        },
        "product2": {
            "id": 2,
            "name": "Fruit Overlays"
        }
    }
}
```

> 💡 
Với **mutations**, alias cho phép gửi nhiều yêu cầu trong **một HTTP request** → có thể lợi dụng để **bypass rate limit**.
> 

---

### Fragments

---

**Fragments** là các phần tái sử dụng của query hoặc mutation, chứa một tập hợp fields thuộc về một type. Khi thay đổi fragment, mọi query gọi đến nó cũng được thay đổi theo.

**Ví dụ**:

```graphql
# Define fragment
fragment productInfo on Product {
    id
    name
    listed
}

# Query using fragment
query {
    getProduct(id: 1) {
        ...productInfo
        stock
    }
}
```

```json
# Response
{
    "data": {
        "getProduct": {
            "id": 1,
            "name": "Juice Extractor",
            "listed": "no",
            "stock": 5
        }
    }
}
```

---

## Subscriptions

---

**Subscriptions** là một loại query đặc biệt. Chúng cho phép **client thiết lập kết nối lâu dài** với server, nhờ đó server có thể **đẩy dữ liệu cập nhật theo thời gian thực** đến client mà không cần client phải liên tục gửi request để hỏi (polling).

👉 Subscriptions đặc biệt hữu ích khi:

- Có **các thay đổi nhỏ** trên các object lớn.
- Các chức năng yêu cầu **cập nhật theo thời gian thực**, ví dụ: hệ thống chat, cộng tác trực tuyến (collaborative editing).

Giống như **queries** và **mutations**, request subscription cũng **xác định cấu trúc dữ liệu** sẽ được trả về.

Trong thực tế, **Subscriptions thường được triển khai bằng WebSockets**, giúp duy trì kết nối 2 chiều giữa client và server.

---

## **Introspection**

---

**Introspection** là một chức năng tích hợp sẵn trong GraphQL, cho phép bạn **truy vấn server để lấy thông tin về schema**. Nó thường được sử dụng bởi các ứng dụng như **GraphQL IDEs** (ví dụ: GraphiQL, Apollo Studio) hoặc các công cụ tự động sinh tài liệu API.

Tương tự như query thông thường, bạn có thể chỉ định các **fields** và **cấu trúc phản hồi** mà bạn muốn nhận. Ví dụ: bạn có thể yêu cầu phản hồi chỉ chứa **tên của các mutation khả dụng**.

> ⚠️ **Lưu ý**
Tuy nhiên, introspection cũng tiềm ẩn **nguy cơ rò rỉ thông tin nghiêm trọng**, vì kẻ tấn công có thể lợi dụng để thu thập các thông tin nhạy cảm (như mô tả field, kiểu dữ liệu, quan hệ giữa các object…) và từ đó học cách tương tác với API.
> 

👉 Do đó, **best practice** là nên **tắt introspection trong môi trường production**, chỉ bật khi cần cho mục đích phát triển hoặc kiểm thử.

---

# Tìm kiếm endpoint

---

Trước khi kiểm thử một API GraphQL, bạn cần **tìm endpoint** của nó. Vì API GraphQL sử dụng **một endpoint chung cho tất cả các yêu cầu**, nên biết được endpoint này là thông tin rất quan trọng.

> **Ghi chú**
> 
> 
> Phần này giải thích cách **dò tìm điểm cuối GraphQL thủ công**. Tuy nhiên, Burp Scanner có thể **tự động** kiểm tra các điểm cuối GraphQL trong quá trình quét. Nếu phát hiện được bất kỳ điểm cuối nào, nó sẽ sinh ra một issue có tên **"GraphQL endpoint found"**.
> 

---

## Truy vấn tổng quát

---

Nếu bạn gửi `query{__typename}` đến bất kỳ endpoint GraphQL nào, phản hồi sẽ chứa chuỗi `{"data": {"__typename": "query"}}` ở đâu đó trong kết quả. Điều này được gọi là **truy vấn phổ quát**, và là một công cụ hữu ích để dò xem một URL có tương ứng với dịch vụ GraphQL hay không.

Truy vấn hoạt động vì mọi endpoint GraphQL đều có một trường dành riêng tên là `__typename` trả về kiểu của đối tượng được truy vấn dưới dạng chuỗi.

---

## Endpoint mặc định

---

Các dịch vụ GraphQL thường sử dụng những hậu tố endpoint tương tự nhau. Khi kiểm thử để tìm endpoint GraphQL, bạn nên thử gửi **universal query** tới các vị trí sau:

- `/graphql`
- `/api`
- `/api/graphql`
- `/graphql/api`
- `/graphql/graphql`

Nếu các endpoint phổ biến này không trả về phản hồi GraphQL, bạn cũng có thể thử thêm hậu tố `/v1` vào đường dẫn.

> **Lưu ý**
> 
> 
> Các dịch vụ GraphQL thường sẽ phản hồi với thông báo lỗi như **"query not present"** hoặc tương tự nếu nhận được một yêu cầu không phải GraphQL. Bạn nên ghi nhớ điều này khi thử nghiệm để tránh nhầm lẫn.
> 

---

## Request methods

---

Bước tiếp theo khi cố gắng tìm endpoint GraphQL là thử với các **request methods** khác nhau.

Thực tiễn tốt nhất cho các endpoint GraphQL trong môi trường production là **chỉ chấp nhận yêu cầu POST** với **Content-Type là `application/json`**, vì điều này giúp giảm rủi ro lỗ hổng CSRF. Tuy nhiên, một số endpoint có thể chấp nhận các phương thức thay thế, như **GET** hoặc **POST** với Content-Type là `application/x-www-form-urlencoded`.

Nếu bạn không tìm thấy endpoint GraphQL bằng cách gửi các yêu cầu POST tới các endpoint phổ biến, hãy thử gửi lại **universal query** bằng các **phương thức HTTP khác**.

---

## Kiểm thử ban đầu

---

Khi bạn đã xác định được endpoint, bạn có thể gửi một vài yêu cầu kiểm thử để hiểu thêm cách nó hoạt động. Nếu endpoint đang phục vụ một trang web, hãy thử **duyệt giao diện web bằng trình duyệt của Burp** và sử dụng **lịch sử HTTP** để xem xét các truy vấn đã được gửi.

---

# Khai thác tham số chưa được lọc

---

Ở bước này, bạn có thể bắt đầu tìm kiếm các lỗ hổng. Kiểm thử các **argument** của truy vấn là một nơi tốt để bắt đầu.

Nếu API sử dụng argument để truy cập trực tiếp các đối tượng, nó có thể dễ bị **lỗ hổng kiểm soát truy cập**. Người dùng có thể truy cập thông tin mà họ không được phép chỉ bằng cách cung cấp một argument tương ứng với thông tin đó. Điều này đôi khi được biết đến là **Insecure Direct Object Reference (IDOR)**.

> **Thông tin thêm**
> 
> - Để hiểu chung về argument trong GraphQL, xem *Arguments*.
> - Để biết thêm về IDOR, xem *Insecure direct object references (IDOR)*.

Ví dụ, truy vấn dưới đây yêu cầu danh sách sản phẩm cho một cửa hàng trực tuyến:

```graphql
#Example product query

query {
    products {
        id
        name
        listed
    }
}
```

Danh sách sản phẩm trả về chỉ chứa các sản phẩm đang được liệt kê (listed).

```json
#Example product response

{
    "data": {
        "products": [
            {
                "id": 1,
                "name": "Product 1",
                "listed": true
            },
            {
                "id": 2,
                "name": "Product 2",
                "listed": true
            },
            {
                "id": 4,
                "name": "Product 4",
                "listed": true
            }
        ]
    }
}
```

Từ thông tin này, ta có thể suy ra:

- Các sản phẩm được gán ID tuần tự.
- Product có ID 3 không có trong danh sách, có thể vì nó đã bị gỡ (delisted).
- Bằng cách truy vấn ID của sản phẩm bị thiếu, ta có thể lấy được chi tiết của nó, mặc dù nó không được liệt kê trên cửa hàng và không được trả về trong truy vấn sản phẩm ban đầu.

```graphql
#Query to get missing product

query {
    product(id: 3) {
        id
        name
        listed
    }
}
```

```json
#Missing product response

{
    "data": {
        "product": {
        "id": 3,
        "name": "Product 3",
        "listed": no
        }
    }
}
```

---

# Khai thác schema

---

Bước tiếp theo trong việc kiểm thử API là tổng hợp thông tin về **schema**.

Cách tốt nhất để làm điều này là sử dụng các truy vấn **introspection**. **Introspection** là một chức năng tích hợp sẵn của GraphQL cho phép bạn truy vấn máy chủ để lấy thông tin về **schema**.

**Introspection** giúp bạn hiểu cách tương tác với một API GraphQL. Nó cũng có thể tiết lộ các dữ liệu nhạy cảm tiềm ẩn, chẳng hạn như các trường mô tả (description).

---

## Introspection

---

Để dùng introspection nhằm khám phá thông tin schema, hãy truy vấn trường `__schema`. Trường này có sẵn trên root type của tất cả các query.

Giống như các truy vấn thông thường, bạn có thể chỉ định các field và cấu trúc phản hồi mà bạn muốn nhận khi chạy một introspection query. Ví dụ, bạn có thể yêu cầu phản hồi chỉ chứa **tên** của các mutation khả dụng.

> **Ghi chú**
> 
> 
> Burp có thể tự sinh các introspection query cho bạn. Để biết thêm, xem *Accessing GraphQL API schemas using introspection*.
> 

---

## Thăm dò

---

Phòng thủ tốt nhất là **tắt introspection** trong môi trường production, nhưng khuyến nghị này không phải lúc nào cũng được tuân thủ.

Bạn có thể thăm dò introspection bằng truy vấn đơn giản sau. Nếu introspection được bật, phản hồi sẽ trả về **tên của tất cả các query** khả dụng.

```json
# Introspection probe request

{
    "query": "{__schema{queryType{name}}}"
}
```

> **Ghi chú**
> 
> 
> Burp Scanner có thể tự động kiểm tra introspection trong quá trình quét. Nếu phát hiện introspection được bật, nó sẽ báo một issue có tên **"GraphQL introspection enabled"**.
> 

---

## Truy vấn Introspection

---

Bước tiếp theo là chạy một **truy vấn introspection đầy đủ** với endpoint để thu thập càng nhiều thông tin về **schema** bên dưới càng tốt.

Ví dụ truy vấn dưới đây sẽ trả về đầy đủ chi tiết về tất cả **queries, mutations, subscriptions, types, và fragments**:

```graphql
# Full introspection query

query IntrospectionQuery {
    __schema {
        queryType {
            name
        }
        mutationType {
            name
        }
        subscriptionType {
            name
        }
        types {
            ...FullType
        }
        directives {
            name
            description
            args {
                ...InputValue
            }
            onOperation  #Often needs to be deleted to run query
            onFragment   #Often needs to be deleted to run query
            onField      #Often needs to be deleted to run query
        }
    }
}

fragment FullType on __Type {
    kind
    name
    description
    fields(includeDeprecated: true) {
        name
        description
        args {
            ...InputValue
        }
        type {
            ...TypeRef
        }
        isDeprecated
        deprecationReason
    }
    inputFields {
        ...InputValue
    }
    interfaces {
        ...TypeRef
    }
    enumValues(includeDeprecated: true) {
        name
        description
        isDeprecated
        deprecationReason
    }
    possibleTypes {
        ...TypeRef
    }
}

fragment InputValue on __InputValue {
    name
    description
    type {
        ...TypeRef
    }
    defaultValue
}

fragment TypeRef on __Type {
    kind
    name
    ofType {
        kind
        name
        ofType {
            kind
            name
            ofType {
                kind
                name
            }
        }
    }
}
```

> **Lưu ý**
> 
> 
> Nếu introspection được bật nhưng truy vấn trên không chạy, hãy thử **xóa các directive** `onOperation`, `onFragment`, và `onField` khỏi cấu trúc truy vấn. Nhiều endpoint không chấp nhận những directive này trong introspection query, và việc loại bỏ chúng thường giúp truy vấn thành công hơn.
> 

---

## Trực quan hóa

---

Phản hồi từ introspection query thường chứa rất nhiều thông tin, nhưng thường rất dài và khó xử lý thủ công.

Để dễ dàng hơn, bạn có thể dùng **GraphQL visualizer** – một công cụ trực tuyến có khả năng:

- Nhận kết quả từ introspection query.
- Sinh ra **biểu diễn trực quan** của dữ liệu trả về.
- Hiển thị rõ các **mối quan hệ giữa operations và types**.

👉 Cách này giúp bạn nhanh chóng hiểu cấu trúc schema và cách các entity trong GraphQL API liên kết với nhau.

---

## Suggestions

---

Ngay cả khi introspection bị tắt hoàn toàn, đôi khi bạn vẫn có thể thu thập thông tin về cấu trúc API bằng cách khai thác **suggestions**.

**Suggestions** là một tính năng của nền tảng **Apollo GraphQL**, trong đó server có thể gợi ý chỉnh sửa truy vấn trong thông báo lỗi. Điều này thường xảy ra khi một query hơi sai nhưng vẫn “nhận diện được”.

Ví dụ:

```
There is no entry for 'productInfo'. Did you mean 'productInformation' instead?
```

⚠️ Từ phản hồi như vậy, bạn có thể suy ra được các phần hợp lệ của schema.

- **Clairvoyance** là một công cụ có thể khai thác suggestions để **tự động khôi phục toàn bộ hoặc một phần schema GraphQL**, ngay cả khi introspection bị vô hiệu hóa → giúp tiết kiệm rất nhiều thời gian so với việc thu thập thủ công từ phản hồi lỗi.
- Trong Apollo, bạn **không thể tắt suggestions trực tiếp**. Tuy nhiên, có một số cách workaround được thảo luận trên GitHub.

> **Ghi chú**
> 
> 
> Burp Scanner có thể tự động kiểm tra **suggestions** trong quá trình quét. Nếu phát hiện suggestions đang bật, nó sẽ báo issue **"GraphQL suggestions enabled"**.
> 

[Lab: Accessing private GraphQL posts | Web Security Academy](https://portswigger.net/web-security/graphql/lab-graphql-reading-private-posts)

[Lab: Accidental exposure of private GraphQL fields | Web Security Academy](https://portswigger.net/web-security/graphql/lab-graphql-accidental-field-exposure)

---

# Bypass phòng thủ Introspection

---

Nếu bạn không thể chạy được các truy vấn introspection trên API đang kiểm thử, hãy thử **chèn một ký tự đặc biệt** ngay sau từ khóa `__schema`.

Khi developer vô hiệu hóa introspection, họ có thể dùng một biểu thức chính quy (regex) để loại trừ từ khóa `__schema` trong các truy vấn. Bạn nên thử các ký tự như **dấu cách**, **xuống dòng** và **dấu phẩy**, vì những ký tự này bị GraphQL bỏ qua nhưng có thể không bị một regex kém chính xác xử lý đúng.

Do đó, nếu developer chỉ loại trừ `__schema{`, thì truy vấn introspection dưới đây sẽ **không** bị loại trừ:

```json
# Introspection query with newline

{
    "query": "query{__schema
    {queryType{name}}}"
}
```

Nếu cách này không hiệu quả, hãy thử chạy probe bằng **phương thức yêu cầu khác**, vì introspection có thể chỉ bị vô hiệu hóa khi dùng `POST`. Thử một yêu cầu `GET`, hoặc một `POST` với `Content-Type` là `x-www-form-urlencoded`.

Ví dụ dưới đây là probe introspection được gửi dưới dạng `GET`, với các tham số được mã hóa URL:

```
# Introspection probe as GET request

GET /graphql?query=query%7B__schema%0A%7BqueryType%7Bname%7D%7D%7D
```

> **Lưu ý**
> 
> 
> Bạn có thể lưu các truy vấn GraphQL vào **site map**. Để biết thêm, xem *Working with GraphQL*.
> 

[Lab: Finding a hidden GraphQL endpoint | Web Security Academy](https://portswigger.net/web-security/graphql/lab-graphql-find-the-endpoint)

---

# **Bypassing rate limiting bằng alias**

---

Thông thường, các đối tượng GraphQL không thể chứa nhiều thuộc tính cùng tên. **Aliases (bí danh)** cho phép bạn vượt qua hạn chế này bằng cách đặt tên rõ ràng cho các thuộc tính bạn muốn API trả về. Bạn có thể dùng aliases để trả về nhiều thực thể cùng loại trong một yêu cầu.

> **Thông tin thêm**
> 
> 
> Để biết thêm về aliases trong GraphQL, xem **Aliases**.
> 

Mục đích của aliases là giảm số lần gọi API cần thiết, nhưng chúng cũng có thể bị lợi dụng để thực hiện **brute-force** trên một endpoint GraphQL.

Nhiều endpoint sẽ có một cơ chế **giới hạn tần suất (rate limiter)** nhằm ngăn các cuộc tấn công brute-force. Một số bộ giới hạn tần suất hoạt động dựa trên **số lượng yêu cầu HTTP nhận được** thay vì số lượng **operation** được thực hiện trên endpoint. Vì aliases về cơ bản cho phép bạn gửi nhiều truy vấn trong **một thông điệp HTTP duy nhất**, chúng có thể **vượt qua** hạn chế này.

Ví dụ đơn giản dưới đây cho thấy một chuỗi các truy vấn được gán bí danh để kiểm tra liệu mã giảm giá (discount code) có hợp lệ hay không. Hoạt động này có thể vượt qua giới hạn tần suất vì nó là **một yêu cầu HTTP duy nhất**, mặc dù nó có thể được dùng để kiểm tra rất nhiều mã giảm giá cùng lúc.

```graphql
#Request with aliased queries

query isValidDiscount($code: Int) {
    isvalidDiscount(code:$code){
        valid
    }
    isValidDiscount2:isValidDiscount(code:$code){
        valid
    }
    isValidDiscount3:isValidDiscount(code:$code){
        valid
    }
}
```

[Lab: Bypassing GraphQL brute force protections | Web Security Academy](https://portswigger.net/web-security/graphql/lab-graphql-brute-force-protection-bypass)

---

# GraphQL CSRF

---

Tấn công giả mạo yêu cầu giữa các trang (Cross-site request forgery — CSRF) cho phép kẻ tấn công khiến người dùng thực hiện các hành động mà họ không chủ ý. Việc này được thực hiện bằng cách tạo một website độc hại làm giả một yêu cầu chéo miền tới ứng dụng dễ tổn thương.

> **Thông tin thêm**
> 
> 
> Để biết thêm về lỗ hổng CSRF nói chung, xem chủ đề *CSRF academy*.
> 

GraphQL có thể được lợi dụng làm vectơ cho các cuộc tấn công CSRF, trong đó kẻ tấn công tạo một exploit khiến trình duyệt của nạn nhân gửi một truy vấn độc hại với tư cách người dùng nạn nhân.

---

## **Phát sinh**

---

Lỗ hổng CSRF có thể phát sinh khi một endpoint GraphQL **không kiểm tra (validate) content-type của các yêu cầu** gửi tới nó và không triển khai token CSRF.

Các yêu cầu POST sử dụng content type `application/json` là an toàn trước việc giả mạo miễn là content-type được kiểm tra (validated). Trong trường hợp này, kẻ tấn công sẽ không thể khiến trình duyệt của nạn nhân gửi được yêu cầu này ngay cả khi nạn nhân truy cập một trang web độc hại.

Tuy nhiên, các phương thức thay thế như **GET**, hoặc bất kỳ yêu cầu nào có content type `application/x-www-form-urlencoded`, có thể được trình duyệt gửi và do đó có thể để lộ người dùng trước tấn công nếu endpoint chấp nhận các yêu cầu này. Trong trường hợp đó, kẻ tấn công có thể tạo exploit để gửi các yêu cầu độc hại tới API.

Các bước để cấu trúc một cuộc tấn công CSRF và triển khai exploit **không khác** so với CSRF “thông thường”. Để biết thêm về quy trình này, xem *How to construct a CSRF attack*.

[Lab: Performing CSRF exploits over GraphQL | Web Security Academy](https://portswigger.net/web-security/graphql/lab-graphql-csrf-via-graphql-api)

---

# Bảo mật

---

Để ngăn chặn nhiều hình thức tấn công phổ biến vào GraphQL, khi triển khai API ra môi trường production, bạn cần áp dụng các bước sau:

---

## Introspections

---

- Nếu API **không dành cho công khai**, hãy **tắt introspection**.
    
    Điều này khiến kẻ tấn công khó thu thập thông tin hơn và giảm rủi ro rò rỉ dữ liệu không mong muốn.
    
    Xem thêm cách vô hiệu hóa introspection trên Apollo GraphQL tại blog liên quan.
    
- Nếu API **công khai**, có thể cần giữ introspection **bật**.
    
    Trong trường hợp này, cần **xem xét schema cẩn thận** để đảm bảo không công khai các field không mong muốn.
    

---

## Suggestions

---

- Đảm bảo **tắt suggestions** để ngăn chặn kẻ tấn công khai thác bằng công cụ như **Clairvoyance** nhằm khôi phục schema.
- Trong Apollo, không thể tắt trực tiếp, nhưng có workaround được thảo luận trên GitHub.

---

## Dữ liệu nhạy cảm

---

Kiểm tra schema để chắc chắn rằng không có field riêng tư nào bị công khai, ví dụ: **email, user ID, token**.

---

## Bruteforce

---

GraphQL có thể bị lợi dụng để **bypass rate limiting**, ví dụ bằng cách dùng **aliases** để gửi nhiều truy vấn trong một request.

Để phòng chống, cần thực hiện các biện pháp thiết kế sau:

- **Giới hạn query depth**: kiểm soát số cấp độ lồng nhau trong một query. Query lồng quá sâu có thể ảnh hưởng hiệu năng và mở đường cho DoS.
- **Cấu hình operation limits**: giới hạn số lượng field, alias, và root field tối đa mà API chấp nhận.
- **Giới hạn kích thước truy vấn**: xác định số byte tối đa mà một query có thể chứa.
- **Thực hiện cost analysis**: đánh giá chi phí tài nguyên cho mỗi query khi nhận được. Nếu một query quá phức tạp, API sẽ từ chối.

---

## CSRF

---

Để bảo vệ khỏi **CSRF trong GraphQL**, cần đảm bảo:

- API **chỉ chấp nhận truy vấn qua POST với JSON-encoded (`application/json`)**.
- API **xác thực Content-Type** để khớp với dữ liệu thực tế.
- API triển khai cơ chế **CSRF token an toàn**.
