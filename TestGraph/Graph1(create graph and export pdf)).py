# matplotlib

import matplotlib.pyplot as plt
from matplotlib import rcParams

# ตั้งค่าฟอนต์ที่รองรับภาษาไทย เช่น Tahoma
rcParams['font.family'] = 'Tahoma'

# ข้อมูลสำหรับ Pie Chart
labels = ['แถม','วัตถุดิบ', 'ค่าเช่า ค่าส่วนกลาง นํ้า', 'อุปกรณ์ใช้สอย', 'วัสดุสิ้นเปลือง', 'ค่าใช้สอย', 'ค่าไฟ', 'ค่าแรง', 'Ptime', 'สวัสดิการ', 'Manage']
sizes = [9.89,58.49202515551052, 3.143687454553196, 0.27382873515334827, 0.6284703409251237, 1.0704132225885332, 5.192270349106591, 15.587366811122456, 5.622338413913839, 0.325589044846969, 2.2754500016279455]
# สร้าง Pie Chart
plt.pie(sizes, labels=labels, autopct='%1.1f%%')
plt.title('กราฟวงกลม')

# บันทึกกราฟเป็นไฟล์ PDF
plt.savefig('pie_chart.pdf', format='pdf')

# แสดงกราฟบนหน้าจอ
plt.show()