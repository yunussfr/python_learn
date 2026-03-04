import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from backgroundremover.bg import remove_bg_and_save
import os


input_path = "rakun kardeşim ne bakiyonki daha.jpg"
output_path = "output.png"


try:
    print(f"'{input_path}' dosyasının arka planı kaldırılıyor...")
    remove(
        input_path=input_path,
        output_path=output_path
    )
    print(f"✅ Arka plan başarıyla kaldırıldı ve '{output_path}' olarak kaydedildi.")

    # --- 2. Adım: Kaydedilen Resmi Görüntüleme ---
    if os.path.exists(output_path):

        # Matplotlib ile resmi oku
        img = mpimg.imread(output_path)

        # Resmi göster
        plt.imshow(img)
        plt.title("Arka Planı Kaldırılmış Sonuç")
        plt.axis('off')  # Eksen değerlerini gizle
        plt.show()  # Görüntü penceresini aç
    else:
        print(f"⚠️ Hata: {output_path} dosyası bulunamadı. Görüntüleme yapılamadı.")

except Exception as e:
    print(f"❌ Bir hata oluştu: {e}")