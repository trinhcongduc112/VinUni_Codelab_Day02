# 01 — Problem Scan & Quick-Assess
### AI Engineer tại Vin Smart Future | Lab 02 — AI Product Scoping

---

## 🧑‍💻 Giới thiệu bản thân

Tôi là **AI Product Engineer** tại **Vin Smart Future** (vai trò mô phỏng trong lab), quét vận hành của các công ty thành viên Vingroup để tìm cơ hội tối ưu bằng AI. Điểm khởi đầu là quy trình ra viện ở bệnh viện: bác sĩ soạn tóm tắt xuất viện mất khoảng 20–30 phút mỗi ca *(ước tính)*, còn những việc còn dở sau khi bệnh nhân về — như kết quả xét nghiệm trả về muộn — thì không ai được giao theo dõi.

> Các con số nội bộ trong bài là **ước tính** để định hướng phép đo, không phải số liệu khảo sát tại các đơn vị. Số liệu công khai có nguồn ở cuối [02-deep-dive-report.md](02-deep-dive-report.md).

---

# 🔍 Phase 1 — SCAN: Tìm kiếm cơ hội

> Dùng **4 Lenses** để quét qua vận hành của các công ty thành viên Vingroup.

| # | Subsidiary | Lens | Mô tả ngắn bài toán |
|---|------------|------|---------------------|
| 1 | **Vinmec** | Tốn thời gian | Bác sĩ soạn thủ công tóm tắt xuất viện từ bệnh án điện tử — mất 20–30 phút/bệnh nhân *(ước tính)*; sau ra viện, kết quả xét nghiệm trả về muộn không có người được giao xem. |
| 2 | **Vinhomes** | Lặp lại | Nhân viên ban quản lý phân loại thủ công hàng trăm phản ánh cư dân gửi qua App Vinhomes Resident mỗi ngày và forward đến đúng bộ phận xử lý (chiếm 3–4 giờ làm việc/ngày, ước tính). |
| 3 | **VinFast** | AI có thể tốt hơn | Khách hàng mô tả triệu chứng lỗi xe bằng tiếng Việt tự nhiên (ví dụ: *"xe kêu cụp cụp ở bánh trước khi qua gờ giảm tốc"*), nhưng hệ thống chăm sóc khách hàng không tự động phân loại mã lỗi kỹ thuật — dẫn đến xếp sai chuyên viên sửa chữa. |
| 4 | **Xanh SM** | Pain từ người khác | Tài xế phàn nàn rằng hệ thống gợi ý điểm đón không xét đến kẹt xe thực tế — tài xế phải tự đánh giá và từ chối chuyến, gây mất cuốc và ảnh hưởng KPI. |
| 5 | **Vinpearl** | Tốn thời gian | Nhân viên booking đọc thủ công email đặt phòng theo đoàn (Group Booking) từ các công ty lữ hành — mỗi email dài 1–2 trang, cần trích xuất tay số phòng, ngày check-in/out, loại phòng và yêu cầu đặc biệt. |
| 6 | **Vinmec** | Pain từ người khác | Bệnh nhân phàn nàn bị xếp nhầm chuyên khoa khi đặt lịch khám qua tổng đài — do nhân viên tiếp nhận không có chuyên môn y tế để phân loại triệu chứng chính xác. |

---

# 🃏 Phase 2 — QUICK-ASSESS: 3 Quick Problem Cards

> Chọn **Top 3** từ danh sách SCAN: **#1 (Vinmec Ra viện không khe hở), #2 (Vinhomes Phân loại phản ánh), #6 (Vinmec Phân loại chuyên khoa).**

---

## 🃏 Card #1 — Vinmec: Ra viện không khe hở

