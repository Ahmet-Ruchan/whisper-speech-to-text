import difflib
from collections import Counter
import re

def altyazi_metnini_temizle(metin):
    # Daha esnek zaman damgası deseni (1 veya 2 basamaklı saat/dakika kabul eder)
    desen = re.compile(r"^\s*\[\d{1,2}:\d{2}(?::\d{2})?\.\d{3} --> \d{1,2}:\d{2}(?::\d{2})?\.\d{3}\]\s*")

    satirlar = metin.strip().splitlines()
    temiz_cumleler = []

    for satir in satirlar:
        temiz_satir = desen.sub('', satir).strip()
        if temiz_satir:
            temiz_cumleler.append(temiz_satir)

    return "\n".join(temiz_cumleler)

# Ya da doğrudan metni burada kullanabilirsin:
metin = """
[00:00:00.000 --> 00:00:06.100]   Sizden bu soruların cevaplarını bir süre düşünmenizi rica ediyorum.
[00:00:06.100 --> 00:00:10.860]   Dilerseniz cevaplarınızı not alın ve yazıyı okuduktan sonra kendi yanıtlarınıza karşılaştırın.
[00:00:10.860 --> 00:00:18.660]   Çocukların okulda, evde, sokakta, parkta, yaşıtlarıyla oyun oynaması, ders çalışması günlük hayatın doğal bir parçasıdır.
[00:00:18.660 --> 00:00:23.060]   Ancak zaman zaman bu dengelerin bozulduğu bazı çocukların akranları tarafından
[00:00:23.060 --> 00:00:27.540]   kasıtlı ve dengesiz bir güçle sürekli hedef alındığını gözlemleyebiliyoruz.
[00:00:27.540 --> 00:00:29.540]   Bu durumlara akran zorbalığı da verilir.
[00:00:29.540 --> 00:00:33.140]   Zorbalık tek biçimli değildir. Çeşitli türler bulunmaktadır.
[00:00:33.140 --> 00:00:40.740]   Sözal zorbalık, alay etme, hakaret, lakap takma, fiziksel zorbalık, itme, vurma, eşyaya zarar verme,
[00:00:40.740 --> 00:00:43.700]   duygusal zorbalık, dışlanma, yalnız bırakma.
[00:00:43.700 --> 00:00:48.540]   Dijital zorbalık, sosyal medya üzerinden tehdit, aşağılanma, özel bilgilerin yayılması.
"""

temiz_metin = altyazi_metnini_temizle(metin)

