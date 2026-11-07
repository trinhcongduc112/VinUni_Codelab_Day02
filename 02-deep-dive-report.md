# 02 — Deep-Dive Report: Ra viện không khe hở
### Vinmec International Hospital × Vin Smart Future | Lab 02

**Công ty thành viên:** Vinmec · **Phạm vi pilot:** Khoa Nội Tổng quát – Vinmec Times City · **Nguồn đề tài:** Card #1 trong [01-problem-scan.md](01-problem-scan.md)

> Quy trình hiện tại là **giả định** dựa trên quy trình phổ biến ở bệnh viện và tài liệu công khai, chưa phải kết quả khảo sát tại Vinmec. Số liệu nội bộ được ghi rõ *(ước tính)*; số liệu công khai có nguồn ở cuối bài (phần lớn là nghiên cứu ở Mỹ, cần đo lại tại Vinmec).

---

## 🏛️ Bối cảnh và khung phân tích

**Ý tưởng ban đầu:** AI soạn nháp tóm tắt xuất viện và bản dễ hiểu cho bệnh nhân; bác sĩ duyệt và ký.

**Mở rộng:** viết nhanh hơn chưa đủ, vì phần nguy hiểm nhất nằm *sau* khi bệnh nhân ra về: kết quả trả về muộn và khuyến nghị theo dõi không có người nhận. Vì vậy đề tài bao trọn **toàn bộ dòng thông tin chuyển tiếp**, từ lúc nằm viện cho đến khi mọi việc còn dở được đóng.

Bài dùng hai trục phân loại MECE (không chồng lấn, không bỏ sót):

| Trục | Các nhóm | Dùng cho |
|---|---|---|
| **Giai đoạn** | Trong viện · Lúc ra viện · Sau ra viện | Quy trình hiện tại (3.1) và quy trình tương lai (3.3) |
| **Loại thông tin** | **Đã xảy ra** (lý do vào viện, diễn biến, thủ thuật, kết quả đã có) · **Hiện trạng khi ra viện** (chẩn đoán, thuốc mang về và thay đổi so với lúc vào, dị ứng) · **Việc còn mở** (kết quả chờ, khuyến nghị theo dõi, lịch tái khám, dấu hiệu cần quay lại viện) | Nội dung giấy ra viện và sổ dữ kiện |

Mọi thông tin về đợt điều trị thuộc đúng một nhóm: quá khứ, hiện tại hoặc tương lai.

---

# 🏗️ Phase 3 — DEEP-DIVE

## 3.1. Current-State Workflow Mapping

Quy trình hiện tại, từ ghi chép trong viện đến lần tái khám:

