# 01 — Problem Scan & Quick Problem Cards (Vin Smart Future)

**Họ tên:** Phan Bá An · **MSSV:** 2A202603375 · **Lớp:** L3A (VinUni AI20k K5-L3) · **GitHub:** [anphn3](https://github.com/anphn3)

> **Ghi chú về số liệu:** Mọi con số (phút/lượt, số phiếu/ngày, tỉ lệ sai…) trong file này là **ước tính/giả định của người viết** để phục vụ scoping, **không phải dữ liệu nội bộ của Vingroup**. Trước khi làm thật, mỗi con số cần được xác minh với đơn vị vận hành (xem mục "Điểm yếu cần kiểm chứng" ở từng thẻ).

---

# 🔍 Phase 1 — SCAN (4 Lenses)

| # | Subsidiary | Lens | Mô tả ngắn bài toán |
|---|------------|------|---------------------|
| 1 | **Vinhomes** | Lặp lại | CSKH đọc từng phản ánh của cư dân (mất nước, thang máy, ồn, rò rỉ…) trên app/hotline rồi **phân loại và chuyển thủ công** cho đúng Ban quản lý (BQL) tòa/bộ phận kỹ thuật; ước tính ~9 phút/phiếu và ~15% phiếu bị chuyển nhầm. |
| 2 | **VinFast** | AI có thể tốt hơn | Khách mô tả lỗi xe bằng tiếng Việt đời thường ("đi qua gờ giảm tốc kêu cụp cụp ở bánh trước"), nhân viên tiếp nhận phải tự quy ra hạng mục kiểm tra khi tạo phiếu dịch vụ. |
| 3 | **Xanh SM** | Tốn thời gian | Lý do hủy chuyến nằm rải rác trong ghi chú tài xế, chat và cuộc gọi; analyst vận hành phải đọc mẫu thủ công mới thấy pattern lỗi (chỉ phủ được một phần nhỏ số chuyến). |
| 4 | **Vinmec** | Pain từ người khác | Bác sĩ điều trị phải tự viết tóm tắt xuất viện từ bệnh án, xét nghiệm và diễn tiến; bác sĩ phàn nàn vì mất ~20–30 phút/bệnh nhân ngoài giờ khám. |
| 5 | **VinUni** | Lặp lại | Giảng viên/TA chấm hàng trăm bài lab và soạn nhận xét lặp lại; autograder chỉ cho điểm đạt/không đạt, thiếu phản hồi giải thích lỗi cho sinh viên. |
| 6 | **Vinpearl** | Pain từ người khác | Review khách sạn trên Booking/Agoda/Google Maps có phàn nàn khẩn (vệ sinh, thái độ nhân viên) nhưng nằm lẫn trong hàng trăm review, quản lý đọc muộn. |

**Chọn top 3 để làm Quick Card:** #1 (Vinhomes), #3 (Xanh SM), #4 (Vinmec) — ba bài toán có ba mức rủi ro và ba kiểu kiến trúc khác nhau (Rule+LLM / LLM batch / LLM + bắt buộc có người duyệt), giúp so sánh AI Fit một cách công bằng.

---

# 🃏 Phase 2 — QUICK-ASSESS: 3 Quick Problem Cards

## Card #1 — Vinhomes: Phân loại & điều hướng phản ánh cư dân

```text
┌─────────────────────────────────────────────────────────────┐
│ QUICK PROBLEM CARD #1                                       │
│                                                             │
│ Bài toán: Phản ánh của cư dân được CSKH đọc, phân loại và   │
│ chuyển thủ công tới BQL tòa/kỹ thuật, chậm và hay nhầm nơi. │
│ Công ty thành viên: [x] Vinhomes                            │
│                                                             │
│ Ai đang đau? CSKH tuyến 1 (quá tải), BQL tòa (nhận phiếu    │
│ sai/chậm), cư dân (chờ lâu, không biết ai xử lý).           │
│                                                             │
│ Workflow thủ công hiện tại (5 bước):                        │
│  1. Cư dân gửi phản ánh (app/hotline)                       │
│  → 2. CSKH đọc, gán loại + mức khẩn                         │
│  → 3. CSKH chọn bộ phận, chuyển qua Zalo/email/ticket       │
│  → 4. BQL/kỹ thuật tiếp nhận, xử lý                         │
│  → 5. CSKH phản hồi cư dân, đóng phiếu                      │
│                                                             │
│ Bước nào tốn nhất? Bước 2–3 (⏱ ~9 phút/phiếu, ~15% nhầm)  │
│ AI nhảy vào ở bước nào? Bước 2–3: gợi ý loại/mức khẩn/nơi   │
│ nhận + soạn nháp phản hồi. Sự cố khẩn dùng RULE, không LLM. │
│                                                             │
│ Metric: Thời gian từ lúc nhận → đúng bộ phận tiếp nhận      │
│ giảm từ ~45 phút (median) ──> dưới 10 phút; phân loại đúng  │
│ ≥ 90% trên 500 phiếu đã gán nhãn; 0 sự cố khẩn bị chậm.     │
│                                                             │
│ Quick Architecture: [x] Rule (khẩn cấp, bảng định tuyến)    │
│                     [x] LLM (phân loại câu chữ mơ hồ)       │
└─────────────────────────────────────────────────────────────┘
```

**Điểm yếu cần kiểm chứng (góc nhìn CFO/Trưởng vận hành):**
1. *Rule-based có đủ không?* Nếu app cho cư dân chọn sẵn danh mục thì chỉ cần bảng định tuyến — LLM chỉ đáng dùng cho phần **văn bản tự do** (ước tính chiếm bao nhiêu % phiếu? cần đo trên log thật).
2. *Con số 9 phút và 15% nhầm* là ước tính → phải đo thời gian thật ở 1–2 khu đô thị trước khi tính ROI.
3. *Sự cố khẩn bị LLM phân loại sai* (cháy, rò gas, kẹt thang) là rủi ro lớn nhất → bắt buộc có lớp rule từ khóa chạy **trước** LLM và không phụ thuộc LLM.

---

## Card #2 — Xanh SM: Tổng hợp lý do hủy chuyến

```text
┌─────────────────────────────────────────────────────────────┐
│ QUICK PROBLEM CARD #2                                       │
│                                                             │
│ Bài toán: Lý do hủy chuyến nằm trong ghi chú/chat tài xế    │
│ dạng văn bản tự do; analyst đọc tay nên chỉ phủ phần nhỏ.   │
│ Công ty thành viên: [x] Xanh SM                             │
│                                                             │
│ Ai đang đau? Analyst vận hành, quản lý khu vực (thiếu số    │
│ liệu đáng tin để quyết định).                               │
│                                                             │
│ Workflow thủ công hiện tại (5 bước):                        │
│  1. Xuất log hủy chuyến + ghi chú                           │
│  → 2. Đọc mẫu ngẫu nhiên                                    │
│  → 3. Gán nhãn lý do vào Excel                              │
│  → 4. Tổng hợp báo cáo tuần                                 │
│  → 5. Đề xuất hành động cho vận hành                        │
│                                                             │
│ Bước nào tốn nhất? Bước 2–3 (⏱ ~2 ngày/tuần, phủ ~5% chuyến)│
│ AI nhảy vào ở bước nào? Bước 3: phân loại mọi ghi chú vào   │
│ ~10 nhóm lý do + trích câu tiêu biểu.                       │
│                                                             │
│ Metric: Phủ 100% ghi chú (thay vì ~5%); khớp nhãn analyst   │
│ ≥ 85% trên 300 mẫu; thời gian làm báo cáo tuần 2 ngày ──>   │
│ dưới 2 giờ.                                                 │
│                                                             │
│ Quick Architecture: [x] LLM (batch, offline, không real-time)│
└─────────────────────────────────────────────────────────────┘
```

**Điểm yếu cần kiểm chứng:** (1) Nếu lý do hủy đã là trường dropdown thì chỉ cần thống kê, không cần AI. (2) Ghi chú tài xế có thể thiên lệch (đổ lỗi cho khách) → nhãn LLM chỉ phản ánh *lời kể*, không phải nguyên nhân thật. (3) Giá trị nằm ở quyết định vận hành tiếp theo — nếu không ai hành động theo báo cáo thì ROI bằng 0.

---

## Card #3 — Vinmec: Nháp tóm tắt xuất viện

```text
┌─────────────────────────────────────────────────────────────┐
│ QUICK PROBLEM CARD #3                                       │
│                                                             │
│ Bài toán: Bác sĩ tự tổng hợp bệnh án thành bản tóm tắt xuất │
│ viện, tốn thời gian ngoài giờ khám.                         │
│ Công ty thành viên: [x] Vinmec                              │
│                                                             │
│ Ai đang đau? Bác sĩ điều trị (quá tải hành chính); bệnh     │
│ nhân/người nhà (nhận bản tóm tắt trễ, khó hiểu).            │
│                                                             │
│ Workflow thủ công hiện tại (5 bước):                        │
│  1. Mở hồ sơ bệnh án điện tử, đọc diễn tiến                 │
│  → 2. Tổng hợp chẩn đoán, thuốc, kết quả xét nghiệm         │
│  → 3. Gõ bản tóm tắt + dặn dò                               │
│  → 4. Rà soát, ký                                           │
│  → 5. In/gửi bệnh nhân                                      │
│                                                             │
│ Bước nào tốn nhất? Bước 2–3 (⏱ ~25 phút/bệnh nhân)         │
│ AI nhảy vào ở bước nào? Bước 2–3: soạn NHÁP; bước 4 bắt    │
│ buộc bác sĩ duyệt và ký.                                    │
│                                                             │
│ Metric: 25 phút ──> ≤ 10 phút/ca; ≤ 10% bản nháp phải sửa   │
│ nội dung lâm sàng; 0 bản gửi bệnh nhân khi chưa có chữ ký.  │
│                                                             │
│ Quick Architecture: [x] LLM (+ Human-in-the-loop bắt buộc)  │
└─────────────────────────────────────────────────────────────┘
```

**Điểm yếu cần kiểm chứng:** (1) Dữ liệu bệnh án là dữ liệu nhạy cảm → cần quy định bảo mật/PII trước khi đưa vào bất kỳ LLM nào. (2) Một nhầm lẫn liều thuốc có thể gây hại thật → tỉ lệ sai chấp nhận được gần bằng 0, nên "tiết kiệm 15 phút" khó biện minh nếu bác sĩ phải đọc lại từng chữ. (3) Khả năng **NOT YET** cao hơn hai thẻ còn lại.

---

# 🗳️ Chọn bài toán để Deep-Dive

Tôi chọn **Card #1 — Vinhomes: Phân loại & điều hướng phản ánh cư dân** cho báo cáo Deep-Dive ([02-deep-dive-report.md](02-deep-dive-report.md)).

* **Vì sao chọn #1:** workflow có cấu trúc rõ, tác vụ lặp lại với khối lượng lớn, rủi ro kiểm soát được nhờ tách **rule cho sự cố khẩn** và **người duyệt cho phản hồi gửi cư dân** — thể hiện đúng nguyên tắc *Problem First, AI Second*.
* **Vì sao chưa chọn #2 (Xanh SM hủy chuyến):** là phân tích back-office, giá trị phụ thuộc việc vận hành có hành động theo báo cáo hay không; ít tác động trực tiếp đến trải nghiệm thời gian thực.
* **Vì sao chưa chọn #3 (Vinmec):** rủi ro lâm sàng và quy định dữ liệu quá cao cho một vòng prototype ngắn; nên để sau khi có baseline và khung bảo mật.
