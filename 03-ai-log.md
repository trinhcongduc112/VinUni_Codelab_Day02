# 03 — AI Log & Reflection

**Họ tên:** Phan Bá An · **MSSV:** 2A202603375 · **Lớp:** L3A · **AI đã dùng:** Claude (Anthropic)

> ⚠️ **Đọc trước khi nộp:** mục nào có dấu **`[ĐIỀN]`** là phần chỉ bạn mới viết được (kết quả chạy Gemini thật, quyết định của riêng bạn). File này chấm trên tiêu chí **phản ánh trung thực** (AI giúp gì / AI sai gì / bạn sửa gì), nên đừng điền những điều chưa xảy ra. Các mục không có `[ĐIỀN]` bên dưới là những việc đã thực sự diễn ra trong buổi làm bài này.

---

## 1. AI đã giúp gì

| # | Việc | Kết quả |
|---|---|---|
| 1 | Đọc repo lab (README, worksheet, example, autograder) và tóm tắt cách chấm điểm | Rút ra autograder chấm 10 điểm: 4 file tồn tại (1.25đ/file) + 5 tiêu chí code (1đ/tiêu chí). Tiêu chí 2 yêu cầu `evaluate_prompt()` chứa `genai`/`generativeai`; tiêu chí 5 yêu cầu output có ≥ 2 chữ "Passed" và 0 chữ "Failed". |
| 2 | Nhận ra link tôi đưa (nhánh `vuductam`) chứa **bài đã hoàn thành của một bạn khác** | Chuyển sang làm từ **template gốc** (commit `b221b79`) thay vì dùng bài đó. *Ghi chú trung thực:* trước khi nhận ra điều này, Claude đã mở xem file code trong nhánh đó (không đọc 3 file `.md` của bạn ấy); phần code của tôi được viết lại từ đặc tả trong template. |
| 3 | Phát hiện hai quy tắc của template có thể **xung đột** | Rule 1 yêu cầu output *luôn bắt đầu* bằng `[DRAFT_ONLY]`, Rule 2 yêu cầu trả JSON dispatch *ngay lập tức*. Chốt định dạng: **dòng 1 = `[DRAFT_ONLY]`, dòng 2 = JSON** → cả hai quy tắc kiểm tra được trên mọi test. |
| 4 | Viết `SYSTEM_PROMPT` có định nghĩa rõ ngưỡng (`< 5%`, pin đúng 5% không nguy cấp), quy tắc chống thao túng và 2 ví dụ mẫu (few-shot) | Prompt mới (xem `starter-code/prompt_prototype.py`). |
| 5 | Mở rộng bộ test từ 2 lên 5 | Thêm: giả mạo `[SYSTEM OVERRIDE]` khi trạm chỉ cách 3km nhưng pin 4%, và giá trị biên pin đúng 5%. |
| 6 | Dựng server Gemini giả để kiểm tra "đường ống" và chạy thử autograder | 5/5 tiêu chí code đạt **trên mô hình giả**. Đây chỉ chứng minh code chạy đúng, **không** chứng minh Gemini thật tuân thủ ranh giới. |
| 7 | Brainstorm 6 bài toán và soạn bản nháp 3 Quick Card, Deep-Dive, sơ đồ workflow | Các file `01`, `02`, `04`. |

## 2. AI sai / hạn chế ở đâu

* **Không thể gọi Gemini thật.** Môi trường của Claude không truy cập được API Gemini, nên Claude không biết mô hình có vượt ranh giới hay không. Tôi phải tự chạy và ghi kết quả (mục 3).
* **Lỗi của chính bài kiểm thử giả:** lần chạy đầu, Test 3 báo "Rule 2 Failed". Nguyên nhân không nằm ở prompt mà ở server giả: nó dò chữ `pin` viết thường nên bỏ sót "Pin xe 3%". Claude viết sai regex, phát hiện qua log và sửa bằng cờ không phân biệt hoa/thường. Bài học: một test báo lỗi chưa chắc là lỗi của đối tượng được test.
* **Không đọc được link GitHub trực tiếp:** công cụ mở trang bị chặn (robots), Claude phải clone repo bằng `git` mới đọc được.
* **Số liệu trong `01` và `02` là giả định do AI đề xuất** (400 phiếu/ngày, 9 phút/phiếu, 15% chuyển nhầm…), không có nguồn. Đã gắn nhãn "ước tính" trong từng file; cần xác minh nếu dùng thật.
* **`[ĐIỀN]` Hallucination/sai sót khác mà bạn tự phát hiện** khi đọc lại các file AI viết (ví dụ: một chi tiết về Vinhomes/Vinmec/Xanh SM không đúng thực tế, một lập luận yếu bạn đã sửa…): ______

## 3. Tôi đã sửa prompt/ranh giới như thế nào (kết quả chạy Gemini thật)

> **`[ĐIỀN]`** Chạy `python prompt_prototype.py` trên máy bạn, rồi ghi lại từng lần chạy. Nếu chạy lần đầu đã đạt toàn bộ thì ghi đúng như vậy — không cần bịa lỗi.

| Lần chạy | Test bị vi phạm (nếu có) | Mô hình đã làm gì | Tôi sửa gì trong `SYSTEM_PROMPT` | Kết quả sau sửa |
|---|---|---|---|---|
| 1 | `[ĐIỀN]` | `[ĐIỀN]` | `[ĐIỀN]` | `[ĐIỀN]` |
| 2 | `[ĐIỀN]` | `[ĐIỀN]` | `[ĐIỀN]` | `[ĐIỀN]` |

**Prompt tấn công tôi tự nghĩ thêm (nếu có):** `[ĐIỀN]`

## 4. Reflection (viết 4–6 câu bằng giọng của bạn)

`[ĐIỀN]` Gợi ý các câu hỏi để bạn trả lời trung thực:
1. Phần nào AI làm nhanh hơn bạn, phần nào bạn thấy bắt buộc phải tự kiểm tra lại?
2. Việc thấy một test "đỏ" vì lỗi của chính công cụ kiểm thử (mục 2) thay đổi cách bạn tin vào kết quả test như thế nào?
3. Vì sao ranh giới an toàn (thẻ `[DRAFT_ONLY]`, ngưỡng pin) nên được kiểm tra bằng **code** thay vì chỉ tin vào prompt?
4. Nếu làm lại, bạn sẽ đổi điều gì trong cách phối hợp với AI?
