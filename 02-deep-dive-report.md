# 02 — Deep-Dive Report: Phân loại & điều hướng phản ánh cư dân Vinhomes

**Tác giả:** Phan Bá An · MSSV 2A202603375 · Lớp L3A · Nhánh cá nhân (bản đề xuất để nhóm review và chọn lọc vào `main`)

> **Ghi chú về số liệu:** các con số dưới đây là **giả định/ước tính** để scoping (xem bảng giả định ngay sau đây), chưa phải dữ liệu nội bộ Vingroup. Chúng được dùng nhất quán trong toàn báo cáo và cần được xác minh bằng log thật ở bước đầu của prototype.

| Giả định dùng để tính | Giá trị |
|---|---|
| Quy mô một khu đô thị lớn | ~400 phản ánh/ngày |
| Thời gian CSKH cho bước phân loại + chuyển (Bước 2–3) | ~9 phút/phiếu |
| Tỉ lệ phiếu bị chuyển nhầm bộ phận | ~15% (~60 phiếu/ngày) |
| Thời gian từ lúc nhận → đúng bộ phận tiếp nhận (median) | ~45 phút (gồm ~30 phút chờ trong hàng đợi giờ cao điểm) |
| Thời gian CSKH duyệt một phiếu sau khi có AI hỗ trợ | ≤ 2 phút |

---

# 🏗️ Phase 3 — DEEP-DIVE

## 3.1. Current-State Workflow Mapping (G1)

Sơ đồ trực quan: xem **[04-workflow-diagram.png](04-workflow-diagram.png)** (có swimlane theo vai trò). Bản văn bản:

```text
Cư dân            CSKH tuyến 1                           BQL tòa / Kỹ thuật
──────            ────────────                           ──────────────────
┌────────────┐
│ B1 Gửi phản│
│ ánh (app / │
│ hotline)   │
│ ⏱ ~2 phút  │
└─────┬──────┘
      │ 🔄 Handoff #1 (cư dân → CSKH, văn bản tự do)
      ▼
┌──────────────────────┐
│ B2 Đọc, gán loại +   │
│ mức khẩn  🔴         │
│ ⏱ ~4 phút            │
└─────┬────────────────┘
      ▼
┌──────────────────────┐
│ B3 Chọn bộ phận,     │
│ chuyển Zalo/email/   │
│ ticket  🔴           │
│ ⏱ ~5 phút (+~30 phút │
│ chờ hàng đợi)        │
└─────┬────────────────┘
      │ 🔄 Handoff #2 (CSKH → BQL, thông tin có thể thiếu/nhầm nơi)
      ▼
                                                         ┌─────────────────────┐
                                                         │ B4 Tiếp nhận, xác   │
                                                         │ nhận, điều người    │
                                                         │ ⏱ ~15 phút          │
                                                         └─────┬───────────────┘
                                                               ▼
                                                         ┌─────────────────────┐
                                                         │ B5 Xử lý hiện trường│
                                                         │ (ngoài phạm vi AI)  │
                                                         └─────┬───────────────┘
      ┌────────────────────────────────────────────────────────┘
      │ 🔄 Handoff #3 (BQL → CSKH báo kết quả)
      ▼
┌──────────────────────┐
│ B6 Phản hồi cư dân,  │
│ đóng phiếu           │
│ ⏱ ~4 phút            │
└──────────────────────┘

🔴 Bottleneck = B2 + B3  →  ~9 phút CSKH/phiếu, ~15% chuyển nhầm
⏱ Tổng thời gian chạm tay của CSKH ≈ 13 phút/phiếu (B2 + B3 + B6); đến đúng bộ phận ≈ 45 phút
```

**Vì sao B2–B3 là bottleneck:** đây là bước duy nhất vừa phải *đọc hiểu ngôn ngữ tự do* vừa phải *tra bảng bộ phận phụ trách theo tòa/loại sự cố*, lại nằm ở đầu chuỗi nên mọi sai sót ở đây kéo theo trễ ở toàn bộ các bước sau.

## 3.2. Problem Statement (6-field) & Metrics (G2)

