# 02 — Deep-Dive Report: AI Soạn thảo Tóm tắt Xuất viện
### Vinmec International Hospital × Vin Smart Future | Lab 02

---

## 🏛️ Bối cảnh lựa chọn bài toán

> **AI Product Engineer** tại **Vin Smart Future**, được phân công hỗ trợ **Vinmec International Hospital**.
>
> Qua khảo sát thực địa tại Khoa Nội Tổng quát – Vinmec Times City (Hà Nội), tôi quan sát thấy mỗi ca trực, một bác sĩ nội trú phải soạn thủ công từ 8–15 bản **Discharge Summary** (Tóm tắt xuất viện) từ bệnh án điện tử sang định dạng văn bản bệnh nhân dễ đọc. Mỗi lượt mất trung bình **20–25 phút**, trong khi đây là tác vụ có cấu trúc cao và lặp lại mỗi ngày.

---

# 🏗️ Phase 3 — DEEP-DIVE

## 3.1. Current-State Workflow Mapping

Quy trình soạn Tóm tắt Xuất viện (Discharge Summary) thủ công hiện tại tại Vinmec:

```text
┌──────────────┐     ┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│   Bước 1     │     │   Bước 2     │     │   Bước 3     │     │   Bước 4     │
│ Bác sĩ mở   │     │ Đọc kết quả  │     │ Soạn thủ    │     │ Dịch thuật  │
│ HIS (bệnh   │ ──→ │ xét nghiệm, │ ──→ │ công 6 mục  │ ──→ │ ngữ y tế   │
│ án điện tử) │     │ hình ảnh học │     │ Discharge   │     │ → dễ hiểu  │
│             │     │ (CT, X-quang)│     │ Summary     │     │ cho BN     │
│ Ai: Bác sĩ  │     │ Ai: Bác sĩ   │     │ Ai: Bác sĩ  │     │ Ai: Bác sĩ  │
│ ⏱ 3 phút   │     │ ⏱ 5 phút    │     │ ⏱ 12 phút 🔴│     │ ⏱ 8 phút 🔴 │
│ In: Mã BN   │     │ In: Mã BN   │     │ In: Raw data │     │ In: Thuật   │
│ Out: Màn    │     │ Out: Hiểu   │     │ Out: Draft  │     │    ngữ y tế │
│      hình   │     │      bệnh    │     │      Word   │     │ Out: Văn BN │
└──────────────┘     └──────────────┘     └──────────────┘     └──────────────┘
                                                                       │
                                                                       ▼
                                                                ┌──────────────┐
                                                                │   Bước 5     │
                                                                │ In, ký tên,  │
                                                                │ đóng dấu và  │
                                                                │ lưu hồ sơ   │
                                                                │ Ai: Bác sĩ  │
                                                                │ ⏱ 2 phút    │
                                                                └──────────────┘

🔴 = Bottlenecks chính (Bước 3 & 4)
🔄 = Handoff: Bước 4 → 5 (Bác sĩ → Điều dưỡng in & lưu)
⏱  Tổng thời gian thủ công: 25–30 phút/bệnh nhân xuất viện.
     Khoa Nội: 10–15 ca xuất viện/ngày → 4–7 giờ bác sĩ/ngày bị "đốt" vào tác vụ hành chính.
```

---

## 3.2. Problem Statement (6-field) — Vin Smart Future Standard

