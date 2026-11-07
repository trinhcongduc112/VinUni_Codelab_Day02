# 01 — Problem Scan & Quick-Assess
### Trần Hoàng Phát | AI Product Engineer tại Vin Smart Future | Lab 02

---

## 🧑‍💻 Giới thiệu bản thân

Tôi là **AI Product Engineer** tại **Vin Smart Future** (vai trò mô phỏng trong lab), quét vận hành của các công ty thành viên Vingroup để tìm cơ hội tối ưu bằng AI. Điểm khởi đầu là lúc một ticket bảo trì cư dân được đề nghị đóng hoặc mở lại: bằng chứng sửa chữa có thể thuộc một lần can thiệp cũ, trong khi vấn đề hoặc can thiệp mới đã xuất hiện sau đó.

> Các con số nội bộ trong bài là **ước tính** để định hướng phép đo, không phải số liệu khảo sát tại các đơn vị. Các nguồn công khai và giới hạn diễn giải được trình bày ở mục **“Cơ sở công khai và giới hạn của giả thuyết”** trong [02-deep-dive-report.md](02-deep-dive-report.md).

---

# 🔍 Phase 1 — SCAN: Tìm kiếm cơ hội (Cá nhân)

> Dùng **4 Lenses** — Lặp lại · Tốn thời gian · AI có thể tốt hơn · Pain từ người khác — để quét ít nhất 5 bottleneck vận hành.

| # | Công ty thành viên | Lens | Mô tả ngắn bài toán |
|---|---|---|---|
| 1 | **VinFast** | AI có thể tốt hơn | Phiếu sửa chữa/bảo hành mô tả triệu chứng tự do có thể được ghi khác nhau; nhân viên phải đọc và gom các phiếu liên quan trước khi chuyển kỹ sư chất lượng review. |
| 2 | **Xanh SM** | Pain từ người khác | Khi tài xế báo pin thấp hoặc điểm đón khó tiếp cận, điều phối phải ghép dữ kiện từ cuộc gọi, vị trí và điều kiện vận hành trước khi soạn phương án hỗ trợ. |
| 3 | **Vinhomes** | Tốn thời gian; Pain từ người khác | Trước khi đóng hoặc mở lại ticket bảo trì cư dân, BQL phải đối chiếu mô tả, lịch sử can thiệp, ảnh/ghi chú và mốc thời gian. Bằng chứng của lần sửa cũ có thể bị dùng nhầm cho vấn đề hoặc can thiệp mới. |
| 4 | **Vinmec** | Tốn thời gian | Khi một dịch vụ được điều chỉnh gần lúc ra viện, bộ chứng từ bảo lãnh viện phí đã chuẩn bị có thể không còn khớp. Nhân viên phải đối chiếu yêu cầu bảo lãnh, dữ liệu dịch vụ và chứng từ trước khi chuyển xử lý. |
| 5 | **Vinpearl** | Lặp lại; Tốn thời gian | Yêu cầu của khách đoàn đến qua email, điện thoại và kênh nhắn tin có thể thiếu ngữ cảnh khi được chuyển cho các bộ phận vận hành. |
| 6 | **VinUni** | Pain từ người khác | Khi sinh viên yêu cầu xem lại bài lab, trợ giảng cần ghép rubric, nhận xét và log chấm để soạn phản hồi có căn cứ. |

---

# 🃏 Phase 2 — QUICK-ASSESS: 3 Quick Problem Cards (Cá nhân)

> Chọn Top 3 từ Scan: **#3 Vinhomes — rà soát bằng chứng đóng/mở lại ticket; #5 Vinpearl — handoff khách đoàn; #1 VinFast — gom phiếu sửa chữa.**

## 🃏 Card #1 — Vinhomes: Rà soát bằng chứng đóng/mở lại ticket bảo trì