class TextAccuracyCalculator:
    def __init__(self):
        self.original_text = ""
        self.modified_text = ""

    def load_texts(self, original, modified):
        """Orijinal ve değiştirilmiş metinleri yükle"""
        self.original_text = original.strip()
        self.modified_text = modified.strip()

    def preprocess_text(self, text):
        """Metni temizle ve normalize et"""
        # Küçük harfe çevir
        text = text.lower()
        # Fazla boşlukları temizle
        text = re.sub(r'\s+', ' ', text)
        # Noktalama işaretlerini normalize et
        text = re.sub(r'[^\w\s]', '', text)
        return text.strip()

    def split_into_sentences(self, text):
        """Metni cümlelere ayır"""
        sentences = re.split(r'[.!?]+', text)
        return [s.strip() for s in sentences if s.strip()]

    def split_into_words(self, text):
        """Metni kelimelere ayır"""
        return text.split()

    def calculate_word_accuracy(self):
        """Kelime bazında doğruluk oranını hesapla"""
        original_words = self.split_into_words(self.preprocess_text(self.original_text))
        modified_words = self.split_into_words(self.preprocess_text(self.modified_text))

        # Ortak kelimeleri bul
        original_counter = Counter(original_words)
        modified_counter = Counter(modified_words)

        # Doğru kelimeler (her iki metinde de bulunan)
        correct_words = sum((original_counter & modified_counter).values())

        # Toplam kelime sayısı (orijinal metindeki)
        total_words = len(original_words)

        if total_words == 0:
            return 0.0

        accuracy = (correct_words / total_words) * 100
        return accuracy

    def calculate_sentence_accuracy(self):
        """Cümle bazında doğruluk oranını hesapla"""
        original_sentences = self.split_into_sentences(self.preprocess_text(self.original_text))
        modified_sentences = self.split_into_sentences(self.preprocess_text(self.modified_text))

        if not original_sentences:
            return 0.0

        correct_sentences = 0

        for orig_sentence in original_sentences:
            # Her orijinal cümle için en benzer cümleyi bul
            best_match = difflib.get_close_matches(orig_sentence, modified_sentences, n=1, cutoff=0.8)
            if best_match:
                correct_sentences += 1

        accuracy = (correct_sentences / len(original_sentences)) * 100
        return accuracy

    def calculate_similarity_ratio(self):
        """Genel benzerlik oranını hesapla"""
        original_clean = self.preprocess_text(self.original_text)
        modified_clean = self.preprocess_text(self.modified_text)

        similarity = difflib.SequenceMatcher(None, original_clean, modified_clean).ratio()
        return similarity * 100

    def get_detailed_diff(self):
        """Detaylı fark analizi"""
        original_lines = self.original_text.splitlines()
        modified_lines = self.modified_text.splitlines()

        diff = list(difflib.unified_diff(original_lines, modified_lines,
                                         fromfile='Orijinal', tofile='Değiştirilmiş', lineterm=''))
        return diff

    def analyze_changes(self):
        """Değişiklikleri analiz et"""
        original_words = set(self.split_into_words(self.preprocess_text(self.original_text)))
        modified_words = set(self.split_into_words(self.preprocess_text(self.modified_text)))

        # Silinen kelimeler
        deleted_words = original_words - modified_words

        # Eklenen kelimeler
        added_words = modified_words - original_words

        # Ortak kelimeler
        common_words = original_words & modified_words

        return {
            'silinen_kelimeler': list(deleted_words),
            'eklenen_kelimeler': list(added_words),
            'ortak_kelimeler': list(common_words),
            'toplam_orijinal': len(original_words),
            'toplam_degistirilmis': len(modified_words)
        }

    def full_analysis(self):
        """Tam analiz raporu"""
        word_accuracy = self.calculate_word_accuracy()
        sentence_accuracy = self.calculate_sentence_accuracy()
        similarity = self.calculate_similarity_ratio()
        changes = self.analyze_changes()

        print("=" * 50)
        print("METİN DOĞRULUK ANALİZİ RAPORU")
        print("=" * 50)

        print(f"\n📊 DOĞRULUK ORANLARI:")
        print(f"  • Kelime Doğruluğu: {word_accuracy:.2f}%")
        print(f"  • Cümle Doğruluğu: {sentence_accuracy:.2f}%")
        print(f"  • Genel Benzerlik: {similarity:.2f}%")

        print(f"\n📈 İSTATİSTİKLER:")
        print(f"  • Orijinal metin kelime sayısı: {changes['toplam_orijinal']}")
        print(f"  • Değiştirilmiş metin kelime sayısı: {changes['toplam_degistirilmis']}")
        print(f"  • Ortak kelime sayısı: {len(changes['ortak_kelimeler'])}")
        print(f"  • Silinen kelime sayısı: {len(changes['silinen_kelimeler'])}")
        print(f"  • Eklenen kelime sayısı: {len(changes['eklenen_kelimeler'])}")

        if changes['silinen_kelimeler']:
            print(f"\n❌ SİLİNEN KELİMELER (İlk 10):")
            for word in changes['silinen_kelimeler'][:10]:
                print(f"  • {word}")

        if changes['eklenen_kelimeler']:
            print(f"\n✅ EKLENEN KELİMELER (İlk 10):")
            for word in changes['eklenen_kelimeler'][:10]:
                print(f"  • {word}")

        return {
            'kelime_dogruluğu': word_accuracy,
            'cumle_dogruluğu': sentence_accuracy,
            'genel_benzerlik': similarity,
            'degisiklikler': changes
        }


# Kullanım örneği
if __name__ == "__main__":
    # Örnek metinler
    original_text = """
Sizden bu soruların cevaplarını bir süre düşünmenizi rica ediyorum. Dilerseniz cevaplarınızı not alın ve yazıyı okuduktan sonra kendi yanıtlarınızla karşılaştırın.
Çocukların okulda, evde, sokakta, parkta yaşıtlarıyla oyun oynaması, ders çalışması günlük hayatın doğal bir parçasıdır. Ancak zaman zaman bu dengelerin bozulduğunu, bazı çocukların akranları tarafından kasıtlı ve dengesiz bir güçle sürekli hedef alındığını gözlemleyebiliyoruz. Bu durumlara akran zorbalığı adı verilir.
Zorbalık tek biçimli değildir; çeşitli türleri bulunmaktadır:
Sözel Zorbalık: Alay etme, hakaret, lakap takma
Fiziksel Zorbalık: İtme, vurma, eşyaya zarar verme
Duygusal Zorbalık: Dışlama, yalnız bırakma
Dijital Zorbalık: Sosyal medya üzerinden tehdit, aşağılama, özel bilgilerin yayılması
"""

    new_original_text = altyazi_metnini_temizle(original_text)

    modified_text = temiz_metin

    # Analiz yap
    calculator = TextAccuracyCalculator()
    calculator.load_texts(original_text, modified_text)

    # Tam analiz raporu
    results = calculator.full_analysis()

    print(f"\n" + "=" * 50)
    print("ÖZELLEŞTİRİLMİŞ KULLANIM:")
    print("=" * 50)
    print("# Kendi metinlerinizi analiz etmek için:")

    # Kendi metinlerinizi ekleyin
    calculator = TextAccuracyCalculator()
    calculator.load_texts(new_original_text, modified_text)
    results = calculator.full_analysis()

    print(temiz_metin)
    #print(new_original_text)