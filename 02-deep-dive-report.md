# Lab 02 — Deliverable 2: Deep-Dive Report & Evaluation
**Dự án:** Trợ lý Điều phối Thông minh Ứng phó Sự cố Pin Thực địa (Xanh SM Dispatcher Co-pilot)  
**Đơn vị:** Vin Smart Future — Khối Công nghệ Tập đoàn Vingroup  
**Phối hợp vận hành:** Công ty Cổ phần Di chuyển Xanh và Thông minh GSM (Xanh SM) & VinFast Charging Network  
**Tác giả:** Nguyễn Tuấn Kiệt (AI Product Engineer)  

---

## Executive Summary (Tóm tắt điều hành)

Trong bối cảnh quy mô đội xe điện của **Xanh SM (GSM)** tăng trưởng thần tốc với hàng chục nghìn phương tiện (VF e34, VF 5 Plus, VF 8) hoạt động liên tục tại các đô thị trọng điểm, việc xử lý các sự cố pin yếu và tìm trạm sạc khả dụng trong khung giờ cao điểm đang tạo áp lực khổng lồ lên đội ngũ Điều phối viên (Dispatchers).

Báo cáo phân tích chuyên sâu này nghiên cứu giải pháp xây dựng **Dispatcher Co-pilot** — một tính năng tích hợp mô hình ngôn ngữ lớn (LLM Feature) nhằm tự động hóa việc tổng hợp dữ liệu viễn thông xe (Telematics), tra cứu mạng lưới trạm sạc VinFast theo thời gian thực và soạn thảo bản tin hướng dẫn tiêu chuẩn, kết hợp cơ chế kích hoạt đội cứu hộ pin di động (Mobile Charging Vehicle) khi pin đạt ngưỡng nguy cấp (< 5%).

---

# 🏗️ Phase 3 — DEEP-DIVE: Phân tích Chi tiết Bài toán

## 3.1. Current-State Workflow Mapping (Quy trình Vận hành Hiện tại)

Hiện tại, toàn bộ quy trình xử lý khi tài xế gặp sự cố pin yếu trên đường diễn ra hoàn toàn thủ công với 5 bước tuần tự:

```text
┌─────────────────┐       ┌─────────────────┐       ┌─────────────────┐       ┌─────────────────┐       ┌─────────────────┐
│ Bước 1          │       │ Bước 2          │       │ Bước 3          │       │ Bước 4          │       │ Bước 5          │
│ Tiếp nhận cuộc  │ ────> │ Tra cứu định vị │ ────> │ Tra cứu mạng    │ ────> │ Soạn văn bản    │ ────> │ Kích hoạt cứu   │
│ gọi / báo cáo   │       │ GPS & SoC xe    │       │ trạm sạc VinFast│  🔴   │ hướng dẫn SMS   │  🔴   │ hộ di động      │
│ ⏱ 2.0 phút      │       │ ⏱ 2.0 phút      │       │ ⏱ 5.0 phút      │       │ ⏱ 5.0 phút      │       │ ⏱ 1.0 phút      │
│ 🔄 Call Center  │       │ 🔄 Telematics   │       │ 🔄 CMS Portal   │       │ 🔄 Driver App   │       │ 🔄 Mobile Team  │
└─────────────────┘       └─────────────────┘       └─────────────────┘       └─────────────────┘       └─────────────────┘
```

* **Chi tiết các bước:**
  * **Bước 1 (Tiếp nhận):** Tài xế gọi điện qua hotline tổng đài hoặc nhấn nút khẩn cấp trên Driver App báo sắp hết pin hoặc trạm sạc dự kiến bị quá tải. *(Thời gian: 2.0 phút | Actor: Điều phối viên)*.
  * **Bước 2 (Định vị & Kiểm tra pin):** Điều phối viên chuyển sang tab hệ thống Quản lý đội xe (Fleet Telematics), nhập biển số xe để lấy tọa độ GPS hiện tại và tỷ lệ % pin thực tế (State of Charge - SoC). *(Thời gian: 2.0 phút | Actor: Điều phối viên)*.
  * **Bước 3 (Tra cứu trạm sạc) [🔴 Bottleneck 1]:** Điều phối viên mở Cổng quản lý mạng lưới sạc VinFast (Charging CMS), tìm kiếm thủ công các trạm sạc xung quanh bán kính xe, kiểm tra xem loại cổng sạc (CCS2) có tương thích với dòng xe hay không và còn trụ nào đang trống. *(Thời gian: 5.0 phút | Điểm nghẽn: Giao diện phân mảnh, dữ liệu tải chậm vào giờ cao điểm)*.
  * **Bước 4 (Soạn tin hướng dẫn) [🔴 Bottleneck 2]:** Điều phối viên tự gõ tin nhắn hướng dẫn đường đi, địa chỉ trạm sạc và lưu ý an toàn bằng tiếng Việt vào khung chat gửi tới App tài xế. Tác vụ gõ phím tự do dễ gây sai sót về tên phố, địa chỉ trạm sạc hoặc văn phong căng thẳng khi tài xế đang bối rối. *(Thời gian: 5.0 phút | Điểm nghẽn: Tốn thời gian biên soạn văn bản tiếng Việt)*.
  * **Bước 5 (Kích hoạt cứu hộ khẩn cấp):** Nếu tài xế báo pin còn dưới 5% và không thể tới trạm sạc, điều phối viên phải gọi điện sang đội xe cứu hộ sạc pin di động ngoài hiện trường. *(Thời gian: 1.0 phút)*.