```text
┌────────────────────────────────────────────────────────────────┐
│ QUICK PROBLEM CARD #1                                          │
│                                                                │
│ Bài toán: Ticket có thể được đề nghị đóng dựa trên ảnh hoặc    │
│ ghi chú của lần sửa cũ, dù cư dân mở lại phản ánh hoặc có một  │
│ can thiệp mới sau bằng chứng đó.                               │
│                                                                │
│ Công ty thành viên: [x] Vinhomes                               │
│                                                                │
│ Ai đang đau (Actor)?                                           │
│   CSKH/BQL nhận ticket; kỹ thuật/nhà thầu cập nhật bằng        │
│   chứng; BQL hoặc kỹ sư có thẩm quyền review. Cư dân là        │
│   người chịu thời gian chờ và kết quả xử lý.                   │
│                                                                │
│ Workflow thủ công hiện tại (5 bước):                           │
│ 1. CSKH/BQL tiếp nhận yêu cầu bảo trì                          │
│ → 2. CSKH/BQL tìm căn hộ, phạm vi và lịch sử ticket            │
│ → 3. Kỹ thuật/nhà thầu cập nhật ảnh, ghi chú, checklist        │
│ → 4. BQL đối chiếu lần can thiệp mới nhất với bằng chứng       │
│ → 5. Người có thẩm quyền đóng, mở lại hoặc yêu cầu bổ sung     │
│                                                                │
│ Bước nào tốn nhất? Bước 2 và 4: tìm lịch sử và đối chiếu       │
│ bằng chứng (3 + 8 = 11/20 phút/ticket, ước tính).              │
│                                                                │
│ AI hỗ trợ ở bước 2 và 4: đọc ghi chú, chú thích ảnh và         │
│ checklist; trích mốc/phạm vi/câu nguồn. Người xem ảnh gốc;     │
│ rule tìm bằng chứng sau can thiệp từ dữ kiện đã xác nhận.      │
│                                                                │
│ Metric thành công (đề xuất trên 30 ca mô phỏng):               │
│   Gắn cờ 10/10 ca thiếu bằng chứng sau can thiệp;              │
│   tối đa 1 cờ thiếu nhầm/10 ca có đủ bằng chứng phù hợp.       │
│   10/10 ca thiếu/lệch hoặc mơ hồ chuyển review thủ công.       │
│   Median thao tác hồ sơ: ~20 → ≤10 phút, gồm cả duyệt.         │
│                                                                │
│ Quick Architecture: [ ] No AI [x] Rule [x] LLM [ ] Agent       │
│ Boundary: không tự đóng/mở ticket, điều nhà thầu, hứa SLA hay  │
│ đánh giá chất lượng/sự an toàn của hạng mục.                   │
└────────────────────────────────────────────────────────────────┘
```

**⚡ Stress-Test (CFO và Trưởng phòng Vận hành phản biện)** — ba góc theo worksheet:

- **Logic:** ticket mở lại có thể là lỗi mới. Ngược lại, ticket có ảnh cũ nhưng đã có đủ bằng chứng mới thì không được gắn cờ thiếu chỉ vì ảnh cũ còn tồn tại. BQL/kỹ sư xác nhận phạm vi và quyết định trạng thái; AI không đánh giá chất lượng sửa chữa.
- **Metric:** 20 phút/ticket là baseline ước tính. So ba phương án thủ công, biểu mẫu + rule, và cùng biểu mẫu/rule có thêm LLM; tính cả thời gian người xác nhận/duyệt để không gán lợi ích của biểu mẫu cho AI.
- **Rule-based:** nếu mọi mốc, phạm vi và bằng chứng đã có cấu trúc thì rule đủ. Gắn nhãn riêng nhóm văn bản tự do trong 30 ca để so B và C. Chỉ giữ LLM nếu C nhanh hơn B mà không tăng lỗi; không đạt thì **NO-GO cho LLM**. Ghi chú thiếu ngữ cảnh phải trả `null`/cần xác minh, không đoán.

---

## 🃏 Card #2 — Vinpearl: Bàn giao yêu cầu khách đoàn đa kênh

```text
┌────────────────────────────────────────────────────────────────┐
│ QUICK PROBLEM CARD #2                                          │
│                                                                │
│ Bài toán: Yêu cầu khách đoàn đi qua email, điện thoại và       │
│ tin nhắn; khi chuyển ca, người nhận thiếu số phòng,            │
│ mốc thời gian hoặc yêu cầu đặc biệt.                           │
│                                                                │
│ Công ty thành viên: [x] Vinpearl                               │
│                                                                │
│ Ai đang đau (Actor)?                                           │
│   Nhân viên booking, điều phối dịch vụ và người nhận ca.       │
│                                                                │
│ Workflow thủ công hiện tại (5 bước):                           │
│   1. Nhận yêu cầu                                              │
│   → 2. Ghép và trích thông tin đa kênh                         │
│   → 3. Xác nhận với người gửi                                  │
│   → 4. Giao bộ phận phụ trách                                  │
│   → 5. Theo dõi phản hồi.                                      │
│                                                                │
│ Bước nào tốn nhất? Bước 2–3 (~10 phút/handoff, ước tính).      │
│ AI hỗ trợ ở bước 2: đề xuất 5 dữ kiện và câu nguồn; rule       │
│ kiểm thiếu dữ kiện, nhân viên hỏi lại và xác nhận.             │
│                                                                │
│ Metric thành công (đề xuất trên 20 handoff mô phỏng):          │
│   ≥18/20 bản nháp trích đúng toàn bộ dữ kiện có trong nguồn;   │
│   100% dữ kiện thiếu được gắn cờ; median bước 2–3 ≤5 phút.     │
│   5 dữ kiện: mã đoàn, số phòng, ngày đến, ngày đi, yêu cầu.    │
│                                                                │
│ Quick Architecture: [ ] No AI [x] Rule [x] LLM [ ] Agent       │
│ Boundary: không tự hứa dịch vụ, đổi giá, tạo booking hay gửi   │
│ xác nhận ra ngoài.                                             │
└────────────────────────────────────────────────────────────────┘
```

