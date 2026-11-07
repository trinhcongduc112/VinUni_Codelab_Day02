# Problem Scan — Lab 02: AI Product Scoping (Vin Smart Future)

**Học viên:** Trịnh Công Đức · branch `TrinhCongDuc`

> Các mốc thời gian trong bài là **ước tính** để định hướng phép đo, không phải số liệu nội bộ của Vingroup.

---

# 🔍 Phase 1 — SCAN (Cá nhân)

Dùng **4 Lenses** (Lặp lại · Tốn thời gian · AI có thể tốt hơn · Pain từ người khác) quét hoạt động vận hành của các công ty thành viên Vingroup.

### 📝 List bài toán của tôi:
| # | Subsidiary (VinFast/Xanh SM...) | Lens | Mô tả ngắn bài toán |
|---|----------------------------------|------|---------------------|
| 1 | **VinFast** | AI có thể tốt hơn | Kỹ sư chất lượng phát hiện lỗi an toàn lặp lại bằng cách lọc từ khóa và đọc tay phiếu sửa chữa/bảo hành viết bằng nhiều ngôn ngữ (Việt, Anh, Pháp, Đức…); dữ liệu về theo đợt hằng tháng nên tín hiệu đến chậm. |
| 2 | **Vinschool** (Khác) | Tốn thời gian | Giáo viên viết nhận xét định kỳ cho từng học sinh, dồn vào cuối kỳ; dùng câu mẫu thì nhanh nhưng phụ huynh thấy chung chung. |
| 3 | **Xanh SM** | Pain từ người khác | Tài xế khiếu nại thu nhập / đối soát cuốc ("cuốc hôm qua bị trừ tiền sai"); bộ phận hỗ trợ phải tra lịch sử chuyến và chính sách phí để giải thích từng trường hợp. |
| 4 | **VinCons** (thuộc Vinhomes) | Tốn thời gian | Kỹ sư giám sát gom tin nhắn, ảnh, khối lượng của các tổ đội để viết nhật ký thi công và báo cáo tiến độ hằng ngày. |
| 5 | **VinCons** (thuộc Vinhomes) | Lặp lại | Tuyển hàng loạt công nhân xây dựng: ứng viên nhắn Zalo / gọi điện, nhân viên tuyển dụng hỏi lại tay nghề, nhập Excel rồi phân bổ về từng công trường. |
| 6 | **Vinhomes** | Lặp lại | Lỗi phát hiện khi bàn giao căn hộ (tường nứt, cửa kẹt…) được ghi tay rồi phân loại, giao đúng nhà thầu sửa và theo dõi đến khi đóng. |

---

# 🃏 Phase 2 — QUICK-ASSESS (Cá nhân)

Chọn top 3 từ danh sách SCAN: **#1 (VinFast — lỗi an toàn), #2 (Vinschool — nhận xét học sinh), #3 (Xanh SM — khiếu nại thu nhập tài xế).**

## Card #1 — VinFast: Phát hiện sớm lỗi an toàn từ phiếu sửa chữa đa ngôn ngữ

