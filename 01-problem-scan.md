# Lab 02 — Deliverable 1: Problem Scan & Quick Assessments
**Đơn vị:** Vin Smart Future — Tập đoàn Vingroup  
**Dự án:** Sáng kiến Tối ưu hóa Vận hành & Trải nghiệm Khách hàng bằng Trí tuệ Nhân tạo  
**Học viên thực hiện:** Nguyễn Tuấn Kiệt (AI Product Engineer)  

---

## 🏛️ 1. Bối cảnh & Mục tiêu

Tại **Vin Smart Future**, các kỹ sư AI và Product Engineer đóng vai trò chủ chốt trong việc tìm kiếm các điểm nghẽn (bottlenecks) và rò rỉ hiệu suất vận hành (operational inefficiency) xuyên suốt các công ty thành viên Vingroup: **VinFast, Xanh SM (GSM), Vinhomes, Vinmec, Vinpearl**. 

Tài liệu này thể hiện giai đoạn **Phase 1 (SCAN)** nhằm quét cơ hội bằng 4 Lenses tư duy và **Phase 2 (QUICK-ASSESS)** nhằm định hình nhanh 3 bài toán tiềm năng nhất trước khi chọn ra bài toán trọng tâm để tiến hành Deep-Dive.

---

# 🔍 Phase 1 — SCAN: Bảng quét cơ hội (Opportunity Scan)

Sử dụng **4 Lenses** phân tích:
1. **Lặp lại (Repetitive):** Tác vụ tuần hoàn hàng ngày, tần suất cao, tốn nhân lực cho việc nhập liệu, tra cứu cố định.
2. **Tốn thời gian (Time-consuming):** Tác vụ thủ công ngốn thời gian xử lý của nhân sự cấp cao hoặc điều phối viên.
3. **AI có thể tốt hơn (AI-upgrade):** Tác vụ hiện tại xử lý rập khuôn, thiếu cá nhân hóa hoặc chatbot truyền thống không hiểu ngữ cảnh tiếng Việt phức tạp.
4. **Pain từ người khác (Stakeholder Pain):** Điểm nghẽn gây ức chế, phàn nàn trực tiếp cho khách hàng, tài xế hoặc y bác sĩ thực địa.

### 📝 Bảng tổng hợp 6 bài toán thực tế tại Vingroup:

| # | Đơn vị thành viên (Subsidiary) | Lens áp dụng | Tên bài toán / Nghiệp vụ | Mô tả ngắn bài toán & Điểm nghẽn thực tế |
|---|---|---|---|---|
| **1** | **Xanh SM (GSM)** | **Tốn thời gian & Stakeholder Pain** | Ứng phó sự cố cạn pin/sạc xe taxi điện trên đường | Khi tài xế taxi điện báo nguy cơ hết pin (< 5%) hoặc trạm sạc quá tải, điều phối viên mất 15-20 phút tra cứu bản đồ, tình trạng trụ sạc và gõ tin chỉ đường thủ công, gây ùn ứ xe và nguy cơ chết máy giữa đường. |
| **2** | **Vinhomes** | **Lặp lại & AI-upgrade** | Phân loại và điều hướng phản ánh cư dân (Resident Ticket Triage) | Cư dân gửi hàng nghìn phản ánh tự do qua ứng dụng Vinhomes Resident (hỏng đèn, rò rỉ nước, tiếng ồn, đăng ký đỗ xe). CSKH mất 12-24 giờ để đọc, phân loại thủ công và chuyển giao cho ban quản lý tòa nhà tương ứng. |
| **3** | **VinFast** | **Lặp lại** | Đối soát & So khớp hóa đơn sạc điện tại trụ đối tác | Nhân viên tài chính phải đối chiếu hàng chục nghìn log sạc từ các trạm sạc nhượng quyền/đối tác bên ngoài với hóa đơn điện tử hàng tuần, mất hàng trăm giờ làm việc mỗi tháng và dễ sai lệch dữ liệu. |
| **4** | **Vinmec** | **Tốn thời gian & Stakeholder Pain** | Soạn thảo tóm tắt hồ sơ bệnh án xuất viện (Discharge Summary) | Bác sĩ chuyên khoa mất 20–30 phút cho mỗi bệnh nhân xuất viện để tổng hợp kết quả xét nghiệm, chẩn đoán, phác đồ điều trị và dặn dò thuốc thành văn bản tóm tắt, gây quá tải giờ làm việc lâm sàng. |
| **5** | **Vinpearl / VinWonders** | **AI-upgrade** | Trợ lý ảo tư vấn & xếp lịch trình vui chơi cá nhân hóa | Du khách gặp khó khăn khi lên kế hoạch vui chơi tại các quần thể lớn (Phú Quốc United Center, Nha Trang), chatbot hiện tại chỉ trả lời FAQ cứng nhắc theo từ khóa, không đề xuất được tour phù hợp theo thời tiết và độ tuổi gia đình. |
| **6** | **Xanh SM (GSM)** | **Pain từ người khác** | Phân tích căn nguyên hủy chuyến xe (Cancellation Root-Cause Analysis) | Trích xuất thông tin từ ghi chú tài xế và ghi âm cuộc gọi hủy chuyến để phát hiện các khu vực thiếu xe cục bộ hoặc lỗi kỹ thuật điều vận, hiện đang làm mẫu ngẫu nhiên bằng mắt thường < 5% số lượng cuốc hủy. |

