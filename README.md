# Micromouse Classic Simulator
  micromouse classic เป็นหุ่นยนต์ขนาดเล็กที่ทำภารกิจวิ่งไปในเขาวงกตและหาทางที่สั้นที่สุดระหว่างจุดเริ่มต้นและเส้นชัยที่อยู่ในเขาวงกต โดยโปรแกรมตัวนี้เป็นการจำลองการทำงานของหุ่นยนต์ เพื่อใช้ในการทดสอบอัลกอริทึม
#### ขั้นตอนการทำงาน
* รอบแรกเดินหาสำรวจเขาวงกตโดยใช้ flood fill algorithm โดยเริ่มเดินจากจุดเริ่มต้นและกลับมายังจุดเริ่มต้น

![IMG](https://github.com/thangmo01/micromouse-classic-simulator/blob/master/img_1.png)

* รอบที่สองหา shortest path โดย breadth first search

![IMG](https://github.com/thangmo01/micromouse-classic-simulator/blob/master/img_2.png)

#### การ implement ลงบนหุ่นจริง 
* ตามไปได้ที่ https://github.com/thangmo01/john-smith-2019