* **Tổng thời gian xử lý thủ công:** **~15.0 phút/lượt**.
* **Điểm chuyển giao thông tin (🔄 Handoffs):** 4 lần chuyển giao giữa các hệ thống rời rạc (Call Center ➔ Telematics Fleet ➔ VinFast CMS ➔ Driver App ➔ Rescue Dispatch).

---

## 3.2. Problem Statement (Khung 6 Trường Thông Tin Tiêu Chuẩn)

| Trường thông tin (Field) | Định nghĩa & Nội dung chi tiết tại Vin Smart Future |
|---|---|
| **1. Actor / Operator** | **Điều phối viên vận hành (Dispatcher)** tại Trung tâm Điều vận Thông minh Xanh SM (Hà Nội, TP.HCM, Đà Nẵng). |
| **2. Current Workflow** | Khi tài xế báo cạn pin hoặc trạm sạc đầy, điều phối viên thao tác thủ công qua 4 hệ thống phần mềm riêng biệt: tra cứu tọa độ xe, kiểm tra trụ trống trên bản đồ trạm sạc VinFast, gõ tin nhắn hướng dẫn tiếng Việt gửi tài xế, hoặc liên hệ cứu hộ pin nếu mức pin quá thấp. Quy trình tốn 15 phút/lượt. |
| **3. Bottleneck** | **Bước 3 & 4 (Chiếm 10/15 phút):** Tra cứu thủ công trụ sạc trống tương thích cổng sạc dòng xe và soạn thảo văn bản hướng dẫn chỉ đường bằng tiếng Việt. Trong giờ cao điểm mưa gió, số lượng cuộc gọi dồn ứ khiến điều phối viên quá tải và tài xế phải chờ đợi lâu. |
| **4. Business Impact** | - Mỗi ngày ghi nhận trung bình **~80 – 120 sự cố pin/sạc** tại mỗi thành phố lớn.<br>- Lãng phí hơn **25 giờ công lao động/ngày** của đội ngũ điều phối.<br>- Tỉ lệ tài xế phải dừng cuốc tăng, dẫn đến rò rỉ ước tính **12% – 15% doanh thu vận tải theo giờ** và nguy cơ xe chết máy trên cầu hoặc cao tốc gây thiệt hại nghiêm trọng đến hình ảnh dịch vụ xe taxi điện văn minh của GSM. |
| **5. Success Metric** | - **Metric 1 (Hiệu suất vận hành):** Giảm thời gian xử lý mỗi sự cố từ **15.0 phút xuống dưới 2.5 phút** (Cắt giảm > 80% thời gian).<br>- **Metric 2 (Độ chính xác kỹ thuật):** Tỉ lệ gợi ý đúng trạm sạc còn trụ trống tương thích đạt **≥ 98%**.<br>- **Metric 3 (An toàn tuyệt đối):** **0% trường hợp** xe hết pin trên đường do hệ thống hướng dẫn sai hoặc điều xe tới trạm quá xa (> 5km khi pin < 5%). |
| **6. Operational Boundary** | **AI ĐƯỢC PHÉP:** Tự động gọi API lấy tọa độ, đọc trạng thái trụ sạc VinFast và dự thảo (draft) tin nhắn gửi tài xế hoặc cấu trúc JSON cứu hộ.<br>**AI TUYỆT ĐỐI KHÔNG ĐƯỢC PHÉP:**<br>1. Tự động bấm gửi tin nhắn trực tiếp đến tài xế mà chưa qua xác nhận của Điều phối viên (Bắt buộc gắn nhãn `[DRAFT_ONLY]`).<br>2. Đề xuất trạm sạc cách xa quá 5km khi mức pin xe dưới ngưỡng nguy cấp 5% (< 5%). Trong trường hợp này, AI bắt buộc phải kích hoạt lệnh điều xe cứu hộ pin di động `dispatch_mobile_charger`. |

---

## 3.3. Future-State Flow & AI Fit Analysis

### 🎯 Đánh giá Mức độ Phù hợp của AI (AI-Fit Matrix)