```text
┌──────────────────────┐     ┌──────────────────────┐     ┌──────────────────────┐     ┌──────────────────────┐
│ Bước 1               │     │ Bước 2  BOTTLENECK   │     │ Bước 3  BOTTLENECK   │     │ Bước 4  BOTTLENECK   │
│ Ghi chép hằng ngày   │     │ Rà hồ sơ trên HIS    │     │ Soạn tóm tắt         │     │ Soạn hướng dẫn       │
│ trong viện           │     │ (nhiều màn hình)     │     │ cho bác sĩ           │     │ cho bệnh nhân        │
│ Ai: BS + điều dưỡng  │     │ Ai: Bác sĩ điều trị  │     │ Ai: Bác sĩ điều trị  │     │ Ai: Bác sĩ điều trị  │
│ TG: hằng ngày        │ ──→ │ TG: 8 phút           │ ──→ │ TG: 12 phút          │ ──→ │ TG: 8 phút           │
│ In: khám, y lệnh     │     │ In: chẩn đoán, thuốc,│     │ In: ý đã rà          │     │ In: tóm tắt          │
│ Out: ghi chú (nhiều  │     │ XN, CĐHA, ghi chú    │     │ Out: tóm tắt         │     │ Out: thuốc, tái khám,│
│ đoạn copy hôm trước) │     │ Out: ý cần đưa vào   │     │ ra viện              │     │ dấu hiệu cần quay lại│
└──────────────────────┘     └──────────────────────┘     └──────────────────────┘     └──────────────────────┘
                                                                                                   │
                                                                                                   ▼
                             ┌──────────────────────┐     ┌──────────────────────┐     ┌──────────────────────┐
                             │ Bước 7               │     │ Bước 6  BOTTLENECK   │     │ Bước 5               │
                             │ Tái khám             │     │ Kết quả XN/CĐHA về   │     │ Ký, in, giao giấy    │
                             │                      │     │ sau khi BN đã về     │     │ ra viện              │
                             │ Ai: BN → BS tái khám │     │ Ai: Phòng XN → hồ sơ │     │ Ai: BS → Điều dưỡng  │
                             │ TG: sau 1–4 tuần     │ <═══│ TG: — (không ai làm) │ <═══│ TG: 2 phút           │
                             │ In: giấy ra viện     │     │ Không ai được giao   │     │ → Bệnh nhân          │
                             │ (có thể thiếu kết quả│     │ xem kết quả          │     │ Out: BN cầm giấy về  │
                             │ mới về)              │     │ Out: kết quả nằm im  │     │                      │
                             └──────────────────────┘     └──────────────────────┘     └──────────────────────┘

Giai đoạn: Trong viện = bước 1 · Lúc ra viện = bước 2–5 · Sau ra viện = bước 6–7
🔴 BOTTLENECK = bước 2, 3, 4 (thời gian, chất lượng) · bước 6 (đứt vòng sau ra viện)
──→ = chuyển tiếp trong cùng bộ phận   ═══> = 🔄 Handoff giữa các bộ phận
⏱ Thời gian bác sĩ mỗi ca: 8 + 12 + 8 + 2 = 30 phút (bước 2–5, ước tính).
⏱ Bước 6 không tốn thời gian của ai, chính vì không ai được giao xem kết quả.
```

Sơ đồ trực quan (file nộp riêng): [04-workflow-diagram.png](04-workflow-diagram.png)

* 🔴 **Bottleneck** (3 loại, không chồng lấn):
  * **Thời gian — bước 2–4:** 28/30 phút bác sĩ mỗi ca *(ước tính)* dành để rà hồ sơ trên nhiều màn hình và viết hai bản cho hai người đọc khác nhau.
  * **Chất lượng — bước 3–4:** lỗi bỏ sót không hiện ra để người duyệt bắt, và nguồn để tóm tắt không sạch: ở một bệnh viện Mỹ, chỉ khoảng 18% chữ trong ghi chú tiến triển là gõ mới, còn lại là copy hoặc import (Wang 2017).
  * **Liên tục — bước 6:** kết quả về sau khi bệnh nhân đã ra viện không có người được giao xem. 41% bệnh nhân ra viện khi còn kết quả chờ; khoảng 9% số kết quả đó có thể làm thay đổi điều trị (Roy 2005).
* 🔄 **Handoff (4 điểm):** Bác sĩ → Điều dưỡng (bước 5) · Điều dưỡng → Bệnh nhân (bước 5) · Phòng xét nghiệm/CĐHA → hồ sơ, **không có người nhận** (bước 6) · Bệnh nhân → Bác sĩ tái khám (bước 7).
* ⏱ **Tổng cộng = 30 phút bác sĩ/ca ra viện** (bước 2–5); khoa ~12 ca/ngày → **~6 giờ bác sĩ/ngày** *(ước tính)*. Bước 6 không tốn thời gian của ai — chính vì không ai được giao.

---

## 3.2. Problem Statement (6-field) & Metrics