```text
┌─────────────────────────────────────────────────────────────┐
│ QUICK PROBLEM CARD #1                                       │
│                                                             │
│ Bài toán (1 câu): Kỹ sư chất lượng phát hiện chậm các lỗi   │
│   an toàn lặp lại trên xe VF8 vì phải lọc từ khóa và đọc    │
│   tay phiếu sửa chữa/bảo hành viết bằng nhiều ngôn ngữ.     │
│ Công ty thành viên: [x] VinFast  [ ] Xanh SM  [ ] Vinhomes  │
│                     [ ] Vinmec   [ ] Khác (Ghi rõ)________  │
│                                                             │
│ Ai đang đau (Actor)? Kỹ sư chất lượng hiện trường (trụ sở   │
│   VinFast). Gián tiếp: Hội đồng An toàn, Pháp chế, chủ xe.  │
│                                                             │
│ Workflow thủ công hiện tại (5 bước):                        │
│   1. Kỹ thuật viên đại lý ghi phiếu sửa chữa bằng tiếng địa │
│      phương                                                 │
│   ──> 2. Đại lý gửi hồ sơ bảo hành, VinFast duyệt để thanh  │
│          toán                                               │
│   ──> 3. Dữ liệu được xuất cho bộ phận Chất lượng hằng      │
│          tháng                                              │
│   ──> 4. Kỹ sư chất lượng lọc từ khóa, đọc, dịch, gom nhóm  │
│          lỗi                                                │
│   ──> 5. R&D phân tích nguyên nhân, Hội đồng An toàn quyết  │
│          định thu hồi                                       │
│                                                             │
│ Bước nào tốn thời gian/lỗi nhất? Bước 4 (⏱ ~5 phút/phiếu;   │
│   cả chu kỳ phát hiện 6–10 tuần — ước tính)                 │
│ AI có thể nhảy vào hỗ trợ ở bước nào? Từ bước 1:            │
│   khách báo sự cố → AI hỏi thêm câu còn thiếu, ca khẩn      │
│   chuyển kỹ sư trực ngay; kỹ thuật viên được gợi ý ca       │
│   tương tự toàn cầu; AI đọc mọi phiếu ngay khi lưu, gắn cờ  │
│   kèm trích dẫn; trụ sở có dashboard từ mọi thị trường và   │
│   báo cáo tuần do AI soạn nháp, kỹ sư duyệt.                │
│                                                             │
│ Đo thành công bằng gì (Metric có số)?                       │
│   • 100% phiếu VF8 được soát an toàn trong ≤ 24 giờ kể từ   │
│     khi tạo ticket (hiện 3–8 tuần, chỉ đọc một phần phiếu)  │
│   • Ca khẩn được kỹ sư trực gọi lại trong ≤ 2 giờ           │
│   • Độ nhạy với phiếu an toàn ≥ 95% trên bộ test có nhãn    │
│                                                             │
│ Quick Architecture: [ ] No AI  [ ] Rule  [x] LLM  [ ] Agent │
└─────────────────────────────────────────────────────────────┘
```

## Card #2 — Vinschool: Nhận xét định kỳ cho học sinh

```text
┌─────────────────────────────────────────────────────────────┐
│ QUICK PROBLEM CARD #2                                       │
│                                                             │
│ Bài toán (1 câu): Giáo viên mất nhiều giờ mỗi cuối kỳ để    │
│   viết nhận xét riêng cho từng học sinh; dùng câu mẫu thì   │
│   nhanh nhưng nhận xét na ná nhau.                          │
│ Công ty thành viên: [ ] VinFast  [ ] Xanh SM  [ ] Vinhomes  │
│                     [ ] Vinmec  [x] Khác (Ghi rõ): Vinschool│
│                                                             │
│ Ai đang đau (Actor)? Giáo viên chủ nhiệm và bộ môn. Gián    │
│   tiếp: phụ huynh, tổ trưởng chuyên môn.                    │
│                                                             │
│ Workflow thủ công hiện tại (5 bước):                        │
│   1. Giáo viên ghi chú quan sát học sinh trong kỳ           │
│   ──> 2. Nhập điểm vào hệ thống                             │
│   ──> 3. Viết nhận xét cho từng học sinh                    │
│   ──> 4. Tổ trưởng / ban giám hiệu duyệt                    │
│   ──> 5. Gửi phụ huynh qua sổ liên lạc điện tử              │
│                                                             │
│ Bước nào tốn thời gian/lỗi nhất? Bước 3 (⏱ ~5 phút/học sinh │
│   — ước tính)                                               │
│ AI có thể nhảy vào hỗ trợ ở bước nào? Bước 3: soạn nháp     │
│   nhận xét từ điểm và ghi chú của giáo viên; giáo viên sửa  │
│   và chịu trách nhiệm.                                      │
│                                                             │
│ Đo thành công bằng gì (Metric có số)?                       │
│   • Giảm thời gian viết nhận xét từ ~5 phút ──> ≤ 2         │
│     phút/học sinh                                           │
│   • 0 nhận xét chứa thông tin không có trong ghi chú của    │
│     giáo viên                                               │
│                                                             │
│ Quick Architecture: [ ] No AI  [ ] Rule  [x] LLM  [ ] Agent │
└─────────────────────────────────────────────────────────────┘
```

