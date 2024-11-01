# Bacurbpara
Calculate and Update Urban Planning Parameters Automatically

### Giới thiệu và Hướng dẫn Sử dụng Plugin Bacurbpara

---

#### **Tiếng Việt**

**Giới thiệu**

Plugin **Bacurbpara** dành cho QGIS giúp người dùng tính toán và cập nhật tự động các trường thông tin trong lớp dữ liệu không gian dựa trên các thông số về diện tích, mật độ xây dựng, số lượng đơn vị, dân số và nhiều chỉ số khác. Plugin này cung cấp các tính năng tính toán linh hoạt và khả năng lựa chọn đối tượng để cập nhật theo yêu cầu.

**Hướng dẫn sử dụng**

1. **Cài đặt Plugin**: Tải và cài đặt plugin từ thư mục plugin QGIS của bạn.

2. **Mở Plugin**: Sau khi cài đặt, mở QGIS và truy cập vào **Plugins > Bacurbpara**.

3. **Lựa chọn Lớp Dữ liệu**:
   - Chọn lớp dữ liệu không gian bạn muốn tính toán. Đảm bảo rằng lớp dữ liệu này đang ở chế độ chỉnh sửa (**Edit mode**).
   - Nếu bạn muốn chỉ cập nhật các đối tượng được chọn, hãy đánh dấu vào hộp kiểm **Chỉ cập nhật các đối tượng đã chọn**.

4. **Nhập Thông số Tính Toán**:
   - Điền các thông số cần thiết vào các trường trong giao diện, bao gồm **Diện tích (sq)**, **Diện tích (ha)**, **Mật độ xây dựng**, **Số tầng tối thiểu và tối đa**, **Diện tích sàn**, **Số lượng đơn vị**, **Dân số**, và các thông số liên quan khác.

5. **Thực hiện Tính Toán**:
   - Nhấn các nút tương ứng để thực hiện từng tính toán, như:
     - **Cập nhật Diện tích (Area_sq, Area_ha)**
     - **Cập nhật Mật độ xây dựng (Coverage)**
     - **Cập nhật Số tầng (FloorMin, FloorMax)**
     - **Tính Tổng Diện tích sàn (GFA)**
     - **Tính FAR (Hệ số sử dụng đất)**
     - **Tính Số lượng đơn vị (Unit)** và **Dân số (Population)**

6. **Kiểm tra và Lưu Kết Quả**:
   - Plugin sẽ hiển thị thông báo số lượng đối tượng được cập nhật thành công sau mỗi phép tính.
   - Sau khi hoàn thành, nhấn nút **Lưu** hoặc **Kết thúc chế độ chỉnh sửa** để lưu lại các thay đổi của bạn.

---

#### **English**

**Introduction**

The **Bacurbpara** plugin for QGIS enables users to automatically calculate and update spatial data layer fields based on various parameters, such as area, building density, unit count, population, and other indicators. This plugin provides flexible calculation options and allows users to choose specific features to update as needed.

**Instructions**

1. **Install the Plugin**: Download and install the plugin in your QGIS plugin directory.

2. **Open the Plugin**: After installation, open QGIS and go to **Plugins > Bacurbpara**.

3. **Select a Layer**:
   - Choose the spatial data layer you want to perform calculations on. Ensure that this layer is in **Edit mode**.
   - If you want to update only selected features, check the **Only update selected features** checkbox.

4. **Enter Calculation Parameters**:
   - Fill in the required parameters in the interface fields, including **Area (sq)**, **Area (ha)**, **Coverage**, **Min and Max Floors**, **Gross Floor Area (GFA)**, **Unit Count**, **Population**, and other relevant values.

5. **Execute Calculations**:
   - Click the corresponding buttons to perform each calculation, such as:
     - **Update Area (Area_sq, Area_ha)**
     - **Update Coverage**
     - **Update Floor Count (FloorMin, FloorMax)**
     - **Calculate Total Gross Floor Area (GFA)**
     - **Calculate FAR (Floor Area Ratio)**
     - **Calculate Unit Count** and **Population**

6. **Review and Save Results**:
   - After each calculation, the plugin will display a message showing the number of features updated successfully.
   - When finished, click **Save** or **Exit Edit Mode** to save your changes.

--- 

This guide provides the steps needed to install, configure, and effectively use the Bacurbpara plugin for spatial data calculations in QGIS.