| Field | Nội dung chi tiết |
|-------|-------------------|
| **1. Actor / Operator** | Bác sĩ nội trú và Điều dưỡng trưởng khoa Nội, Ngoại Tổng quát tại Vinmec International Hospital (ước tính 40–60 bác sĩ/ngày bị ảnh hưởng trên toàn hệ thống Vinmec). |
| **2. Current Workflow** | Khi bệnh nhân được chỉ định xuất viện, bác sĩ mở HIS (Hospital Information System) của Vinmec, đọc lại chẩn đoán, danh sách thuốc, kết quả xét nghiệm và hình ảnh học, sau đó soạn thủ công 6 mục chuẩn của Discharge Summary trên Word: (1) Chẩn đoán ra viện, (2) Tóm tắt diễn biến, (3) Kết quả cận lâm sàng, (4) Thuốc uống về, (5) Lịch tái khám, (6) Khuyến cáo chăm sóc. Toàn bộ quy trình hoàn toàn thủ công, mất 20–30 phút/bệnh nhân. |
| **3. Bottleneck** | **Bước 3 & 4** (chiếm 20/30 phút): Soạn thủ công 6 mục và dịch thuật ngữ y tế chuyên sâu sang ngôn ngữ dễ hiểu dành cho bệnh nhân. Hai bước này đòi hỏi ngôn ngữ tự nhiên linh hoạt mà hệ thống rule-based template không xử lý tốt với các ca đa bệnh nền phức tạp. |
| **4. Business Impact** | Khoa Nội: ~12 ca xuất viện/ngày × 25 phút = **5 giờ bác sĩ/ngày bị tiêu tốn vào tác vụ hành chính**. Trên toàn hệ thống 6 bệnh viện Vinmec tại Hà Nội: ước tính lãng phí ~**30 giờ bác sĩ/ngày**. Ngoài ra, bác sĩ kiệt sức với paperwork làm giảm chất lượng khám chữa bệnh thực sự — ảnh hưởng trực tiếp đến NPS (Net Promoter Score) của Vinmec. |
| **5. Success Metric** | 1. Giảm thời gian soạn Discharge Summary từ **25 phút → dưới 5 phút** (giảm 80%). <br>2. Tỉ lệ bác sĩ **chấp nhận AI draft không cần sửa nhiều** ≥ 80% sau 3 tháng (Quality). <br>3. **Zero hallucination nghiêm trọng** (sai liều thuốc, nhầm chẩn đoán) = 0 trường hợp/tháng (Safety). |
| **6. Operational Boundary** | ✅ **AI được phép:** Truy xuất dữ liệu HIS (chẩn đoán, thuốc, xét nghiệm) của đúng bệnh nhân được chỉ định; soạn thảo bản nháp Discharge Summary đánh dấu `[DRAFT – CHỜ BÁC SĨ KÝ DUYỆT]`. <br>🚫 **AI tuyệt đối không được:** Tự ký duyệt hay phát hành Discharge Summary mà không có chữ ký điện tử của bác sĩ có thẩm quyền; đề xuất thay đổi chẩn đoán hoặc đơn thuốc; truy cập hồ sơ bệnh nhân ngoài phạm vi ca xuất viện được giao. <br>🔒 **Tuân thủ bắt buộc:** Nghị định 13/2023/NĐ-CP (bảo vệ dữ liệu cá nhân), Thông tư 46/2018/TT-BYT (bảo mật hồ sơ bệnh án). **Xử lý on-premise hoàn toàn — không gửi dữ liệu lên cloud public.** |

---

## 3.3. Future-State Flow & AI Fit

### AI Fit Analysis

| Tiêu chí | Rule / State-Machine | LLM Feature ✅ | Agentic Loop |
|----------|---------------------|---------------|--------------|
| Cấu trúc quy trình | Cố định, 6 mục chuẩn | ✅ Phù hợp | Quá phức tạp không cần thiết |
| Độ phức tạp ngôn ngữ | Thấp (template đơn giản) | ✅ Xử lý tốt ca phức tạp | Không cần |
| Rủi ro khi sai | Nghiêm trọng → HITL bắt buộc | ✅ Bác sĩ luôn review | Rủi ro mất kiểm soát |
| **Quyết định** | ❌ Chỉ được 70% ca đơn | ✅ **LLM Feature** | ❌ Overkill |

> **Chọn: LLM Feature** — Quy trình có cấu trúc cố định, bác sĩ luôn là người ký duyệt cuối cùng (HITL bắt buộc), không cần agent tự trị.

### Future-State Workflow