```text
┌─────────────────────────────────────────────────────────────┐
│ QUICK PROBLEM CARD #1                                       │
│                                                             │
│ Bài toán: Thông tin chuyển tiếp lúc ra viện bị chậm, thiếu  │
│ và đứt quãng: bác sĩ mất ~30 phút/ca soạn 2 bản, dễ bỏ sót; │
│ việc còn dở (kết quả chờ, khuyến nghị theo dõi) không có    │
│ người nhận sau khi bệnh nhân về.                            │
│ Công ty thành viên: [x] Vinmec                              │
│                                                             │
│ Ai đang đau (Actor)?                                        │
│   Bác sĩ điều trị khoa Nội (soạn, ký); bệnh nhân và bác sĩ  │
│   tái khám (nhận thông tin thiếu hoặc muộn).                │
│                                                             │
│ Workflow thủ công hiện tại (5 bước):                        │
│   1. Rà hồ sơ trên HIS (chẩn đoán, thuốc, XN, CĐHA)         │
│   → 2. Soạn tóm tắt cho bác sĩ                              │
│   → 3. Soạn hướng dẫn dễ hiểu cho bệnh nhân                 │
│   → 4. Ký, in, giao giấy ra viện                            │
│   → 5. Kết quả về sau ra viện: không ai được giao xem       │
│                                                             │
│ Bước nào tốn nhất? Bước 1–3 (~28 phút/ca, ước tính)         │
│ Bước nào rủi ro nhất? Bước 5 (kết quả về không ai nhận)     │
│ AI có thể nhảy vào hỗ trợ ở đâu?                            │
│   Trích dữ kiện hằng ngày (bác sĩ xác nhận) → tìm việc dở   │
│   ẩn trong văn bản → viết bản cho bệnh nhân → gợi ý ưu      │
│   tiên khi kết quả về. Rule: đối chiếu bỏ sót, theo dõi     │
│   việc còn mở đến khi đóng.                                 │
│                                                             │
│ Metric thành công?                                          │
│   Thời gian bác sĩ/ca: ~30 phút → ≤ 10 phút.                │
│   ≥ 95% kết quả về sau ra viện được xác nhận trong 72 giờ.  │
│   0 lỗi nghiêm trọng trong giấy ra viện đã ký.              │
│                                                             │
│ Quick Architecture: [ ] No AI  [x] Rule  [x] LLM  [ ] Agent │
└─────────────────────────────────────────────────────────────┘
```

**⚡ Stress-Test (đóng vai CFO và Trưởng phòng Vận hành phản biện)** — 3 điểm yếu theo đúng 3 góc của worksheet:
- *Logic:* "Viết nhanh hơn không sửa được việc giấy ra viện đến muộn và kết quả bị bỏ quên." → **Đã sửa:** card chuyển trọng tâm từ *viết* sang *khép vòng*; mọi việc còn mở có người phụ trách và hạn chót.
- *Metric:* "30 phút/ca chưa ai đo." → **Đúng, đây là ước tính:** phải đo baseline ít nhất 2 tuần bằng audit log HIS trước khi pilot.
- *Rule-based có tốt hơn không?* "Kết quả chờ đã nằm trong y lệnh thì rule báo được." → **Đúng một phần:** rule giữ phần có cấu trúc (email báo kết quả chờ đã được thử nghiệm từ 2014); LLM chỉ dùng cho khuyến nghị theo dõi nằm trong văn bản tự do, và chỉ được giữ nếu tìm thêm được việc còn mở so với chỉ dùng rule.

---

## 🃏 Card #2 — Vinhomes: AI Phân loại & Route Phản ánh Cư dân

```text
┌─────────────────────────────────────────────────────────────┐
│ QUICK PROBLEM CARD #2                                       │
│                                                             │
│ Bài toán: Nhân viên BQL Vinhomes mất 3–4 giờ/ngày phân     │
│ loại thủ công 200–500 phản ánh cư dân từ App & Hotline      │
│ và forward đến đúng bộ phận xử lý.                          │
│ Công ty thành viên: [x] Vinhomes                            │
│                                                             │
│ Ai đang đau (Actor)?                                        │
│   Nhân viên CSKH Ban Quản lý tòa nhà Vinhomes Smart City    │
│   (2–3 nhân viên/ca x 3 ca/ngày/tòa nhà).                  │
│                                                             │
│ Workflow thủ công hiện tại (4 bước):                        │
│   1. Nhân viên đọc từng phản ánh từ App / nghe lại gọi     │
│   → 2. Phân loại danh mục (điện, nước, thang máy, ANTT...) │
│   → 3. Gán độ ưu tiên (khẩn cấp / bình thường)             │
│   → 4. Forward ticket đến đúng kỹ thuật viên / bộ phận     │
│                                                             │
│ Bước nào tốn nhất? Bước 1–2 (⏱ 2 phút/ticket x 300 vé)    │
│ AI có thể nhảy vào hỗ trợ ở đâu? Bước 1–3:                 │
│   Auto-classify → Auto-prioritize → Human confirm & route   │
│                                                             │
│ Metric thành công?                                          │
│   Tỉ lệ phân loại đúng danh mục ≥ 95%.                      │
│   Giảm thời gian xử lý ticket từ trung bình 4 giờ → 30 phút│
│                                                             │
│ Quick Architecture: [x] LLM Feature + Rule Router           │
└─────────────────────────────────────────────────────────────┘
```

