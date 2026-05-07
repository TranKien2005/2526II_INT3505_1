## 1. Phân tích hiện trạng (v1)
- **Endpoint**: `/v1/payments` (Đã được versioning ngay từ đầu - **Best Practice**).
- **Lợi ích của việc có /v1 ngay từ đầu**: 
    - Khi nâng cấp lên v2, ta chỉ cần thêm route `/v2/` mà không làm ảnh hưởng đến cấu trúc URL cũ của khách hàng.
    - Khách hàng không cần phải thay đổi code ngay lập tức để chuyển từ "không version" sang "có version".
- **Vấn đề cần nâng cấp**: 
    - Nhận trực tiếp `card_number` (Vi phạm bảo mật PCI-DSS).
    - Cấu trúc dữ liệu đơn giản, thiếu thông tin metadata.
    - Khó mở rộng mà không làm hỏng các tích hợp hiện có.

## 2. Thiết kế v2
- **Endpoint mới**: `/v2/payments`
- **Thay đổi chính**:
    - **Tokenization**: Thay `card_number` bằng `payment_token`.
    - **Metadata**: Thêm object `metadata` cho các thông tin bổ sung.
    - **Error Handling**: Chuẩn hóa mã lỗi và thông điệp trả về.

## 3. Lộ trình triển khai (Migration Strategy)
1. **Giai đoạn 1: Co-existence (Song song)**
    - Triển khai v2 đồng thời giữ nguyên v1.
    - Log lại toàn bộ các request gọi vào v1 để xác định developer nào chưa nâng cấp.
2. **Giai đoạn 2: Deprecation Warning**
    - Gửi thông báo cho developer qua email và thêm header `Warning: 299 - "v1 is deprecated"` vào phản hồi API v1.
3. **Giai đoạn 3: Sunset (Ngừng hỗ trợ)**
    - Sau 6 tháng (hoặc 1 năm), ngừng hỗ trợ v1 hoàn toàn.

---

# THÔNG BÁO: Kế hoạch ngừng hỗ trợ (Deprecation Notice) - Payment API v1

**Ngày thông báo**: 07/05/2026  
**Trạng thái**: DEPRECATED  
**Ngày Sunset dự kiến**: 07/11/2026

Chào các nhà phát triển,

Chúng tôi đang thực hiện một bước tiến lớn để tăng cường bảo mật và hiệu suất cho hệ thống thanh toán. Vì vậy, chúng tôi chính thức thông báo kế hoạch nâng cấp từ **Payment API v1** lên **Payment API v2**.

### Tại sao bạn nên nâng cấp?
- **Bảo mật tuyệt đối**: v2 sử dụng cơ chế Tokenization, giúp hệ thống của bạn không phải xử lý dữ liệu thẻ nhạy cảm (tuân thủ PCI-DSS).
- **Tính năng mới**: Hỗ trợ thanh toán đa tiền tệ và hoàn tiền một phần (partial refund).
- **Hiệu suất**: Tốc độ xử lý nhanh hơn 30% nhờ kiến trúc mới.

### Lộ trình (Timeline)
- **Nay - 07/11/2026**: Cả v1 và v2 đều hoạt động. Bạn nên bắt đầu chuyển sang v2 ngay lập tức.
- **07/08/2026**: Chúng tôi sẽ bắt đầu giới hạn tốc độ (rate limit) trên v1 để khuyến khích chuyển đổi.
- **07/11/2026**: Endpoint v1 sẽ chính thức ngừng hoạt động (Returns 410 Gone).

### Hướng dẫn chuyển đổi nhanh (Migration Guide)
1. **Thay đổi Endpoint**: Đổi từ `POST /payments` sang `POST /v2/payments`.
2. **Cập nhật dữ liệu gửi đi**:
   - **v1**: `{ "card_number": "1234..." }`
   - **v2**: `{ "payment_method_id": "pm_..." }` (Lấy từ bộ SDK Frontend của chúng tôi).

Vui lòng tham khảo tài liệu kỹ thuật đầy đủ tại: [docs.payment-api.com/v2](https://docs.payment-api.com/v2)

Nếu có bất kỳ câu hỏi nào, hãy liên hệ với đội ngũ hỗ trợ qua email: `api-support@example.com`.

Trân trọng,  
**Đội ngũ Kỹ thuật Payment System**