---

# 🃏 Phase 2 — QUICK-ASSESS: 3 Quick Problem Cards

Từ 6 bài toán trên, 3 bài toán tiềm năng nhất được lựa chọn để thiết lập Thẻ Bài Toán Nhanh (Quick Problem Card):

---

### 📇 Quick Problem Card #1: Xanh SM — Trợ lý điều phối ứng phó sự cố pin & trạm sạc thực địa

```text
┌─────────────────────────────────────────────────────────────────────────────────────────────────┐
│ QUICK PROBLEM CARD #1                                                                           │
│                                                                                                 │
│ Bài toán (1 câu): Hỗ trợ điều phối viên Xanh SM tự động hóa tra cứu trạm sạc tương thích        │
│                   và soạn thảo chỉ dẫn khẩn cấp khi xe taxi điện gặp nguy cơ cạn pin giữa đường. │
│ Công ty thành viên: [x] Xanh SM (GSM)   [ ] VinFast   [ ] Vinhomes   [ ] Vinmec   [ ] Khác      │
│                                                                                                 │
│ Ai đang đau (Actor)?                                                                            │
│ - Điều phối viên (Dispatcher): Quá tải tra cứu đa màn hình, áp lực thời gian phản hồi.        │
│ - Tài xế Xanh SM: Lo sợ xe chết máy giữa đường phố đông đúc, mất doanh thu chuyến xe.          │
│                                                                                                 │
│ Workflow thủ công hiện tại (5 bước):                                                            │
│   1. Nhận báo cáo sự cố ──> 2. Tra GPS vị trí xe ──> 3. Tra cứu trạm sạc VinFast còn trụ trống │
│   ──> 4. Soạn tin nhắn hướng dẫn ──> 5. Điều xe sạc pin cứu hộ di động (nếu pin < 5%)          │
│                                                                                                 │
│ Bước nào tốn thời gian/lỗi nhất? Bước 3 & 4 (⏱ 10 - 12 phút/lượt)                               │
│ AI có thể nhảy vào hỗ trợ ở bước nào? Bước 3, 4 và 5: Tự động tổng hợp toạ độ, lọc trụ sạc còn  │
│ chỗ trống phù hợp dòng xe (VF5/VF8), dự thảo tin nhắn điều phối chuẩn mực và kích hoạt cứu hộ.   │
│                                                                                                 │
│ Đo thành công bằng gì (Metric có số)?                                                           │
│ - Thời gian xử lý sự cố giảm từ 15 phút ──> dưới 2.5 phút/lượt.                                │
│ - 98% chỉ dẫn gợi ý đúng loại cổng sạc và trạng thái trụ thực tế.                               │
│ - 0 trường hợp xe cạn pin trên đường do chỉ dẫn đến trạm sạc quá xa (> 5km khi pin < 5%).       │
│                                                                                                 │
│ Quick Architecture: [ ] No AI   [ ] Rule   [x] LLM Feature (Draft Copilot)   [ ] Autonomous Agent│
└─────────────────────────────────────────────────────────────────────────────────────────────────┘
```