| Field | Nội dung chi tiết |
|---|---|
| **1. Actor / Operator** | **Người thao tác hằng ngày:** bác sĩ điều trị khoa Nội (rà hồ sơ, soạn, ký) và điều dưỡng (in, bàn giao).<br>**Người nhận thông tin:** bệnh nhân và gia đình; bác sĩ tái khám.<br>**Người đặt quy định:** trưởng khoa; phòng Quản lý chất lượng (phụ trách chuẩn JCI). |
| **2. Current Workflow** | Trong viện, bác sĩ và điều dưỡng ghi chép hằng ngày trên HIS nhưng không ai tổng hợp. Khi có y lệnh ra viện, bác sĩ mở nhiều màn hình (chẩn đoán, thuốc, xét nghiệm, chẩn đoán hình ảnh, ghi chú) để rà, soạn tóm tắt cho bác sĩ, soạn tiếp hướng dẫn dễ hiểu cho bệnh nhân, rồi ký và giao qua điều dưỡng. Sau ra viện, kết quả trả về được lưu vào hồ sơ mà không có người được giao xem. **7 bước, 4 handoff, ~30 phút bác sĩ/ca** *(ước tính)*. |
| **3. Bottleneck** | **Thời gian (bước 2–4):** 28/30 phút/ca để rà và viết hai bản *(ước tính)*.<br>**Chất lượng (bước 3–4):** bỏ sót không ai nhìn thấy; nguồn tóm tắt chứa nhiều đoạn copy từ ngày trước.<br>**Liên tục (bước 6):** kết quả về sau ra viện và khuyến nghị theo dõi nằm trong văn bản tự do không có người phụ trách. |
| **4. Business Impact** | • **Thời gian:** ~12 ca/ngày × 30 phút ≈ **6 giờ bác sĩ/ngày/khoa** *(ước tính)*.<br>• **Chất lượng chăm sóc:** giấy ra viện chỉ có mặt ở **12–34%** lần tái khám đầu tiên; chất lượng chăm sóc bị ảnh hưởng ở khoảng **1/4** lần tái khám (Kripalani 2007).<br>• **An toàn:** **41%** bệnh nhân ra viện khi còn kết quả chờ, khoảng **9%** số kết quả đó có thể thay đổi điều trị (Roy 2005); khoảng **1/7** bệnh nhân có bất thường lớn trên chẩn đoán hình ảnh được khuyến nghị theo dõi nhưng không có ghi nhận theo dõi.<br>• **Tuân thủ:** Vinmec Times City và Central Park đạt chuẩn JCI; theo bản chuẩn JCI nhóm tìm được, giấy ra viện phải được gửi cho bệnh nhân và người chăm sóc tiếp theo trong thời hạn quy định *(cần kiểm tra bản hiện hành)*. |
| **5. Success Metric** | 1. **Hiệu quả:** tổng thời gian bác sĩ cho một ca (gồm cả xác nhận hằng ngày) từ **~30 → ≤ 10 phút**; thời gian từ y lệnh ra viện đến lúc ký giảm **≥ 50%** so với baseline; thời gian bàn giao của điều dưỡng **≤ 5 phút/ca** (tăng có chủ đích so với ~2 phút hiện nay). Đo bằng audit log HIS.<br>2. **Chất lượng tài liệu:** **100%** giấy ra viện đủ 3 nhóm thông tin (đã xảy ra · hiện trạng · việc còn mở); điểm PDQI-9 của bản có AI hỗ trợ **không thấp hơn** bản viết tay (2 bác sĩ chấm mù, ≥ 100 hồ sơ).<br>3. **An toàn & liên tục:** **0** lỗi nghiêm trọng (bịa, sai thuốc) trong bản đã ký trên mẫu kiểm tra ngẫu nhiên; **≥ 90%** bệnh nhân tự nhắc lại đúng 3 điều khi bàn giao (thuốc thay đổi, lịch tái khám, dấu hiệu phải quay lại viện); **100%** giấy ra viện có sẵn cho bác sĩ tái khám trong hệ thống Vinmec trước lần tái khám đầu; **≥ 95%** kết quả về sau ra viện được người phụ trách xác nhận trong **72 giờ**; số việc còn mở bị bỏ sót giảm **≥ 50%** so với baseline.<br>4. **Chấp nhận:** **≥ 70%** cảnh báo được bác sĩ xác nhận là đúng (tránh "nhờn" cảnh báo); **≥ 80%** ca ra viện ở khoa pilot dùng hệ thống. |
| **6. Operational Boundary** | **Phạm vi:** khoa Nội Tổng quát – Vinmec Times City; người lớn; nằm viện ≤ 7 ngày; không phẫu thuật; tiếng Việt. Ngoài phạm vi: nhi, sản, ca tử vong hoặc chuyển viện, mã ICD/bảo hiểm, bản tiếng Anh.<br>**AI được tự làm:** đọc dữ liệu của đúng bệnh nhân được giao; đề xuất dữ kiện kèm trích dẫn nguồn; **thêm** cờ bỏ sót và việc còn mở; **nâng** mức ưu tiên; soạn nháp có nhãn `[DRAFT – CHỜ BÁC SĨ KÝ DUYỆT]`.<br>**Phải có người duyệt (HITL):** đưa dữ kiện vào sổ; danh sách việc còn mở và người phụ trách; giấy ra viện (bác sĩ ký số; chỉ bản đã ký mới được gửi cho bệnh nhân và bác sĩ tái khám); mọi thông báo khác gửi bệnh nhân.<br>**TUYỆT ĐỐI KHÔNG:** tự viết con số (liều thuốc, giá trị xét nghiệm chỉ do code chép từ dữ liệu gốc); xóa, ẩn hoặc hạ mức bất kỳ kết quả hay việc còn mở nào; tự gửi thông tin cho bệnh nhân; đưa chẩn đoán mới hoặc đề xuất đổi điều trị; giải thích kết quả bất thường trực tiếp cho bệnh nhân; truy cập hồ sơ ngoài phạm vi.<br>**Ràng buộc dữ liệu & pháp lý:** dữ liệu sức khỏe là dữ liệu cá nhân nhạy cảm theo Luật Bảo vệ dữ liệu cá nhân 2025 và Nghị định 356/2025/NĐ-CP → đánh giá tác động trước khi xử lý, chỉ dùng dữ liệu tối thiểu, ghi log truy cập, ưu tiên chạy trên hạ tầng nội bộ; tích hợp với bệnh án điện tử theo Thông tư 13/2025/TT-BYT. |