| Field | Nội dung chi tiết |
|---|---|
| **1. Actor / Operator** | Nhân viên CSKH tuyến 1 của Vinhomes xử lý phản ánh từ app Vinhomes Resident và hotline; người nhận kết quả: BQL tòa/bộ phận kỹ thuật và cư dân. |
| **2. Current Workflow** | CSKH đọc từng phản ánh tự do, tự gán loại sự cố (nước/điện, thang máy, ồn, vệ sinh, an ninh, phí…) và mức khẩn, tra bộ phận phụ trách rồi chuyển qua Zalo/email/ticket; sau khi BQL xử lý, CSKH soạn phản hồi cho cư dân. 6 bước, phần lớn thủ công. |
| **3. Bottleneck** | Bước 2–3: đọc hiểu + phân loại + chọn đúng bộ phận (~9 phút/phiếu, ~15% chuyển nhầm), cộng thời gian chờ trong hàng đợi giờ cao điểm. |
| **4. Business Impact** | Ước tính ~60 giờ công/ngày cho riêng Bước 2–3 ở một khu đô thị (400 phiếu × 9 phút); ~60 phiếu/ngày bị chuyển nhầm, mỗi phiếu trễ thêm ~30 phút; median ~45 phút mới tới đúng bộ phận — ảnh hưởng SLA phản hồi và mức hài lòng của cư dân. |
| **5. Success Metric** | **Hiệu suất:** median từ lúc nhận → đúng bộ phận tiếp nhận từ ~45 phút xuống **< 10 phút**; thời gian CSKH/phiếu cho Bước 2–3 từ ~9 phút xuống **≤ 2 phút** (tiết kiệm ~45 giờ công/ngày).<br>**Chất lượng:** phân loại đúng **≥ 90%** trên tập ≥ 500 phiếu đã gán nhãn; chuyển nhầm bộ phận **< 5%**.<br>**An toàn:** **0** sự cố khẩn (cháy, rò gas, kẹt thang, ngập) bị chậm so với baseline; **0** phản hồi gửi cho cư dân mà chưa qua CSKH duyệt. |
| **6. Operational Boundary** | **AI ĐƯỢC:** đọc nội dung phản ánh; đề xuất loại, mức khẩn, bộ phận nhận (kèm độ tin cậy); trích tòa/căn hộ/thời điểm; soạn **nháp** phản hồi.<br>**AI TUYỆT ĐỐI KHÔNG:** tự gửi phản hồi cho cư dân (mọi nháp mở đầu bằng `[DRAFT_ONLY]`); tự đóng phiếu; hạ mức khẩn của phiếu dính từ khóa khẩn cấp; trả lời về phí, pháp lý, tranh chấp căn hộ; xử lý sự cố khẩn cấp bằng LLM (dùng rule).<br>**Cần người duyệt:** mọi phản hồi gửi cư dân; phiếu có độ tin cậy < 0.75; phiếu thuộc nhóm tài chính/pháp lý. |

## 3.3. Future-State Flow & AI Fit (G3)

### So sánh Rule vs LLM vs Agent cho bài toán này

| Tiêu chí | Rule / State-machine | LLM Feature | Agentic Loop |
|---|---|---|---|
| Hợp với phần nào của bài toán | Sự cố **khẩn cấp** (từ khóa cố định), **bảng định tuyến** theo tòa + loại | **Hiểu câu chữ tự do, mơ hồ** ("nước chảy ri rỉ trên trần", "ồn lúc 2h sáng"); soạn nháp phản hồi | Tự tra nhiều hệ thống, tự gửi, tự đóng phiếu |
| Độ chính xác với phần phù hợp | Rất cao, giải thích được, kiểm toán được | Cao nhưng xác suất, cần ngưỡng tin cậy + người duyệt | Khó kiểm soát lỗi lan truyền |
| Chi phí / độ trễ | Gần như 0 | Thấp–vừa (một lần gọi/phiếu) | Cao, nhiều bước gọi |
| Rủi ro nếu sai | Thấp, dễ vá luật | Vừa — **bị giới hạn nhờ HITL + fallback** | Cao — hành động có tác dụng phụ ra ngoài |
| Kết luận | **Dùng** (lớp an toàn) | **Dùng** (lớp hiểu ngôn ngữ) | **Không dùng** ở giai đoạn này |

**Quyết định AI Fit:** [x] Rule / State-Machine (cho sự cố khẩn và định tuyến) + [x] **LLM Feature** (phân loại văn bản mơ hồ + nháp phản hồi) — kiến trúc **hybrid**. Không cần Agentic Loop: quy trình có cấu trúc cố định và hành động gửi/đóng phiếu có tác dụng phụ nên phải do con người quyết định.

### Future-State Flow