---

### 📇 Quick Problem Card #2: Vinhomes — Phân loại & Điều hướng ticket phản ánh cư dân thông minh

```text
┌─────────────────────────────────────────────────────────────────────────────────────────────────┐
│ QUICK PROBLEM CARD #2                                                                           │
│                                                                                                 │
│ Bài toán (1 câu): Tự động phân loại, trích xuất độ khẩn cấp và chuyển tiếp phản ánh cư dân trên │
│                   App Vinhomes Resident đến đúng phòng kỹ thuật / ban quản trị từng tòa nhà.    │
│ Công ty thành viên: [ ] Xanh SM   [ ] VinFast   [x] Vinhomes   [ ] Vinmec   [ ] Khác            │
│                                                                                                 │
│ Ai đang đau (Actor)?                                                                            │
│ - Nhân viên Helpdesk Vinhomes: Quá tải hàng nghìn phản ánh gửi dưới dạng văn bản tự do mỗi ngày. │
│ - Cư dân khu đô thị: Bức xúc vì các sự cố khẩn cấp (mất nước, rò rỉ ga) chậm được xử lý.       │
│                                                                                                 │
│ Workflow thủ công hiện tại (4 bước):                                                            │
│   1. Cư dân gửi phản ánh ──> 2. Helpdesk đọc & gán nhãn ──> 3. Chuyển tiếp tới BQL toà nhà      │
│   ──> 4. Soạn tin nhắn xác nhận tiến độ gửi cư dân                                             │
│                                                                                                 │
│ Bước nào tốn thời gian/lỗi nhất? Bước 2 & 3 (⏱ 4 - 8 tiếng chờ duyệt trong hàng đợi)           │
│ AI có thể nhảy vào hỗ trợ ở bước nào? Bước 2 & 3: Đọc hiểu ngôn ngữ tự nhiên tiếng Việt,        │
│ trích xuất loại sự cố (kỹ thuật/an ninh/vệ sinh), mức độ khẩn cấp và route thẳng tới kỹ thuật.  │
│                                                                                                 │
│ Đo thành công bằng gì (Metric có số)?                                                           │
│ - Giảm thời gian định tuyến phản ánh từ 6 giờ ──> dưới 3 phút.                                  │
│ - Tỉ lệ định tuyến chính xác phân loại sự cố đạt trên 95%.                                      │
│ - Thời gian phản hồi xác nhận ban đầu cho cư dân đạt dưới 1 phút.                              │
│                                                                                                 │
│ Quick Architecture: [ ] No AI   [ ] Rule   [x] LLM Feature (NLP Classification)   [ ] Agent     │
└─────────────────────────────────────────────────────────────────────────────────────────────────┘
```

---

### 📇 Quick Problem Card #3: Vinmec — Tự động soạn thảo tóm tắt hồ sơ xuất viện (Discharge Summary)

