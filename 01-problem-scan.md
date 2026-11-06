# Problem Scan — Trợ lý điều phối sự cố pin Xanh SM

Bài làm Lab 02 — AI Product Scoping. Vai trò mô phỏng: AI Product Engineer tại Vin Smart Future.

> Phạm vi học tập: các quy trình, lưu lượng và thời gian bên dưới là **giả định để scoping**, chưa được xác nhận bởi doanh nghiệp. Không có khảo sát thực địa hay dữ liệu nội bộ. Không coi nội dung tình huống trong đề là thông tin doanh nghiệp đã được kiểm chứng.

## Phase 1 — SCAN

| # | Đơn vị theo đề bài | Lens | Bài toán và điểm nghẽn giả định |
|---|---|---|---|
| 1 | Xanh SM | Tốn thời gian; Stakeholder Pain | Điều phối viên phải đọc báo cáo sự cố pin, kiểm tra thông tin trạm và soạn phản hồi; tài xế chờ hỗ trợ. |
| 2 | VinFast | Lặp lại | Nhân viên đối chiếu từng phiên sạc với hóa đơn đối tác; lệch mã giao dịch cần kiểm tra tay. |
| 3 | Vinhomes | AI-upgrade; Lặp lại | Phản ánh cư dân viết tự do khiến nhân viên phải đọc và chọn đội xử lý thủ công. |
| 4 | Vinpearl | Stakeholder Pain | Quản lý đọc nhiều review để tìm cụm phàn nàn về vệ sinh và thái độ phục vụ. |
| 5 | Vinmec | Tốn thời gian | Nhân viên hành chính đọc yêu cầu đổi lịch và nhập lại thông tin; không bao gồm phân loại triệu chứng. |
| 6 | Xanh SM | AI-upgrade | Tổng hợp lý do hủy chuyến từ ghi chú tự do để tìm lỗi trải nghiệm thường gặp. |

Đủ bốn lenses. Không suy ra các điểm nghẽn trên đang thực sự xảy ra tại các đơn vị.

## Phase 2 — QUICK-ASSESS

### Card #1 — Xanh SM: soạn đề xuất hỗ trợ sự cố pin

- **Bài toán:** Giảm thời gian chuẩn bị đề xuất xử lý sự cố pin mà vẫn giữ quyền quyết định ở điều phối viên.
- **Actor:** Điều phối viên trực ca; tài xế chịu thời gian chờ.
- **Workflow 5 bước:** Nhận báo cáo (2 phút) → xác minh pin/vị trí (2 phút) → tra dữ liệu trạm (4 phút) → soạn đề xuất (4 phút) → duyệt, gửi và ghi log (3 phút).
- **Bottleneck:** Tra cứu và soạn nháp, 8/15 phút mỗi lượt.
- **AI hỗ trợ:** Đọc mô tả tiếng Việt và soạn nháp từ dữ liệu đã xác minh; không tự điều xe.
- **Metric mục tiêu:** Median thời gian tiếp nhận đến gửi ≤6 phút thay vì baseline giả định 15 phút; ≥95% action đúng trên tập đánh giá; 100% thông báo phải qua người duyệt.
- **Quick Architecture:** Rule + LLM Feature. Rule kiểm dữ liệu; LLM soạn nháp; không dùng Agent tự trị.
- **Dữ liệu cần:** Báo cáo đã ẩn danh, telemetry pin, danh mục trạm và khả năng tương thích đã xác minh.

### Card #2 — VinFast: đối chiếu hóa đơn sạc

- **Bài toán:** Giảm công sức đối chiếu phiên sạc và hóa đơn.
- **Actor:** Nhân viên kế toán đối soát.
- **Workflow 4 bước:** Xuất bảng phiên sạc (5 phút/lô) → chuẩn hóa mã (10 phút) → ghép hóa đơn (20 phút) → rà chênh lệch, duyệt (10 phút).
- **Bottleneck:** Ghép và rà sai lệch, 30/45 phút mỗi lô giả định 100 phiên.
- **Điểm hỗ trợ:** SQL/rule join theo transaction ID; LLM chỉ có thể diễn giải ghi chú ngoại lệ.
- **Metric mục tiêu:** Median ≤15 phút/lô; 100% giao dịch không ghép được phải vào danh sách đối soát tay; không tự phê duyệt thanh toán.
- **Quick Architecture:** Rule; chưa cần LLM cho dữ liệu bảng chuẩn.
- **Dữ liệu cần:** Hai bảng có khóa đối chiếu ổn định; chưa có dữ liệu thật.

### Card #3 — Vinhomes: gợi ý phân loại phản ánh

- **Bài toán:** Giảm thời gian đọc và gán nhãn phản ánh về điện, nước, vệ sinh.
- **Actor:** Nhân viên CSKH và đội vận hành nhận việc.
- **Workflow 4 bước:** Nhận ticket (1 phút) → đọc, tìm địa điểm (3 phút) → chọn đội phụ trách (2 phút) → kiểm tra và chuyển (2 phút).
- **Bottleneck:** Hiểu mô tả tự do và chọn đội, 5/8 phút mỗi ticket.
- **AI hỗ trợ:** Gợi ý nhãn từ danh mục đóng; nhân viên xác nhận trước khi chuyển.
- **Metric mục tiêu:** Median ≤3 phút/ticket; macro-F1 ≥0,90 trên 200 ticket đã gán nhãn; 100% nội dung khẩn cấp chuyển người trực.
- **Quick Architecture:** Rule + LLM Feature; bỏ ngoài scope phí, tranh chấp và lời khuyên pháp lý.
- **Dữ liệu cần:** Ticket ẩn danh, danh mục đội và tiêu chí khẩn cấp do vận hành duyệt.

## Lựa chọn và phản biện

Chọn **Card #1** vì có thể kiểm thử ranh giới bằng dữ liệu tổng hợp và khớp starter code. Đây là lựa chọn bài lab, không khẳng định đã có business case được doanh nghiệp duyệt.

| Phản biện của CFO / Vận hành | Điều chỉnh phạm vi |
|---|---|
| Con số 15 phút có được đo chưa? | Ghi rõ giả định; yêu cầu đo ít nhất 50 lượt thực trước pilot. |
| Vì sao không dùng mẫu tin và rule? | Giữ rule làm baseline; chỉ giữ LLM nếu xử lý mô tả đa dạng tốt hơn với chi phí hợp lý. |
| AI gợi ý sai có làm tài xế gặp nguy hiểm? | Chỉ nháp; không kết nối công cụ gửi/điều xe; dữ liệu thiếu thì chuyển người. |

Card #2 ưu tiên rule vì khóa đối chiếu xác định. Card #3 cần taxonomy và dữ liệu gán nhãn trước. Không loại bỏ hai card này chỉ vì chúng ít phức tạp hơn.