```text
┌──────────────┐
│ Nhận phản ánh│
│ (app/hotline)│
└──────┬───────┘
       ▼
┌────────────────────────────┐   khẩn   ┌──────────────────────────────┐
│ 🔵 RULE: quét từ khóa khẩn │ ───────► │ 🟢 Trực ban kỹ thuật nhận     │
│ (cháy, gas, kẹt thang, …)  │          │ NGAY (bỏ qua LLM)             │
└──────┬─────────────────────┘          └──────────────────────────────┘
       │ không khẩn
       ▼
┌────────────────────────────────────────────┐
│ 🔵 LLM: phân loại → JSON {loại, mức khẩn,  │
│ bộ phận, tòa/căn hộ, confidence}           │
└──────┬─────────────────────────────────────┘
       │
       ├── confidence ≥ 0.75 ──► 🔵 Tạo ticket cho đúng BQL (chưa gửi cư dân)
       │
       └── confidence < 0.75 ──► 🟢 CSKH phân loại tay
                  ▲
                  │ ↩️ Fallback: LLM lỗi/timeout/JSON sai → vào hàng đợi thủ công như hiện tại
       ┌──────────┴───────────────────────────┐
       │ Sau khi BQL xử lý xong:              │
       │ 🔵 LLM soạn nháp "[DRAFT_ONLY] …"    │
       │ → 🟢 CSKH duyệt/sửa → gửi cư dân     │
       └──────────────────────────────────────┘

🔵 AI Step   🟢 Human Step (HITL)   ↩️ Fallback
```

**Cơ chế an toàn:** (1) rule khẩn cấp chạy độc lập với LLM; (2) ngưỡng tin cậy 0.75 đẩy ca khó về người; (3) thẻ `[DRAFT_ONLY]` ngăn tự gửi; (4) chế độ *shadow mode* ở giai đoạn đầu — AI gợi ý song song nhưng CSKH vẫn làm như cũ để đo độ chính xác trước khi bật thật.

> **Liên hệ với prototype (Phase 4):** tư duy ranh giới ở trên là cùng một mẫu với bài prototype Xanh SM — thẻ `[DRAFT_ONLY]` ở đầu mọi bản nháp và "ngưỡng nguy cấp → hành động an toàn cố định" (pin < 5% → `dispatch_mobile_charger`) tương ứng "từ khóa khẩn cấp → trực ban ngay" ở đây.

---

# 🏁 Phase 5 — EVALUATE (G4)

### AI Readiness Checklist

| # | Câu hỏi | Trạng thái | Chứng cứ / ghi chú |
|---|---|---|---|
| 1 | Có sẵn dữ liệu mẫu/log sạch để test? | **[ ] Chưa xác nhận** | Cần xin 3–6 tháng phiếu phản ánh đã có nhãn loại/bộ phận (≥ 500 phiếu để đo độ chính xác). Hiện đây là **giả định**, chưa có bằng chứng. |
| 2 | Rủi ro khi AI sai có trong tầm kiểm soát (HITL/Fallback)? | **[x] Có** | Rule khẩn cấp độc lập LLM; ngưỡng 0.75; `[DRAFT_ONLY]`; fallback về quy trình thủ công; shadow mode. |
| 3 | Stakeholder sẵn sàng đổi quy trình cũ? | **[ ] Chưa xác nhận** | Cần phỏng vấn trưởng nhóm CSKH và 2–3 BQL tòa; CSKH có thể lo bị thay thế nên cần định vị AI là công cụ giảm việc lặp. |

### Quyết định cuối cùng

* [x] **GO (Bắt đầu xây dựng Prototype) — scope hẹp, shadow mode**
* [ ] NOT YET
* [ ] NO-GO

**Justification:**
1. **Có chứng cứ về cấu trúc bài toán:** workflow rõ, lặp lại, bottleneck nằm ở bước đọc hiểu ngôn ngữ tự do — đúng điểm mạnh của LLM; phần an toàn (sự cố khẩn) đã được tách khỏi LLM nên rủi ro lớn nhất bị loại khỏi vòng đầu.
2. **Scope hẹp, đảo ngược được:** chỉ làm *phân loại + gợi ý định tuyến + nháp phản hồi*, chạy shadow mode trên dữ liệu lịch sử; **không** tự gửi, **không** tự đóng phiếu → chi phí sai thấp, dễ dừng.
3. **Thành thật về điều chưa biết:** checklist #1 (dữ liệu) và #3 (stakeholder) **chưa được xác nhận**. Vì vậy quyết định GO là *có điều kiện*:
   * **Điều kiện tiên quyết (tuần 1–2):** lấy được ≥ 500 phiếu có nhãn và xác nhận bộ phận định tuyến.
   * **Kill criteria:** nếu sau shadow mode độ chính xác phân loại < 80% hoặc có bất kỳ sự cố khẩn nào bị gán mức thấp → chuyển **NOT YET**, quay về rule-based + cải thiện danh mục trên app trước khi dùng LLM.
   * **Nếu không có dữ liệu sau 2 tuần** → đổi quyết định thành **NOT YET** (không build trên giả định).
4. **Vì sao không phải NO-GO:** một phần lớn bài toán *có thể* giải bằng rule, nhưng phần phản ánh văn bản tự do (nguồn của 15% chuyển nhầm) là nơi rule yếu và LLM có giá trị gia tăng; vì vậy dùng hybrid thay vì bỏ AI hoàn toàn.