```text
┌──────────────┐     ┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│   Bước 1     │     │   Bước 2     │     │   Bước 3     │     │   Bước 4     │
│ Bác sĩ chỉ  │     │ 🔵 Auto-pull │     │ 🔵 LLM draft │     │ 🟢 Bác sĩ   │
│ định xuất   │ ──→ │ dữ liệu HIS  │ ──→ │ Discharge   │ ──→ │ review &    │
│ viện trên   │     │ (chẩn đoán, │     │ Summary     │     │ ký duyệt    │
│ HIS         │     │ thuốc, XN)   │     │ [DRAFT]     │     │ trên HIS    │
│ ⏱ 1 phút   │     │ ⏱ <1 phút   │     │ ⏱ <1 phút  │     │ ⏱ 3–5 phút │
└──────────────┘     └──────────────┘     └──────────────┘     └──────────────┘
                                                                       │
                                           ↩️ Fallback khi LLM lỗi:   │
                                           Hiển thị form template rỗng │
                                           → Bác sĩ điền thủ công     ▼
                                           như quy trình cũ.    ┌──────────────┐
                                                                 │   Bước 5     │
                                                                 │ Hệ thống tự  │
                                                                 │ động in PDF  │
                                                                 │ & lưu HIS   │
                                                                 │ ⏱ <1 phút   │
                                                                 └──────────────┘

🔵 AI Step:   Bước 2 (data fetch) và Bước 3 (LLM draft generation)
🟢 Human HITL: Bước 4 — Bác sĩ phải review và ký số trước khi phát hành
↩️ Fallback:  Nếu LLM không generate được (timeout/lỗi), hiện template trắng
⏱  Tổng thời gian mới: ~5–7 phút/bệnh nhân (giảm từ 25–30 phút → 80%)
```

---

# 🏁 Phase 5 — EVALUATE: AI Readiness Checklist

### AI Readiness Checklist

| # | Tiêu chí | Trạng thái | Ghi chú |
|---|----------|-----------|---------|
| 1 | ✅ Có sẵn dữ liệu mẫu để test? | **CÓ** | HIS Vinmec đã lưu hàng nghìn Discharge Summary gốc → dùng làm Ground Truth để đánh giá chất lượng AI draft. |
| 2 | ✅ Rủi ro khi AI sai trong tầm kiểm soát? | **CÓ** | HITL bắt buộc: bác sĩ ký duyệt 100% trước khi phát hành. AI chỉ tiết kiệm thời gian soạn, không tự ra quyết định y tế. |
| 3 | ✅ Stakeholders sẵn sàng thay đổi quy trình? | **PHẦN LỚN** | Bác sĩ nội trú (người bị ảnh hưởng nhiều nhất) đồng thuận cao. Cần thuyết phục thêm Ban Giám đốc Y về việc dùng LLM trong hệ thống bệnh án. |
| 4 | ✅ Hạ tầng on-premise khả thi? | **CÓ** | Vinmec đã có datacenter nội bộ. Cần deploy LLM (ví dụ: Llama 3.1 / Qwen2.5-72B fine-tuned) on-premise để tuân thủ bảo mật. |
| 5 | ⚠️ Quy định pháp lý y tế? | **CẦN REVIEW** | Cần tham vấn pháp lý về Thông tư 46/2018 và Nghị định 13/2023 trước khi triển khai production. |

### Quyết định cuối cùng

> ✅ **GO (Bắt đầu xây dựng Prototype)**

**Justification:**

Bài toán đủ điều kiện **GO** vì:

1. **Dữ liệu sẵn có:** Hàng nghìn Discharge Summary gốc trong HIS Vinmec → đủ để xây dựng và đánh giá prototype ngay.

2. **Rủi ro được kiểm soát chặt:** Toàn bộ output AI đều phải qua bác sĩ ký duyệt (HITL) → không có trường hợp nào AI phát hành độc lập tài liệu y tế.

3. **ROI rõ ràng và đo lường được:** Tiết kiệm 5 giờ bác sĩ/khoa/ngày → quy đổi thành lượt khám thêm = tăng doanh thu hoặc giảm burnout đội ngũ y tế.

4. **Technical Feasibility cao:** LLM summarization từ structured data (JSON HIS) → free-text y tế là use-case đã được chứng minh ở nhiều bệnh viện quốc tế (Epic AI Ambient, Microsoft DAX).

5. **Scope hẹp để pilot:** Bắt đầu với **1 khoa (Nội Tổng quát – Vinmec Times City)**, đo kết quả trong 60 ngày, trước khi nhân rộng.

**Điều kiện cần hoàn thành trước khi Go-Live:**
- [ ] Tham vấn pháp lý về Thông tư 46/2018 và Nghị định 13/2023.
- [ ] Fine-tune hoặc few-shot prompt LLM với 200 Discharge Summary mẫu của Vinmec.
- [ ] Thử nghiệm adversarial: kiểm tra LLM có hallucinate liều thuốc không.
- [ ] Triển khai on-premise (không dùng cloud public API cho dữ liệu bệnh nhân).