---

## 3.3. Future-State Flow & AI Fit

* **Xác định mức AI Fit (AI-Fit Matrix):** [ ] Rule / State-Machine  [x] **LLM Feature** (kết hợp lớp rule)  [ ] Agentic Loop

| Tiêu chí | Rule / State-Machine | LLM Feature | Agentic Loop |
|---|---|---|---|
| Lọc y lệnh chưa có kết quả, theo dõi hạn, nhắc việc | **Tốt nhất** — xác định, đã được thử nghiệm (email báo kết quả chờ, Dalal 2014) | Không cần | Không cần |
| Đối chiếu sổ dữ kiện với dữ liệu có cấu trúc trong HIS | **Tốt nhất** — kiểm tra lại được | Không nên giao cho LLM | Không cần |
| Đọc văn bản tự do: ghi chú, kết quả CĐHA/giải phẫu bệnh, viết tắt (THA, ĐTĐ), phủ định ("không loại trừ…") | Kém — dò từ khóa bỏ sót | **Tốt** — LLM tìm ra số ca cần chụp theo dõi gấp **6,18 lần** hệ thống thủ công (Parkland 2026) | Tốt, nhưng không thêm năng lực cần thiết |
| Viết lời: đoạn diễn biến, bản cho bệnh nhân, tóm tắt bối cảnh | Template cứng, khó đọc | **Tốt** — bản cho bệnh nhân dễ đọc hơn hẳn (trình độ lớp 11 → lớp 6), nhưng 18% lượt đánh giá có lo ngại an toàn (Zaretsky 2024) → bắt buộc duyệt | Không cần |
| Rủi ro chính | Bỏ sót phần văn bản tự do | Bịa và bỏ sót (GPT-4 bỏ sót ở 47% bản tóm tắt; chỉ bắt được 64% báo cáo cần theo dõi) → kiểm soát bằng quyền một chiều, trích dẫn nguồn, code chép số, bác sĩ duyệt | Tự hành động trong lĩnh vực lâm sàng — không chấp nhận được |