---

## 🃏 Card #3 — VinFast: Gom phiếu sửa chữa để kỹ sư review

```text
┌────────────────────────────────────────────────────────────────┐
│ QUICK PROBLEM CARD #3                                          │
│                                                                │
│ Bài toán: Mô tả triệu chứng trong phiếu sửa chữa/bảo hành có   │
│ thể khác cách diễn đạt, khiến nhân viên khó gom các trường     │
│ hợp cần kỹ sư chất lượng đọc cùng nhau.                        │
│                                                                │
│ Công ty thành viên: [x] VinFast                                │
│                                                                │
│ Ai đang đau (Actor)?                                           │
│   Nhân viên bảo hành và kỹ sư chất lượng.                      │
│                                                                │
│ Workflow thủ công hiện tại (4 bước):                           │
│   1. Nhận phiếu                                                │
│   → 2. Lọc dữ kiện có cấu trúc                                 │
│   → 3. Đọc mô tả và gom phiếu liên quan                        │
│   → 4. Chuyển kỹ sư review.                                    │
│                                                                │
│ Bước nào tốn nhất? Bước 3 (~15 phút/lô 10 phiếu, ước tính).    │
│ AI hỗ trợ ở bước 3: đề xuất nhóm và câu nguồn, kỹ sư duyệt.    │
│                                                                │
│ Metric thành công (đề xuất): trên 20 cặp phiếu, tìm ≥9/10 cặp  │
│ liên quan và gom nhầm ≤1/10 cặp không liên quan; 100% nhóm     │
│ đề xuất phải qua kỹ sư review.                                 │
│                                                                │
│ Quick Architecture: [ ] No AI [x] Rule [x] LLM [ ] Agent       │
│ Boundary: không chẩn đoán lỗi, ra lệnh sửa chữa, phát thông    │
│ báo thu hồi hay khẳng định rủi ro an toàn.                     │
└────────────────────────────────────────────────────────────────┘
```

---

## 🗳️ Quyết định lựa chọn bài toán cho Deep-Dive

> **Chọn Card #1 — Vinhomes: Rà soát bằng chứng đóng/mở lại ticket bảo trì cư dân** để thực hiện Phase 3.

**Vì sao chọn:**

1. **Gần vận hành Vinhomes và có pain rõ:** cư dân, CSKH/BQL và đội kỹ thuật cùng tham gia; ticket bị chậm đóng hoặc mở lại gây công rà soát và trải nghiệm không tốt.
2. **Tình huống biên có cơ chế kiểm tra được:** kiểm tra đã có bằng chứng phù hợp sau lần can thiệp liên quan mới nhất hay chưa; có thể đối chiếu căn hộ, phạm vi, mốc tạo và nguồn thay vì chỉ nhìn giờ tải lên.
3. **AI có vai trò hẹp nhưng hợp lý:** rule kiểm mốc/dữ kiện có cấu trúc; LLM đọc ghi chú tự do, trích câu nguồn và chỉ đề xuất cờ review.
4. **Ranh giới vận hành rõ:** không có hành động tự trị; người có thẩm quyền mới đóng/mở ticket, điều phối nhà thầu hoặc trả lời cư dân.

**Lý do chưa chọn các thẻ khác:**

- **Card #2 (Vinpearl):** cần chuẩn hóa biểu mẫu và bàn giao trước; khi dữ liệu đã đủ dữ kiện thì rule có thể đáp ứng mà chưa cần LLM.
- **Card #3 (VinFast):** cần dữ liệu kỹ thuật đã gán nhãn và người có chuyên môn xác nhận các cặp phiếu liên quan; phải chuẩn bị thêm trước khi thử nghiệm.

**Kịch bản minh hoạ:** 09:00 nhà thầu cập nhật “đã sửa”; 10:00 BQL nhận checklist/ảnh; 13:00 có can thiệp mới cùng phạm vi; 14:00 ticket được đề nghị review nhưng bộ hồ sơ chỉ có bằng chứng 09:00–10:00. Hệ thống ghi **“chưa tìm thấy bằng chứng sau lần can thiệp mới nhất trong hồ sơ được cung cấp”** để BQL/kỹ sư xử lý. Nếu đã có đủ bằng chứng phù hợp lúc 13:30, không gắn cờ thiếu vì ảnh cũ vẫn còn; quyết định đóng/mở vẫn do người có thẩm quyền.

Cơ sở công khai, ba ví dụ input → JSON → rule và cách kiểm tra giả thuyết được trình bày trong [02-deep-dive-report.md](02-deep-dive-report.md). Tình huống dùng bằng chứng cũ tại Vinhomes vẫn cần xác minh, chưa phải sự cố đã được nguồn công khai xác nhận.
