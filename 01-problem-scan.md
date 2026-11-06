# 01 — Problem Scan & Quick-Assess
### AI Engineer tại Vin Smart Future | Lab 02 — AI Product Scoping

---

## 🧑‍💻 Giới thiệu bản thân

Tôi là **AI Product Engineer** tại **Vin Smart Future**. Trong tuần vừa qua, tôi được phân công khảo sát quy trình vận hành tại **Vinmec International Hospital** (Hà Nội) và **Vinhomes Smart City** để tìm kiếm các cơ hội tối ưu hóa bằng AI.

Qua quan sát thực tế tại khoa Nội tổng quát Vinmec, tôi nhận thấy các bác sĩ đang dành 20–30 phút mỗi ca để soạn thủ công **Tóm tắt hồ sơ xuất viện (Discharge Summary)** — một tác vụ lặp đi lặp lại, tốn nhiều thời gian nhưng có thể cấu trúc hóa rõ ràng. Đây là điểm khởi đầu tôi mang vào buổi Lab.

---

# 🔍 Phase 1 — SCAN: Tìm kiếm cơ hội

> Dùng **4 Lenses** để quét qua vận hành của các công ty thành viên Vingroup.

| # | Subsidiary | Lens | Mô tả ngắn bài toán |
|---|------------|------|---------------------|
| 1 | **Vinmec** | Tốn thời gian | Bác sĩ soạn thủ công Tóm tắt xuất viện (Discharge Summary) từ bệnh án điện tử — mất 20–30 phút/bệnh nhân, gây quá tải khi khoa có 15–20 lượt xuất viện/ngày. |
| 2 | **Vinhomes** | Lặp lại | Nhân viên ban quản lý phân loại thủ công hàng trăm phản ánh cư dân gửi qua App Vinhomes Resident mỗi ngày và forward đến đúng bộ phận xử lý (chiếm 3–4 giờ làm việc/ngày). |
| 3 | **VinFast** | AI có thể tốt hơn | Khách hàng mô tả triệu chứng lỗi xe bằng tiếng Việt tự nhiên (ví dụ: *"xe kêu cụp cụp ở bánh trước khi qua gờ giảm tốc"*), nhưng hệ thống chăm sóc khách hàng không tự động phân loại mã lỗi kỹ thuật — dẫn đến xếp sai chuyên viên sửa chữa. |
| 4 | **Xanh SM** | Pain từ người khác | Tài xế phàn nàn rằng hệ thống gợi ý điểm đón không xét đến kẹt xe thực tế — tài xế phải tự đánh giá và từ chối chuyến, gây mất cuốc và ảnh hưởng KPI. |
| 5 | **Vinpearl** | Tốn thời gian | Nhân viên booking đọc thủ công email đặt phòng theo đoàn (Group Booking) từ các công ty lữ hành — mỗi email dài 1–2 trang, cần trích xuất tay số phòng, ngày check-in/out, loại phòng và yêu cầu đặc biệt. |
| 6 | **Vinmec** | Pain từ người khác | Bệnh nhân phàn nàn bị xếp nhầm chuyên khoa khi đặt lịch khám qua tổng đài — do nhân viên tiếp nhận không có chuyên môn y tế để phân loại triệu chứng chính xác. |

---

# 🃏 Phase 2 — QUICK-ASSESS: 3 Quick Problem Cards

> Chọn **Top 3** từ danh sách SCAN: **#1 (Vinmec Discharge Summary), #2 (Vinhomes Phân loại phản ánh), #6 (Vinmec Phân loại chuyên khoa).**

---

## 🃏 Card #1 — Vinmec: AI Soạn thảo Tóm tắt Xuất viện

```text
┌─────────────────────────────────────────────────────────────┐
│ QUICK PROBLEM CARD #1                                       │
│                                                             │
│ Bài toán: Bác sĩ Vinmec mất 20–30 phút soạn thủ công       │
│ Discharge Summary mỗi lượt xuất viện từ bệnh án điện tử.    │
│ Công ty thành viên: [x] Vinmec                              │
│                                                             │
│ Ai đang đau (Actor)?                                        │
│   Bác sĩ nội trú / Điều dưỡng trưởng khoa Nội, Ngoại tổng  │
│   quát tại Vinmec (5–8 bác sĩ/khoa x 2 ca/ngày).           │
│                                                             │
│ Workflow thủ công hiện tại (5 bước):                        │
│   1. Bác sĩ mở bệnh án điện tử (HIS) xem chẩn đoán, thuốc  │
│   → 2. Đọc lại kết quả xét nghiệm, hình ảnh (CT/X-quang)   │
│   → 3. Soạn tay 6 mục chuẩn của Discharge Summary trên Word │
│   → 4. Dịch thuật ngữ y tế sang ngôn ngữ dễ hiểu cho BN    │
│   → 5. In, ký tên, đóng dấu, lưu hồ sơ cứng                │
│                                                             │
│ Bước nào tốn nhất? Bước 3–4 (⏱ 20 phút/lượt)               │
│ AI có thể nhảy vào hỗ trợ ở đâu? Bước 3–4:                 │
│   Auto-pull data HIS → AI draft summary → Bác sĩ review     │
│                                                             │
│ Metric thành công?                                          │
│   Giảm thời gian soạn từ 25 phút → dưới 5 phút.            │
│   Tỉ lệ bác sĩ chấp nhận draft (không sửa nhiều) ≥ 80%.     │
│                                                             │
│ Quick Architecture: [x] LLM Feature                        │
└─────────────────────────────────────────────────────────────┘
```

**⚡ Stress-Test (đóng vai CFO phản biện):**
- *Điểm yếu 1:* Dữ liệu y tế cực kỳ nhạy cảm → cần tuân thủ Nghị định 13/2023/NĐ-CP về bảo vệ dữ liệu cá nhân. Phải xử lý on-premise, không được gửi lên cloud public.
- *Điểm yếu 2:* LLM có thể hallucinate liều thuốc hoặc chẩn đoán sai → bắt buộc HITL (bác sĩ ký duyệt 100% trước khi in).
- *Điểm yếu 3:* Rule-based template có thể xử lý được 70% ca đơn giản với chi phí thấp hơn nhiều → chỉ nên dùng LLM cho ca phức tạp đa bệnh nền.

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

> **Nhóm chọn Card #1 — Vinmec AI Discharge Summary** để thực hiện Phase 3.

**Lý do chọn Card #1:**
- Quy trình có cấu trúc rõ ràng, 6 mục chuẩn → LLM có thể học template dễ.
- Impact định lượng được ngay: tiết kiệm 20 phút x 15 ca/ngày = **5 giờ bác sĩ/ngày/khoa**.
- Fallback an toàn: bác sĩ luôn review và ký duyệt → rủi ro hallucination được kiểm soát.

**Lý do loại bỏ các thẻ khác:**
- **Card #2 (Vinhomes):** Có thể giải quyết 80% bằng Rule-based Router + keyword matching trước, không cần LLM ngay.
- **Card #3 (Vinmec):** Rủi ro pháp lý y tế cao hơn khi AI đề xuất chuyên khoa sai → cần dữ liệu lịch sử bệnh án đủ lớn để fine-tune trước khi triển khai.

