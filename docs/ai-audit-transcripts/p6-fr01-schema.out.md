AI output (rút gọn)

40 AI cases: 7 sanity (unique email + strong password 200; mass-assign ignored; BVA 8); 31 discovery (invalid email/password/missing; duplicate 409; SQLi); 2 catalog. Schema 200 {message,id}; không leak password.
Người: 1 INCOMPLETE (FR-01-H05b round-trip register→login — phụ thuộc FR-02 của Member 1, giữ catalog không chạy). Human 6: H01 case-insensitive; H02 form-urlencoded; H03 double-submit; H04 whitespace name; H05/H05b round-trip.