| Mô hình tiếp cận | Đánh giá độ phù hợp cho bài toán Xanh SM | Kết luận |
|---|---|---|
| **Chỉ dùng Rule-based** | Tra cứu trạm sạc gần nhất bằng thuật toán khoảng cách Euclid / Dijkstra là rất tốt và nhanh. Tuy nhiên, việc tổng hợp các điều kiện thời gian thực (loại xe VF e34/VF5/VF8 dùng chuẩn sạc khác nhau, tình trạng giao thông, khả năng giao tiếp ngữ cảnh tiếng Việt thân thiện, thấu cảm để trấn an tài xế đang hoảng loạn) thì Rule-based rất cứng nhắc và rập khuôn. | Không đủ linh hoạt |
| **LLM Feature (Co-pilot)** | Kết hợp hoàn hảo: Tầng backend sử dụng Rule/API để lấy tọa độ và danh sách trạm khả dụng, sau đó chuyển giao cho **LLM làm nhiệm vụ tổng hợp thông tin, kiểm tra ranh giới an toàn và soạn bản nháp chỉ dẫn chất lượng cao**. Điều phối viên chỉ cần 1 click để duyệt (Human-in-the-loop). | **Lựa chọn tối ưu (Best Fit)** |
| **Autonomous Multi-Agent Loop** | Cho phép các Agent tự động điều hướng xe và tự động đặt lịch trạm sạc mà không cần con người can thiệp. Mức độ tự trị này tiềm ẩn rủi ro quá lớn (nếu Agent hallucinate chỉ đường sai, xe có thể chết máy giữa ngã tư hoặc trên cao tốc, gây ách tắc đô thị và rủi ro an toàn giao thông nghiêm trọng). | Rủi ro quá cao, chưa phù hợp |

### 🔄 Quy trình Tương lai (Future-State Workflow)

```text
                                           ┌────────────────────────────────────────┐
                                           │  Tài xế báo sự cố qua App / Tổng đài   │
                                           └───────────────────┬────────────────────┘
                                                               │
                                                               ▼
                                           ┌────────────────────────────────────────┐
                                           │ 🔵 System Rule / API Fetch             │
                                           │ Tự động lấy: GPS, % Pin (SoC), Mã xe,  │
                                           │ Trạng thái mạng lưới trạm sạc VinFast  │
                                           └───────────────────┬────────────────────┘
                                                               │
                                                               ▼
                                           ┌────────────────────────────────────────┐
                                           │ 🔵 AI Dispatcher Co-pilot (LLM Step)   │
                                           │ Kiểm tra ranh giới an toàn pin (< 5%)   │
                                           │ Sinh nháp: [DRAFT_ONLY] + Chỉ dẫn trạm │
                                           │ hoặc JSON: dispatch_mobile_charger     │
                                           └───────────────────┬────────────────────┘
                                                               │
                                         ┌─────────────────────┴─────────────────────┐
                       Thành công        │                                           │  Gặp sự cố / Lỗi
                     ┌───────────────────┘                                           └───────────────────┐
                     ▼                                                                                   ▼
       ┌───────────────────────────┐                                                       ┌───────────────────────────┐
       │ 🟢 Human-in-the-Loop      │                                                       │ ↩️ Fallback Quy trình     │
       │ Điều phối viên xem bản    │                                                       │ Hệ thống hiển thị cảnh    │
       │ nháp, bấm [DUYỆT & GỬI]   │                                                       │ báo, Điều phối viên thao  │
       │ hoặc chỉnh sửa nhanh (15s)│                                                       │ tác thủ công theo quy     │
       └─────────────┬─────────────┘                                                       │ trình dự phòng chuẩn      │
                     │                                                                     └─────────────┬─────────────┘
                     ▼                                                                                   │
       ┌───────────────────────────┐                                                                     │
       │ Tin nhắn đến Driver App   │ <───────────────────────────────────────────────────────────────────┘
       │ hoặc Đội cứu hộ xuất phát │
       └───────────────────────────┘
```

* **Cơ chế An toàn & Dự phòng:**
  * **🔵 AI Step:** LLM tiếp nhận dữ liệu có cấu trúc từ hệ thống Telematics, phân tích tình trạng khẩn cấp và sinh ra văn bản chỉ dẫn có gắn nhãn `[DRAFT_ONLY]`.
  * **🟢 Human Step (HITL):** Mọi quyết định gửi thông tin ra ngoài môi trường thực tế đều phải thông qua nút bấm xác nhận của Điều phối viên. Điều phối viên có quyền sửa đổi nội dung trong 5 giây nếu cần bổ sung thông tin đặc thù.
  * **↩️ Fallback Mechanism:** Nếu dịch vụ LLM gặp sự cố quá tải (HTTP 429/503), mạng chập chờn hoặc mô hình phản hồi không hợp lệ, hệ thống tự động rơi về chế độ Fallback: kích hoạt danh sách trạm sạc gần nhất tính theo bán kính GPS thuần túy bằng code cứng và gửi thông báo cho điều phối viên soạn thảo thủ công như quy trình cũ.

