from os import listdir
from os.path import isdir
from PIL import Image
from numpy import savez_compressed, asarray
from mtcnn.mtcnn import MTCNN

# Hàm trích xuất khuôn mặt từ một ảnh
def extract_face(filename, required_size=(160, 160)):
    # Tải ảnh từ tệp
    image = Image.open(filename)
    # Chuyển đổi sang RGB nếu cần thiết
    image = image.convert('RGB')
    # Chuyển đổi sang mảng
    pixels = asarray(image)
    # Tạo bộ phát hiện, sử dụng trọng số mặc định
    detector = MTCNN()
    # Phát hiện khuôn mặt trong ảnh
    results = detector.detect_faces(pixels)
    # Kiểm tra nếu không có khuôn mặt nào được phát hiện
    if len(results) == 0:
        return None
    # Trích xuất hộp giới hạn từ khuôn mặt đầu tiên
    x1, y1, width, height = results[0]['box']
    # Sửa lỗi
    x1, y1 = abs(x1), abs(y1)
    x2, y2 = x1 + width, y1 + height
    # Trích xuất khuôn mặt
    face = pixels[y1:y2, x1:x2]
    # Thay đổi kích thước mảng thành kích thước mô hình yêu cầu
    image = Image.fromarray(face)
    image = image.resize(required_size)
    face_array = asarray(image)
    return face_array

# Hàm tải hình ảnh và trích xuất khuôn mặt cho tất cả hình ảnh trong một thư mục
def load_faces(directory):
    faces = list()
    # Liệt kê các tệp
    for filename in listdir(directory):
        # Đường dẫn
        path = directory + '/' + filename
        # Trích xuất khuôn mặt
        face = extract_face(path)
        # Nếu không có khuôn mặt nào được phát hiện, bỏ qua ảnh này
        if face is None:
            continue
        # Lưu trữ
        faces.append(face)
    return faces

# Hàm tải tập dữ liệu chứa một thư mục con cho mỗi lớp chứa các hình ảnh
def load_dataset(directory):
    X, y = list(), list()
    # Liệt kê các thư mục, một cho mỗi lớp
    for subdir in listdir(directory):
        # Đường dẫn
        path = directory + subdir + '/'
        # Bỏ qua các tệp có thể có trong thư mục
        if not isdir(path):
            continue
        # Tải tất cả các khuôn mặt trong thư mục con
        faces = load_faces(path)
        # Tạo nhãn
        labels = [subdir for _ in range(len(faces))]
        # Tóm tắt tiến trình
        print('>loaded %d examples for class: %s' % (len(faces), subdir))
        # Lưu trữ
        X.extend(faces)
        y.extend(labels)
    return asarray(X), asarray(y)

# Tải tập dữ liệu huấn luyện
trainX, trainy = load_dataset('dataset_split/train/')
print(trainX.shape, trainy.shape)

# Tải tập dữ liệu kiểm tra
testX, testy = load_dataset('dataset_split/val/')

# Lưu mảng vào một tệp ở định dạng nén
savez_compressed('5-celebrity-faces-dataset.npz', trainX, trainy, testX, testy)