→ **Chọn LLM Feature kết hợp Rule:** rule làm toàn bộ phần có cấu trúc và là lưới an toàn; LLM chỉ làm 6 việc đọc–viết (T1, T4, T6, T7, T12, T14 bên dưới). Không dùng Agent vì không có bước nào cần AI tự quyết định hay tự hành động. **Quy tắc quyền một chiều:** AI chỉ được thêm cảnh báo hoặc nâng mức, không bao giờ được xóa, ẩn hay hạ — nên lỗi tệ nhất của AI là một cảnh báo thừa, không phải một kết quả bị mất.

* **Future-State Flow** (16 bước, mỗi bước có đúng một chủ: 🔵 AI · [RULE]/[CODE] · 🟢 Người):

```text
━━ GIAI ĐOẠN 1 · TRONG VIỆN (lặp lại mỗi ngày) ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 T1  · 🔵 AI — đọc ghi chú, y lệnh, kết quả mới trong ngày → đề xuất dữ kiện, mỗi dữ kiện kèm
       trích dẫn nguồn (ghi chú nào, ngày nào); con số do code chép
        ▼
 T2  · 🟢 Bác sĩ — xác nhận / sửa / loại dữ kiện khi đi buồng (~1 phút/ngày, ước tính)
       → SỔ DỮ KIỆN đã xác minh: đã xảy ra · hiện trạng · việc còn mở
        ▼
━━ GIAI ĐOẠN 2 · LÚC RA VIỆN (từ y lệnh ra viện đến khi bệnh nhân rời khoa) ━━━━━━━━━━━━━━━━━━━━━━━
 T3  · [RULE] — đối chiếu sổ với HIS: sự kiện có trong HIS mà chưa có trong sổ → cờ đỏ bỏ sót;
       y lệnh chưa có kết quả → thêm vào việc còn mở
        ▼
 T4  · 🔵 AI — tìm việc còn mở ẩn trong văn bản: khuyến nghị theo dõi trong kết quả CĐHA/giải
       phẫu bệnh, xét nghiệm gửi ngoài, kế hoạch trong ghi chú (chỉ được thêm)
        ▼
 T5  · [CODE] — điền phần có cấu trúc của giấy ra viện từ sổ: chẩn đoán, thuốc, kết quả, lịch hẹn
        ▼
 T6  · 🔵 AI — viết đoạn diễn biến cho bản bác sĩ, chỉ từ dữ kiện đã xác minh; không tự viết số
        ▼
 T7  · 🔵 AI — viết bản dễ hiểu cho bệnh nhân: thuốc thay đổi, lịch tái khám, dấu hiệu phải quay
       lại viện và danh sách việc còn mở bằng lời dễ hiểu; không tự viết số
        ▼
 T8  · 🟢 Bác sĩ — duyệt 2 bản, bấm "đã xem" từng cờ đỏ, giao người phụ trách và hạn chót cho
       từng việc còn mở, ký số (~5 phút, ước tính)
        ▼
 T9  · 🟢 Điều dưỡng — bàn giao cho bệnh nhân/gia đình: giấy ra viện, bản dễ hiểu, danh sách việc
       còn mở (kết quả nào đang chờ, ai sẽ liên lạc, khi nào); hỏi lại để bệnh nhân tự nhắc 3
       điều: thuốc thay đổi, lịch tái khám, dấu hiệu phải quay lại viện; xác nhận số điện thoại
       nhận thông báo (~5 phút, ước tính)
        ▼
 T10 · [CODE] — hoàn tất ra viện: gửi bản điện tử đã ký cho bệnh nhân và bác sĩ tái khám, đặt
       lịch tái khám, bật theo dõi cho từng việc còn mở
        ▼
━━ GIAI ĐOẠN 3 · SAU RA VIỆN (đến khi việc còn mở cuối cùng được đóng) ━━━━━━━━━━━━━━━━━━━━━━━━━━━
 T11 · [RULE] — theo dõi việc còn mở: kết quả về → báo người phụ trách; quá 72 giờ chưa xác nhận
       → báo trưởng khoa; bệnh nhân lỡ lịch tái khám → báo điều dưỡng
        ▼
 T12 · 🔵 AI — gợi ý mức ưu tiên ("có thể cần hành động" + lý do) và tóm tắt bối cảnh 3 dòng có
       trích dẫn; chỉ được NÂNG mức, không được hạ hay ẩn
        ▼
 T13 · 🟢 Bác sĩ phụ trách — quyết định: gọi bệnh nhân / hẹn khám sớm / không cần làm gì (đóng
       việc ngay)
        ▼
 T14 · 🔵 AI — soạn nháp thông báo dễ hiểu cho bệnh nhân
        ▼
 T15 · 🟢 Bác sĩ phụ trách — duyệt thông báo rồi mới gửi → đóng việc
        ▼
 T16 · 🟢 Bác sĩ tái khám — xem giấy ra viện và danh sách việc còn mở; đóng các việc còn lại hoặc
       giao tiếp cho người khác. Vòng chỉ khép khi không còn việc nào mở.

 ↩️ FALLBACK:
    • AI lỗi / quá thời gian / sai định dạng (T1, T4, T6, T7, T12, T14) → bỏ qua phần AI; bác sĩ
      dùng template trống như quy trình cũ; rule vẫn chạy nên mọi kết quả vẫn đến bác sĩ
    • Dữ kiện không có trích dẫn hợp lệ → không được đưa vào sổ
    • Bệnh nhân không nhắc lại được 3 điều (T9) → điều dưỡng giải thích lại; vẫn chưa rõ → báo bác sĩ
    • Không liên lạc được bệnh nhân (T13) → gọi người nhà đã đăng ký; vẫn không được → báo trưởng khoa
    • Hệ thống dừng → quay về quy trình cũ; không mất dữ liệu vì HIS vẫn là nguồn gốc

 ⏱ Bác sĩ: ~1 phút/ngày × ~5 ngày + ~5 phút duyệt và ký ≈ 10 phút/ca (hiện ~30 phút)
 ⏱ Điều dưỡng: ~5 phút bàn giao (hiện ~2 phút) — tăng có chủ đích để bệnh nhân hiểu đúng
```