---

## 🃏 Card #3 — Vinmec: AI Phân loại Chuyên khoa Khám ban đầu

```text
┌─────────────────────────────────────────────────────────────┐
│ QUICK PROBLEM CARD #3                                       │
│                                                             │
│ Bài toán: Bệnh nhân đặt khám qua tổng đài Vinmec bị xếp    │
│ nhầm chuyên khoa do nhân viên không có chuyên môn phân loại │
│ triệu chứng y tế chính xác.                                 │
│ Công ty thành viên: [x] Vinmec                              │
│                                                             │
│ Ai đang đau (Actor)?                                        │
│   Nhân viên tiếp nhận tổng đài đặt lịch Vinmec (10–15 cuộc │
│   gọi/giờ), Bệnh nhân (xếp nhầm khoa, phải đổi lịch lại).  │
│                                                             │
│ Workflow thủ công hiện tại (4 bước):                        │
│   1. Bệnh nhân gọi điện mô tả triệu chứng bằng tiếng Việt  │
│   → 2. Nhân viên tự phán đoán chuyên khoa từ mô tả         │
│   → 3. Đặt lịch vào hệ thống HIS Vinmec                    │
│   → 4. Bệnh nhân đến, bác sĩ phát hiện nhầm khoa → đổi lịch│
│                                                             │
│ Bước nào tốn nhất? Bước 2 (⏱ 3–5 phút/cuộc)               │
│   + Tỉ lệ nhầm khoa: 15–20% → gây đổi lịch, giảm hài lòng │
│ AI có thể nhảy vào hỗ trợ ở đâu? Bước 2:                   │
│   AI phân tích triệu chứng → Gợi ý Top 3 chuyên khoa       │
│   → Nhân viên confirm và đặt lịch chính xác hơn             │
│                                                             │
│ Metric thành công?                                          │
│   Giảm tỉ lệ nhầm khoa từ 18% xuống dưới 5%.               │
│   Thời gian xử lý cuộc gọi đặt lịch giảm từ 5 phút → 2 phút│
│                                                             │
│ Quick Architecture: [x] LLM Feature                        │
└─────────────────────────────────────────────────────────────┘
```

---

## 🗳️ Quyết định lựa chọn bài toán cho Deep-Dive

> **Nhóm chọn Card #1 — Vinmec: Ra viện không khe hở** để thực hiện Phase 3.

**Lý do chọn Card #1** (mỗi lý do ứng với một tiêu chí, không chồng lấn):
- **Mức nghiêm trọng:** ảnh hưởng trực tiếp đến an toàn người bệnh — 41% bệnh nhân ra viện khi còn kết quả chờ, khoảng 9% số kết quả đó có thể làm thay đổi điều trị (nghiên cứu ở Mỹ, cần đo lại tại Vinmec).
- **Dữ liệu:** bệnh án điện tử đã bắt buộc tại bệnh viện chậm nhất từ 30/9/2025, nên dữ liệu có cấu trúc nhiều khả năng đã có.
- **Vai trò của AI:** có phần việc rule không làm được — đọc khuyến nghị theo dõi nằm trong văn bản tự do.
- **Kiểm soát rủi ro:** AI chỉ được thêm cảnh báo, không được xóa; bác sĩ xác nhận và ký mọi thứ trước khi đến tay bệnh nhân.

**Lý do loại bỏ các thẻ khác** (mỗi thẻ một lý do chính):
- **Card #2 (Vinhomes):** phần lớn có thể giải quyết bằng rule-based router + từ khóa *(ước tính ~80%)* → chưa cần LLM.
- **Card #3 (Vinmec):** gợi ý chuyên khoa là quyết định lâm sàng ngay ở đầu vào, sai thì khó kiểm soát hậu quả; cần dữ liệu lịch sử lớn để đánh giá trước khi làm.
