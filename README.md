# 濾波器於模擬語音降噪之效果比較

這是一個以 Python 開發的圖形化應用程式，結合 [Flet](https://flet.dev/)、[Tkinter](https://docs.python.org/3/library/tkinter.html) 和 [padasip](https://matousc89.github.io/padasip/)，實現 **LMS、RLS、NLMS** 三種Adaptive Filter的模擬與比較。

---

## 功能特色

- 提供三種Adaptive Filter：LMS、RLS、NLMS
- 可自訂濾波器係數
- 模擬含噪音檔的濾波
- 顯示：
  - 濾波器適應過程圖（目標值與預測值）
  - 濾波誤差圖（以 dB 為單位）
- 可同時比較三種濾波器的平均誤差並推薦最佳濾波器
- 提供調整聲源與收音距離，模擬不同情況下製造的噪音和濾波效果

---

## 畫面預覽

請將模擬後的圖表截圖後放入 `images/` 資料夾，並使用以下語法插入：

### 單一濾波器模擬結果



### 三種濾波器誤差比較