* **Đối chiếu hiện tại → tương lai** (mỗi bước hiện tại đều có bước tương lai tương ứng; mỗi bước tương lai thuộc đúng một bước hiện tại):

| Bước hiện tại (3.1) | Bước tương lai | Điều thay đổi |
|---|---|---|
| 1. Ghi chép hằng ngày | T1–T2 | Dữ kiện được xác minh ngay trong ngày, không dồn đến lúc ra viện |
| 2. Rà hồ sơ trên HIS | T3–T4 | Rule và AI rà thay bác sĩ; chỗ bỏ sót thành cờ đỏ |
| 3. Soạn tóm tắt cho bác sĩ | T5–T6 | Code điền số liệu, AI viết lời |
| 4. Soạn hướng dẫn cho bệnh nhân | T7 | AI viết bản dễ hiểu từ cùng một sổ dữ kiện |
| 5. Ký, in, giao giấy ra viện | T8–T10 | Tách thành 3 bước, mỗi bước một chủ: bác sĩ ký · điều dưỡng bàn giao có hỏi lại · hệ thống gửi bản điện tử, đặt lịch, bật theo dõi |
| 6. Kết quả về, không ai nhận | T11–T15 | Có người phụ trách, hạn 72 giờ, quá hạn thì báo trưởng khoa |
| 7. Tái khám | T16 | Bác sĩ tái khám có sẵn giấy ra viện và danh sách việc còn mở; vòng chỉ khép khi không còn việc nào mở |

