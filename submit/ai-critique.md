# Phê bình AI (200–300 từ)

AI hữu ích khi mở rộng độ bao phủ, nhưng bản nháp đầu tiên thường nhầm lẫn giữa một ý tưởng kiểm thử hợp lý và một test case có thể thực thi. AI đưa ra nhiều mã trạng thái thay thế cho cùng một oracle, dùng lại dữ liệu seed có thể thay đổi và đôi khi coi token đã xác thực là token Admin. Với FR-10, ma trận trạng thái trông đầy đủ nhưng nhiều dòng không có cách tin cậy để tạo trạng thái ban đầu. Với FR-19, AI còn đề xuất kiểm thử cập nhật role trong khi API công bố chỉ có liệt kê và xóa user. Nguyên nhân là prompt ban đầu nhấn mạnh số lượng hơn tính cô lập của fixture, oracle chính xác và hậu điều kiện.

Thiếu sót quan trọng nhất nằm ở tương tác bảo mật và vòng đời dữ liệu. AI ban đầu không liên hệ việc xóa user với hiệu lực của JWT đã cấp, và không phân biệt tốt một lỗi gốc với nhiều assertion thất bại. Quá trình rà soát thủ công đã sửa từng case thành một status mong đợi duy nhất, fixture riêng, kiểm tra schema/invariant và postcondition.

Bài học là phải cộng tác với AI qua nhiều vòng có ràng buộc: chuẩn hóa contract, phân hoạch input, liệt kê đồ thị trạng thái, ánh xạ rủi ro bảo mật, xác định schema, sau đó audit khả năng thực thi. Bằng chứng runtime phải ưu tiên hơn lời giải thích tự tin của AI; việc đọc code chỉ giải thích lỗi đã tái hiện, không thay thế request thực tế.