## Card #3 — Xanh SM: Khiếu nại thu nhập của tài xế

```text
┌─────────────────────────────────────────────────────────────┐
│ QUICK PROBLEM CARD #3                                       │
│                                                             │
│ Bài toán (1 câu): Nhân viên hỗ trợ tài xế mất nhiều thời    │
│   gian tra cứu và giải thích từng khiếu nại thu nhập / đối  │
│   soát cuốc xe.                                             │
│ Công ty thành viên: [ ] VinFast  [x] Xanh SM  [ ] Vinhomes  │
│                     [ ] Vinmec   [ ] Khác (Ghi rõ)________  │
│                                                             │
│ Ai đang đau (Actor)? Nhân viên hỗ trợ tài xế. Gián tiếp:    │
│   tài xế chờ phản hồi.                                      │
│                                                             │
│ Workflow thủ công hiện tại (5 bước):                        │
│   1. Tài xế gửi khiếu nại qua app hoặc hotline              │
│   ──> 2. Nhân viên xác định cuốc xe liên quan               │
│   ──> 3. Tra lịch sử chuyến, cước, phí, thưởng / phạt       │
│   ──> 4. Đối chiếu chính sách, viết giải thích cho tài xế   │
│   ──> 5. Nếu tính sai, chuyển kế toán điều chỉnh            │
│                                                             │
│ Bước nào tốn thời gian/lỗi nhất? Bước 3–4 (⏱ ~15 phút/khiếu │
│   nại — ước tính)                                           │
│ AI có thể nhảy vào hỗ trợ ở bước nào? Bước 2–4: trích mã    │
│   cuốc và thời gian từ khiếu nại, đối chiếu dữ liệu chuyến, │
│   soạn nháp giải thích kèm số liệu; nhân viên duyệt. AI     │
│   không tự điều chỉnh tiền.                                 │
│                                                             │
│ Đo thành công bằng gì (Metric có số)?                       │
│   • Giảm thời gian xử lý từ ~15 phút ──> ≤ 5 phút/khiếu nại │
│   • ≥ 95% bản giải thích khớp số liệu hệ thống              │
│                                                             │
│ Quick Architecture: [ ] No AI  [ ] Rule  [x] LLM  [ ] Agent │
└─────────────────────────────────────────────────────────────┘
```

---

# 🗳️ Đề xuất lựa chọn cho Deep-Dive (mang đến buổi họp nhóm)

Tôi đề xuất chọn **"Card #1 — VinFast: Phát hiện sớm lỗi an toàn từ phiếu sửa chữa đa ngôn ngữ"** để thực hiện Deep-Dive.

## Lý do lựa chọn và loại bỏ các thẻ khác:
* **Card #1 (VinFast) — chọn:** hậu quả lớn và có bằng chứng công khai (nhiều đợt thu hồi VF8 tại Mỹ, trong đó có đợt được đưa ra sau khi cơ quan quản lý mở điều tra). Cách làm bằng rule (lọc từ khóa) thực sự yếu với văn bản tự do đa ngôn ngữ, nên LLM là cần thiết. Ranh giới rõ ràng: AI chỉ hỏi thêm theo bộ câu đã duyệt, đọc và thêm cảnh báo; con người quyết định thu hồi.
* **Card #2 (Vinschool):** dễ triển khai nhưng giá trị chủ yếu là tiết kiệm thời gian giáo viên; ngân hàng câu nhận xét mẫu đã giải quyết được một phần; có rủi ro phụ huynh không chấp nhận nhận xét do AI soạn.
* **Card #3 (Xanh SM):** hợp với LLM kết hợp tra dữ liệu chuyến, nhưng phần lớn khiếu nại lặp lại có thể trả lời bằng mẫu soạn sẵn; giá trị thấp hơn nhiều so với rủi ro an toàn và pháp lý ở Card #1.