---

# 🏁 Phase 5 — EVALUATE

### AI Readiness Checklist:
1. [ ] **Chúng tôi có sẵn dữ liệu mẫu/logs sạch để test?** — *Chưa.* Bệnh án điện tử đã bắt buộc tại bệnh viện chậm nhất từ 30/9/2025 (Thông tư 13/2025/TT-BYT) nên dữ liệu nhiều khả năng đã có, nhưng nhóm chưa có quyền truy cập và chưa biết mức độ copy trong ghi chú. Giấy ra viện cũ **không dùng làm đáp án**, vì chính chúng cũng bỏ sót; bộ đáp án phải do bác sĩ gán từ hồ sơ gốc.
2. [x] **Rủi ro khi AI sai có nằm trong tầm kiểm soát (qua HITL hoặc Fallback)?** — *Có, theo thiết kế.* AI chỉ được thêm, không được xóa hay hạ mức; code chép mọi con số; bác sĩ xác nhận dữ kiện và ký; AI lỗi thì rule và template cũ vẫn chạy. Rủi ro còn lại — bác sĩ tin AI mà ký không đọc kỹ, hoặc "nhờn" cảnh báo — được đo bằng tỉ lệ cảnh báo đúng và thời gian duyệt mỗi ca.
3. [ ] **Stakeholders sẵn sàng thay đổi quy trình làm việc cũ?** — *Chưa xác nhận.* Chưa phỏng vấn bác sĩ, điều dưỡng và phòng Quản lý chất lượng. Chưa có quy định ai chịu trách nhiệm một kết quả về sau khi bệnh nhân ra viện — đây là bài toán tổ chức, AI không giải được.

### Quyết định cuối cùng của Ban Giám Đốc Vin Smart Future:
[ ] **GO (Bắt đầu xây dựng Prototype):** Bắt đầu phát triển với scope hẹp.<br>
[x] **NOT YET (Cần tích lũy thêm dữ liệu/xác lập baseline):** Trì hoãn để chuẩn bị thêm.<br>
[ ] **NO-GO (Không khả thi / Rule-based tốt hơn):** Hủy bỏ dự án AI này.

**Justification (Lý giải quyết định dựa trên bằng chứng kỹ thuật và chi phí):**
> **Vì sao không NO-GO:** Pain có bằng chứng mạnh từ các nghiên cứu lớn (41% bệnh nhân ra viện còn kết quả chờ; giấy ra viện chỉ có mặt ở 12–34% lần tái khám đầu). Rule-based giải quyết tốt phần có cấu trúc nhưng không đọc được khuyến nghị theo dõi trong văn bản tự do — đúng chỗ LLM tìm ra nhiều gấp 6,18 lần hệ thống thủ công ở Parkland. Chi phí chính là tích hợp HIS và máy chủ chạy nội bộ, không phải tiền model: mỗi ca chỉ cần đọc khoảng 20.000 token *(ước tính)*, và có thể dùng model mã nguồn mở như Parkland đã làm.
>
> **Vì sao chưa GO:** (1) Chưa có dữ liệu được phép dùng và chưa có baseline tại Vinmec — các con số trên là của Mỹ. (2) Stakeholders chưa xác nhận và chưa có quy định về người phụ trách việc còn mở. (3) Nhóm chưa tìm thấy nghiên cứu nào trên văn bản y khoa tiếng Việt (nhiều viết tắt như THA, ĐTĐ, CTM), nên chưa biết AI đạt mức nào.
>
> **Làm ngay, không cần chờ:** dựng prototype trên hồ sơ giả lập có cài sẵn việc còn mở bị giấu trong văn bản; phỏng vấn 3–5 bác sĩ và điều dưỡng; thiết kế nghiên cứu offline.
>
> **Điều kiện chuyển sang GO** (pilot 1 khoa, chạy im lặng 4 tuần trước khi cho bác sĩ thấy): (1) đo baseline ≥ 2 tuần bằng audit log HIS; (2) có ≥ 200 hồ sơ ẩn danh được duyệt và bộ đáp án do 2 bác sĩ gán; (3) trên bộ đó, AI + rule tìm được nhiều việc còn mở hơn chỉ dùng rule, với độ nhạy ≥ 90% và tỉ lệ cảnh báo đúng ≥ 70%; (4) bệnh viện ban hành quy định người phụ trách việc còn mở; (5) hoàn thành đánh giá tác động xử lý dữ liệu cá nhân. Nếu điều kiện (3) không đạt → **NO-GO** cho LLM, giữ giải pháp rule (tự động báo kết quả chờ).