```text
┌─────────────────────────────────────────────────────────────────────────────────────────────────┐
│ QUICK PROBLEM CARD #3                                                                           │
│                                                                                                 │
│ Bài toán (1 câu): Hỗ trợ bác sĩ lâm sàng tự động tổng hợp kết quả điều trị và soạn thảo bản     │
│                   tóm tắt xuất viện cùng hướng dẫn dùng thuốc dễ hiểu cho bệnh nhân Vinmec.     │
│ Công ty thành viên: [ ] Xanh SM   [ ] VinFast   [ ] Vinhomes   [x] Vinmec   [ ] Khác            │
│                                                                                                 │
│ Ai đang đau (Actor)?                                                                            │
│ - Bác sĩ điều trị: Mất nhiều thì giờ cho thủ tục giấy tờ hành chính thay vì khám chữa bệnh.    │
│ - Bệnh nhân xuất viện: Nhận hồ sơ chậm trễ và khó hiểu các thuật ngữ chuyên môn phức tạp.       │
│                                                                                                 │
│ Workflow thủ công hiện tại (4 bước):                                                            │
│   1. Mở bệnh án điện tử (EMR) ──> 2. Đọc & tổng hợp chỉ số xét nghiệm, đơn thuốc, phẫu thuật    │
│   ──> 3. Viết tay bản tóm tắt xuất viện ──> 4. Ký duyệt và bàn giao cho bệnh nhân              │
│                                                                                                 │
│ Bước nào tốn thời gian/lỗi nhất? Bước 2 & 3 (⏱ 25 - 35 phút/bệnh nhân)                          │
│ AI có thể nhảy vào hỗ trợ ở bước nào? Bước 2 & 3: Trích xuất các trường dữ liệu quan trọng từ  │
│ hệ thống EMR, chuyển đổi thuật ngữ y khoa thành văn bản dặn dò mạch lạc, dễ nhớ.                 │
│                                                                                                 │
│ Đo thành công bằng gì (Metric có số)?                                                           │
│ - Giảm thời gian soạn thảo hồ sơ xuất viện từ 30 phút ──> dưới 5 phút/ca.                       │
│ - 100% bản tóm tắt bắt buộc phải có chữ ký số xác nhận của Bác sĩ điều trị (Strict HITL).      │
│ - Tỉ lệ bệnh nhân hiểu rõ phác đồ uống thuốc tại nhà tăng từ 72% lên 94%.                       │
│                                                                                                 │
│ Quick Architecture: [ ] No AI   [ ] Rule   [x] LLM Feature (Clinical Summarization)   [ ] Agent │
└─────────────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 🗳️ Quyết định lựa chọn bài toán cho Deep-Dive

Nhóm kỹ sư Vin Smart Future thống nhất lựa chọn **Bài toán #1: Xanh SM — Trợ lý điều phối ứng phó sự cố pin & trạm sạc thực địa** để tiến hành phân tích sâu (Phase 3 Deep-Dive) và lập trình bản mẫu an toàn (Phase 4 Prototype).

### Lý do lựa chọn và loại trừ:
1. **Lý do chọn Bài toán #1 (Xanh SM Dispatcher Co-pilot):**
   - **Tác động kinh doanh tức thì:** Sự cố hết pin giữa đường ảnh hưởng trực tiếp đến SLA phục vụ khách hàng, uy tín thương hiệu taxi điện Xanh SM và gây nguy cơ ách tắc giao thông công cộng.
   - **Tính khả thi kỹ thuật cao:** Dữ liệu GPS xe, trạng thái trụ sạc VinFast và thông số dung lượng pin (SoC) đã có sẵn qua hệ thống Telematics IoT. 
   - **Ranh giới an toàn rõ ràng:** Có thể áp dụng chặt chẽ mô hình Human-in-the-Loop (`[DRAFT_ONLY]`) và quy tắc an toàn vật lý cứng (ngưỡng pin < 5% kích hoạt xe cứu hộ).
2. **Lý do hoãn thực hiện Bài toán #2 (Vinhomes) và #3 (Vinmec):**
   - *Vinhomes Ticket:* Cần hoàn thiện chuẩn hóa cơ sở dữ liệu định danh cư dân và quy chế bảo mật thông tin cá nhân nội bộ trước khi cấp quyền truy xuất cho LLM.
   - *Vinmec Clinical Summary:* Mảng y tế đòi hỏi các chứng chỉ nghiêm ngặt về an toàn dữ liệu sức khỏe (HIPAA/Bộ Y tế) và độ trễ rủi ro pháp lý cao, phù hợp với lộ trình phát triển giai đoạn tiếp theo.

