"""Render the lab's current-state diagram using Pillow and Windows Arial."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
FONT_DIR = Path('C:/Windows/Fonts')

def font(size, bold=False):
    return ImageFont.truetype(str(FONT_DIR / ('arialbd.ttf' if bold else 'arial.ttf')), size)

im = Image.new('RGB', (1800, 1120), '#f1f5f9')
d = ImageDraw.Draw(im)
d.text((65, 45), 'XANH SM | QUY TRÌNH XỬ LÝ SỰ CỐ PIN', font=font(39, True), fill='#0f172a')
d.text((65, 105), 'CURRENT STATE — Mô phỏng cho Lab 02; chưa xác nhận bằng dữ liệu doanh nghiệp', font=font(23), fill='#475569')
steps = [
    ('01', 'TIẾP NHẬN', 'Tài xế → Điều phối viên', 'Điện thoại / app', 'Input: mô tả sự cố', 'Output: ticket', '2 phút'),
    ('02', 'XÁC MINH', 'Điều phối viên', 'Dashboard telemetry', 'Input: ticket, mã xe', 'Output: pin, vị trí, giờ đo', '2 phút'),
    ('03', 'TRA CỨU TRẠM', 'Điều phối viên', 'Danh mục trạm sạc', 'Input: vị trí, loại xe', 'Output: dữ liệu trạm phù hợp', '4 phút'),
    ('04', 'SOẠN ĐỀ XUẤT', 'Điều phối viên', 'Màn hình nhập tin', 'Input: dữ liệu đã kiểm', 'Output: bản nháp hỗ trợ', '4 phút'),
    ('05', 'DUYỆT / GỬI / LOG', 'Điều phối viên', 'App / gọi đội hỗ trợ', 'Input: bản nháp', 'Output: tin duyệt, log', '3 phút'),
]
for i, (num, title, actor, tool, inp, out, duration) in enumerate(steps):
    x = 65 + i * 340
    hot = i in (2,3)
    d.rounded_rectangle((x, 215, x+305, 690), radius=20, fill='white', outline='#dc2626' if hot else '#cbd5e1', width=4)
    d.text((x+20, 235), num, font=font(42, True), fill='#dc2626' if hot else '#0f766e')
    d.text((x+18, 305), title, font=font(22, True), fill='#0f172a')
    for yy, label in [(365,actor),(410,tool),(475,inp),(515,out)]:
        d.text((x+14, yy), label, font=font(18), fill='#334155')
    d.text((x+20, 585), duration, font=font(33, True), fill='#dc2626' if hot else '#0f766e')
    if hot:
        d.text((x+20, 647), 'BOTTLENECK', font=font(19, True), fill='#dc2626')
    if i < 4:
        d.line((x+310, 440, x+332, 440), fill='#64748b', width=4)
        d.polygon([(x+332,440),(x+322,433),(x+322,447)], fill='#64748b')
d.rounded_rectangle((65, 740, 1735, 930), radius=18, fill='#e2e8f0')
for yy, label in [
    (760,'HANDOFF H1: Tài xế → Điều phối viên (nhận báo cáo ở bước 1).'),
    (805,'HANDOFF H2: Dashboard → Điều phối viên (pin / vị trí ở bước 2).'),
    (850,'HANDOFF H3: Điều phối viên → Tài xế / Đội hỗ trợ (bước 5).'),
]:
    d.text((90, yy), label, font=font(25), fill='#0f172a')
d.text((65, 965), 'Tổng: 15 phút/lượt | Tra cứu + soạn nháp: 8 phút (~53%)', font=font(30, True), fill='#0f766e')
d.text((65, 1020), 'Thời gian là giả định; không gồm chờ tổng đài, chờ cứu hộ hoặc thời gian sạc.', font=font(24), fill='#475569')
im.save(ROOT / '04-workflow-diagram.png')