---

### Nguồn tham khảo
* **Pain point:** Kripalani et al., JAMA 2007 — [PSNet](https://psnet.ahrq.gov/issue/deficits-communication-and-information-transfer-between-hospital-based-and-primary-care); Roy et al., Ann Intern Med 2005 — [PSNet](https://psnet.ahrq.gov/issue/patient-safety-concerns-arising-test-results-return-after-hospital-discharge); Wang et al., JAMA Intern Med 2017 — [PubMed](https://pubmed.ncbi.nlm.nih.gov/28558106/); tỉ lệ không theo dõi phát hiện trên chẩn đoán hình ảnh (JAMA Network Open) — [Reed Smith](https://viewpoints.reedsmith.com/post/102htla/how-prevalent-is-failure-to-follow-up-on-radiologists-incidental-findings-and-th)
* **AI và cách đánh giá:** Williams et al. 2024, GPT-4 tóm tắt ra viện — [medRxiv](https://www.medrxiv.org/content/10.1101/2024.04.03.24305088.full.pdf); Zaretsky et al., JAMA Netw Open 2024 — [JAMA](https://jamanetwork.com/journals/jamanetworkopen/fullarticle/10.1001/jamanetworkopen.2024.0347); Dalal et al., JAMIA 2014 — [PSNet](https://psnet.ahrq.gov/issue/impact-automated-email-notification-system-results-tests-pending-discharge-cluster-randomized); Parkland Health, NEJM Catalyst 2026 — [AuntMinnie](https://www.auntminnie.com/clinical-news/digital-x-ray/article/15817694/ai-accurately-flags-followup-imaging-recommendations); GPT-4 và Pennsylvania Act 112 — [SIIM 2025](https://annualmeeting.siim.org/wp-content/uploads/2025/04/Automating-Pennsylvania-Act-112-Satvik-Tripathi.pdf); PDQI-9 — [Stetson et al. 2012](https://pmc.ncbi.nlm.nih.gov/articles/PMC3347480)
* **Vinmec và pháp lý:** Vinmec Times City đạt JCI — [Vinmec](https://www.vinmec.com/eng/blog/vinmec-times-city-achieves-jci-certification-for-the-fourth-time); Vinmec Central Park đạt JCI — [Vinmec](https://www.vinmec.com/eng/blog/vinmec-central-park-hospital-achieves-global-jci-accreditation); chuẩn JCI về giấy ra viện (bản errata 2011, nguồn không chính thức) — [Scribd](https://www.scribd.com/doc/308048022/Errata-for-Hospital-06-20-11); Thông tư 13/2025/TT-BYT — [caselaw.vn](https://caselaw.vn/bai-viet/ho-so-benh-an-dien-tu-bat-buoc-trien-khai-cham-nhat-tu-30-9-2025-theo-thong-tu-13-2025-tt-byt); Luật Bảo vệ dữ liệu cá nhân 2025 — [hoatieu.vn](https://hoatieu.vn/phap-luat/luat-bao-ve-du-lieu-ca-nhan-so-91-2025-qh15-234849); Nghị định 356/2025/NĐ-CP — [luatvietnam.vn](https://luatvietnam.vn/dan-su/nghi-dinh-356-2025-nd-cp-quy-dinh-chi-tiet-luat-bao-ve-du-lieu-ca-nhan-422896-d1.html)