---

# 🏁 Phase 5 — EVALUATE: Đánh giá Độ Sẵn Sàng & Quyết Định Đầu Tư

## 5.1. Bảng Kiểm Đánh Giá Độ Sẵn Sàng (AI Readiness Checklist)

| Tiêu chí đánh giá (Checklist Item) | Trạng thái thực tế tại Vin Smart Future / Xanh SM | Đánh giá |
|---|---|:---:|
| **1. Dữ liệu mẫu & Hệ sinh thái số sẵn có?** | Hệ thống IoT Telematics trên toàn bộ xe VinFast đã truyền dữ liệu GPS và mức pin (SoC) theo thời gian thực về máy chủ Vin Smart Future mỗi 10 giây. Mạng lưới trạm sạc VinFast đã có API trạng thái trụ sạc theo thời gian thực. Logs lịch sử các cuộc gọi sự cố đã được lưu trữ hơn 1 năm. | **SẴN SÀNG (YES)** |
| **2. Rủi ro sai sót nằm trong tầm kiểm soát?** | Nhờ cơ chế Human-in-the-loop bắt buộc qua tag `[DRAFT_ONLY]` và quy tắc an toàn vật lý cứng chặn xe pin < 5% không được đi xa, rủi ro ảo giác (hallucination) của LLM bị triệt tiêu hoàn toàn trước khi thông tin đến được tài xế. Tầng Fallback đảm bảo vận hành không bao giờ bị gián đoạn. | **SẴN SÀNG (YES)** |
| **3. Khối Vận hành sẵn sàng đón nhận thay đổi?** | Đội ngũ Điều phối viên Xanh SM hiện đang bị quá tải nghiêm trọng trong các khung giờ cao điểm và đã chủ động kiến nghị giải pháp tự động hóa soạn thảo chỉ dẫn để giảm áp lực thao tác lặp lại. Ban lãnh đạo GSM cam kết hỗ trợ thử nghiệm pilot tại Hà Nội. | **SẴN SÀNG (YES)** |

---

## 5.2. Quyết định của Hội đồng Kỹ thuật Vin Smart Future

* [x] **GO (Bắt đầu xây dựng Prototype & Triển khai Pilot hẹp)**
* [ ] **NOT YET (Cần tích lũy thêm dữ liệu / chuẩn hóa hạ tầng)**
* [ ] **NO-GO (Hủy bỏ dự án do không khả thi hoặc Rule-based vượt trội)**

---

## 5.3. Lý Giải Quyết Định (Justification & ROI Analysis)

### 1. Về mặt Hiệu quả Vận hành & Tài chính (Business & ROI):
- **Tiết kiệm thời gian vượt trội:** Giảm thời gian xử lý sự cố từ **15 phút xuống dưới 2.5 phút** (giảm 83%), giúp mỗi điều phối viên có thể xử lý gấp 5 lần số lượng sự cố trong giờ cao điểm mà không cần tăng biên chế nhân sự.
- **Bảo toàn doanh thu vận tải:** Việc đưa xe điện quay trở lại vận hành nhanh hơn giúp giảm thiểu thời gian "chết" của xe, ước tính mang lại giá trị gia tăng hơn **350 triệu VNĐ/tháng** trên toàn đội xe tại thị trường Hà Nội.
- **Chi phí triển khai cực thấp:** Mô hình được thiết kế dưới dạng **LLM Feature** gọn nhẹ (sử dụng Gemini Flash API), chi phí token ước tính chỉ tốn khoảng **~0.0005 USD/lượt xử lý sự cố**, hoàn toàn không đáng kể so với lợi ích kinh tế thu lại.

### 2. Về mặt Kỹ thuật & Quản trị Rủi ro (Technical Feasibility & Safety):
- Đã được nghiệm chứng tính khả thi và an toàn qua mã nguồn kiểm thử **Programmatic Boundary Prototype** (`prompt_prototype.py`), vượt qua 100% các bài test tấn công adversarial (cố tình ép bỏ tag draft hoặc yêu cầu xe pin 2% chạy 8km).
- Kiến trúc kết hợp linh hoạt: Rule-based xử lý lọc số liệu viễn thông chính xác 100%, LLM chịu trách nhiệm giao tiếp ngôn ngữ tự nhiên và tổng hợp thông tin, con người giữ quyền quyết định tối cao (Human-in-the-loop).

**Kế hoạch tiếp theo:** Triển khai thử nghiệm phiên bản Pilot nội bộ trong vòng 2 tuần tại Trung tâm Điều vận Xanh SM Hà Nội trước khi mở rộng toàn quốc.

