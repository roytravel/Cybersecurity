from PIL import ImageGrab
import time

# 현재 시각 확인
now = time.localtime()

# 저장될 시간 포맷 설정
time = "%04d-%02d-%02d-%02dh-%02dm-%02ds" % (now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min, now.tm_sec)

# 캡처 기능을 사용하기 위해 ImageGrab 모듈 사용
image = ImageGrab.grab()

# 파일 이름 지정
fileName = "{}.png".format(time)

# 캡처 된 파일 저장
image.save(fileName)
