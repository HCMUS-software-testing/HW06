# Phê Bình AI (AI Critique)

**Họ và tên:** Lê Trung Kiên  
**MSSV:** 23127075  
**Độ dài:** 200 - 300 từ  

## Nội Dung Phê Bình

Trong quá trình ứng dụng AI vào kiểm thử API cho hệ thống EShop, AI đã thể hiện điểm mạnh vượt trội trong việc tự động hóa tạo nhanh các test case chuẩn hóa về cú pháp, bao phủ phân hoạch miền cơ bản và tạo JSON Schema validation. Tuy nhiên, AI bộc lộ những hạn chế rõ rệt ở các kịch bản kiểm thử bảo mật nâng cao và máy trạng thái nghiệp vụ phức tạp.

Cụ thể, đối với API FR-08 (Thanh toán) và FR-18 (Quản lý đơn hàng admin), AI thường bỏ sót các lỗi IDOR (Insecure Direct Object References), kiểm tra quyền sở hữu tài nguyên giữa người dùng thông thường và admin, cũng như các hành vi chuyển trạng thái không hợp lệ của đơn hàng (ví dụ: chuyển từ Cancelled ngược về Delivered). Nguyên nhân chính là do các mô hình ngôn ngữ lớn hoạt động dựa trên xác suất dự đoán từ tiếp theo từ văn bản prompt, thiếu ngữ cảnh thực thi động (dynamic execution state) và không hiểu sâu về logic phân quyền nội bộ nếu prompt không mô tả chi tiết từng luồng dữ liệu.

Bài học quan trọng rút ra là sinh viên không được coi AI là "hộp đen" tự động hoàn toàn. Cần đóng vai trò là một người kiểm thử có kỷ luật: dẫn dắt AI từng bước (step-by-step prompting), rà soát nghiêm ngặt từng test case do AI sinh ra, và chủ động thiết kế bổ sung các kịch bản biên về bảo mật và quy tắc nghiệp vụ mà AI bỏ sót.
